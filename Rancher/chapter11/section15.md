##标签
Rancher在服务/容器和主机上使用标签来帮助管理Rancher的不同功能。

###RANCHER COMPOSE标签使用指南
标签用于帮助Rancher启动服务并利用Rancher的功能。下列的标签索引用于帮助用户使用Rancher Compose来创建服务。 这些标签在UI上有对应关系，不需要额外添加到服务上。

|Key	|Value	|描述
|:-|:-|:-|
|io.rancher.sidekicks	|服务名称	|用来定义哪些服务属于从容器
|io.rancher.loadbalancer.target.SERVICE_NAME	|REQUEST_HOST:SOURCE_PORT/REQUEST_PATH=TARGET_PORT	|用于判定 L7 Load Balancing
|io.rancher.container.dns	|true	|服务能够使用基于Rancher DNS的服务发现来解析其他服务，并能被其他服务解析。 如果你需要此DNS服务，且网络设置为主机，则此标签是必需的.
|io.rancher.container.hostname_override	|容器名称	|用于将容器的主机名设置为容器的名称 (例如： StackName_ServiceName_CreateIndex)
|io.rancher.container.start_once	|true	|用于设置容器只运行一次，并在容器为停止状态时显示active状态。
|io.rancher.container.pull_image	|always	|用于在部署容器之前始终拉取新的镜像.
|io.rancher.container.requested_ip	|IP于10.42.0.0/16的地址空间	|允许你选择容器的特定IP。从v1.6.6版本开始，服务内的容器将会使用配置的多个IP地址中的可用地址，直到这些地址全被占用。这些地址要用逗号隔开，例如10.42.100.100, 10.42.100.101。 在v1.6.6之前，只有服务中的一个容器可以使用这个特定IP。注意：如果IP在主机上不可用，则容器将以随机IP开始.
|io.rancher.container.dns.priority	|service_last	|在服务域之前使用主机的DNS搜索路径。 保证主机将从/etc/resolv.conf搜索后再对*.rancher.internal搜索。
|io.rancher.service.selector.container	|Selector Label Values	|用于服务，以支持选择独立的容器来加入DNS服务。 注意：作为独立容器，任何服务操作都不会影响独立容器（即停用/删除/编辑服务，健康检查等）。
|io.rancher.service.selector.link	|Selector Label Values	|用于服务以允许服务基于服务标签链接到服务。 示例：Service1具有标签io.rancher.service.selector.link：foo = bar。 任何添加到Rancher的具有foo=bar标签的服务将自动链接到Service1。
|io.rancher.scheduler.global	|true	|用于设置全局服务
|io.rancher.scheduler.affinity:host_label	|主机标签的Key Value配对	|用于根据主机标签在主机上编排容器
|io.rancher.scheduler.affinity:container_label	|容器标签的Key Value配对	|用于根据容器标签或服务名称在主机上编排容器
|io.rancher.scheduler.affinity:container	|容器名称	|用于根据容器名称在主机上安排容器
|io.rancher.lb_service.target	|Target Service Label Values	|用于配置负载均衡，以便将流量转发到与负载均衡位于同一主机上的容器。


> 注意：
对于以io.rancher.scheduler.affinity为前缀的标签，根据你想要匹配的方式（即相等或不相等，hard或soft规则）会有轻微的变化。 更多细节可以在这里找到这里.

####选择器标签
使用 选择器标签（即io.rancher.service.selector.link, io.rancher.service.selector.container），Rancher可以通过标签识别服务/容器，并将它们自动链接到服务。 将在以下两种情况下进行评估。 情景1是将 选择器标签 添加到服务时。 在情景1中，对所有现有标签进行评估，以查看它们是否与 选择器标签 匹配。 情景2是服务已经有 选择器标签 时。 在情景2中，检查添加到Rancher的任何新服务/容器，看看它是否符合链接条件。 选择器标签 可以由多个要求组成，以逗号分隔。 如果有多个要求，则必须满足所有要求，因此逗号分隔符作为** AND **逻辑运算符。

