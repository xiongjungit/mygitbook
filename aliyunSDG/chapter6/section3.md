很多站长饱受自己的小站被上传了webshell导致数据泄露或其他安全事件的困扰，下面将为大家详细介绍webshell及处置、防御方式。

#一.什么是WebShell？

“web”的含义是显然需要服务器开放web服务，“shell”的含义是取得对服务器某种程度上操作权限。webshell常常被称为匿名用户（入侵者）通过网站端口对网站服务器的某种程度上操作的权限。

简单理解： WebShell通常是以asp、php、jsp、asa或者cgi等网页文件形式存在的—种命令执行环境，也可以称为—种网页后门。黑客在入侵网站后，通常会将WebShell后门文件与网站服务器WEB目录下正常的网页文件混在—起，然后就可以使用浏览器来访问这些后门，得到命令执行环境，以达到控制网站或者WEB系统服务器的目的。

webshell中由于需要完成一些特殊的功能就不可避免的用到一些特殊的函数，我们也就可以对着特征值做检查来定位webshell，同样的webshell本身也会进行加密来躲避这种检测。

#二.webshell长什么样子

以下是asp webshell的样例，从界面看，它的功能还是比较全的，可以对服务器的文件目录进行读写操作，如果你是网站管理员的话肯定是不希望普通用户获得下面的权限的。

![webshell](http://docs-aliyun.cn-hangzhou.oss.aliyun-inc.com/assets/pic/60859/cn_zh/1508832382077/webshell.jpg)

#三.WebShell是如何入侵系统的？

1）利用站点上传漏洞实现上传webshell

利用系统前台的上传业务，上传WebShell脚本，上传的目录往往具有可执行的权限。在web中有上传图像、上传资料文件的地方，上传完后通常会向客户端返回上传的文件的完整URL信息，有时候不反馈，我们也可以猜到常见的image、upload等目录下面，如果Web对网站存取权限或者文件夹目录权限控制不严，就可能被利用进行webshell攻击，攻击者可以利用上传功能上传一个脚本文件，然后在通过url访问这个脚本，脚本就被执行。然后就会导致黑客可以上传webshell到网站的任意目录中，从而拿到网站的管理员控制权限。

2）黑客获取管理员的后台密码，登陆到后台系统，利用后台的管理工具向配置文件写入WebShell木马，或者黑客私自添加上传类型，允许脚本程序类似asp、php的格式的文件上传。

3）利用数据库备份与恢复功能获取webshell。如备份时候把备份文件的后缀改成asp。或者后台有mysql数据查询功能，黑客可以通过执行select..in To outfile 查询输出php文件，然后通过把代码插入到mysql，从而导致生成了webshell的木马。

4）系统其他站点被攻击，或者服务器上还搭载了ftp服务器，ftp服务器被攻击了，然后被注入了webshell的木马，从而导致网站系统也被感染。

5）黑客直接攻击Web服务器系统漏洞入侵Web服务器在系统层面也可能存在漏洞，如果黑客利用其漏洞攻击了服务器系统，那么黑客获取了其权限，则可以在web服务器目录里上传webshell文件。

#四.WebShell能够肆虐的重要原因是什么？

1）通过web站点漏洞上传webshell

WebShell能够被注入很大程度是由于服务器或中间件的安全漏洞。例如：老版本的IIS目录解析漏洞、文件名解析漏洞、应用后台暴露和弱口令、fast-CGI解析漏洞、apache文件解析漏洞、截断上传、后台数据库备份功能上传、利用数据库语句上传等漏洞实现。

2）站点部署时混入了webshell文件

我们发现有大量的客户在使用从网上下载的第三方开源代码时，混入了WebShell的恶意脚本，造成二次入侵或多次入侵，所以在部署前期，如果不是新开发的代码，需要对代码进行恶意文件扫描查杀，防止上线后被入侵。

#五.如何防止系统被植入WebShell?

- 配置必要的防火墙开启防火墙策略,防止暴露不必要的服务，为黑客提供利用条件。- 

- 对服务器进行[安全加固](https://help.aliyun.com/knowledge_list/60793.html?spm=5176.7760859.2.3.sWPZcI)，例如:关闭远程桌面这些功能、定期更换密码、禁止使用最高权限用户运行程序、使用https加密协议。

- 加强权限管理，对敏感目录进行权限设置，限制上传目录的脚本执行权限，不允许配置执行权限。

安装[webshell检测工具](https://www.aliyun.com/product/aegis?spm=5176.7760859.2.4.sWPZcI)，发现检测结果后，立即隔离查杀，并排查漏洞。

- 排查程序存在的漏洞，并及时修补漏洞，如果没有安全能力，可以通过[应急响应服务](https://promotion.aliyun.com/ntms/act/xianzhiresponse.html?spm=5176.7760859.2.5.sWPZcI)人工界入协助排查漏洞及入侵原因，同时可以选用[阿里云商业web应用防火墙](https://www.aliyun.com/product/waf?spm=5176.7760859.2.6.sWPZcI)防御，降低入侵机率。