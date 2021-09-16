# MinIO S3网关

 [![Slack](https://slack.min.io/slack?type=svg)](http://slack.minio.org.cn/questions)

MinIO S3 Gateway向AWS S3或任何其他与AWS S3兼容的服务中添加了MinIO功能，如MinIO浏览器和磁盘缓存。

## 运行适用于AWS S3的MinIO Gateway

作为运行MinIO S3网关的先决条件，默认情况下，您需要有效的AWS S3访问密钥和秘密密钥。（可选）当您通过环境变量（即AWS_ACCESS_KEY_ID）旋转AWS IAM凭证或AWS凭证时，还可以设置自定义访问/秘密密钥。

### 使用Docker

```
docker run -p 9000:9000 --name minio-s3 \
 -e "MINIO_ACCESS_KEY=aws_s3_access_key" \
 -e "MINIO_SECRET_KEY=aws_s3_secret_key" \
 minio/minio gateway s3
```

### 使用二进制

```
export MINIO_ACCESS_KEY=aws_s3_access_key
export MINIO_SECRET_KEY=aws_s3_secret_key
minio gateway s3
```

### 在EC2中使用Binary

使用适用于AWS S3的IAM旋转凭证

```
export MINIO_ACCESS_KEY=custom_access_key
export MINIO_SECRET_KEY=custom_secret_key
minio gateway s3
```

如果您的后端URL是AWS S3，则MinIO网关将按以下顺序自动查找证书样式列表。

- AWS环境变量（即AWS_ACCESS_KEY_ID）
- AWS凭证文件（即AWS_SHARED_CREDENTIALS_FILE或〜/ .aws / credentials）
- 基于IAM配置文件的凭据。（执行对预定义端点的HTTP调用，仅在已配置的ec2实例内部有效）

如果您希望使用AWS凭证提供受限访问权限，则需要最低权限，请确保为您的AWS用户或角色遵循以下IAM策略。

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "readonly",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": "arn:aws:s3:::testbucket"
        },
        {
            "Sid": "readonly",
            "Effect": "Allow",
            "Action": "s3:HeadBucket",
            "Resource": "arn:aws:s3:::testbucket"
        }
    ]
}
```

## 运行适用于AWS S3兼容服务的MinIO Gateway

作为在AWS S3兼容服务上运行MinIO S3网关的先决条件，您需要有效的访问密钥，秘密密钥和服务端点。

## 使用双重加密运行MinIO Gateway

到S3的MinIO网关支持静态数据加密。支持三种类型的加密模式

- 可以将加密设置 `pass-through` 为后端
- `single encryption` (在网关)
- `double encryption` (在网关处进行单一加密，然后传递到后端)。

可以通过设置MINIO_GATEWAY_SSE环境变量来指定。如果未设置MINIO_GATEWAY_SSE和KMS，则所有加密标头都将传递到后端。如果设置了KMS环境变量， `single encryption` 则会在网关上自动执行，并将加密的对象保存在后端。

要指定 `double encryption` ，对于sse-s3 ，需要将MINIO_GATEWAY_SSE环境变量设置为“ s3”，而对于sse-c加密则需要设置为“  c”。可以设置多个加密选项，以“;”分隔。对象在网关处被加密，并且网关也对后端进行传递。请注意，在使用SSE-C加密的情况下，网关会使用密钥派生功能（KDF）从SSE-C客户端密钥派生唯一的SSE-C密钥进行传递。

```sh
export MINIO_GATEWAY_SSE="s3;c"
export MINIO_KMS_VAULT_APPROLE_ID=9b56cc08-8258-45d5-24a3-679876769126
export MINIO_KMS_VAULT_APPROLE_SECRET=4e30c52f-13e4-a6f5-0763-d50e8cb4321f
export MINIO_KMS_VAULT_ENDPOINT=https://vault-endpoint-ip:8200
export MINIO_KMS_VAULT_KEY_NAME=my-minio-key
export MINIO_KMS_VAULT_AUTH_TYPE=approle
minio gateway s3
```

### 使用Docker

```
docker run -p 9000:9000 --name minio-s3 \
 -e "MINIO_ACCESS_KEY=access_key" \
 -e "MINIO_SECRET_KEY=secret_key" \
 minio/minio gateway s3 https://s3_compatible_service_endpoint:port
```

### 使用二进制

```
export MINIO_ACCESS_KEY=access_key
export MINIO_SECRET_KEY=secret_key
minio gateway s3 https://s3_compatible_service_endpoint:port
```

## MinIO 缓存

MinIO边缘缓存允许将内容存储在离应用程序更近的地方。经常访问的对象存储在基于本地磁盘的缓存中。利用MinIO网关功能进行边缘缓存

- 显着提高了任何对象到第一个字节的时间。
- 避免 S3 [数据传输费用](https://aws.amazon.com/s3/pricing/).

请参考 [本文档](http://docs.minio.org.cn/docs/master/minio-disk-cache-guide.html) 以开始使用MinIO Caching。

## MinIO浏览器

MinIO Gateway带有基于嵌入式Web的对象浏览器。将您的Web浏览器指向http://127.0.0.1:9000 ，以确保服务器已成功启动。

![屏幕截图](https://github.com/minio/minio/blob/master/docs/screenshots/minio-browser-gateway.png?raw=true)

借助MinIO S3网关，您可以使用MinIO浏览器浏览基于AWS S3的对象。

### 已知限制

- 不支持存储桶通知API。

## 进一步探索

- [`mc` 命令行界面](http://docs.minio.org.cn/docs/master/minio-client-quickstart-guide)
- [`aws` 命令行界面](http://docs.minio.org.cn/docs/master/aws-cli-with-minio)
- [`minio-go` 转到SDK](http://docs.minio.org.cn/docs/master/golang-client-quickstart-guide)