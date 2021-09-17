# MinIO多用户快速入门指南

除了在服务器启动期间创建的默认用户外，MinIO还支持多个长期用户。服务器启动后，可以添加新用户，并且可以将服务器配置为拒绝或允许这些用户访问存储桶和资源。本文档说明了如何添加/删除用户以及修改其访问权限。

## 开始使用

在本文档中，我们将详细说明如何配置多个用户。

### 1. 先决条件

- 安装 mc - [MinIO Client快速入门指南](http://docs.minio.org.cn/docs/master/minio-client-quickstart-guide.html)
- 安装 MinIO - [MinIO 快速入门指南](http://docs.minio.org.cn/docs/master/minio-quickstart-guide)
- 配置 etcd (仅在网关或联合身份验证模式下才需要) - [Etcd V3 快速入门指南](https://github.com/minio/minio/blob/master/docs/sts/etcd.md)

### 2. 使用固定策略创建新用户

使用[`mc admin policy`](http://docs.minio.org.cn/docs/master/minio-admin-complete-guide.html#policies)创建罐装政策。服务器提供罐装政策的默认设置，即`writeonly`，`readonly`和`readwrite`*（这些政策适用于所有服务器上的资源）*。可以使用`mc admin policy`命令通过自定义策略来覆盖这些设置。

创建新的罐头策略文件`getonly.json`。使用此策略，用户可以下载下的所有对象`my-bucketname`。

```json
cat > getonly.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:GetObject"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::my-bucketname/*"
      ],
      "Sid": ""
    }
  ]
}
EOF
```

`getonly`使用`getonly.json`策略文件按名称创建新的固定策略。

```
mc admin policy add myminio getonly getonly.json
```

`newuser` 在MinIO使用上创建一个新用户 `mc admin user`。

```
mc admin user add myminio newuser newuser123
```

成功创建用户后，您现在可以 `getonly` 为该用户应用策略。

```
mc admin policy set myminio getonly user=newuser
```

### 3. 创建一个新组

```
mc admin group add myminio newgroup newuser
```

成功创建组后，您现在可以 `getonly` 对该组应用策略。

```
mc admin policy set myminio getonly group=newgroup
```

### 4. 禁用用户

禁用用户 `newuser`。

```
mc admin user disable myminio newuser
```

禁用组 `newgroup`。

```
mc admin group disable myminio newgroup
```

### 5. 删除用户

删除用户 `newuser`。

```
mc admin user remove myminio newuser
```

从组中删除用户 `newuser`。

```
mc admin group remove myminio newgroup newuser
```

删除组 `newgroup`。

```
mc admin group remove myminio newgroup
```

### 6. 更改用户或组策略

将用户策略更改 `newuser` 为 `putonly` 固定策略。

```
mc admin policy set myminio putonly user=newuser
```

将组策略更改 `newgroup` 为 `putonly` 固定策略。

```
mc admin policy set myminio putonly group=newgroup
```

### 7. 列出所有用户或组

列出所有启用和禁用的用户。

```
mc admin user list myminio
```

列出所有启用或禁用的组。

```
mc admin group list myminio
```

### 8. 配置 `mc`

```
mc config host add myminio-newuser http://localhost:9000 newuser newuser123 --api s3v4
mc cat myminio-newuser/my-bucketname/my-objectname
```

## 进一步探索

- [MinIO客户端完整指南](http://docs.minio.org.cn/docs/master/minio-client-complete-guide)
- [MinIO STS快速入门指南](http://docs.minio.org.cn/docs/master/minio-sts-quickstart-guide)
- [MinIO管理员完成指南](http://docs.minio.org.cn/docs/master/minio-admin-complete-guide.html)
- [MinIO文档网站](http://docs.minio.org.cn)