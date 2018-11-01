# Crossdomain.xml 配置不当

## 漏洞描述
网站根目录下的 crossdomain.xml 文件指明了远程 Flash 是否可以加载当前网站的资源（图片、网页内容、Flash等）。如果配置不当，可能导致遭受跨站请求伪造（CSRF）攻击。

## 修复方案
对于不需要从外部加载资源的网站，在 crossdomain.xml 文件中更改allow-access-from的domain属性为域名白名单。