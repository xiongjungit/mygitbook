##调度服务
Rancher的核心调度逻辑是Rancher的一部分，它可以处理端口冲突和根据主机／容器上的标签进行调度的能力。除了核心调度逻辑，Rancher还使用应用商店里的Rancher Scheduler支持额外的调度策略。

- [能够调度多IP的主机](https://rancher.com/docs/rancher/v1.6/zh/rancher-services/scheduler/#multiple-ips)
- [基于资源约束的调度能力 (例如CPU和内存)](https://rancher.com/docs/rancher/v1.6/zh/rancher-services/scheduler/#resource-constraints)
- [能够限制在主机上调度哪些服务](https://rancher.com/docs/rancher/v1.6/zh/rancher-services/scheduler/#restrict-services-on-host)

> 注意：
这些特性不适用于Kubernets，因为Kubernets自己处理pod的调度。

###启用RANCHER调度程序
Rancher调度服务需要在环境中启用。如果你将它从你的环境中删除了，可以在应用商店 -> 官方认证中添加应用Rancher Scheduler。


###多IP主机调度
默认情况下，Rancher假定在调度发布有暴露端口的服务以及启动负载均衡器时，主机上只有一个IP可用。如果你的主机有多个可以使用的IP，则需要配置主机以允许Rancher调度程序知道哪些IP可用。

当主机上有多个IP可用于调度时，当通过服务或者负载均衡器发布端口时，Rancher将对所有可用的调度IP进行编排。当主机上的所有可用的调度IP都被分配给那个端口之后，调度器将会报告端口冲突。


###基于资源约束的调度
当Rancher主机被添加到Rancher时，它们将根据主机的大小自动限制资源。可以通过编辑主机来调整这些限制。在基础架构 -> 主机中，你可以从主机的下拉框中选择编辑。在主机的资源限制选项中，你可以更新内存或者CPU为你期望需要用到的最大值。

####在UI上设置资源预留
创建服务时，可以在安全/主机选项卡中指定内存预留和mCPU预留。设置这些预留时，服务的容器只能安排在具有可用资源的主机上。主机上这些资源的最大限制是根据主机的资源限制确定的。如果将容器调度到主机上会迫使这些限制超过阈值，则容器将不会被调度到主机上。

####在RANCHER COMPOSE中设置预留
docker-compose.yml示例

```
version: '2'
services:
  test:
    image: ubuntu:14.04.3
    stdin_open: true
    tty: true
    # Set the memory reservation of the container
    mem_reservation: 104857600
rancher-compose.yml示例

version: '2'
services:
  test:
    # Set the CPU reservation of the container
    milli_cpu_reservation: 10
    scale: 1
```

####在主机上调度指定服务
通常，大部分的容器调度规则定义在了服务中。服务对可以运行容器的主机设置了一些规则或限制。例如，容器必须安排在具有特定标签的主机上。Rancher还可以支持只允许将特定的容器调度到某个主机上。例如，你可能希望某台专用主机只运行数据库容器。

> 注意：
当你在主机上添加运行容器的限制标签时，你将需要包含一个特定标签，以便将Rancher的基础设施服务调度到主机上。没有这些服务，容器将无法正常运行。

对于任何主机，你可以通过从主机的下拉列表中选择编辑来编辑主机以添加可运行容器必须具有的标签。 在容器标签需求选项中，你可以添加要在服务中使用哪些标签，以便将这些容器调度到主机上。UI将自动将标签（例如，io.rancher.container.system =`）标记为必需的标签。