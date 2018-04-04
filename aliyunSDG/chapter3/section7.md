Elasticsearch 是一个基于 Lucene 的搜索服务，它提供了 RESTful web 接口的分布式、多用户全文搜索引擎 。Elasticsearch 是用 Java 开发的，并作为 Apache 许可条款下的开放源码发布，是第二大最流行的企业搜索引擎。

Elasticsearch 应用于云计算中，具有实时搜索、稳定、可靠、快速、安装使用方便等优势；但也存在一些安全隐患：默认安装完成后，Elasticsearch 可以使用 9200 端口通告 web 的方式访问查看数据信息。

#漏洞详情

Elasticsearch 中存在以下高危漏洞。

<table><tbody><tr><th width="16%">类型</th><th width="16%">CVE</th><th width="16%">受影响版本</th><th>描述</th></tr><tr><td>远程命令执行</td><td>CVE-2014-3120</td><td>-</td><td>Elasticsearch 的脚本执行 (scripting) 功能，可以很方便地对查询出来的数据进行再加工处理。但是，其使用的 MVEL 脚本引擎没有做过任何防护（或者沙盒包装），可以直接执行任意代码。</td></tr><tr><td>远程代码执行</td><td>-</td><td>1.3.0-1.3.7，1.4.0-1.4</td><td>Elasticsearch 使用 Groovy 作为脚本语言，虽然加入了沙盒进行控制，危险的代码会被拦截。但是由于沙盒限制不严格，仅通过黑白名单来判断，导致攻击者可以绕过沙盒，执行远程代码。</td></tr><tr><td>未授权访问</td><td>-</td><td>-</td><td>Elasticsearch 在安装了 River 机制之后可以同步多种数据库数据（包括关系型的MySQL、MongoDB 等）。如果 <code>http://localhost:9200/cat/indices</code>中 <code>indices</code> 包含了 <code>_river</code>，则代表 Elasticsearch 已安装 River 机制。而通过泄露的 <code>http://localhost:9200/_rvier/_search</code> URL 地址，攻击者可以获取到敏感信息。</td></tr></tbody></table>


#漏洞成因与危害

由于 Elasticsearch 的 HTTP 连接没有提供任何的权限控制措施，一旦部署在公共网络就容易有数据泄露的风险。

#安全加固方案

##使用最新的 Elasticsearch 版本

