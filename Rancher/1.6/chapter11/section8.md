##服务调度
在Rancher中，你可以根据严格或宽松的关联与斥关联规则，在特定主机上安排服务。 这些规则可以比较主机上的标签或主机上容器上的标签，以确定容器应该安排在哪个主机上。

默认情况下，Rancher将检测主机上的端口冲突，如果端口不可用，则不会将需要此端口的容器调度到这一主机上。

这个核心调度逻辑内置于Rancher，但Rancher还支持位于我们外部调度器中的其他调度能力，这是我们基础设施服务的一部分。其他调度能力包括：

- [多个IP的主机调度能力](https://rancher.com/docs/rancher/v1.6/zh/rancher-services/scheduler/#multiple-ips)
- [基于资源约束的调度能力 (例如 CPU和内存)](https://rancher.com/docs/rancher/v1.6/zh/rancher-services/scheduler/#resource-constraints)
- [能够限制在主机上安排哪些服务](https://rancher.com/docs/rancher/v1.6/zh/rancher-services/scheduler/#restrict-services-on-host)

###标签和调度规则
不管是通过服务或者负载均衡来创建容器时，我们都提供了为容器创建标签的选项，并且可以安排你想要放置容器的主机。 对于本节的剩余部分，我们将使用服务这个术语，但这些标签也适用于负载均衡器（即特定类型的服务）

调度规则提供了让Rancher选择要使用哪个主机的灵活性。 在Rancher中，我们使用标签来帮助定义调度规则。 你可以根据需要在容器上创建任意数量的标签。 通过多个调度规则，你可以完全控制容器在哪些主机上创建。 你可以要求在具有特定主机标签，容器标签或名称或特定服务的主机上启动该容器。 这些调度规则可以帮助你创建容器对主机的黑名单和白名单。

###在UI中添加标签
对于添加服务，可以在标签选项卡中添加标签。 对于添加负载均衡，也可以在标签选项卡中找到添加标签。

通过向负载均衡添加标签，每个负载均衡容器将接收该标签，该标签是一个键值对。 在Rancher中，我们使用这些容器标签来帮助定义调度规则。 你可以根据需要在负载均衡上创建任意数量的标签。 默认情况下，Rancher已经在每个容器上添加了系统相关的标签。

###在UI中调度选项
对于服务和负载均衡，标签可以在调度选项卡中找到。

对于 服务,
我们提供了两个选项来确定在哪里启动容器。

####选项1：在指定主机上运行 全部 容器
通过选择此选项，容器/服务将在特定主机上启动。 如果你的主机掉线，则容器也将离线。 如果你从容器页面创建一个容器，即使有端口冲突，容器也将被启动。 如果创建一个数量大于1且服务端口冲突的服务，则你的服务可能会停留在 Activating 状态，直到你编辑正确的服务数量为止。

####选项2：为每一个容器自动选择符合调度规则的主机
通过选择此选项，你可以灵活地选择调度规则。 遵循所有规则的任何主机都是可以启动容器的主机。 你可以通过点击 + 按钮添加规则。

对于负载均衡，只有选项2可用，因为端口冲突。 你只能添加调度规则。 点击 调度 选项卡。 你可以通过点击 添加调度规则 按钮添加任意数量的调度规则。

对于每个规则，你可以选择规则的条件。 有四种不同的条件，它们定义了遵守规则的严格程度。 字段确定要应用规则的字段。 键和值是要检查字段的值。 如果你启动了一个服务或负载均衡，Rancher将根据每个主机的负载来扩展容器在适用主机上的分发。 根据所选择的条件将确定适用的主机是什么。

> 注意：
对于添加服务/添加负载均衡，如果你在数量那里选择了 总是在每台主机上运行一个此容器的实例，则只有主机标签将显示为可能的字段。

####条件
- 必须 或 不能：Rancher只会使用与字段和值匹配或不匹配的主机。 如果Rancher找不到符合这些条件的所有规则的主机，你的服务可能会停留在 Activating 状态。 该服务将不断尝试找到容器的主机。 要修复此状态，你可以编辑服务的数量或添加/编辑将满足所有这些规则的其他主机。
- 应该或不应该：Rancher将尝试使用匹配字段和值的主机。 在没有匹配所有规则的主机的情况下，Rancher将逐个删除软约束（应该/不应该规则），直到主机满足剩余的约束。

####字段
- 主机标签：当选择要用于容器/服务的主机时，Rancher将检查主机上的标签，看它们是否与提供的键/值对匹配。 由于每个主机都可以有一个或多个标签，所以Rancher会将键/值对与主机上的所有标签进行比较。 将主机添加到Rancher时，可以向主机添加标签。 你还可以使用主机下拉菜单中的编辑选项来编辑主机上的标签。 活动主机上的标签列表可从关键字段的下拉列表中找到。
- 容器标签：选择此字段时，Rancher会查找已经具有与键/值对匹配的标签的容器的主机。 由于每个容器都可以有一个或多个标签，所以Rancher会将键/值对与主机中每个容器上的所有标签进行比较。 容器标签位于容器的标签选项中。 在容器启动后，你将无法编辑容器标签。 为了创建具有相同设置的新容器，你可以克隆容器或服务，并在启动之前添加标签。 运行容器上的用户标签列表可从关键字段的下拉列表中找到。
- 服务名称: Rancher将检查主机上是否有一个具有特定名称的服务。 如果在稍后的时间，该服务名称将更改或不活动/已删除，该规则将不再有效。 如果你选择此字段，则该值将需要以应用名称/服务名称的格式。 运行服务的列表可从值字段的下拉列表中获得。
- 容器名称: Rancher会检查一个主机是否有一个具有特定名称的容器。 如果稍后时间，容器有名称更改或不活动/已删除，该规则将不再有效。 运行容器的列表可从值字段的下拉列表中获得。

###在RANCHER COMPOSE中添加标签
Rancher根据docker-compose.yml文件中定义的labels来决定如何安排一个服务的容器。 所有带有调度的标签都将在docker-compose.yml文件中使用。 Rancher通过3个主要组件定义了调度规则：条件，字段和值。 条件决定了Rancher遵守规则的严格程度。 字段是要比较的项目。 价值是你在字段上定义的。 在介绍一些例子之前，我们将广泛讨论这些组件。

####调度条件
当我们编写我们的调度规则时，我们对每个规则都有条件，这说明了Rancher如何使用规则。亲和条件是当我们试图找到一个符合我们的价值的字段。反亲和条件是当我们试图找到一个不符合我们价值的字段时。

为了区分亲和力和反亲和度，我们在标签名称中添加_ne来表示标签是不符合字段和值。

规则也有硬条件和软条件。

一个硬条件相当于说必须或不能。 Rancher只会使用匹配或不匹配字段和值的主机。如果Rancher找不到符合这些条件的所有规则的主机，你的服务可能会停留在 Activating 状态。该服务将不断尝试找到容器的主机。要修复此状态，你可以编辑服务的数量或添加/编辑一台主机来满足所有这些规则。

一个软条件相当于应该或不应该。 Rancher将尝试使用与该字段和值相匹配的主机。在没有匹配所有规则的主机的情况下，Rancher将逐个删除软约束（应该/不应该规则），直到主机满足剩余的约束。

为了区分 must 和 should 条件，我们将“_soft”添加到我们的标签名称中，以表明标签是应该尝试匹配字段和值。

####字段
Rancher能够与主机标签，容器标签，容器名称或服务名称的值进行比较。 标签前缀是Rancher用来定义哪个字段将被评估的用法。

|字段	|标签前缀
|:-|:-|
|主机标签	|io.rancher.scheduler.affinity:host_label
|容器标签/服务名称|io.rancher.scheduler.affinity:container_label
|容器名称	|io.rancher.scheduler.affinity:container

请注意，服务名称中没有特定的前缀。 当Rancher创建服务时，会将系统标签添加到服务的所有容器中，以指示应用和服务名称。

当我们创建标签的关键字时，我们从一个字段前缀（例如io.rancher.scheduler.affinity：host_label）开始，根据我们正在寻找的条件，我们附加我们想要的条件类型。 例如，如果我们希望容器在不能等于（即_ne）主机标签值的主机上启动，则标签键将是io.rancher.scheduler.affinity：host_label_ne。

####值
你可以使用这些值来定义要检查的字段。 如果你有两个值要与同一条件和字段进行比较，则需要为标签名称使用一个标签。 对于标签的值，你需要使用逗号分隔列表。 如果有多个具有相同键的标签（例如io.rancher.scheduler.affinity：host_label_ne），则Rancher将使用与标签键一起使用的最后一个值覆盖任何先前的值。

```
labels:
  io.rancher.scheduler.affinity:host_label: key1=value1,key2=value2
```

####全局服务
将服务提供到全局服务中相当于在UI中的每个主机上选择总是在每台主机上运行一个此容器的实例。 这意味着将在环境中的任何主机上启动一个容器。 如果将新主机添加到环境中，并且主机满足全局服务的主机要求，则该服务将自动启动。

目前，全局服务只支持使用硬条件的主机标签字段。 这意味着只有在调度时才会遵守与主机标签相关的标签，并且必须或不能等于该值。 任何其他标签类型将被忽略。

#####例子 DOCKER-COMPOSE.YML

```
version: '2'
services:
  wordpress:
    labels:
      # 使wordpress成为全局服务
      io.rancher.scheduler.global: 'true'
      # 使wordpress只在具有key1 = value1标签的主机上运行容器
      io.rancher.scheduler.affinity:host_label: key1=value1
      # 使wordpress只在没有key2 = value2标签的主机上运行
      io.rancher.scheduler.affinity:host_label_ne: key2=value2
    image: wordpress
    links:
    - db: mysql
    stdin_open: true
```

####使用主机标签查找主机
将主机添加到Rancher时，你可以添加主机标签。 调度服务时，你可以利用这些标签来创建规则来选择要部署服务的主机。

#####使用主机标签的示例

```
labels:
  # 主机必须有`key1 = value1`的标签
  io.rancher.scheduler.affinity:host_label: key1=value1
  # 主机不得有`key2 = value2`的标签
  io.rancher.scheduler.affinity:host_label_ne: key2=value2
  # 主机应该有`key3 = value3`的标签
  io.rancher.scheduler.affinity:host_label_soft: key3=value3
  # 主机应该没有`key4 = value4`的标签
  io.rancher.scheduler.affinity:host_label_soft_ne: key4=value4
```

#####自动创建的主机标签
Rancher会自动创建与主机的linux内核版本和Docker Engine版本相关的主机标签。

|Key	|Value	|描述
|:-|:-|:-|
|io.rancher.host.linux_kernel_version	|主机上的Linux内核版本 (例如3.19)	|主机上运行的Linux内核的版本
|io.rancher.host.docker_version	|主机上的Docker版本（例如1.10.3）	|主机上运行的Docker Engine版本
|io.rancher.host.provider	|云提供商信息	|云提供商名称（目前仅适用于AWS）
|io.rancher.host.region	|云提供商区域	|云提供商区域（目前仅适用于AWS）
|io.rancher.host.zone	|云提供商可用区	|云提供商可用区（目前仅适用于AWS）

```
labels:
# 主机必须运行Docker版本1.10.3
io.rancher.scheduler.affinity:host_label: io.rancher.host.docker_version=1.10.3
# 主机必须不运行Docker 1.6版
io.rancher.scheduler.affinity:host_label_ne: io.rancher.host.docker_version=1.6
```

> 注意：
Rancher不支持在具有>=特定版本的主机上调度容器的概念。 你可以使用主机调度规则来创建特定的白名单和黑名单，以确定你的服务是否需要特定版本的Docker Engine。

####用容器标签查找主机
向Rancher添加容器或服务时，可以添加容器标签。 这些标签可以用于你希望规则与之进行比较的字段。 提醒：如果将全局服务设置为true，则无法使用。

> 注意：
如果容器标签有多个值，Rancher会查看主机上所有容器上的所有标签，以检查容器标签。 多个值不需要在主机上的同一容器上。

#####使用容器标签的示例

```
labels:
  # 主机必须有一个标签为`key1=value1`的容器
  io.rancher.scheduler.affinity:container_label: key1=value1
  # 主机不能有一个标签为`key2=value2`的容器
  io.rancher.scheduler.affinity:container_label_ne: key2=value2
  ＃主机应该有一个标签为`key3=value3`的容器
  io.rancher.scheduler.affinity:container_label_soft: key3=value3
  # 主机应该没有一个标签为`key4=value4`的容器
  io.rancher.scheduler.affinity:container_label_soft_ne: key4=value4
```

#####服务名称
当Rancher Compose启动服务的容器时，它也会自动创建多个容器标签。 因为检查一个特定的容器标签正在寻找一个key=value，所以我们可以使用这些系统标签作为我们规则的关键。 以下是在Rancher启动服务时在容器上创建的系统标签：

|标签	|值
|:-|:-|
|io.rancher.stack.name	|$${stack_name}
|io.rancher.stack_service.name	|$${stack_name}/$${service_name}


> 注意：
使用io.rancher.stack_service.name时，该值必须为应用名称/服务名称的格式。

宏$$ {stack_name}和$$ {service_name}也可以在任何其他标签中的docker-compose.yml文件中使用，并在服务启动时进行评估。

#####使用服务名称的示例

```
labels:
  # Host必须有一个服务名称为`value1`的容器
  io.rancher.scheduler.affinity:container_label: io.rancher.stack_service.name=stackname/servicename
```

####查找具有容器名称的主机
向Rancher添加容器时，可以给每个容器一个名称。 你可以使用此名称作为希望规则进行比较的字段。 提醒：如果将全局服务设置为true，则无法使用。

#####使用容器名称的示例

```
labels:
  # 主机必须有一个名为`value1`的容器
  io.rancher.scheduler.affinity:container: value1
  # 主机不能有一个名称为`value2`的容器
  io.rancher.scheduler.affinity:container_ne: value2
  # 主机应该有一个名称为`value3`的容器
  io.rancher.scheduler.affinity:container_soft: value3
  # 主机应该没有一个名为`value4`的容器
  io.rancher.scheduler.affinity:container_soft_ne: value4
```

###示例
####示例1:
典型的调度策略可能是尝试在不同的可用主机之间部署服务的容器。 实现这一点的一个方法是使用反相关性规则来关联自身:

```
labels:
  io.rancher.scheduler.affinity:container_label_ne: io.rancher.stack_service.name=$${stack_name}/$${service_name}
```

由于这是一个很强的反相关性规则，如果比例大于可用主机数量，我们可能会遇到问题。 在这种情况下，我们可能需要使用软反相关性规则，以便调度程序仍然允许将容器部署到已经具有该容器的主机。 基本上，这是一个软规则，所以如果没有更好的选择存在，它可以被忽略。
yaml labels: io.rancher.scheduler.affinity:container_label_soft_ne: io.rancher.stack_service.name=$${stack_name}/$${service_name}

#####示例2:
另一个例子可能是将所有容器部署在同一个主机上，而不考虑哪个主机。 在这种情况下，可以使用对其自身的软亲合力。

```
labels:
  io.rancher.scheduler.affinity:container_label_soft: io.rancher.stack_service.name=$${stack_name}/$${service_name}
```

如果选择了自己的硬约束规则，则第一个容器的部署将失败，因为目前没有运行该服务的主机。

###调度标签表
|标签	|值	|描述
|:-|:-|:-|
|io.rancher.scheduler.global	|true	|将此服务指定为全局服务
|io.rancher.scheduler.affinity:host_label	|key1=value1,key2=value2, etc…	|容器必须部署到具有标签key1=value1和key2 = value2的主机上
|io.rancher.scheduler.affinity:host_label_soft	|key1=value1,key2=value2	|容器应该被部署到具有标签key1=value1和key2=value2”的主机
|io.rancher.scheduler.affinity:host_label_ne	|key1=value1,key2=value2	|容器不能被部署到具有标签key1=value1或key2=value2的主机
|io.rancher.scheduler.affinity:host_label_soft_ne	|key1=value1,key2=value2	|容器不应该被部署到具有标签key1=value1或key2=value2的主机
|io.rancher.scheduler.affinity:container_label	|key1=value1,key2=value2	|容器必须部署到具有标签key1=value1和key2=value2的容器的主机上。 注意：这些标签不必在同一个容器上。 可以在同一主机内的不同容器上。
|io.rancher.scheduler.affinity:container_label_soft	|key1=value1,key2=value2	|容器应该部署到具有运行标签key1=value1和key2=value2的主机上
|io.rancher.scheduler.affinity:container_label_ne	|key1=value1,key2=value2	|容器不能部署到具有运行标签key1=value1或key2=value2的容器的主机上
|io.rancher.scheduler.affinity:container_label_soft_ne	|key1=value1,key2=value2	|容器不应该被部署到具有标签key1=value1或key2=value2的容器的主机上
|io.rancher.scheduler.affinity:container	|container_name1,container_name2	|容器必须部署到具有名称为container_name1和container_name2运行的容器的主机上
|io.rancher.scheduler.affinity:container_soft	|container_name1,container_name2	|容器应该被部署到具有名称为container_name1和container_name2运行的容器的主机上
|io.rancher.scheduler.affinity:container_ne	|container_name1,container_name2	|容器不能部署到具有名称为container_name1或container_name2运行的容器的主机上
|io.rancher.scheduler.affinity:container_soft_ne	|container_name1,container_name2	|容器不应该被部署到具有容器名称为container_name1或container_name2运行的主机