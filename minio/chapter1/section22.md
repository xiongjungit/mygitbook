# 压缩指南 

[![Slack](https://slack.min.io/slack?type=svg)](http://slack.minio.org.cn/questions)

MinIO服务器允许流式压缩以确保有效的磁盘空间使用。压缩是在飞行中发生的，即对象在写入磁盘之前已被压缩。MinIO [`klauspost/compress/s2`](https://github.com/klauspost/compress/tree/master/s2)由于其稳定性和性能而使用流式压缩。

该算法专门针对机器生成的内容进行了优化。每个CPU内核的写吞吐量通常至少为300MB / s。解压缩速度通常至少为1GB / s。 这意味着在原始IO低于这些数字的情况下，压缩不仅会减少磁盘使用量，而且有助于提高系统吞吐量。 通常，当可以压缩内容时，在旋转磁盘系统上启用压缩将提高速度。

## 开始使用

### 1. 先决条件

安装MinIO - [MinIO 快速入门指南](http://docs.minio.org.cn/docs/master/minio-quickstart-guide).

### 2. 通过压缩运行MinIO

可以通过更新`compress` MinIO服务器配置的配置设置来启用压缩。配置`compress`设置采用扩展名和mime类型进行压缩。

```
$ mc admin config get myminio compression
compression extensions=".txt,.log,.csv,.json,.tar,.xml,.bin" mime_types="text/*,application/json,application/xml"```
```

默认配置包括最常见的高度可压缩的内容扩展名和mime类型。

```
$ mc admin config set myminio compression extensions=".pdf" mime_types="application/pdf"
```

使用默认扩展名和mime类型对所有内容启用压缩。

```
~ mc admin config set myminio compression
```

压缩设置也可以通过环境变量来设置。设置后，环境变量将覆盖`compress`服务器配置中定义的配置设置。

```bash
export MINIO_COMPRESS="on"
export MINIO_COMPRESS_EXTENSIONS=".pdf,.doc"
export MINIO_COMPRESS_MIME_TYPES="application/pdf"
```

### 3. 注意

- 已经压缩的对象不具有可压缩的模式，因此不适合进行压缩。这样的对象不能产生有效的效率[`LZ compression`](https://en.wikipedia.org/wiki/LZ77_and_LZ78)，这是无损数据压缩的适用性。以下是不适合压缩的常见文件和内容类型的列表。

  - 扩展名

    | `gz` | (GZIP)
     | `bz2` | (BZIP2)
     | `rar` | (WinRAR)
     | `zip` | (ZIP)
     | `7z` | (7-Zip)
     | `xz` | (LZMA)
     | `mp4` | (MP4)
     | `mkv` | (MKV media)
     | `mov` | (MOV)

  - 内容类型

    | `video/*` |
     | `audio/*` |
     | `application/zip` |
     | `application/x-gzip` |
     | `application/zip` |
     | `application/x-bz2` |
     | `application/x-compress` |
     | `application/x-xz` |

即使所有类型都启用了压缩，所有具有这些扩展名和mime类型的文件都将从压缩中排除。

- MinIO不支持压缩加密，因为压缩和加密在一起可能为诸如 [`CRIME and BREACH`](https://blog.minio.io/c-e-compression-encryption-cb6b7f04a369)
- MinIO不支持网关（Azure / GCS / NAS）实现的压缩。

## 测试设置

要测试此设置，请练习使用`mc`和`mc ls`在数据目录上使用来对服务器进行调用，以查看对象的大小。

## 进一步探索

- [`mc`与 MinIO 服务器一起使用](http://docs.minio.org.cn/docs/master/minio-client-quickstart-guide)
- [`aws-cli` 与 MinIO 服务器一起使用](http://docs.minio.org.cn/docs/master/aws-cli-with-minio)
- [`s3cmd` 与 MinIO 服务器一起使用](http://docs.minio.org.cn/docs/master/s3cmd-with-minio)
- [`minio-go` SDK 与 MinIO 服务器一起使用](http://docs.minio.org.cn/docs/master/golang-client-quickstart-guide)
- [MinIO文档网站](http://docs.minio.org.cn)