通过正规渠道（如 [Elastic 官网](https://www.elastic.co/downloads?spm=5176.7749913.2.3.AZI2Dw)）下载 Elasticsearch 的最新版本。

- 下载完成后，将下载文件的 sha1 值和下载时官网页面提供的 sha1 值进行对比，避免下载过程中被恶意攻击者拦截破坏文件，甚至注入恶意代码。
- 不要随便安装第三方的插件，插件有可能引入安全漏洞甚至本身自带后门，需谨慎使用。
- 关注 Elastic 网站，及时更新 Elasticsearch 至最新版本。Elasticsearch 每次版本发布都会优化和改进一部分功能，尤其是安全漏洞的补丁。同时，仔细阅读 Elasticsearch 的版本更新记录。

注意：更新升级前，建议您先进行快照备份，及本地测试。

##网络访问控制（推荐）

Elasticsearch 默认端口是 9200。

- 不要把 Elasticsearch 的 9200 端口服务发布到互联网上。
- 使用 [阿里云安全组防火墙](https://help.aliyun.com/document_detail/25475.html?spm=5176.7749913.2.4.AZI2Dw) 或本地操作系统防火墙对访问源 IP 进行隔离控制。

##绑定访问源 IP

进入 config 目录，修改 elasticsearch.yml 配置文件中以下参数：

```
network.bind_host: 192.168.0.1
# 设置绑定的 IP 地址，可以是 IPv4 或 IPv6 地址，默认为 0.0.0.0。
network.publish_host: 192.168.0.1
# 设置其它节点和该节点交互的 IP 地址，如果不设置它会自动判断，值必须是个真实的 IP 地址。
network.host: 192.168.0.1
# 同时设置上述两个参数：bind_host 和 publish_host。
```

##修改默认端口

进入 config 目录，修改 elasticsearch.yml 配置文件中以下参数：

```
ransport.tcp.port: 9300
# 设置节点间交互的 TCP 端口，默认是 9300。
transport.tcp.compress: true
# 设置是否压缩 TCP 传输时的数据，默认为 false，即不压缩。
http.port: 9200
# 设置对外服务的 HTTP 端口，默认为 9200。
```

##关闭 HTTP 访问

进入 config 目录，修改 elasticsearch.yml 配置文件中以下参数：

```
http.enabled: false
# 是否使用 HTTP 协议对外提供服务，默认为 true，即开启。
```

##使用 Shield 安全插件

Shield 是 Elastic 公司为 Elasticsearch 开发的一个安全插件。在安装此插件后，Shield 会拦截所有对 Elasticsearch 的请求，并进行认证与加密，保障 Elasticsearch 及相关系统的安全性。Shield 是商业插件，需要 Elasticsearch 的商业许可。第一次安装许可的时候，会提供 30 天的免费试用权限。30 天后，Shield 将会屏蔽 clusterhealth, cluster stats, index stats 等 API，其余功能不受影响。

用户认证

使用 Shield 可以定义一系列已知的用户，并用其认证用户请求。这些用户存在于抽象的“域”中。一个“域”可以是下面几种类型：

- LDAP 服务
- ActiveDirectory 服务
- 本地 esusers 配置文件（类似 /etc/passwd)

权限控制

Shield 的权限控制包含下面几种元素：

- 被保护的资源 SecuredResource：权限所应用到的对象，比如某个 index，cluster 等。
- 特权 Priviliege：角色对对象可以执行的一种或多种操作，比如 read，write 等。还可以是 indicies:/data/read/perlocate 等对某种对象特有的操作。
- 许可 Permissions：对被保护的资源拥有的一个或多个特权，如 read on the"products" index。
- 角色 Role：一组许可的集成，具有独立的名称。
- 用户 Users：用户实体，可以被赋予多种角色，他们可以对被保护的资源执行相应角色所拥有的各种特权。

安装 Shield

执行安装步骤前，请确保满足以下安装环境条件：

- 您安装了 Java7 或更新版本。
- 您将 Elasticsearch 1.5.0+ 解压安装到了本机上。如果您使用 APT 或 YUM 安装，默认的安装目录可能在 /usr/share/elasticsearch。

参照以下步骤完成安装：

1. 进入 Elasticsearch 安装目录：
```
cd /usr/share/elasticsearch
```

2. 安装 Elasticsearch 许可插件：
```
bin/plugin -i elasticsearch/license/latest
```

3. 安装 Shield 插件：
```
bin/plugin -i elasticsearch/shield/latest
```

4. 将 Shield 配置文件移动或链接至 /etc/elasticsearch/shield 目录中：
```
ln -s /usr/share/elasticsearch/config/shield /etc/elasticsearch/shield
```
说明：Elasticsearch 服务在启动时会在 /etc/elasticsearch/shield 目录下寻找 Shield 配置文件，而这些配置文件在安装 Shield 时会出现在 /usr/share/elasticsearch/config/shield 中，因此需要将配置文件移动或链接至该目录。

5. 重启 Elasticsearch 服务：
```
service elasticsearch restart
```

6. 新建一个 Elasticsearch 管理员账户，填写新密码：
```
bin/shield/esusers
useradd es_admin -r admin
```

7. 直接使用 RESTFUL API 访问 Elasticsearch 的请求都会被拒绝：
```
curl -XGET 'http://localhost:9200/'
```
需要在请求中添加用户名和密码：
```
curl -u es_admin -XGET 'http://localhost:9200/'
```

更多信息，请参考：

- [Shield 官方安装指南](https://www.elastic.co/downloads/shield?spm=5176.7749913.2.5.AZI2Dw)
- [Shield 官方使用配置指南](https://www.elastic.co/guide/en/shield/current/getting-started.html?spm=5176.7749913.2.6.AZI2Dw)


##修改默认的 Elasticsearch 集群名称

Elasticsearch 默认的集群名称是 elasticsearch，请在您的生产环境中将其修改成其他名称。确保在不同的环境和不同的集群下使用不同的名称；并且在监控集群节点时，如果有未知节点加入，一定要及时预警。

##不要以 root 身份运行 Elasticsearch

不要以 root 身份来运行 Elasticsearch，不要和其他服务共用相同的用户，并把用户的权限最小化。

应用示例：

```
sudo -u es-user ES_JAVA_OPTS="-Xms1024m -Xmx1024m"
/opt/elasticsearch/bin/elasticsearc
正确设置 Elasticsearch 的数据目录
```

请确保为 Elasticsearch 的目录分配了合理的读写权限，避免使用共享文件系统。确保只有 Elasticsearch 的启动用户才有权访问目录。日志目录也需要正确配置，避免泄露敏感信息。

##定期对 Elasticsearch 进行备份

使用 Elasticsearch 提供的备份还原机制，定期对 Elasticsearch 的数据进行快照备份。

##禁用批量删除索引

Elasticsearch 支持使用全部（_all）和通配符（*）来批量删除索引。在生产环境，该操作存在一定风险，你可以通过设置 action.destructive_requires_name: true 参数来禁用它。

##启用日志记录功能

Elasticsearch 的 config 文件夹里面有两个配置文件：

- elasticsearch.yml：基本配置文件。
- logging.yml：日志配置文件。由于 Elasticsearch 使用 log4j 来记录日志的，logging.yml 中的设置请按普通 log4j 配置文件进行设置。

启用日志功能需要修改 elasticsearch.yml 配置文件：

```
path.logs: /path/to/logs
# 设置日志文件的存储路径，默认是 Elasticsearch 根目录下的 logs 文件夹
```

更多信息

[Elasticsearch 安全方案](https://www.elastic.co/products/x-pack/security?spm=5176.7749913.2.7.AZI2Dw)
[Elasticsearch 安全加固](https://www.elastic.co/cn/blog/reinforce-the-security-of-elasticsearch-101?spm=5176.7749913.2.8.AZI2Dw)