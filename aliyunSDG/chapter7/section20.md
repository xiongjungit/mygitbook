# 跨站攻击

## 漏洞描述
跨站脚本攻击（Cross-site scripting，简称XSS攻击），通常发生在客户端，可被用于进行隐私窃取、钓鱼欺骗、密码偷取、恶意代码传播等攻击行为。XSS攻击使用到的技术主要为HTML和Javascript脚本，也包括VBScript和ActionScript脚本等。
恶意攻击者将对客户端有危害的代码放到服务器上作为一个网页内容，用户不经意打开此网页时，这些恶意代码会注入到用户的浏览器中并执行，从而使用户受到攻击。一般而言，利用跨站脚本攻击，攻击者可窃取会话cookie，从而获得用户的隐私信息，甚至包括密码等敏感信息。

## 漏洞危害
XSS攻击对Web服务器本身虽无直接危害，但是它借助网站进行传播，对网站用户进行攻击，窃取网站用户账号信息等，从而也会对网站产生较严重的危害。XSS攻击可导致以下危害：

- 钓鱼欺骗：最典型的就是利用目标网站的反射型跨站脚本漏洞将目标网站重定向到钓鱼网站，或者通过注入钓鱼JavaScript脚本以监控目标网站的表单输入，甚至攻击者基于DHTML技术发起更高级的钓鱼攻击。
- 网站挂马：跨站时，攻击者利用Iframe标签嵌入隐藏的恶意网站，将被攻击者定向到恶意网站上、或弹出恶意网站窗口等方式，进行挂马攻击。
- 身份盗用：Cookie是用户对于特定网站的身份验证标志，XSS攻击可以盗取用户的cookie，从而利用该cookie盗取用户对该网站的操作权限。如果一个网站管理员用户的cookie被窃取，将会对网站引发巨大的危害。
- 盗取网站用户信息：当窃取到用户cookie从而获取到用户身份时，攻击者可以盗取到用户对网站的操作权限，从而查看用户隐私信息。
- 垃圾信息发送：在社交网站社区中，利用XSS漏洞借用被攻击者的身份发送大量的垃圾信息给特定的目标群。
- 劫持用户Web行为：一些高级的XSS攻击甚至可以劫持用户的Web行为，从而监视用户的浏览历史、发送与接收的数据等等。
- XSS蠕虫：借助XSS蠕虫病毒还可以用来打广告、刷流量、挂马、恶作剧、破坏网上数据、实施DDoS攻击等。

## 修复方案

### 方案一
目前，云盾的“DDoS高防IP服务”以及“Web应用防火墙”均提供对Web应用攻击的安全防护能力。选择以上服务开通Web应用攻击防护，可以保障您的服务器安全。

### 方案二
将用户所提供的内容输入输出进行过滤。可以运用下面这些函数对出现XSS漏洞的参数进行过滤：
- PHP的htmlentities()或是htmlspecialchars()
- Python的cgi.escape()
- ASP的Server.HTMLEncode()
- ASP.NET的Server.HtmlEncode()或功能更强的Microsoft Anti-Cross Site Scripting Library
- Java的xssprotect(Open Source Library)
- Node.js的node-validator

### 方案三
使用开源的漏洞修复插件。（需要系统管理员懂得编程并且能够修改服务器代码。）