# KMS指南 

[![Slack](https://slack.min.io/slack?type=svg)](http://slack.minio.org.cn/questions)

MinIO使用密钥管理系统（KMS）支持SSE-S3。如果客户端请求SSE-S3，或 启用了自动加密，则MinIO服务器会使用唯一的对象密钥对每个对象进行加密，该对象密钥受 KMS管理的主密钥保护。

> MinIO仍提供本机Hashicorp Vault支持。但是，此功能已**弃用**， 将来可能会删除。因此，强烈建议您使用下面的体系结构和KMS指南。 如果您必须维护旧版MinIO-Vault部署，则可以在[此处](http://docs.minio.org.cn/docs/master/minio-vault-legacy.html).找到旧版文档。 

## 建筑与概念

KMS将MinIO作为面向应用程序的存储系统与安全密钥存储区分开，并且 可以由专门的安全团队进行管理。MinIO 通过我们的[KES project](https://github.com/minio/kes)支持常用的KMS实现，例如 [Hashicorp Vault](https://www.vaultproject.io/)。 通过KES，可以利用存储基础架构（MinIO群集）水平扩展KMS。 通常，MinIO-KMS基础结构如下所示：

```
     ┌─────────┐         ┌────────────┐         ┌─────────┐  
     │  MinIO  ├─────────┤ KES Server ├─────────┤   KMS   │ 
     └─────────┘         └────────────┘         └─────────┘  
```

当您将存储基础架构扩展到多个MinIO群集时，您的架构应如下所示：

```
    ┌────────────┐
    │ ┌──────────┴─┬─────╮          ┌────────────┐
    └─┤ ┌──────────┴─┬───┴──────────┤ ┌──────────┴─┬─────────────────╮
      └─┤ ┌──────────┴─┬─────┬──────┴─┤ KES Server ├─────────────────┤
        └─┤   MinIO    ├─────╯        └────────────┘            ┌────┴────┐
          └────────────┘                                        │   KMS   │
                                                                └─────────┘
```

请注意，所有MinIO群集均仅具有“其自己的” KES实例的连接，而不能直接访问Vault（作为一种可能的KMS实现）。 每个KES实例将处理“其” MinIO群集发出的所有加密/解密请求，从而使中央KMS实现不必处理 大量流量。相反，每个KES实例都将使用中央KMS实现作为安全密钥存储，并从中获取所需的主密钥。

## 入门指南

在随后的章节中，该指南显示了如何使用Hashicorp Vault作为KMS实施来设置MinIO-KMS部署。 因此，它显示了如何设置和配置：

- Vault服务器作为中央密钥库。
- 一个KES服务器实例，作为MinIO和保险柜之间的中间件。
- MinIO实例本身。

> 请注意，为简便起见，本指南使用自签名证书。在生产部署中，应使用 由“公共”（例如，让我们加密）或组织内部的CA颁发的X.509证书。

本指南说明如何在同一台计算机上设置三台不同的服务器：

- Vault服务器为 https://127.0.0.1:8200
- KES服务器为 https://127.0.0.1:7373
- MinIO服务器为 https://127.0.0.1:9000

### 1 先决条件

安装MinIO，KES和Vault。对于MinIO，请参阅 [MinIO 快速入门指南](http://docs.minio.org.cn/docs/master/minio-quickstart-guide). 然后[安装KES](https://github.com/minio/kes#install)并下载 适用于您的操作系统和平台的[最新Vault二进制文件](https://www.vaultproject.io/downloads)

### 2 生成TLS证书

由于KES将对象加密密钥发送给MinIO，并且Vault将主密钥（用于加密对象加密密钥）发送给KES，因此我们绝对需要 MinIO，KES和Vault之间的TLS连接。因此，我们需要至少生成两个TLS证书。

#### 2.1 为保险柜生成TLS证书

要为保险柜的证书生成新的私钥，请运行以下openssl命令：

```sh
openssl ecparam -genkey -name prime256v1 | openssl ec -out vault-tls.key
```

然后通过以下方式为私钥/公钥对生成新的TLS证书：

```sh
openssl req -new -x509 -days 365 \
    -key vault-tls.key \
    -out vault-tls.crt \
    -subj "/C=/ST=/L=/O=/CN=localhost" \
    -addext "subjectAltName = IP:127.0.0.1"
```

> 您可以忽略输出消息，例如：req：没有为主体属性C提供任何值，已跳过。 OpenSSL只是告诉您尚未为证书主题指定国家/地区，州/直辖市。 您可能需要调整X.509主题（`-subj`参数）和主题备用名称（SAN）。 请注意，这是一个自签名证书。对于生产部署，此证书应由 CA颁发。

#### 2.2 为KES生成TLS证书

要为KES的证书生成新的私钥，请运行以下openssl命令：

```sh
openssl ecparam -genkey -name prime256v1 | openssl ec -out kes-tls.key
```

要为KES的证书生成新的私钥，请运行以下openssl命令：

```sh
openssl req -new -x509 -days 365 \
    -key kes-tls.key \
    -out kes-tls.crt \
    -subj "/C=/ST=/L=/O=/CN=localhost" \
    -addext "subjectAltName = IP:127.0.0.1"
```

> 您可以忽略输出消息，例如：req：没有为主体属性C提供任何值，已跳过。 OpenSSL只是告诉您尚未为证书主题指定国家/地区，州/直辖市。 您可能需要调整X.509主题（`-subj`参数）和主题备用名称（SAN）。 请注意，这是一个自签名证书。对于生产部署，此证书应由 CA颁发。

#### 2.3 为MinIO生成TLS证书（可选）

T此步骤是可选的。但是，我们建议您通过TLS来上传/下载S3对象-尤其是当它们应该在 存储后端使用KMS 加密时。

看有关配置MinIO和TLS 的[MinIO TLS指南](http://docs.minio.org.cn/docs/master/how-to-secure-access-to-minio-server-with-tls.html)。

### 3 设置保险柜

在类似Unix的系统上，Vault使用`mlock` syscall来防止操作系统将内存中的数据 写入磁盘（交换）。因此，您应该赋予Vault可执行文件使用`mlock` syscall 的能力，而无需以root用户身份运行进程。为此，请运行：

```sh
sudo setcap cap_ipc_lock=+ep $(readlink -f $(which vault))
```

然后创建保管库配置文件：

```sh
cat > vault-config.json <<EOF
{
  "api_addr": "https://127.0.0.1:8200",
  "backend": {
    "file": {
      "path": "vault/file"
    }
  },
  "default_lease_ttl": "168h",
  "max_lease_ttl": "720h",
  "listener": {
    "tcp": {
      "address": "0.0.0.0:8200",
      "tls_cert_file": "vault-tls.crt",
      "tls_key_file": "vault-tls.key",
      "tls_min_version": "tls12"
    }
  }
}
EOF
```

> 请注意，我们使用文件后端运行Vault。为了获得高可用性，您可能需要使用其他 后端，例如[etcd](https://www.vaultproject.io/docs/configuration/storage/etcd/)或[consul](https://learn.hashicorp.com/vault/operations/ops-vault-ha-consul)。

最后，通过以下方式启动Vault服务器：

```sh
vault server -config vault-config.json
```

#### 3.1 初始化和解封保管箱

在单独的终端窗口中设置环境`VAULT_ADDR`。保险柜服务器的变量：

```sh
export VAULT_ADDR='https://127.0.0.1:8200'
```

此外，`export VAULT_SKIP_VERIFY=true`如果Vault使用自签名TLS 证书，则可能要运行。当Vault提供 由计算机信任的CA颁发的TLS证书（例如，让我们加密）时，则无需运行此命令。

然后通过以下方式初始化保险柜：

```sh
vault operator init
```

保管箱将打印`n`（默认情况下为5）解封密钥共享，其中至少`m`（至少3） 为重新生成实际解封密钥才能解封保管库。因此，请务必 记住它们。特别是，请将那些未密封的密钥共享放在安全且持久的位置。

您应该看到类似于以下内容的输出：

```
Unseal Key 1: eyW/+8ZtsgT81Cb0e8OVxzJAQP5lY7Dcamnze+JnWEDT
Unseal Key 2: 0tZn+7QQCxphpHwTm6/dC3LpP5JGIbYl6PK8Sy79R+P2
Unseal Key 3: cmhs+AUMXUuB6Lzsvgcbp3bRT6VDGQjgCBwB2xm0ANeF
Unseal Key 4: /fTPpec5fWpGqWHK+uhnnTNMQyAbl5alUi4iq2yNgyqj
Unseal Key 5: UPdDVPto+H6ko+20NKmagK40MOskqOBw4y/S51WpgVy/

Initial Root Token: s.zaU4Gbcu0Wh46uj2V3VuUde0

Vault is initialized with 5 key shares and a key threshold of 3. Please securely
distribute the key shares printed above. When the Vault is re-sealed,
restarted, or stopped, you must supply at least 3 of these keys to unseal it
before it can start servicing requests.

Vault does not store the generated master key. Without at least 3 key to
reconstruct the master key, Vault will remain permanently sealed!

It is possible to generate new unseal keys, provided you have a quorum of
existing unseal keys shares. See "vault operator rekey" for more information.
```

现在，设置环境。变量`VAULT_TOKEN`到命令之前打印的根令牌：

```sh
export VAULT_TOKEN=s.zaU4Gbcu0Wh46uj2V3VuUde0
```

然后，使用任何先前生成的密钥共享来打开Vault的密封。

```sh
vault operator unseal eyW/+8ZtsgT81Cb0e8OVxzJAQP5lY7Dcamnze+JnWEDT
vault operator unseal 0tZn+7QQCxphpHwTm6/dC3LpP5JGIbYl6PK8Sy79R+P2
vault operator unseal cmhs+AUMXUuB6Lzsvgcbp3bRT6VDGQjgCBwB2xm0ANeF
```

提交足够的有效密钥共享后，保管箱将被密封 并能够处理请求。

#### 3.2 启用保险柜的K / V后端

加密主密钥（而不是对象加密密钥）将存储 在Vault中。因此，我们需要启用Vault的K / V后端。为此，请运行：

```sh
vault secrets enable kv
```

#### 3.3 启用AppRole身份验证

由于我们希望稍后将一个/多个KES服务器连接到Vault，因此必须启用 AppRole身份验证。为此，请运行：

```sh
vault auth enable approle
```

#### 3.4 为K / V引擎创建访问策略

以下策略确定应用程序（即KES服务器）如何 与Vault 交互。

```sh
cat > minio-kes-policy.hcl <<EOF
path "kv/minio/*" {
  capabilities = [ "create", "read", "delete" ]
}

EOF
```

> 观察路径前缀`minio`在`kv/minio/*`。此前缀确保 KES服务器只能在`minio`/*-下进行读取，而只能在-下进行写入 `some-app/*`。如何在K / V引擎上分隔域取决于您的基础结构 和安全要求。

然后，我们将政策上传到保险柜：

```sh
vault policy write minio-key-policy ./minio-kes-policy.hcl
```

#### 3.5 创建一个新的AppRole ID并将其绑定到策略

现在，我们需要创建一个新的AppRole ID并授予该ID特定的权限。 该应用程序（即KES服务器）将通过AppRole角色ID 和机密ID 向Vault进行身份验证，并且仅允许执行特定策略授予的操作。

因此，我们首先为KES服务器创建一个新角色：

```sh
vault write auth/approle/role/kes-role token_num_uses=0  secret_id_num_uses=0  period=5m
```

然后，我们将策略绑定到角色：

```sh
vault write auth/approle/role/kes-role policies=minio-key-policy
```

最后，我们从Vault请求AppRole角色ID和秘密ID。 一，角色ID：

```sh
vault read auth/approle/role/kes-role/role-id 
```

然后是秘密ID：

```sh
vault write -f auth/approle/role/kes-role/secret-id
```

> 我们只对`secret_id`-不感兴趣`secret_id_accessor`。

### 4 设置KES

与Vault类似，KES `mlock`在Linux系统上使用syscall来防止OS将内存中的 数据写入磁盘（交换）。因此，您应该赋予KES可执行文件使用`mlock` syscall 的能力，而无需以root用户身份运行进程。为此，请运行：

```sh
sudo setcap cap_ipc_lock=+ep $(readlink -f $(which kes))
```

#### 4.1 为MinIO创建标识

连接到KES服务器（mTLS）时，每个用户或应用程序必须出示有效的X.509证书。 KES服务器将接受/拒绝连接尝试，并根据证书应用策略。

因此，每个MinIO群集都需要一个X.509 TLS证书来进行客户端身份验证。您可以 通过运行以下命令来创建（自签名）证书：

```sh
kes tool identity new MinIO --key=minio.key --cert=minio.cert --time=8760h
```

> 注意，*MinIO*是[subject name](https://en.wikipedia.org/wiki/X.509#Structure_of_a_certificate)。 您可以为您的部署方案选择一个更合适的名称。此外，对于生产部署，我们 建议获取由CA颁发的用于客户端身份验证的TLS证书。

要获取X.509证书的身份，请运行：

```sh
kes tool identity of minio.cert
```

> 此命令可与任何（有效）X.509证书一起使用-无论如何创建它-并 产生类似于以下内容的输出：
>
> > ```
> > Identity:  dd46485bedc9ad2909d2e8f9017216eec4413bc5c64b236d992f7ec19c843c5f
> > ```

#### 4.2 创建KES配置文件

现在，我们可以创建KES配置文件并启动KES服务器。

```yaml
# The TCP address (ip:port) for the KES server to listen on.
address: 0.0.0.0:7373

tls:
  key:  kes-tls.key
  cert: kes-tls.crt

policy:
  minio:
    paths:
    - /v1/key/create/minio-*
    - /v1/key/generate/minio-*
    - /v1/key/decrypt/minio-*
    identities:
    - dd46485bedc9ad2909d2e8f9017216eec4413bc5c64b236d992f7ec19c843c5f

cache:
  expiry:
    any:    5m0s 
    unused: 20s 

keys:
  vault:
    endpoint: https://127.0.0.1:8200  # The Vault endpoint - i.e. https://127.0.0.1:8200
    prefix:   minio                   # The domain resp. prefix at Vault's K/V backend 

    approle:
      id:     ""    # Your AppRole Role ID 
      secret: ""    # Your AppRole Secret ID
      retry:  15s   # Duration until the server tries to re-authenticate after connection loss.

    tls:
      ca: vault-tls.crt  # Since we use self-signed certificates

    status:
      ping: 10s
```

> 请`identities`在`policy`部分中将的值更改为您的身份`minio.cert`。 另外，插入您在保险柜设置过程中之前创建的AppRole角色ID和密码ID。 您可以[在此处](https://github.com/minio/kes/blob/master/server-config.yaml)找到包含所有可用参数的文档化配置文件。

最后，通过以下方式启动KES服务器：

```
kes server --config=kes-config.yaml --mlock --root=disabled --auth=off
```

> 请注意，由于不需要特殊的*根*标识，因此我们实际上将其禁用。 有关KES访问控制模型和身份验证的更多信息： [KES Concepts](https://github.com/minio/kes/wiki/Concepts)。此外，请注意，由于客户端X.509证书是自签名证书，因此我们将其 禁用`--auth=off`。

#### 4.3 创建一个新的主密钥

在继续进行MinIO设置之前，我们需要创建一个新的主密钥。因此，我们使用 MinIO身份和KES CLI。

在新的终端窗口中，通过以下方式成为MinIO身份：

```
export KES_CLIENT_TLS_KEY_FILE=minio.key
export KES_CLIENT_TLS_CERT_FILE=minio.cert
```

然后运行以下命令来创建主密钥：

```
kes key create minio-key-1 -k
```

> `-k`由于我们使用自签名证书，因此仅需要该标志。 另外，请注意，基于服务器配置文件， 仅允许MinIO标识创建/使用以开头的主密钥`minio-`。 因此，尝试创建密钥（例如）`kes key create my-key-1 -k`将 失败，并出现策略错误禁止的消息。

### 5 设置MinIO服务器

MinIO服务器将需要知道KES服务器端点， 用于身份验证和授权的mTLS客户端证书以及默认的主密钥名称。

```
export MINIO_KMS_KES_ENDPOINT=https://localhost:7373
export MINIO_KMS_KES_KEY_FILE=minio.key
export MINIO_KMS_KES_CERT_FILE=minio.cert
export MINIO_KMS_KES_KEY_NAME=minio-key-1
export MINIO_KMS_KES_CA_PATH=kes-tls.crt
```

> `MINIO_KMS_KES_CAPATH`由于我们使用自签名证书，因此仅需要。

（可选）启用自动加密以自动加密上传的对象：

```
export MINIO_KMS_AUTO_ENCRYPTION=on
```

> 有关自动加密的更多信息，请参见：[附录A](http://docs.minio.org.cn/docs/master/minio-kms-quickstart-guide#appendix-a---auto-encryption)

然后启动MinIO服务器：

```
export MINIO_ACCESS_KEY=minio
export MINIO_SECRET_KEY=minio123
minio server ~/export
```

### 附录A-自动加密

(可选）您可以指示MinIO服务器使用KES 服务器中的密钥自动加密所有对象-即使客户端在S3 PUT操作期间未指定任何加密标头。

当MinIO操作员希望确保存储在MinIO上的所有数据在 写入存储后端之前都已加密时，自动加密特别有用。

要启用自动加密，请将环境变量设置为`on`：

```
export MINIO_KMS_AUTO_ENCRYPTION=on
```

> 请注意，自动加密只会影响没有S3加密标头的请求。因此，如果S3客户端发送 例如SSE-C标头，则MinIO将使用客户端发送的密钥对对象进行加密，并且不会 与KMS进行联系。 要验证自动加密，请使用以下`mc`命令：

```
mc cp test.file myminio/crypt/
test.file:              5 B / 5 B  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  100.00% 337 B/s 0s
mc stat myminio/crypt/test.file
Name      : test.file
...
Encrypted :
  X-Amz-Server-Side-Encryption: AES256
```

### 附录B-指定主密钥

除了正确的KMS设置，您还可以使用KMS主密钥测试 MinIO加密。 **通过env的单个主密钥。变量仅用于测试目的，不建议用于生产部署。**

KMS主密钥由一个主密钥ID（CMK）和编码为十六进制值的256位主密钥组成，并以分隔`:`。 可以使用以下命令直接指定KMS主密钥：

```
export MINIO_KMS_MASTER_KEY=minio-demo-key:6368616e676520746869732070617373776f726420746f206120736563726574
```

请使用您自己的主密钥。可以使用以下命令在Linux / Mac / BSD系统上生成随机主密钥：

```
head -c 32 /dev/urandom | xxd -c 32 -ps
```

------

或者，您可以将主密钥作为[Docker secret](https://docs.docker.com/engine/swarm/secrets/)传递。

```bash
echo "my-minio-key:6368616e676520746869732070617373776f726420746f206120736563726574" | docker secret create kms_master_key
```

要使用其他秘密名称，请按照上述说明操作，并`kms_master_key`用您的自定义名称（例如`my_kms_master_key`）替换。 然后，将`MINIO_KMS_MASTER_KEY_FILE`环境变量设置为您的秘密名称：

```bash
export MINIO_KMS_MASTER_KEY_FILE=my_kms_master_key
```

## 进一步探索

- [`mc` 与MinIO服务器一起使用](http://docs.minio.org.cn/docs/master/minio-client-quickstart-guide)
- [`aws-cli` 与MinIO服务器一起使用](http://docs.minio.org.cn/docs/master/aws-cli-with-minio)
- [`s3cmd` 与MinIO服务器一起使用](http://docs.minio.org.cn/docs/master/s3cmd-with-minio)
- [`minio-go` SDK 与MinIO Server一起使用](http://docs.minio.org.cn/docs/master/golang-client-quickstart-guide)
- [MinIO文档网站](http://docs.minio.org.cn)