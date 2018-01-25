#漏洞描述

Memcached是一套常用的key-value缓存系统，由于它本身没有权限控制模块，所以对公网开放的Memcache服务很容易被攻击者扫描发现，攻击者通过命令交互可直接读取Memcached中的敏感信息。

#修复方案

因为Memcached没有权限控制功能，所以需要对访问来源进行限制。

##Memcached服务加固方案

###1. 配置访问控制。
建议用户不要将服务发布到互联网上而被黑客利用，可以通过ECS安全组规则或IPtables配置访问控制规则。
例如，在Linux环境中运行命令iptables -A INPUT -p tcp -s 192.168.0.2 —dport 11211 -j ACCEPT，在IPtables中添加此规则只允许192.168.0.2这个IP对11211端口进行访问。

###2. 绑定监听IP。
如果Memcached没有在公网开放的必要，可在Memcached启动时指定绑定的IP地址为 127.0.0.1。例如，在Linux环境中运行以下命令：
memcached -d -m 1024 -u memcached -l 127.0.0.1 -p 11211 -c 1024 -P /tmp/memcached.pid

###3. 最小化权限运行。
使用普通权限账号运行，指定Memcached用户。例如，在Linux环境中运行以下命令来运行Memcached：
memcached -d -m 1024 -u memcached -l 127.0.0.1 -p 11211 -c 1024 -P /tmp/memcached.pid

###4. 修改默认端口。
修改默认11211监听端口为11222端口。在Linux环境中运行以下命令：
```
memcached -d -m 1024 -u memcached -l 127.0.0.1 -p 11222 -c 1024 -P /tmp/memcached.pid
```

Memcached命令参数说明

- -d 是指启动一个守护进程。
- -m 是指分配给Memcached使用的内存数量，单位是MB，以上为1024MB。
- -u 是指运行Memcached的用户，推荐使用单独普通权限用户memcached，而不要使用root权限账户。
- -l 是指监听的服务器IP地址，例如指定服务器的IP地址为127.0.0.1。
- -p 是用来设置Memcached的监听端口，默认端口为11211。建议设置1024以上的端口。
- -c 是指最大运行的并发连接数，默认是1024。可按照您服务器的负载量来设定。
- -P 是指设置保存Memcached的pid文件，例如保存在 /tmp/memcached.pid 位置。

###5. 备份数据。
为避免数丢失，升级前请做好备份，或者建立ECS硬盘快照。

###6. 云盾检测及防护。
云盾态势感知已经支持该漏洞的检测和防护，您可以到[云盾管理控制台](https://yundun.console.aliyun.com/?spm=5176.7737553.2.4.TjFc1q)开通并使用。