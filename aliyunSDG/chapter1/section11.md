#问题现象
由于某些服务配置不当，导致服务器被黑客利用进行DDoS攻击。具体表现为机器对外带宽占满；使用抓包工具检测，可看到大量同一源端口的包对外发出。

#解决方案
##Linux系统
1.加固NTP服务

1. 通过Iptables配置只允许信任的IP访问本机UDP的123端口。
```
修改配置文件，然后执行以下命令：
echo "disable monitor" >> /etc/ntp.conf
执行以下命令重启NTP服务：
service ntpd restart
```

2. 我们建议您直接关闭掉NTP服务，并禁止其开机自启动。
```
执行service ntpd stop命令。
执行chkconfig ntpd off命令。
```

2.加固Chargen服务
1. 通过Iptables配置只允许信任的IP访问本机UDP的19端口。
2. 我们建议您直接关闭掉chargen服务。编辑配置文件”/etc/inetd.conf”，用#号注释掉chargen服务，然后重启inetd服务。

##Windows系统
1.加固Simple TCP/IP服务

注意： Windows系统默认不安装Simple TCP/IP服务，如果您无需使用此服务，可跳过此步骤。

1. 通过防火墙配置，只允许信任的IP访问本机UDP、TCP的19、17端口。
2. 我们建议您直接关闭Simple TCP/IP服务，并禁止自启动。
![](https://img.alicdn.com/tps/TB1B_g9LVXXXXczXVXXXXXXXXXX-857-529.png)

2.Web应用的加固

Wordpress的Pingback

1. 您可以通过增加Wordpress插件来防止Pinback被利用，加入如下过滤器：
```
add_filter( ‘xmlrpc_methods’, function( $methods ) {
   unset( $methods[‘pingback.ping’] );
   return $methods;
} );
```

2. 建议您直接删除xmlrpc.php文件。