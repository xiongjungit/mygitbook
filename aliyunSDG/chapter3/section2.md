Docker的快速增长得益于它不仅是一款简单、易用的轻量虚拟环境的工具，而且它还有自己特有的概念，并且越来越多的特性的添加。有时不是很容易获取有关于它们的正确信息，从而造成误解。尤其是，安全隐患常常随着情绪被高估或低估而非基于正确信息。但是为了让Docker成为方便、安全的工具，了解准确的信息去使用Docker是至关重要的。

#1.加固主机操作系统

在部署前需要对服务器操作系统进行安全加固，例如:更新所有软件补丁、配置强密码、关闭不必要的服务端口等，具体参考以下手册：

Windows操作系统安全加固

Linux操作系统加固

#2.使用强制访问控制策略

使用强制访问控制（mandatory access control (MAC)）对Docker中使用的各种资源根据业务场景的具体分析进行资源的访问的控制。

启用AppAamor或SElinux功能:

```
docker run --interactive --tty --security-opt="apparmor:PROFILENAME" centos /bin/bash

docker daemon --selinux-enabled
```

#3.配置严格的网络访问控制策略

根据实际应用会被外网访问的端口(例如:管理界面、API 2375端口等重要端口)、应用会与外网的交互网络地址、端口、协议等进行梳理，使用iptables或使用ECS安全组策略对网络的出入进行严格的访问控制。

#4.不要使用root用户运行docker应用程序

在实际应用程序使用中，有一些必须要使用root用户才能够进行的操作，那么从安全的角度，需要将这一部分与仅使用普通用户权限执行的部分分离解耦。那么如何在docker中使用普通用户权限对不需要root权限执行的部分进行实施呢？

在编写dockerfile时，使用类似如下的命令进行创建一个普通权限的用户，并设置创建的UID为以后运行程序的用户，如下：RUN useradd noroot -u 1000 -s /bin/bash —no-create-homeUSER norootRUN Application_name

docker命令参考：https://docs.docker.com/reference/builder/#userhttps://docs.docker.com/reference/builder/#run

#5.禁止使用特权

默认情况下，Docker容器是没有特权的，默认一个容器是不允许访问任何设备的；当使用—privileged选项时，则此窗口将能访问所有设备。例如：打开此选项后，即可以进行对Host中的/dev/下有的所有设备进行操作。若非要对host上的某些设备进行访问的话，可以使用—device来进行设备的添加，而不是全部的设备。

#6.Docker容器资源配额控制

##CPU资源配额控制
###CPU份额控制

Docker提供了–cpu-shares参数，在创建容器时指定容器所使用的CPU份额值。使用示例：

使用命令docker run -tid –cpu-shares 100 ubuntu:stress，创建容器，则最终生成的cgroup的cpu份额配置可以下面的文件中找到：

docker提供了–cpu-period、–cpu-quota两个参数控制容器可以分配到的CPU时钟周期。–cpu-period是用来指定容器对CPU的使用要在多长时间内做一次重新分配，而–cpu-quota是用来指定在这个周期内，最多可以有多少时间用来跑这个容器。跟–cpu-shares不同的是这种配置是指定一个绝对值，而且没有弹性在里面，容器对CPU资源的使用绝对不会超过配置的值。

cpu-period和cpu-quota的单位为微秒（μs）。cpu-period的最小值为1000微秒，最大值为1秒（10^6 μs），默认值为0.1秒（100000 μs）。cpu-quota的值默认为-1，表示不做控制。

举个例子，如果容器进程需要每1秒使用单个CPU的0.2秒时间，可以将cpu-period设置为1000000（即1秒），cpu-quota设置为200000（0.2秒）。当然，在多核情况下，如果允许容器进程需要完全占用两个CPU，则可以将cpu-period设置为100000（即0.1秒），cpu-quota设置为200000（0.2秒）。

使用示例：

使用命令docker run -tid –cpu-period 100000 –cpu-quota 200000 ubuntu，创建容器

###CPU core控制