```
# 其中一个容器标签必须具有一个等于`foo1`的键，并且值等于`bar1`
foo1 = bar1
# 其中一个容器标签必须具有一个等于`foo2'的键，值不等于`bar2`
foo2 != bar2
＃其中一个容器标签必须有一个等于`foo3`的键，标签的值不重要
foo3
＃其中一个容器标签必须有一个等于`foo4`的键，值等于`bar1`或`bar2`
foo4 in (bar1, bar2)
＃其中一个容器标签必须有一个等于`foo5'的键和'bar3`或`bar4`以外的值
foo5 notin (bar3, bar4)
```

> 注意：
如果标签有中包含逗号的标签，则选择器将无法与标签匹配，因为 选择器标签 可以匹配任何没有关联值的键。 示例：io.rancher.service.selector.link: foo=bar1,bar2的标签将转换为任何服务必须具有一个标签为foo的键值，并且值等于bar1 和另一个带有等于bar2的标签。 它不会选择一个键等于foo，并且值等于bar1，bar2的标签的服务。

####逗号分隔列表的示例

```
service1:
  labels:
    # 添加选择器标签来接收其他服务
    io.rancher.service.selector.link: hello != world, hello1 in (world1, world2), foo = bar
```

在此示例中，将链接到service1的服务需要满足以下所有条件：

- 具有键等于hello并且值不等于world的标签
- 具有键等于“hello1”但值可以等于world1或world2的标签
- 具有键等于foo和值等于bar的标签

以下示例，service2在部署时会自动链接到service1。

```
service2:
   labels:
      hello: test
      hello1: world2
      foo: bar
```

###服务上的系统标签
除了Rancher Compose可以使用的标签之外，Rancher在启动服务时还会创建一系列系统标签。

|Key	|描述
|:-|:-|
|io.rancher.stack.name/io.rancher.project.name	|根据应用名称创建
|io.rancher.stack_service.name/io.rancher.project_service.name	|根据服务名称创建
|io.rancher.service.deployment.unit	|根据部署的从容器服务创建
|io.rancher.service.launch.config	|基于从容器服务的配置创建。
|io.rancher.service.requested.host.id	|根据该服务安排在哪个主机上创建

###主机标签
主机标签 可以在主机注册期间添加到主机，创建后可通过编辑在主机中添加。

|Key	|Value	|描述
|:-|:-|:-|
|io.rancher.host.external_dns_ip	|用于外部DNS的IP, 例如： a.b.c.d	|用于外部DNS服务，并需要对DNS记录进行编程使用主机IP以外的IP

###自动创建的主机标签
Rancher会自动创建与主机的linux内核版本和Docker Engine版本相关的主机标签。 这些标签可以用于调度.

|Key	|Value	|描述
|:-|:-|:-|
|io.rancher.host.linux_kernel_version	|主机上的Linux内核版本 (例如3.19)	|主机上运行的Linux内核的版本
|io.rancher.host.docker_version	|主机上的Docker版本（例如1.10.3）	|主机上运行的Docker Engine版本
|io.rancher.host.provider	|云提供商信息	|云提供商名称（目前仅适用于AWS）
|io.rancher.host.region	|云提供商区域	|云提供商区域（目前仅适用于AWS）
|io.rancher.host.zone	|云提供商可用区	|云提供商可用区（目前仅适用于AWS）

###本地DOCKER标签
|Key	|Value	|描述
|:-|:-|:-|
|io.rancher.container.network	|true	|将此标签添加到docker run命令中，以将Rancher网络添加到容器中

###目标服务标签
负载均衡可以配置为将流量优先分发于同负载均衡为同一主机的目标容器。 根据标签的值，负载均衡将被配置为将流量定向到指定的容器，或者将流量的优先级设置为某些指定的容器。 默认情况下，负载平衡器以Round-robin算法将流量分发到目标服务下的所有容器。

|Key	|Value	|描述
|:-|:-|:-|
|io.rancher.lb_service.target	|only-local	|只能将流量转发到与负载均衡为相同主机的容器上。 如果同一主机上没有目标服务的容器，则不会将流量转发到该服务。
|io.rancher.lb_service.target	|prefer-local	|将流量优先于同负载均衡容器为同一主机上的容器。 如果在同一主机上没有目标服务的容器，则流量将被路由到其他拥有目标服务容器的宿主机上。