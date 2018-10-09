##安装 Rancher Server
Rancher是使用一系列的Docker容器进行部署的。运行Rancher跟启动两个容器一样简单。一个容器作为管理服务器部署，另外一个作为集群节点的Agent部署

- [Rancher Server - 单容器部署 (non-HA)](https://rancher.com/docs/rancher/v1.6/zh/installing-rancher/installing-server/#single-container)
- [Rancher Server - 单容器部署 (non-HA) - 使用外置数据库](https://rancher.com/docs/rancher/v1.6/zh/installing-rancher/installing-server/#single-container-external-database)
- [Rancher Server - 单容器部署 (non-HA)- 挂载MySQL数据库的数据目录](https://rancher.com/docs/rancher/v1.6/zh/installing-rancher/installing-server/#single-container-bind-mount)
- [Rancher Server - 多节点的HA部署](https://rancher.com/docs/rancher/v1.6/zh/installing-rancher/installing-server/#multi-nodes)
- [Rancher Server - 使用AWS的Elastic/Classic Load Balancer作为Rancher Server HA的负载均衡器](https://rancher.com/docs/rancher/v1.6/zh/installing-rancher/installing-server/#elb)
- [Rancher Server - 使用TLS认证的AD/OPENLDAP](https://rancher.com/docs/rancher/v1.6/zh/installing-rancher/installing-server/#ldap)
- [Rancher Server - 在HTTP代理后方启动 Rancher Server](https://rancher.com/docs/rancher/v1.6/zh/installing-rancher/installing-server/#http-proxy)
- [Rancher Server - 通过SSL连接MySQL](https://rancher.com/docs/rancher/v1.6/zh/installing-rancher/installing-server/#mysql-ssl)

> 注意：
你可以运行Rancher Server的容器的命令 docker run rancher/server --help 来获得所有选项以及帮助信息。

###安装需求
- 所有安装有支持的Docker版本的现代Linux发行版。 RancherOS, Ubuntu, RHEL/CentOS 7 都是经过严格的测试。
 - 对于 RHEL/CentOS, 默认的 storage driver, 例如 devicemapper using loopback, 并不被Docker推荐。 请参考Docker的文档去修改使用其他的storage driver。
 - 对于 RHEL/CentOS, 如果你想使用 SELinux, 你需要安装额外的 SELinux 组件.
- 1GB内存
- 精确的时钟同步服务 (例如 ntpd)
- MySQL服务器需要 max_connections 的设置 > 150
 - MYSQL配置需求
   - 选项1: 用默认COMPACT选项运行Antelope
   - 选项2: 运行MySQL 5.7，使用Barracuda。默认选项ROW_FORMAT需设置成Dynamic
 - 推荐设定
   - max_packet_size >= 32M
   - innodb_log_file_size >= 256M (如果你已有现存数据库，请根据实际情况更改此设定)
   - innodb_file_per_table=1
   - innodb_buffer_pool_size >= 1GB (对于更高需求的配置，请在专属MySQL服务器机器上使用4-8G的值)

> 注意：
目前Rancher中并不支持Docker for Mac

###RANCHER SERVER 标签
Rancher Server当前版本中有2个不同的标签。对于每一个主要的release标签，我们都会提供对应版本的文档。

- rancher/server:latest 此标签是我们的最新一次开发的构建版本。这些构建已经被我们的CI框架自动验证测试。但这些release并不代表可以在生产环境部署。
- rancher/server:stable 此标签是我们最新一个稳定的release构建。这个标签代表我们推荐在生产环境中使用的版本。

请不要使用任何带有 rc{n} 前缀的release。这些构建都是Rancher团队的测试构建。


###启动 RANCHER SERVER - 单容器部署 (NON-HA)
在安装了Docker的Linux服务器上，使用一个简单的命令就可以启动一个单实例的Rancher。

```
$ sudo docker run -d --restart=unless-stopped -p 8080:8080 rancher/server
```

###RANCHER UI
UI以及API会使用 8080 端口对外服务。下载Docker镜像完成后，需要1到2分钟的时间Rancher才能完全启动并提供服务。

访问如下的URL: http://<SERVER_IP>:8080。<SERVER_IP> 是运行Rancher Server的主机的公共IP地址。

当UI已经启动并运行，你可以先添加主机 或者在应用商店中选择一个容器编排引擎。在默认情况下，如果没有选择不同的容器编排引擎，当前环境会使用Cattle引擎。在主机被添加都Rancher中后，你可以开始添加服务或者从应用商店通过应用模版启动一个应用。


###启动 RANCHER SERVER - 单容器部署 - 使用外部数据库
除了使用内部的数据库，你可以启动一个Rancher Server并使用一个外部的数据库。启动命令与之前一样，但添加了一些额外的参数去说明如何连接你的外部数据库。

> 注意：
在你的外部数据库中，只需要提前创建数据库名和数据库用户。Rancher会自动创建Rancher所需要的数据库表。

以下是创建数据库和数据库用户的SQL命令例子

```
> CREATE DATABASE IF NOT EXISTS cattle COLLATE = 'utf8_general_ci' CHARACTER SET = 'utf8';
> GRANT ALL ON cattle.* TO 'cattle'@'%' IDENTIFIED BY 'cattle';
> GRANT ALL ON cattle.* TO 'cattle'@'localhost' IDENTIFIED BY 'cattle';
```

启动一个Rancher连接一个外部数据库，你需要在启动容器的命令中添加额外参数。

```
$ sudo docker run -d --restart=unless-stopped -p 8080:8080 rancher/server \
    --db-host myhost.example.com --db-port 3306 --db-user username --db-pass password --db-name cattle
```

大部分的输入参数都有默认值并且是可选的，只有MySQL server的地址是必须输入的。

```
--db-host               IP or hostname of MySQL server
--db-port               port of MySQL server (default: 3306)
--db-user               username for MySQL login (default: cattle)
--db-pass               password for MySQL login (default: cattle)
--db-name               MySQL database name to use (default: cattle)
```

> 注意：
在之前版本的Rancher Server中，我们需要使用环境变量去连接外部数据库。在新版本中，这些环境变量会继续生效，但Rancher建议使用命令参数代替。


###启动 RANCHER SERVER - 单容器部署 - 挂载MYSQL数据库的数据目录
在Rancher Server容器中，如果你想使用一个主机上的卷来持久化数据库，如下命令可以在启动Rancher时挂载MySQL的数据卷。

```
$ sudo docker run -d -v <host_vol>:/var/lib/mysql --restart=unless-stopped -p 8080:8080 rancher/server
```

使用这条命令，数据库就会持久化在主机上。如果你有一个现有的Rancher Server容器并且想挂在MySQL的数据卷，可以参考以下的Rancher升级介绍。


###启动 RANCHER SERVER - 多节点的HA部署
在高可用(HA)的模式下运行Rancher Server与使用外部数据库运行Rancher Server一样简单，需要暴露一个额外的端口，添加额外的参数到启动命令中，并且运行一个外部的负载均衡就可以了。

####HA部署需求
- HA 节点:
 - 所有安装有支持的Docker版本的现代Linux发行版 RancherOS, Ubuntu, RHEL/CentOS 7 都是经过严格的测试。
    - 对于 RHEL/CentOS, 默认的 storage driver, 例如 devicemapper using loopback, 并不被Docker推荐。 请参考Docker的文档去修改使用其他的storage driver。
    - 对于 RHEL/CentOS, 如果你想使用 SELinux, 你需要 安装额外的 SELinux 组件.
  - 9345, 8080 端口需要在各个节点之间能够互相访问
  - 1GB内存
- MySQL数据库
 - 至少 1 GB内存
 - 每个Rancher Server节点需要50个连接 (例如：3个节点的Rancher则需要至少150个连接)
 - MYSQL配置要求
   - 选项1: 用默认COMPACT选项运行Antelope
   - 选项2: 运行MySQL 5.7，使用Barracuda。默认选项ROW_FORMAT需设置成Dynamic
- 外部负载均衡服务器
 - 负载均衡服务器需要能访问Rancher Server节点的 8080 端口

> 注意：
目前Rancher中并不支持Docker for Mac

###大规模部署建议
- 每一个Rancher Server节点需要有4 GB 或者8 GB的堆空间，意味着需要8 GB或者16 GB内存
- MySQL数据库需要有高性能磁盘
- 对于一个完整的HA，建议使用一个有副本的Mysql数据库。另一种选择则是使用Galera集群并强制写入一个MySQL节点。

在每个需要加入Rancher Server HA集群的节点上，运行以下命令：
```
# Launch on each node in your HA cluster
$ docker run -d --restart=unless-stopped -p 8080:8080 -p 9345:9345 rancher/server \
     --db-host myhost.example.com --db-port 3306 --db-user username --db-pass password --db-name cattle \
     --advertise-address <IP_of_the_Node>
```
在每个节点上，<IP_of_the_Node> 需要在每个节点上唯一，因为这个IP会被添加到HA的设置中。

如果你修改了 -p 8080:8080 并在host上暴露了一个不一样的端口，你需要添加 --advertise-http-port <host_port> 参数到命令中。

> 注意：
你可以使用 docker run rancher/server --help 获得命令的帮助信息

配置一个外部的负载均衡器，这个负责均衡负责将例如80或443端口的流量，转发到运行Rancher Server的节点的8080端口中。负载均衡器必须支持websockets 以及 forwarded-for 的Http请求头以支持Rancher的功能。参考 使用SSL 这个配置的例子。

###ADVERTISE-ADDRESS选项
|选项|	例子|	描述|
|:-|:-|:-|
|IP address|	--advertise-address 192.168.100.100	|使用指定IP
|Interface|	--advertise-address eth0	|从指定网络接口获取
|awslocal|	--advertise-address awslocal|	从这里获取http://169.254.169.254/latest/meta-data/local-ipv4
|ipify|	--advertise-address ipify	|从这里获取https://api.ipify.org

###HA模式下的RANCHER SERVER节点
如果你的Rancher Server节点上的IP修改了，你的节点将不再存在于Rancher HA集群中。你必须停止在--advertise-address配置了不正确IP的Rancher Server容器并启动一个使用正确IP地址的Rancher Server的容器。


###使用AWS的ELASTIC/CLASSIC LOAD BALANCER作为RANCHER SERVER HA的负载均衡器
我们建议使用AWS的ELB作为你Rancher Server的负载均衡器。为了让ELB与Rancher的websockets正常工作，你需要开启proxy protocol模式并且保证HTTP support被停用。 默认的，ELB是在HTTP/HTTPS模式启用，在这个模式下不支持websockets。需要特别注意listener的配置。

如果你在配置ELB中遇到问题，我们建议你参考terraform version。

> 注意：
如果你正在使用自签名的证书, 请参考我们SSL部分里的如何在AWS里配置ELB.

###LISTENER 配置 - PLAINTEXT
简单的来说，使用非加密的负载均衡，需要以下的listener配置：

|Configuration Type	|Load Balancer Protocol|	Load Balancer Port|	Instance Protocol|	Instance Port
|:-|:-|:-|:-|:-|
|Plaintext	|TCP	|80	|TCP	|8080 (或者使用启动Rancher Server时 --advertise-http-port 指定的端口)

###启用 PROXY PROTOCOL
为了使websockets正常工作，ELB的proxy protocol policy必须被启用。

- 启用 proxy protocol 模式
```
$ aws elb create-load-balancer-policy --load-balancer-name <LB_NAME> --policy-name <POLICY_NAME> --policy-type-name ProxyProtocolPolicyType --policy-attributes AttributeName=ProxyProtocol,AttributeValue=true
$ aws elb set-load-balancer-policies-for-backend-server --load-balancer-name <LB_NAME> --instance-port 443 --policy-names <POLICY_NAME>
$ aws elb set-load-balancer-policies-for-backend-server --load-balancer-name <LB_NAME> --instance-port 8080 --policy-names <POLICY_NAME>
```
- Health check可以配置使用HTTP:8080下的 /ping 路径进行健康检查

###使用TERRAFORM进行配置
以下是使用Terraform配置的例子：

```
resource "aws_elb" "lb" {
  name               = "<LB_NAME>"
  availability_zones = ["us-west-2a","us-west-2b","us-west-2c"]
  security_groups = ["<SG_ID>"]

  listener {
    instance_port     = 8080
    instance_protocol = "tcp"
    lb_port           = 443
    lb_protocol       = "ssl"
    ssl_certificate_id = "<IAM_PATH_TO_CERT>"
  }

}

resource "aws_proxy_protocol_policy" "websockets" {
  load_balancer  = "${aws_elb.lb.name}"
  instance_ports = ["8080"]
}
```

###使用AWS的APPLICATION LOAD BALANCER(ALB) 作为RANCHER SERVER HA的负载均衡器

我们不再推荐使用AWS的Application Load Balancer (ALB)替代Elastic/Classic Load Balancer (ELB)。如果你依然选择使用ALB，你需要直接指定流量到Rancher Server节点上的HTTP端口，默认是8080。


###使用TLS认证的AD/OPENLDAP
为了在Rancher Server上启用Active Directory或OpenLDAP并使用TLS，Rancher Server容器在启动的时候需要配置LDAP证书，证书是LDAP服务提供方提供。证书保存在需要运行Rancher Server的Linux机器上。

启动Rancher并挂载证书。证书在容器内部 必须 命名为ca.crt。

```
$ sudo docker run -d --restart=unless-stopped -p 8080:8080 \
  -v /some/dir/cert.crt:/var/lib/rancher/etc/ssl/ca.crt rancher/server
```

你可以使用Rancher Server的日志检查传入的 ca.crt 证书是否生效

```
$ docker logs <SERVER_CONTAINER_ID>
```

在日志的开头，会显示证书已经被正确加载的信息。

```
Adding ca.crt to Certs.
Updating certificates in /etc/ssl/certs... 1 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d....done.
Certificate was added to keystore
```

###在HTTP代理后方启动 RANCHER SERVER
为了设置HTTP Proxy，Docker守护进程需要修改配置并指向这个代理。在启动Rancher Server前，需要编辑配置文件 /etc/default/docker 添加你的代理信息并重启Docker服务。

```
$ sudo vi /etc/default/docker
```

在文件中，编辑 #export http_proxy="http://127.0.0.1:3128/" 并修改它指向你的代理。保存修改并重启Docker。重启Docker的方式在每个OS上都不一样。

> 注意：
如果你使用systemd运行Docker, 请参考Docker官方的文档 去配置http proxy设置。

为了使得应用商店加载正常，HTTP代理设置必须在Rancher Server运行的环境变量中。

```
$ sudo docker run -d \
    -e http_proxy=<proxyURL> \
    -e https_proxy=<proxyURL> \
    -e no_proxy="localhost,127.0.0.1" \
    -e NO_PROXY="localhost,127.0.0.1" \
    --restart=unless-stopped -p 8080:8080 rancher/server
```

如果你不使用应用商店，则使用你平常的Rancher Server命令即可。

当向Rancher添加主机时，在HTTP代理中不需要额外的设置和要求。

###通过SSL连接MYSQL的RANCHER SERVER

> 注意：
目前在Rancher 1.6.3以上版本才支持

###重要提示
如果你正在使用LDAP或者AD认证方式，并且这些认证方式的证书发放方CA并不是MySQL服务器SSL的证书发放方CA，这篇指南无法适用于你的情况。

###前提条件
- MySQL服务器的证书或CA证书

###步骤
1. 拷贝MySQL服务器的证书或CA证书到Rancher Server的主机上。当启动rancher/server容器的时候你必须将证书挂载到/var/lib/rancher/etc/ssl/ca.crt。
2. 更改以下的模板的对应参数，构建一个JDBC URL:
jdbc:mysql://<DB_HOST>:<DB_PORT>/<DB_NAME>?useUnicode=true&characterEncoding=UTF-8&characterSetResults=UTF-8&prepStmtCacheSize=517&cachePrepStmts=true&prepStmtCacheSqlLimit=4096&socketTimeout=60000&connectTimeout=60000&sslServerCert=/var/lib/rancher/etc/ssl/ca.crt&useSSL=true
3. 使用环境变量CATTLE_DB_CATTLE_MYSQL_URL和CATTLE_DB_LIQUIBASE_MYSQL_URL来导入上面的JDBC URL到容器里面。
4. 加入环境变量CATTLE_DB_CATTLE_GO_PARAMS="tls=true"到容器里面。但是如果服务器证书的标题名字不符合服务器的主机名，你需要使用的是CATTLE_DB_CATTLE_GO_PARAMS="tls=skip-verify".

例子

```
$ export JDBC_URL="jdbc:mysql://<DB_HOST>:<DB_PORT>/<DB_NAME>?useUnicode=true&characterEncoding=UTF-8&characterSetResults=UTF-8&prepStmtCacheSize=517&cachePrepStmts=true&prepStmtCacheSqlLimit=4096&socketTimeout=60000&connectTimeout=60000&sslServerCert=/var/lib/rancher/etc/ssl/ca.crt&useSSL=true"

$ cat <<EOF > docker-compose.yml
version: '2'
  services:
    rancher-server:
      image: rancher/server:stable
      restart: unless-stopped
      command: --db-host <DB_HOST> --db-port <DB_PORT> --db-name <DB_NAME> --db-user <DB_USER> --db-pass <DB_PASS>
      environment:
        CATTLE_DB_LIQUIBASE_MYSQL_URL: $JDBC_URL
        CATTLE_DB_CATTLE_MYSQL_URL: $JDBC_URL
        CATTLE_DB_CATTLE_GO_PARAMS: "tls=true"
      volumes:
        - /path/to/mysql/ca.crt:/var/lib/rancher/etc/ssl/ca.crt
      ports:
        - "8080:8080"
EOF

$ docker-compose up -d
```

重要: 你必须在两个环境变量里都写入构建好的JDBC_URL，还必须加入--db-xxx参数!