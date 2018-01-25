#说明
本文提到的挖矿程序排查场景，仅为技术人员提供故障排查思路，不保证与攻击者实际使用方式一致，具体场景以实际情况为准。

#问题描述
云服务器 ECS Linux 服务器上 CPU 使用率超过 70%，严重时可达到 100%，或者服务器响应越来越慢。

#原因分析

##恶意 minerd、tplink 进程
在服务器上运行 top 命令，结果如下：

![top](http://docs-aliyun.cn-hangzhou.oss.aliyun-inc.com/assets/pic/41206/cn_zh/1511512265249/Image%201.png)

可以看到，有一个 minerd （或 tplink）的异常进程，占用了大量 CPU 资源。该进程是服务器被入侵后，被恶意安装的比特币挖矿程序，一般存在于 /tmp/ 目录下。

如果使用 top 命令查看不到所述进程，可以用 ps 命令检查相关进程。例如，

![ps](http://docs-aliyun.cn-hangzhou.oss.aliyun-inc.com/assets/pic/41206/cn_zh/1511512525962/Image%202.png)

可以看到，服务器中存在这个进程。如果它不是您主动开启的，则很可能是被入侵所致。服务器被恶意利用来挖比特币。

##隐藏的恶意模块
黑客通过驱动 rootkit 程序入侵主机，并部署隐藏挖矿程序，CPU 使用率可能达到 90-100%。该场景无法通过 top 命令和 ps 命令来检测确认。

#处理方案
##恶意 minerd、tplink 进程
- 使用如下命令，通过 PID 获取对应文件的路径。然后，找到并删除对应的文件。
```
ls -l /proc/$PID/exe
```
其中，$PID 为进程对应的 PID 号，可以通过 ps 或者 top 获取。

- 使用 kill 命令关闭进程。

- 建议您平时增强服务器的安全维护，优化代码，以避免因程序漏洞等导致服务器被入侵。

##隐藏的恶意模块
被隐藏的恶意模块一般有：raid.ko、iptable_mac.ko、snd_pcs.ko、usb_pcs.ko 和 ipv6_kac.ko。您可以使用 file /lib/udev/usb_control/... 命令，分别检查是否存在以上模块。

例如，使用以下命令查看是否存在 iptable_mac.ko 模块：

```
file /lib/udev/usb_control/iptable_mac.ko
```

结果如下图所示，表明存在隐藏的 iptable_mac.ko 模块。

![ko](http://docs-aliyun.cn-hangzhou.oss.aliyun-inc.com/assets/pic/41206/cn_zh/1489484776410/%E7%B2%98%E8%B4%B4%E5%9B%BE%E7%89%87.png)

  