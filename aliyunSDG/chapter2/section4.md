Rsync 是一个通过检查文件的时间戳和大小，来跨计算机系统高效地传输和同步文件的工具。

通常情况下，管理程序在启动 Rsync 服务后，会直接运行传输任务。如果 Rsync 服务未经过安全加固，则很容易出现未授权访问等安全问题；其直接后果是传输数据裸露在互联网上，可以被任何人访问获取，带来严重的数据泄露风险。

建议您在使用 Rsync 服务端时，参考本文对 Rsync 服务进行安全加固，保障数据安全。

#加固方案

隐藏 module 信息

将配置文件修改为以下内容：

```
list = false
```

#使用权限控制

将不需要写入权限的 module 设置为只读：

```
read only = true
```

#限制网络访问

使用 [安全组策略](https://help.aliyun.com/document_detail/25475.html?spm=5176.7751079.2.3.j5M2sS) 或白名单，限制允许访问主机的 IP 地址。

```
hosts allow = 123.123.123.123
```

#启用账户认证

只允许指定的用户，使用指定的密码，来调用 Rsync 服务。

- ###服务端配置
```
auth users = ottocho
secrets file = /etc/rsyncd.secrets
```
在文件 /etc/rsyncd.secrets 中写入使用的账号密码，格式为：username:password，支持多行。</br>
注意：密码要求满足强密码策略，必须是 8 位以上，且包括大小写字母、数字、特殊字符的字符串。此处的 password 使用明文。

- ###客户端配置
在客户端，使用 --password-file=/etc/rsyncd.secrets 参数，在 /etc/rsyncd.secrets 中写入密码。
```
Rsync -av --password-file=/etc/rsyncd.secrets test.host.com::files /des/path
```
在上述 /etc/rsyncd.secrets 密码文件中，用户或用户组必须和实际使用者保持一致，且权限必须是 600。

#数据加密传输

Rsync 默认不支持加密传输，如果需要使用 Rsync 传输重要性很高的数据，可以使用 SSH 模式。

Rsync 支持以下两种同步模式：

- 当源路径或目的路径的主机名后面包含一个冒号分隔符时，Rsync 使用 SSH 传输。
- 当源路径或目的路径的主机名后面包含两个冒号，或使用 Rsync://URL 时，Rsync 使用 TCP 直接连接 Rsync daemon。

在配置好 SSH 后，推荐参照以下方式来使用：

```
Rsync -av test.host.com:/path/to/files /des/path
```