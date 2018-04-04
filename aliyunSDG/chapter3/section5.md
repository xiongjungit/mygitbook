#Hadoop 介绍

Hadoop 是一个由 Apache 基金会所开发的一个开源、高可靠、可扩展的分布式计算框架。

Hadoop 的框架最核心的设计就是 HDFS 和 MapReduce 模块。HDFS 为海量的数据提供了存储，MapReduce 则为海量的数据提供了计算。

- HDFS 是 Google File System (GFS) 的开源实现。
- MapReduce 是一种编程模型，用于大规模数据集(大于1TB)的并行运算。

#Hadoop 环境安全问题

##1. WebUI 敏感信息泄漏

Hadoop 默认开放了很多端口来提供 WebUI 服务。下表列举了相关的端口信息：

<table><tbody><tr><th>模块</th><th>节点</th><th>默认端口</th></tr><tr><td rowspan="4">HDFS</td><td>NameNode</td><td>50070</td></tr><tr><td>SecondNameNode</td><td>50090</td></tr><tr><td>DataNode</td><td>50075</td></tr><tr><td>Backup/Checkpoint node</td><td>50105</td></tr><tr><td rowspan="2">MapReduce</td><td>JobTracker</td><td>50030</td></tr><tr><td>TaskTracker</td><td>50060</td></tr></tbody></table>

通过访问 NameNode WebUI 管理界面的 50070 端口，可以下载任意文件。而且，如果 DataNode 的默认端口 50075 开放，攻击者可以通过 HDSF 提供的 restful API 对 HDFS 存储的数据进行操作。

##2. MapReduce 代码执行漏洞

##3. Hadoop 的第三方插件安全漏洞

- Cloudera Manager 版本 <= 5.5

 - [Cloudera Manager CVE-2016-4949 Information Disclosure Vulnerability](http://www.securityfocus.com/bid/93882?spm=5176.7750128.2.3.MSTicp)
 - [Template rename stored XSS (CVE-2016-4948)](https://cve.mitre.org/cgi-bin/cvename.cgi?spm=5176.7750128.2.4.MSTicp&name=CVE-2016-4948)
 - [Kerberos wizard stored XSS (CVE-2016-4948)](https://cve.mitre.org/cgi-bin/cvename.cgi?spm=5176.7750128.2.5.MSTicp&name=CVE-2016-4948)
 - [Host addition reflected XSS (CVE-2016-4948)](https://cve.mitre.org/cgi-bin/cvename.cgi?spm=5176.7750128.2.6.MSTicp&name=CVE-2016-4948)


- Cloudera HUE 版本 <= 3.9.0

 - [Enumerating users with an unprivileged account (CVE-2016-4947)](https://cve.mitre.org/cgi-bin/cvename.cgi?spm=5176.7750128.2.7.MSTicp&name=CVE-2016-4947)
 - [Stored XSS (CVE-2016-4946)](https://cve.mitre.org/cgi-bin/cvename.cgi?spm=5176.7750128.2.8.MSTicp&name=CVE-2016-4946)
 - Open redirect


- Apache Ranger 版本 <= 0.5

 - Unauthenticated policy download
 - [Authenticated SQL injection (CVE-2016-2174)]()

- Apache Group Hadoop 2.6.x

 - [Apache Hadoop MapReduce信息泄露漏洞(CVE-2015-1776)](https://www.cve.mitre.org/cgi-bin/cvename.cgi?spm=5176.7750128.2.10.MSTicp&name=CVE-2015-1776)

##4. Hive 任意命令/代码执行漏洞

Hive 是建立在 Hadoop 上的数据仓库基础构架。它提供了一系列的工具，可以用来进行数据的提取转化加载（ETL），是一种可以存储、查询和分析存储在 Hadoop 中的大规模数据的机制。Hive 定义了简单的类 SQL 查询语言，称为 HQL，它允许熟悉 SQL 的用户查询数据。同时，HQL 语言也允许熟悉 MapReduce 开发者的开发自定义的 mapper 和 reducer 来处理内建的 mapper 和 reducer 无法完成的复杂的分析工作。

HQL 语言可以通过 transform 命令自定义 Hive 使用的 Map/Reduce 脚本，从而调用 Shell、Python 等语言，导致攻击者可以通过 Hive 接口等相关操作方式直接获取服务器权限。

#安全加固方案

根据上述 Hadoop 环境安全问题可以发现，对外暴露服务端口会存在严重的安全风险。建议您按照以下方式为 Hadoop 环境进行安全加固。

##1. 网络访问控制

使用 [安全组防火墙](https://help.aliyun.com/document_detail/25475.html?spm=5176.7750128.2.11.MSTicp) 或本地操作系统防火墙对访问源 IP 进行控制。如果您的 Hadoop 环境仅对内网服务器提供服务，建议不要将 Hadoop 服务所有端口发布到互联网。

##2. 启用认证功能

启用 Kerberos 认证功能。

##3. 更新补丁

不定期关注 Hadoop 官方发布的最新版本，并及时更新补丁。

#更多信息

Hadoop 所有端口信息

![](http://docs-aliyun.cn-hangzhou.oss.aliyun-inc.com/assets/pic/50128/cn_zh/1484796013767/Picture1.png)

[Hadoop safari : Hunting for vulnerabilities](http://archive.hack.lu/2016/Wavestone%20-%20Hack.lu%202016%20-%20Hadoop%20safari%20-%20Hunting%20for%20vulnerabilities%20-%20v1.0.pdf?spm=5176.7750128.2.12.MSTicp&file=Wavestone%20-%20Hack.lu%202016%20-%20Hadoop%20safari%20-%20Hunting%20for%20vulnerabilities%20-%20v1.0.pdf)
[Hadoop Default Ports Quick Reference](http://blog.cloudera.com/blog/2009/08/hadoop-default-ports-quick-reference/?spm=5176.7750128.2.13.MSTicp)