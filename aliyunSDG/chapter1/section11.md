在您的网站接入 Web 应用防火墙（WAF） 防护后，您的网站接收到的请求来源 IP 将会是 WAF 的 IP 地址。

如果您的网站有获取真实的访客 IP 的需求，请参考以下方法：

#ASP

```
Request.ServerVariables("HTTP_X_REAL_IP")
```

#ASP.NET(C#)

```
Request.ServerVariables["HTTP_X_REAL_IP"]
```

#PHP

```
$_SERVER["HTTP_X_REAL_IP"]
```

#JSP

```
request.getHeader("HTTP_X_REAL_IP")
```