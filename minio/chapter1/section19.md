# Federation 快速入门指南

 [![Slack](https://slack.min.io/slack?type=svg)](http://slack.minio.org.cn/questions)

本文档说明了如何使用 `Bucket lookup from DNS` 样式联合来配置MinIO 。

## 开始使用

### 1. 先决条件

安装 MinIO - [MinIO 快速入门指南](http://docs.minio.org.cn/docs/master/minio-quickstart-guide).

### 2. 以联合模式运行MinIO

从DNS联合查找存储桶需要两个依赖项

- etcd (用于存储桶DNS服务记录)
- CoreDNS (用于基于填充的桶式DNS服务记录的DNS管理，可选)

## 建筑

![桶查询](https://github.com/minio/minio/blob/master/docs/federation/lookup/bucket-lookup.png?raw=true)

### 环境变量

#### MINIO_ETCD_ENDPOINTS

这是您要用作MinIO联合后端的etcd服务器的逗号分隔列表。 在整个联合部署中，这应该是相同的，即联合部署中的所有MinIO实例都应使用相同的 etcd后端。

#### MINIO_DOMAIN

这是用于联合设置的顶级域名。理想情况下，该域名应解析为 在所有联合MinIO实例之前运行的负载均衡器。域名用于创建etcd的子域条目。对于 例如，如果域名设置为 `domain.com`，水桶 `bucket1`，`bucket2` 将作为访问`bucket1.domain.com` 和 `bucket2.domain.com`。

#### MINIO_PUBLIC_IPS

这是用逗号分隔的IP地址列表，此MinIO实例上创建的存储桶将解析为这些IP地址。例如， 可以 `bucket1` 在上访问在当前MinIO实例上创建的存储区 `bucket1.domain.com`，并且的DNS条目 `bucket1.domain.com` 将指向中设置的IP地址`MINIO_PUBLIC_IPS`。

*注意*

- 对于独立和擦除代码MinIO服务器部署，此字段是必需的，以启用联合模式。
- 对于分布式部署，此字段是可选的。如果您未在联合设置中设置此字段，我们将使用传递给MinIO服务器启动的主机的IP地址，并将其用于DNS条目。 hosts passed to the MinIO server startup and use them for DNS entries.

### 运行多个集群

> 集群1

```sh
export MINIO_ETCD_ENDPOINTS="http://remote-etcd1:2379,http://remote-etcd2:4001"
export MINIO_DOMAIN=domain.com
export MINIO_PUBLIC_IPS=44.35.2.1,44.35.2.2,44.35.2.3,44.35.2.4
minio server http://rack{1...4}.host{1...4}.domain.com/mnt/export{1...32}
```

> 集群2

```sh
export MINIO_ETCD_ENDPOINTS="http://remote-etcd1:2379,http://remote-etcd2:4001"
export MINIO_DOMAIN=domain.com
export MINIO_PUBLIC_IPS=44.35.1.1,44.35.1.2,44.35.1.3,44.35.1.4
minio server http://rack{5...8}.host{5...8}.domain.com/mnt/export{1...32}
```

在此配置中，您可以看到 `MINIO_ETCD_ENDPOINTS`指向etcd后端的指向，该后端管理MinIO `config.json` 和存储桶DNS SRV记录。`MINIO_DOMAIN`表示存储桶的域后缀， 它将用于通过DNS解析存储桶。例如，如果您有一个诸如的存储桶`mybucket`，则 客户端现在可以使用`mybucket.domain.com`它直接将其自身解析为正确的集群。`MINIO_PUBLIC_IPS` 指向可以访问每个群集的公共IP地址，这对于每个群集都是唯一的。

注意：`mybucket` 仅存在于一个群集中，`cluster1` 或者 `cluster2` 这是随机的，并且 由 `domain.com`解析方式决定，如果存在循环DNS，`domain.com`则将 随机选择哪个群集可以提供存储桶。

### 3. 接口升级到 `etcdv3`

从发布运行MinIO联盟用户 `RELEASE.2018-06-09T03-43-35Z`到`RELEASE.2018-07-10T01-42-11Z`，应该ETCD服务器上现有桶数据迁移到`etcdv3`API，和更新版本CoreDNS向`1.2.0`他们MinIO服务器更新到最新版本之前。

这是为什么需要这样做的一些背景-MinIO服务器发布`RELEASE.2018-06-09T03-43-35Z`到`RELEASE.2018-07-10T01-42-11Z`使用过的etcdv2 API，以将存储区数据存储到etcd服务器。这是由于`etcdv3`CoreDNS服务器不支持该功能。因此，即使MinIO使用`etcdv3`API存储存储桶数据，CoreDNS也将无法读取并将其用作DNS记录。

现在CoreDNS [supports etcdv3](https://coredns.io/2018/07/11/coredns-1.2.0-release/)，MinIO服务器使用`etcdv3`API将存储桶数据存储到etcd服务器。由于`etcdv2`和`etcdv3`API不兼容，因此使用`tcdv2`API无法存储使用API 存储的数据`etcdv3`。因此，在完成迁移之前，当前MinIO版本将看不到先前MinIO版本存储的存储桶数据。

CoreOS team has documented the steps required to migrate existing data from `etcdv2` to `etcdv3` in [this blog post](https://coreos.com/blog/migrating-applications-etcd-v3.html). Please refer the post and migrate etcd data to `etcdv3` API. CoreOS团队已在[this blog post](https://coreos.com/blog/migrating-applications-etcd-v3.html)中记录了将现有数据从迁移`etcdv2`到`etcdv3`所需的步骤。请参考该帖子，并将etcd数据迁移到API。

### 4. 测试您的设置

要测试此设置，请通过浏览器或访问MinIO服务器[`mc`](http://docs.minio.org.cn/docs/master/minio-client-quickstart-guide)。您将看到可以从所有MinIO端点访问上载的文件。

# 进一步探索

- [`mc`与MinIO服务器一起使用](http://docs.minio.org.cn/docs/master/minio-client-quickstart-guide)
- [`aws-cli`与MinIO服务器一起使用](http://docs.minio.org.cn/docs/master/aws-cli-with-minio)
- [`s3cmd` 与MinIO服务器一起使用](http://docs.minio.org.cn/docs/master/s3cmd-with-minio)
- [`minio-go`SDK与MinIO Server一起使用](http://docs.minio.org.cn/docs/master/golang-client-quickstart-guide)
- [MinIO文档网站](http://docs.minio.org.cn)