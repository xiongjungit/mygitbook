# MinIO HDFS网关

 [![Slack](https://slack.minio.io/slack?type=svg)](https://slack.minio.io)

MinIO HDFS网关将Amazon S3 API支持添加到Hadoop HDFS文件系统中。应用程序可以同时使用S3和文件API，而无需任何数据迁移。由于网关是无状态且无共享的，因此您可以弹性地分配所需数量的MinIO实例以分配负载。

## 运行MinIO Gateway进行HDFS存储

### 使用二进制

通过`core-site.xml` 自动从hadoop环境变量 *$HADOOP_HOME* 中读取来获取Namenode信息

```
export MINIO_ACCESS_KEY=minio
export MINIO_SECRET_KEY=minio123
minio gateway hdfs
```

您还可以覆盖namenode端点，如下所示。

```
export MINIO_ACCESS_KEY=minio
export MINIO_SECRET_KEY=minio123
minio gateway hdfs hdfs://namenode:8200
```

### 使用 Docker

使用docker是实验性的，大多数Hadoop环境未进行docker化，可能需要其他步骤才能使其正常工作。在这种情况下，最好只使用二进制文件。

```
docker run -p 9000:9000 \
 --name hdfs-s3 \
 -e "MINIO_ACCESS_KEY=minio" \
 -e "MINIO_SECRET_KEY=minio123" \
 minio/minio gateway hdfs hdfs://namenode:8200
```

## 使用MinIO浏览器进行测试

*MinIO网关* 带有基于Web的嵌入式对象浏览器。将您的Web浏览器指向http://127.0.0.1:9000 ，以确保服务器已成功启动。

![屏幕截图](https://raw.githubusercontent.com/minio/minio/master/docs/screenshots/minio-browser-gateway.png)

## 使用MinIO Client进行测试 `mc`

`mc` 提供了诸如ls，cat，cp，mirror，diff等UNIX命令的现代替代方案。它支持文件系统和与Amazon S3兼容的云存储服务。

### 配置 `mc`

```
mc config host add myhdfs http://gateway-ip:9000 access_key secret_key
```

### 在HDFS上列出存储桶

```
mc ls myhdfs
[2017-02-22 01:50:43 PST]     0B user/
[2017-02-26 21:43:51 PST]     0B datasets/
[2017-02-26 22:10:11 PST]     0B assets/
```

### 已知限制

网关继承了HDFS存储层的以下限制：

- 没有存储桶策略支持（HDFS没有这样的概念）
- 不支持存储桶通知API（HDFS不支持fsnotify）
- 不支持服务器端加密（有意未实现）
- 不支持服务器端压缩（有意未实现）

## 路线图

- 对PutObject操作的其他元数据支持
- 多部分操作的其他元数据支持
- 后台附加为多部分操作提供并发支持

如果您希望解决这些问题，请打开GitHub问题。 https://github.com/minio/minio/issues

## 进一步探索

- [`mc` 命令行界面](https://docs.minio.io/docs/minio-client-quickstart-guide)
- [`aws` 命令行界面](https://docs.minio.io/docs/aws-cli-with-minio)
- [`minio-go` 转到 SDK](https://docs.minio.io/docs/golang-client-quickstart-guide)