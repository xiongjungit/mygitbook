NFS（Network File System）是 FreeBSD 支持的一种文件系统，它允许网络中的计算机之间通过 TCP/IP 网络共享资源。不正确的配置和使用 NFS，会带来安全问题。

#概述

NFS 的不安全性，主要体现于以下 4 个方面:

- 缺少访问控制机制
- 没有真正的用户验证机制，只针对 RPC/Mount 请求进行过程验证
- 较早版本的 NFS 可以使未授权用户获得有效的文件句柄
- 在 RPC 远程调用中, SUID 程序具有超级用户权限

#加固方案

为有效应对以上安全隐患，推荐您使用下述加固方案。

#配置共享目录（/etc/exports）

使用 anonuid，anongid 配置共享目录，这样可以使挂载到 NFS 服务器的客户机仅具有最小权限。不要使用 no_root_squash。

#使用网络访问控制

使用 [安全组策略](https://help.aliyun.com/document_detail/25475.html?spm=5176.7751143.2.3.xWQYhd) 或 iptable 防火墙限制能够连接到 NFS 服务器的机器范围。

```
iptables -A INPUT -i eth0 -p TCP -s 192.168.0.0/24 --dport 111 -j ACCEPT
iptables -A INPUT -i eth0 -p UDP -s 192.168.0.0/24 --dport 111 -j ACCEPT
iptables -A INPUT -i eth0 -p TCP -s 140.0.0.0/8 --dport 111 -j ACCEPT
iptables -A INPUT -i eth0 -p UDP -s 140.0.0.0/8 --dport 111 -j ACCEPT
```

#账号验证

使用 Kerberos V5 作为登录验证系统，要求所有访问人员使用账号登录，提高安全性。

#设置 NFSD 的 COPY 数目

在 Linux 中，NFSD 的 COPY 数目定义在启动文件 /etc/rc.d/init.d/nfs 中，默认值为 8。

最佳的 COPY 数目一般取决于可能的客户机数目。您可以通过测试来找到 COPY 数目的近似最佳值，并手动设置该参数。

#选择传输协议

对于不同的网络情况，有针对地选择 UDP 或 TCP 传输协议。传输协议可以自动选择，也可以手动设置。

```
mount -t nfs -o sync,tcp,noatime,rsize=1024,wsize=1024 EXPORT_MACHINE:/EXPORTED_DIR /DIR
```

UDP 协议传输速度快，非连接传输时便捷，但其传输稳定性不如 TCP，当网络不稳定或者黑客入侵时很容易使 NFS 性能大幅降低，甚至导致网络瘫痪。一般情况下，使用 TCP 的 NFS 比较稳定，使用 UDP 的 NFS 速度较快。

- 在机器较少，网络状况较好的情况下，使用 UDP 协议能带来较好的性能。
- 当机器较多，网络情况复杂时，推荐使用 TCP 协议（V2 只支持 UDP 协议）。
- 在局域网中使用 UDP 协议较好，因为局域网有比较稳定的网络保证，使用 UDP 可以带来更好的性能。
- 在广域网中推荐使用 TCP 协议，TCP 协议能让 NFS 在复杂的网络环境中保持最好的传输稳定性。

#限制客户机数量

修改 /etc/hosts.allow 和 /etc /hosts.deny 来限制客户机数量。

```
/etc/hosts.allow
portmap: 192.168.0.0/255.255.255.0 : allow
portmap: 140.116.44.125 : allow
/etc/hosts.deny
portmap: ALL : deny
```

#改变默认的 NFS 端口

NFS 默认使用的是 111 端口，使用 port 参数可以改变这个端口值。改变默认端口值能够在一定程度上增强安全性。

#配置 nosuid 和 noexec

SUID (Set User ID) 或 SGID (Set Group ID) 程序可以让普通用户以超过自己权限来执行。很多 SUID/SGID 可执行程序是必须的，但也可能被一些恶意的本地用户利用，获取本不应有的权限。

尽量减少所有者是 root，或是在 root 组中却拥有 SUID/SGID 属性的文件。您可以删除这样的文件或更改其属性，如：

- 使用 nosuid 选项禁止 set-UID 程序在 NFS 服务器上运行，可以在 /etc/exports 加入一行：

```
/www www.abc.com(rw, root_squash, nosuid)
```

- 使用 noexec 禁止直接执行其中的二进制文件。