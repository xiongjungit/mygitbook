# 如何使用Cyberduck结合MinIO

在本文档中，你将学习如何使用Cyberduck对MinIO进行基本操作。Cyberduck是适用于MacOS和Windows的FTP和SFTP，WebDAV，OpenStack Swift和Amazon S3的开源客户端。它是在GPL许可证v2.0下发布的。  

## 1. 前提条件

- [Cyberduck](https://cyberduck.io/)安装并运行。因为MinIO与Amazon S3兼容，所以你可以从[这里](https://trac.cyberduck.io/wiki/help/en/howto/s3#HTTP)下载一个通用的`HTTP` S3 配置文件。
- MinIO Server已经在本地运行，采用`http`,端口9000, 参考 [MinIO快速入门](http://docs.minio.org.cn/docs/master/minio-quickstart-guide)来安装MinIO。

*注意:* 你也可以用`HTTPS`方式来运行MinIO, 参考[这里](http://docs.minio.org.cn/docs/master/generate-let-s-encypt-certificate-using-concert-for-minio)，以及[这里](https://trac.cyberduck.io/wiki/help/en/howto/s3#HTTPS)描述的Cyberduck通用`HTTPS` S3配置文件。

## 2. 步骤

### 在Cyberduck添加MinIO认证信息

点击open connection, 选择`HTTP`

### 修改已有AWS S3信息为你本地的MinIO凭证

### 点击connect页签建立连接

当连接建立后，那就是天高任鸟飞，你可以去探索更多的操作，下面列出了一部分操作。

#### 列举存储桶

#### 下载存储桶

#### 存储桶镜像

#### 删除存储桶

## 3. 了解更多

- [MinIO Client完全指南](http://docs.minio.org.cn/docs/master/minio-client-complete-guide)
- [Cyberduck project主页](https://cyberduck.io)

