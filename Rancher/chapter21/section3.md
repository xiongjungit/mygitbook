##常见的故障排查与修复方法
请先阅读有关Rancher Server和Rancher Agent的常见问题。

本节假设你能够成功启动Rancher Server并添加主机。

###服务/容器
####为什么我只能编辑容器的名称？
Docker容器在创建之后就不可更改了。唯一可更改的内容是我们要存储的不属于Docker容器本身的那一部分数据。 无论是停止、启动或是重新启动，它始终在使用相同的容器。如需改变任何内容都需要删除或重新创建一个容器。
你可以克隆，即选择已存在的容器，并基于已有容器的配置提前在添加服务界面中填入所有要设置的内容，如果你忘记填入某项内容，可以通过克隆来改变它之后删除旧的容器。

####关联的容器/服务在RANCHER中是如何工作的？
在Docker中，关联的容器（在 docker run中使用--link）会出现在容器的/etc/hosts中。在Rancher中，我们不需要更改容器的/etc/hosts文件，而是通过运行一个内部DNS服务器来关联容器，DNS服务器会返回给我们正确的IP。

####求助! 我不能通过RANCHER的界面打开命令行或查看日志。RANCHER是如何去访问容器的命令行和日志的?
Agent主机有可能会暴露在公网上，Agent上接受到的访问容器命令行或者日志的请求是不可信的。Rancher Server中发出的请求包括一个JWT（JSON Web Token)，JWT是由服务器签名并且可由Agent校验的，Agent可以判断出请求是否来自服务器，JWT中包括了有效期限，有效期为5分钟。这个有效期可以防止它被长时间使用。如果JWT被拦截而且没有用SSL时，这一点尤为重要。

