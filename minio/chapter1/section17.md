## MinIO监控指南

MinIO服务器通过端点公开监视数据。监视工具可以从这些端点中选择数据。本文档列出了监视端点和相关文档。

### 健康检查探针

MinIO服务器具有两个与运行状况检查相关的未经身份验证的端点，一个活动性探针（指示服务器是否工作正常），一个就绪性探针（指示服务器是否由于重负载而未接受连接）。

- 可在以下位置获得活力探针 `/minio/health/live`
- 可在以下位置获得就绪探针 `/minio/health/ready`

在[MinIO healthcheck 指南](https://github.com/minio/minio/blob/master/docs/metrics/healthcheck/README.md)中阅读有关如何使用这些端点的更多信息。 

### Prometheus 探测

MinIO服务器在单个端点上公开与Prometheus兼容的数据。默认情况下，对端点进行身份验证。

- Prometheus 数据可在 `/minio/prometheus/metrics`

要使用此端点，请设置Prometheus以从该端点抓取数据。在如何使用Prometheus监视MinIO服务器中阅读有关如何配置和[使用Prometheus监视MinIO服务器的更多信息](https://github.com/minio/minio/blob/master/docs/metrics/prometheus/README.md)。