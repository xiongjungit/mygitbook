##卷
###概览
持久化卷是有状态应用中非常重要的一部分。Rancher使你在多主机环境下使用卷变得非常容易。

####术语
卷插件和卷驱动同时在Docker和Rancher中使用。他们代表的是同一个东西: 一个Docker卷插件 可以给一个Docker容器提供本地卷或者共享的持久化卷的支持。Rancher卷插件(驱动)目前是以Docker卷插件的形式实现的。并且可以通过docker volume命令行来进行操作，但是这取决于存储技术。卷可以被环境中的某个主机，某些主机或者全部主机访问。Rancher对跨主机使用共享卷的复杂过程进行了封装。例如：rancher-nfs, rancher-ebs 和 pxd (portworx)。

存储驱动是关于容器和镜像是如何在Docker主机上被存储的。例如：aufs, btrfs, zfs, devicemapper等。这些驱动在Rancher的管控范围之外。Rancher UI混合了这个术语，但实际上指的是卷插件和卷驱动。更多关于存储驱动的插件信息信息，请查看这里。

###管理卷
在这一部分，你将会了解如何创建一个可以被容器之间共享的持久化卷。在这里我们将专门使用Rancher命令行。

> 注意：
UI可以用来管理除了由local卷驱动创建的卷。

####创建卷
你可以通过rancher volume create命令创建一个卷。

```
$ rancher volume create --driver local app-data
```

这将创建一个新的名为app-data的本地卷。名称必须由字母数字开头，后面可以接a-z0-9，_ (下划线), . (点) 或者- (横杠)。

--driver参数用来指定使用哪个卷驱动。Docker提供了一个local卷驱动。使用这个驱动的卷会将数据保存在主机的文件系统上，并且同一台主机上的任何容器都可以访问该数据。当使用local卷驱动时，其他主机上的任何容器都无法共享这个数据卷。

####列出卷
你可以列出环境中的卷。

```
$ rancher volume ls
```

如果你创建了一个app-data卷，你可能想知道为什么这个卷没有被列出来。你可以通过添加--all或者-a参数，来查看inactive的卷。

```
$ rancher volume ls --all
```

####删除卷
你可以通过rancher volume rm命令删除一个卷。

```
$ rancher volume rm app-data
```

####卷状态
卷有七个不同的状态：inactive, activating, active, deactivating, detached, removing 和 removed。

一个刚刚建好的卷的状态是inactive，直到有容器尝试挂载这个卷。

当容器创建时，关联的卷进入activating状态。一旦容器进入了running阶段，它等容器就会进入active状态。如果容器去挂载一个已经是active状态的卷，这并不会对该卷的状态产生影响。

当全部挂载了这个卷的容器都被开始删除了，这个卷进入deactivating状态。一旦容器被删除成功，卷进入detached状态。

当卷被标记为删除时，它进入一个removing状态。一旦数据被从主机上删除成功，它进入removed状态。被删除的卷不会出现在列出卷的结果里。但是它们将会继续在Rancher API里存在一段时间，这是为了调试和审计的目的。

###卷作用域
卷可以有不同的作用域。这指的是Rancher管理卷的不同级别。

目前，你可以通过Rancher Compose文件来创建不同类型的卷。有作用域的卷必须定义在docker-compose.yml文件中最顶层的volumes部分。默认情况下，将创建应用栈级别的卷，但是你可以通过修改其值来创建不同作用域的卷。

如果最顶层的定义被遗漏了，卷的行为将会有所不同。请查看更多详情。

通过UI你只能创建环境级别的卷。

####应用级别的卷
应用级别的卷是由创建它的应用来管理的。主要的好处是这种卷的生命周期是其应用生命周期的一部分，将由Rancher自动管理。

应用级别的存储卷，应用中的服务如果引用了相同的卷都将共享同一个存储卷。不在该应用内的服务则无法使用此存储卷。

Rancher中，应用级别的存储卷的命名规则为使用应用名称为前缀来表明该卷为此应用独有，且会以随机生成的一组数字结尾以确保没有重名。在引用该存储卷时，你依然可以使用原来的卷名称。比如，如果你在应用 stackA中创建了一个名为foo 的卷， 你的主机上显示的卷名称将为stackA_foo_<randomNumber>，但在你的服务中，你依然可以使用foo。

#####创建示例
下面的例子中，将会创建应用级别的卷data。

> 注意：
因为在文件中最顶层的volumes部分不存在其他配置值，所以这个卷的级别为应用级。

