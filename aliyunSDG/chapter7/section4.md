# CRLF HTTP 头部注入漏洞

## 漏洞描述
CRLF 是“回车 + 换行”（\r\n）的简称。在 HTTP 协议中，HTTP Header 与 HTTP Body 是用两个 CRLF 符号进行分隔的，浏览器根据这两个 CRLF 符号来获取 HTTP 内容并显示。因此，一旦攻击者能够控制 HTTP 消息头中的字符，注入一些恶意的换行，就能注入一些会话 Cookie 或者 HTML 代码。

## 修复方案

1. 云盾 Web 应用防火墙服务可以有效拦截该漏洞的攻击代码。关于 Web 应用防火墙的更多介绍，请查看 [Web应用防火墙产品详情页](https://www.aliyun.com/product/waf?spm=a2c4g.11186623.2.10.58831b54TPoETW)。

2. 过滤 \r 、\n 之类的换行符，避免输入的数据污染到其他 HTTP 消息头。