如果你运行docker logs -f (rancher-agent名称或ID）。日志会显示令牌过期的信息，随后检查Rancher Server主机和Rancher Agent主机的时钟是否同步。

####在哪里可以看到我的服务日志?
在服务的详细页中，我们提供了一个服务日志的页签日志。在日志页签中，列出了和服务相关的所有事件，包括时间戳和事件相关描述，这些日志将会保留24小时。

###跨主机通信
如果容器运行在不同主机上，不能够ping通彼此, 可能是由一些常见的问题引起的.

####如何检查跨主机通信是否正常?
在应用->基础设施中，检查 healthcheck 应用的状态。如果是active跨主机通信就是正常的。

手动测试，你可以进入任何一个容器中，去ping另一个容器的内部IP。在主机页面中可能会隐藏掉基础设施的容器，如需查看点击“显示系统容器”的复选框。

####UI中显示的主机IP是否正确?
有时，Docker网桥的IP地址会被错误的作为了主机IP，而并没有正确的选择真实的主机IP。这个错误的IP通常是172.17.42.1或以172.17.x.x开头的IP。如果是这种情况，在使用docker run命令添加主机时，请用真实主机的IP地址来配置CATTLE_AGENT_IP环境变量。

```
$ sudo docker run -d -e CATTLE_AGENT_IP=<HOST_IP> --privileged \
    -v /var/run/docker.sock:/var/run/docker.sock \
    rancher/agent:v0.8.2 http://SERVER_IP:8080/v1/scripts/xxxx
```

####在UBUNTU上运行容器时彼此间不能正常通信。
如果你的系统开启了UFW，请关闭UFW或更改/etc/default/ufw中的策略为：

```
DEFAULT_FORWARD_POLICY="ACCEPT"
```

####RANCHER的默认子网（10.42.0.0/16）在我的网络环境中已经被使用或禁止使用，我应该怎么去更改这个子网？
Rancher Overlay网络默认使用的子网是10.42.0.0/16。如果这个子网已经被使用，你将需要更改Rancher网络中使用的默认子网。你要确保基础设施服务里的Network组件中使用着合适的子网。这个子网定义在该服务的rancher－compose.yml文件中的default_network里。

要更改Rancher的IPsec或VXLAN网络驱动，你将需要在环境模版中修改网络基础设施服务的配置。创建新环境模板或编辑现有环境模板时，可以通过单击编辑来配置网络基础结构服务的配置。在编辑页面中，选择配置选项　>　子网输入不同子网，点击配置。在任何新环境中将使用环境模板更新后的子网，编辑已经有的环境模板不会更改现在已有环境的子网。

这个实例是通过升级网络驱动的rancher-compose.yml文件去改变子网为10.32.0.0/16.

```
ipsec:
  network_driver:
    name: Rancher IPsec
    default_network:
      name: ipsec
      host_ports: true
      subnets:
      # After the configuration option is updated, the default subnet address is updated
      - network_address: 10.32.0.0/16
      dns:
      - 169.254.169.250
      dns_search:
      - rancher.internal
    cni_config:
      '10-rancher.conf':
        name: rancher-cni-network
        type: rancher-bridge
        bridge: docker0
        # After the configuration option is updated, the default subnet address is updated
        bridgeSubnet: 10.32.0.0/16
        logToFile: /var/log/rancher-cni.log
        isDebugLevel: false
        isDefaultGateway: true
        hostNat: true
        hairpinMode: true
        mtu: 1500
        linkMTUOverhead: 98
        ipam:
          type: rancher-cni-ipam
          logToFile: /var/log/rancher-cni.log
          isDebugLevel: false
          routes:
          - dst: 169.254.169.250/32
```

> 注意：
随着Rancher通过升级基础服务来更新子网，以前通过API更新子网的方法将不再适用。

###DNS

####如何查看我的DNS是否配置正确?
如果你想查看Rancher　DNS配置，点击应用 > 基础服务。点击network-services应用，选择metadata，在metadata中，找到名为network-services-metadata-dns-X的容器，通过UI点击执行命令行后，可以进入该容器的命令行，然后执行如下命令。

```
$ cat /etc/rancher-dns/answers.json
```

####CENTOS
为什么我的容器无法连接到网络?
如果你在主机上运行一个容器（如：docker run -it ubuntu）该容器不能与互联网或其他主机通信，那可能是遇到了网络问题。

Centos默认设置/proc/sys/net/ipv4/ip_forward为0，这从底层阻断了Docker所有网络。Docker将此值设置为1，但如果在CentOS上运行service restart network，则其将被重新设置为0。


###负载均衡
####为什么我的负载均衡一直是INITIALIZING状态?
负载均衡器自动对其启用健康检查。 如果负载均衡器处于初始化状态，则很可能主机之间无法进行跨主机通信。

####我如何查看负载均衡的配置?
如果要查看负载均衡器的配置，你需要用进入负载均衡器容器内部查找配置文件，你可以在页面选择负载均衡容器的执行命令行

```
$ cat /etc/haproxy/haproxy.cfg
```

该文件将提供负载均衡器的所有配置详细信息。

####我在哪能找到HAPROXY的日志?
HAProxy的日志可以在负载均衡器容器内找到。 负载均衡器容器的docker logs只提供与负载均衡器相关的服务的详细信息，但不提供实际的HAProxy日志记录。

```
$ cat /var/log/haproxy
```

###高可用
####RANCHER COMPOSE EXECUTOR和GO-MACHINE-SERVICE不断重启.
在高可用集群中，如果你正在使用代理服务器后，如果rancher-compose-executor和go-machine-service不断重启，请确保你的代理使用正确的协议。

###认证

####求助！我打开了访问控制但不能访问RANCHER了，我该如何重置RANCHER禁用访问控制？
如果你的身份认证出现问题（例如你的GitHub身份认证已损坏），则可能无法访问Rancher。 要重新获得对Rancher的访问权限，你需要在数据库中关闭访问控制。 为此，你需要访问运行Rancher Server的主机。

```
$ docker exec -it <rancher_server_container_ID> mysql
```

> 注意：
这个 <rancher_server_container_ID>是具有Rancher数据库的容器。 如果你升级并创建了一个Rancher数据容器，则需要使用Rancher数据容器的ID而不是Rancher Server容器。

访问Cattle数据库。

```
mysql> use cattle;
```

查看setting表。

```
mysql> select * from setting;
```

更改api.security.enabled为false，并清除api.auth.provider.configured的值。此更改将关闭访问控制，任何人都可以使用UI / API访问Rancher Server。

```
mysql> update setting set value="false" where name="api.security.enabled";
mysql> update setting set value="" where name="api.auth.provider.configured";
```

确认更改在setting表中生效。

```
mysql> select * from setting;
```

可能需要约1分钟才能在用户界面中关闭身份认证，然后你可以通过刷新网页来登陆没有访问控制的Rancher Server。