```
version: '2'
services:
  redis:
    image: redis:3.0.7
    volumes:
    - data:/data
volumes:
  data:
    driver: local
```

在上面的例子中，我们特意指定了卷驱动为local。默认情况下，卷驱动的值就是local。最简洁的定义data的方法是设置一个空值{}。请看下面的例子。

```
volumes:
  data: {}
```

在通过Rancher命令行创建应用之后，你可以列出卷来确认data卷已经创建成功。这个卷的名称将为<STACK_NAME>_data_<RANDOM_NUMBER>。

> 注意：
应用级别的卷可以被其他应用挂载。应用级别的卷并不是一种安全的机制。仅是为了管理卷的生命周期。

####环境级别的卷
环境级别的卷可能需要被环境中的全部容器共享。Rancher会把容器调度到卷所在的主机，从而保证容器可以挂载这个卷。

环境级别的卷并不能在某个环境中的全部的主机上自动共享。你需要借助一个共享驱动（例如：rancher-nfs）来实现跨主机共享。这意味着一个由local卷驱动创建的环境级别卷只能在一台主机上被访问到，所以使用该卷的容器都会被调度到这台主机上。

你在创建一个使用环境级别卷的服务之前，Rancher需要你先创建这个环境级别的卷。你可以使用任何配置好的卷驱动来创建卷。

环境级别卷的主要好处是，你可以轻松的在不同的服务应用之间共享数据。尤其是当这些应用和服务有着不同的生命周期需要被独立管理。用户可以对卷进行完全的管控

#####共享的环境级别卷示例
首选，创建一个环境级别的卷从而使其他应用共享这个卷。

```
$ rancher volume create --driver local redis-data-external
```

为了创建一个环境级别的卷，在最顶层的volume部分，你需要添加external: true。

```
version: '2'
services:
  redis:
    image: redis:3.0.7
    volumes:
    - redis-data-external:/data
volumes:
  redis-data-external:
    driver: local
    external: true  # 如果没有这个定义，将会创建一个应用级别的卷。
```

> 注意：
如果在volume中没有定义external: true，这个卷将会被创建为一个应用级别的卷.

在通过Rancher命令行创建应用之后，你可以列出卷来确认redis-data-external卷已经创建成功并且状态为active。

> 注意：
对一个服务进行扩容和缩容的时候，将会挂载或卸载同一个共享的卷。

任何新的应用都可以挂载同一个redis-data-external卷。最简单的方法就是复制compose文件中最顶层的volume部分。

```
volumes:
  redis-data-external:
    driver: local
    external: true
```

###V1与V2版本的COMPOSE对比
直到这里，我们讨论的一直是Docker V2 Compose的卷。如果你没有在V2 compose文件中的最顶层定义volumes，它将会按照Docker V1 Compose的方式来处理卷。

你也可能用到了Docker V1 Compose。在V1 compose文件中，不支持最顶层的volume部分。所以这时卷只能被定义在服务里。Rancher会把V1的卷定义直接传递给Docker。所以，卷不会被自动删除同时也无法确保可以正常调度到卷所在的主机。为了解决这个在V1卷下的调度问题，你需要使用调度标签。

> 注意：
请尽可能不要使用V1版本的Compose。

####V1版本的COMPOSE示例
注意这里没有volumes部分；这个配置在V1中不存在。

```
etcd:
  image: rancher/etcd:v2.3.7-11
  volumes:
  - etcd:/pdata
```

####V1和V2版本的COMPOSE文件
Docker compose的V2版本是V1版本的超集；两个格式都可以被使用。我们先创建一个环境级别的卷。

```
$ rancher volume create --driver local etcd_backup
```

这个例子中，etcd_backup是一个V2的环境级别的卷，etcd是一个V1的卷。因为没有定义volume，这隐式的将etcd设置为了V1的卷。

```
version: '2'
services:
  etcd:
    image: rancher/etcd:v2.3.7-11
    environment:
      EMBEDDED_BACKUPS: 'true'
      BACKUP_PERIOD: 5s
      BACKUP_RETENTION: 15s
    volumes:
    - etcd:/pdata
    - etcd_backup:/data-backup
volumes:
  etcd_backup:
    driver: local
    external: true
```

最后，如果你定义了一个空的volumes，这个卷将会被视为一个V1卷。这等同于yaml中完全没有volumes这部分。

```
version: '2'
volumes: {}
```