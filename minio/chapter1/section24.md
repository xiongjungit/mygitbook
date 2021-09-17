# MinIO STS快速入门指南

MinIO安全令牌服务（STS）是一种终结点服务，使客户端可以请求MinIO资源的临时凭据。临时凭据的工作原理几乎与默认管理员凭据相同，但有一些区别：

- 顾名思义，临时证书是短期的。可以将它们配置为持续几分钟到几小时的时间。凭证过期后，MinIO将不再识别它们或允许使用它们发出的API请求进行任何类型的访问。
- 临时凭证不需要与应用程序一起存储，而是动态生成的，并在请求时提供给应用程序。当临时凭证（或什至之前）到期时，应用程序可以请求新凭证。

以下是使用临时凭证的优点：

- 无需在应用程序中嵌入长期凭证。
- 无需提供对存储桶和对象的访问，而无需定义静态凭据。
- 临时凭证的有效期有限，无需旋转或显式吊销它们。过期的临时凭证无法重复使用。

## 身份联盟

| 认证网                                                       | 描述                                                         |
| :----------------------------------------------------------- | ------------------------------------------------------------ |
| [**Client grants**](https://github.com/minio/minio/blob/master/docs/sts/client-grants.md) | 让应用程序client_grants使用任何知名的第三方身份提供商（例如KeyCloak，WSO2）进行请求。这被称为客户端授予方法以进行临时访问。使用这种方法可以帮助客户端保持MinIO凭据的安全。MinIO STS支持客户端授权，并针对身份提供商（例如WSO2，KeyCloak）进行了测试。 |
| [**WebIdentity**](https://github.com/minio/minio/blob/master/docs/sts/web-identity.md) | 让用户使用任何OpenID（OIDC）兼容的Web身份提供商（例如Facebook，Google等）请求临时凭据。 |
| [**AssumeRole**](https://github.com/minio/minio/blob/master/docs/sts/assume-role.md) | 让MinIO用户使用用户访问权限和密钥请求临时凭证。              |
| [**AD/LDAP**](https://github.com/minio/minio/blob/master/docs/sts/ldap.md) | 让AD / LDAP用户使用AD / LDAP用户名和密码来请求临时凭据。     |

## 开始使用

在本文档中，我们将详细说明如何配置所有先决条件。

> 注意：如果仅对AssumeRole API感兴趣，请跳到 [此处](https://github.com/minio/minio/blob/master/docs/sts/assume-role.md)

### 1. 先决条件

- [配置 wso2](https://github.com/minio/minio/blob/master/docs/sts/wso2.md)
- [配置 opa (可选)](https://github.com/minio/minio/blob/master/docs/sts/opa.md)
- [配置 etcd (仅在网关或联合方式下需要可选)](https://github.com/minio/minio/blob/master/docs/sts/etcd.md)

### 2.使用WSO2设置MinIO

确保已按照上一步操作并独立配置每个软件，完成后，我们现在可以继续使用MinIO STS API和MinIO服务器来使用这些凭据来执行对象API操作。

```
export MINIO_ACCESS_KEY=minio
export MINIO_SECRET_KEY=minio123
export MINIO_IDENTITY_OPENID_CONFIG_URL=https://localhost:9443/oauth2/oidcdiscovery/.well-known/openid-configuration
export MINIO_IDENTITY_OPENID_CLIENT_ID="843351d4-1080-11ea-aa20-271ecba3924a"
minio server /mnt/data
```

### 3. 使用WSO2，ETCD设置MinIO网关

确保已按照上一步操作并独立配置每个软件，完成后，我们现在可以继续使用MinIO STS API和MinIO网关来使用这些凭据来执行对象API操作。

> 注意：MinIO网关要求将etcd配置为使用STS API。

```
export MINIO_ACCESS_KEY=aws_access_key
export MINIO_SECRET_KEY=aws_secret_key
export MINIO_IDENTITY_OPENID_CONFIG_URL=https://localhost:9443/oauth2/oidcdiscovery/.well-known/openid-configuration
export MINIO_IDENTITY_OPENID_CLIENT_ID="843351d4-1080-11ea-aa20-271ecba3924a"
export MINIO_ETCD_ENDPOINTS=http://localhost:2379
minio gateway s3
```

### 4. 使用client-grants.go进行测试

在另一个终端上，运行 `client-grants.go` 一个示例客户端应用程序，该应用程序从身份提供者（在我们的情况下为WSO2）获取JWT访问令牌。使用返回的访问令牌响应，通过STS API调用从MinIO服务器获取新的临时凭据 `AssumeRoleWithClientGrants`。

```
go run client-grants.go -cid PoEgXP6uVO45IsENRngDXj5Au5Ya -csec eKsw6z8CtOJVBtrOWvhRWL4TUCga

##### Credentials
{
    "accessKey": "NUIBORZYTV2HG2BMRSXR",
    "secretKey": "qQlP5O7CFPc5m5IXf1vYhuVTFj7BRVJqh0FqZ86S",
    "expiration": "2018-08-21T17:10:29-07:00",
    "sessionToken": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJOVUlCT1JaWVRWMkhHMkJNUlNYUiIsImF1ZCI6IlBvRWdYUDZ1Vk80NUlzRU5SbmdEWGo1QXU1WWEiLCJhenAiOiJQb0VnWFA2dVZPNDVJc0VOUm5nRFhqNUF1NVlhIiwiZXhwIjoxNTM0ODk2NjI5LCJpYXQiOjE1MzQ4OTMwMjksImlzcyI6Imh0dHBzOi8vbG9jYWxob3N0Ojk0NDMvb2F1dGgyL3Rva2VuIiwianRpIjoiNjY2OTZjZTctN2U1Ny00ZjU5LWI0MWQtM2E1YTMzZGZiNjA4In0.eJONnVaSVHypiXKEARSMnSKgr-2mlC2Sr4fEGJitLcJF_at3LeNdTHv0_oHsv6ZZA3zueVGgFlVXMlREgr9LXA"
}
```

## 进一步探索

- [MinIO管理员完成指南](http://docs.minio.org.cn/docs/master/minio-admin-complete-guide.html)
- [MinIO文档网站](http://docs.minio.org.cn)