# 如何使用Prometheus监控MinIO服务器 [![Slack](https://slack.min.io/slack?type=svg)](http://slack.minio.org.cn/questions)

[Prometheus](https://prometheus.io)  Prometheus是最初在SoundCloud上构建的云原生监视平台。Prometheus提供了多维数据模型，其中包含通过度量标准名称和键/值对标识的时间序列数据。数据收集通过HTTP / HTTPS上的拉模型进行。通过服务发现或静态配置发现要提取数据的目标。

MinIO默认情况下将Prometheus兼容数据作为授权端点导出/minio/prometheus/metrics。希望监视其MinIO实例的用户可以指向Prometheus配置，以从该终结点抓取数据。

本文档说明了如何设置Prometheus并将其配置为从MinIO服务器抓取数据。

**目录**

- 先决条件
  - [1. 下载Prometheus](http://docs.minio.org.cn/docs/master/how-to-monitor-minio-using-prometheus#1-download-prometheus)
  - [2. 为Prometheus指标配置身份验证类型](http://docs.minio.org.cn/docs/master/how-to-monitor-minio-using-prometheus#2-configure-authentication-type-for-prometheus-metrics)
  - \3. 配置Prometheus
    - [3.1 经过身份验证的Prometheus配置](http://docs.minio.org.cn/docs/master/how-to-monitor-minio-using-prometheus#31-authenticated-prometheus-config)
    - [3.2 Public Prometheus配置](http://docs.minio.org.cn/docs/master/how-to-monitor-minio-using-prometheus#32-public-prometheus-config)
  - [4. `scrape_configs` prometheus.yml中的更新部分](http://docs.minio.org.cn/docs/master/how-to-monitor-minio-using-prometheus#4-update-scrapeconfigs-section-in-prometheusyml)
  - [5. 启动 Prometheus](http://docs.minio.org.cn/docs/master/how-to-monitor-minio-using-prometheus#5-start-prometheus)
- [MinIO公开的指标列表](http://docs.minio.org.cn/docs/master/how-to-monitor-minio-using-prometheus#list-of-metrics-exposed-by-minio)

## 先决条件

要开始使用MinIO，请参阅[MinIO快速入门文档](http://docs.minio.org.cn/docs/master/minio-quickstart-guide)。请按照以下步骤开始使用Prometheus进行MinIO监视。

### 1. 下载 Prometheus

为您的平台[下载最新版本](https://prometheus.io/download)的Prometheus，然后解压缩

```sh
tar xvfz prometheus-*.tar.gz
cd prometheus-*
```

Prometheus服务器是一个称为prometheus（或prometheus.exe在Microsoft Windows上）的二进制文件。运行二进制和通过--help标志以查看可用选项

```sh
./prometheus --help
usage: prometheus [<flags>]

The Prometheus monitoring server

. . .
```

有关更多详细信息，请参阅[Prometheus文档](https://prometheus.io/docs/introduction/first_steps/)。

### 2. 为Prometheus指标配置身份验证类型

MinIO支持Prometheus `jwt`或两种身份验证模式`public`，默认情况下，MinIO以`jwt`mode 运行。要允许对prometheus度量标准不进行身份验证就可以进行公共访问，请按如下所示设置环境。

```
export MINIO_PROMETHEUS_AUTH_TYPE="public"
minio server ~/test
```

### 3. 配置Prometheus

#### 3.1 经过身份验证的Prometheus配置

> 如果将MinIO配置为在不进行身份验证的情况下公开指标，则无需使用它mc来生成prometheus配置。您可以跳过进一步阅读并移至3.2部分。

MinIO中的Prometheus端点默认需要身份验证。Prometheus支持使用承载令牌方法对Prometheus抓取请求进行身份验证，并使用mc生成的默认Prometheus配置覆盖默认的Prometheus配置。要为别名生成Prometheus配置，请使用[mc](http://docs.minio.org.cn/docs/master/minio-client-quickstart-guide)，如下所示`mc admin prometheus generate <alias>`。

该命令将生成`scrape_configs` prometheus.yml 的部分，如下所示：

```yaml
scrape_configs:
- job_name: minio-job
  bearer_token: <secret>
  metrics_path: /minio/prometheus/metrics
  scheme: http
  static_configs:
  - targets: ['localhost:9000']
```

#### 3.2 Public Prometheus配置

如果Prometheus端点身份验证类型设置为`public`。遵循prometheus的配置足以开始从MinIO抓取指标数据。

```yaml
scrape_configs:
- job_name: minio-job
  metrics_path: /minio/prometheus/metrics
  scheme: http
  static_configs:
  - targets: ['localhost:9000']
```

### 4. `scrape_configs` 更新部分prometheus.yml

要授权每个刮取请求，请将生成的`scrape_configs`部分复制并粘贴到prometheus.yml中，然后重新启动Prometheus服务。

### 5. 启动 Prometheus

通过运行启动（或）重新启动Prometheus服务

```sh
./prometheus --config.file=prometheus.yml
```

这`prometheus.yml`是配置文件的名称。现在，您可以在Prometheus仪表板中查看MinIO指标。默认情况下，可以从访问Prometheus仪表板`http://localhost:9090`。

## MinIO公开的指标列表

MinIO服务器在/ minio / prometheus / metrics端点上公开以下指标。  所有这些都可以通过Prometheus仪表板进行访问。  演示服务器的https://play.min.io:9000/minio/prometheus/metrics  中提供了暴露指标的完整列表及其定义。

这些是将在之后生效的新指标集`RELEASE.2019-10-16*`。下面列出了此更新中的一些关键更改。 -指标绑定到各个节点，并且不在群集范围内。集群中的每个节点都将公开自己的指标。 -添加了涵盖s3和节点间流量统计信息的其他指标。 -记录http统计信息和延迟的度量标准被标记为其各自的API（putobject，getobject等）。 -磁盘使用情况指标已分发并标记到相应的磁盘路径。

有关更多详细信息，请检查 `Migration guide for the new set of metrics`

指标列表及其定义如下。（注意：这里的实例是一个MinIO节点）

> 注意:
>
> 1. 这里的实例是一个MinIO节点。
> 2. `s3 requests`排除节点间请求。

- 标准go运行时指标的前缀 `go_`
- 流程级别指标以开头 `process_`
- prometheus 抓取以开头的指标 `promhttp_`
- `disk_storage_used` : 磁盘使用的磁盘空间。
- `disk_storage_available`: 磁盘上剩余的可用磁盘空间。
- `disk_storage_total`: 磁盘上的总磁盘空间。
- `minio_disks_offline`: 当前MinIO实例中的脱机磁盘总数。
- `minio_disks_total`: 当前MinIO实例中的磁盘总数。
- `s3_requests_total`: 当前MinIO实例中s3请求的总数。
- `s3_errors_total`: 当前MinIO实例中s3请求中的错误总数。
- `s3_requests_current`: 当前MinIO实例中活动s3请求的总数。
- `internode_rx_bytes_total`: 当前MinIO服务器实例接收到的节点间字节总数。
- `internode_tx_bytes_total`: 当前MinIO服务器实例发送到其他节点的字节总数。
- `s3_rx_bytes_total`: 当前MinIO服务器实例接收的s3字节总数。
- `s3_tx_bytes_total`: 当前MinIO服务器实例发送的s3字节总数。
- `minio_version_info`: 具有提交ID的当前MinIO版本。
- `s3_ttfb_seconds`: 保存请求的延迟信息的直方图。

除了上述指标外，MinIO还公开了低于模式的指标

### 缓存特定指标

启用了磁盘缓存的MinIO Gateway实例公开了与缓存相关的指标。

- `cache_data_served`:cache_data_served：从缓存提供的总字节数。
- `cache_hits_total`:cache_hits_total：缓存命中总数。
- `cache_misses_total`:cache_misses_total：缓存未命中总数。

### 网关和缓存特定指标

MinIO Gateway实例公开与网关与云后端（S3，Azure和GCS Gateway）的通信相关的指标。

- `gateway_<gateway_type>_requests`:向云后端发出的请求总数。此度量标准具有method标识GET，HEAD，PUT和POST请求的标签。
- `gateway_<gateway_type>_bytes_sent`:发送到云后端的总字节数（在PUT和POST请求中）。
- `gateway_<gateway_type>_bytes_received`:从云后端接收的字节总数（在GET和HEAD请求中）。

请注意，这目前仅支持Azure，S3和GCS网关

### MinIO自愈指标 - `self_heal_*`

MinIO 仅针对擦除代码部署公开与自我修复相关的指标。这些度量标准在网关或单节点单驱动器部署中不可用。请注意，只有在MinIO服务器上发生相关事件时，才会公开这些指标。

- `self_heal_time_since_last_activity`:自上一次自我修复相关活动以来经过的时间。
- `self_heal_objects_scanned`:在当前运行中由自愈线程扫描的对象数。重新开始自我修复运行时，它将重置。这用扫描的对象类型标记。
- `self_heal_objects_healed`: 当前运行中通过自愈线程修复的对象数。重新开始自我修复运行时，它将重置。这用扫描的对象类型标记。
- `self_heal_objects_heal_failed`:当前运行中自愈失败的对象数。重新开始自我修复运行时，它将重置。这被标记为磁盘状态及其端点。

## 新指标集的迁移指南

本迁移指南适用于旧版本或之前的任何版本  `RELEASE.2019-10-23*`

### MinIO磁盘级别指标 - `disk_*`

迁移包括

```
- `minio_total_disks` to `minio_disks_total`
- `minio_offline_disks` to `minio_disks_offline`
```

### MinIO磁盘级别指标 - `disk_storage_*`

这些指标只有一个标签。

```
- `disk`: Holds the disk path
```

迁移包括

```
- `minio_disk_storage_used_bytes` to `disk_storage_used`
- `minio_disk_storage_available_bytes` to `disk_storage_available`
- `minio_disk_storage_total_bytes` to `disk_storage_total`
```

### MinIO网络级指标

详细介绍了这些指标，以涵盖s3和节点间网络统计信息。

迁移包括

```
- `minio_network_sent_bytes_total` to `s3_tx_bytes_total` and `internode_tx_bytes_total`
- `minio_network_received_bytes_total` to `s3_rx_bytes_total` and `internode_rx_bytes_total`
```

添加的一些其他指标是

```
- `s3_requests_total`
- `s3_errors_total`
- `s3_ttfb_seconds`
```