对多核CPU的服务器，docker还可以控制容器运行限定使用哪些cpu内核和内存节点，即使用–cpuset-cpus和–cpuset-mems参数。对具有NUMA拓扑（具有多CPU、多内存节点）的服务器尤其有用，可以对需要高性能计算的容器进行性能最优的配置。如果服务器只有一个内存节点，则–cpuset-mems的配置基本上不会有明显效果。

使用示例：命令docker run -tid –name cpu1 –cpuset-cpus 0-2 ubuntu，表示创建的容器只能用0、1、2这三个内核。

###CPU配额控制参数的混合使用

当上面这些参数中时，cpu-shares控制只发生在容器竞争同一个内核的时间片时，如果通过cpuset-cpus指定容器A使用内核0，容器B只是用内核1，在主机上只有这两个容器使用对应内核的情况，它们各自占用全部的内核资源，cpu-shares没有明显效果。

cpu-period、cpu-quota这两个参数一般联合使用，在单核情况或者通过cpuset-cpus强制容器使用一个cpu内核的情况下，即使cpu-quota超过cpu-period，也不会使容器使用更多的CPU资源。

cpuset-cpus、cpuset-mems只在多核、多内存节点上的服务器上有效，并且必须与实际的物理配置匹配，否则也无法达到资源控制的目的。

##内存配额控制
和CPU控制一样，docker也提供了若干参数来控制容器的内存使用配额，可以控制容器的swap大小、可用内存大小等各种内存方面的控制。主要有以下参数：

memory-swappiness：控制进程将物理内存交换到swap分区的倾向，默认系数为60。系数越小，就越倾向于使用物理内存。值范围为0-100。当值为100时，表示尽量使用swap分区；当值为0时，表示禁用容器 swap 功能(这点不同于宿主机，宿主机 swappiness 设置为 0 也不保证 swap 不会被使用)。

–kernel-memory：内核内存，不会被交换到swap上。一般情况下，不建议修改，可以直接参考docker的官方文档。

–memory:设置容器使用的最大内存上限。默认单位为byte，可以使用K、G、M等带单位的字符串。

–memory-reservation：启用弹性的内存共享，当宿主机资源充足时，允许容器尽量多地使用内存，当检测到内存竞争或者低内存时，强制将容器的内存降低到memory-reservation所指定的内存大小。按照官方说法，不设置此选项时，有可能出现某些容器长时间占用大量内存，导致性能上的损失。

–memory-swap：等于内存和swap分区大小的总和，设置为-1时，表示swap分区的大小是无限的。默认单位为byte，可以使用K、G、M等带单位的字符串。如果–memory-swap的设置值小于–memory的值，则使用默认值，为–memory-swap值的两倍。

#7.不要运行不可信的Docker镜像

不要运行不可信的Docker镜像作为互联网服务器，避免运行不完全理解的Docker镜像作为互联网服务器。

#8.开启日志记录功能

Docker的日志可以分成两类，一类是stdout标准输出，另外一类是文件日志。

Dockerd支持的日志级别debug、info、warn、error、fatal，默认的日志级别为info。必要的情况下，还需要设置日志级别，这也可以通过配置文件，或者通过启动参数-l或—log-level。

方法一：配置文件/etc/docker/daemon.json

```
{  
  "log-level": "debug"  
}
```

方法二：docker run 的时候指定—log-driver=syslog —log-opt syslog-facility=daemon

#9.定期安全扫描和更新补丁

在生产环境中使用漏洞扫描工具可以检测镜像中的已知漏洞。容器通常都不是从头开始构建的，所以一定要进行安全扫描，便于及时发现基础镜像中任何可能存在的漏洞，并及时更新补丁。在应用程序交付生命周期中加入漏洞扫描的安全质量控制，防止部署易受攻击的容器。

通过采用以上积极的防范措施，即在整个容器的生命周期中建立和实施安全策略，可以有效的保证一个集成容器环境的安全性。

###参考文档:

https://benchmarks.cisecurity.org/downloads/show-single/index.cfm?file=docker16.100
https://linux-audit.com/docker-security-best-practices-for-your-vessel-and-containers/-
https://d3oypxn00j2a10.cloudfront.net/assets/img/Docker%20Security/WP_Intro_to_container_security_03.20.2015.pdf
https://docs.docker.com/edge/engine/reference/commandline/dockerd/