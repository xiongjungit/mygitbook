##服务
- Cattle对服务采用标准Docker Compose术语，并将基本服务定义为从同一Docker镜像创建的一个或多个容器。一旦服务（消费者）链接到同一个应用中的另一个服务（生产者）相关的DNS记录 会被自动创建，“消费”服务的容器可以发现这些容器。在Rancher创建服务的其他好处包括：

- 服务高可用性（HA）：Rancher会不断监控服务中的容器状态，并主动管理以确保所需的服务实例规模。当健康的容器小于（或者多于）正常服务所需容器规模，主机不可用，容器故障或者不能满足健康检查就会被触发。

- 健康检查: Rancher通过在主机上运行healthcheck的基础设施服务，从而实现了容器和服务的分布式健康检查系统。这个healthcheck服务内部使用HAProxy来检查应用程序的运行状况。当在单个容器或服务上启用健康检查时，Rancher将监控每个容器。

###用户界面中的服务选项
在以下示例中，我们假设你已经创建了一个应用, 设置了你的主机，并准备好开始构建应用程序来。

我们将在添加服务的过程中了解一些服务的选项，最后将介绍如何创建一个连接到Mongo数据库的LetsChat应用程序。

在应用中，你可以通过单击添加服务按钮添加服务。也可以在应用列表中添加服务 ，每个单个应用都可以看到添加服务按钮。

在数量部分，你可以使用滑块来指定要为服务启动的容器的数量。或者，你可以选择总是在每台主机上运行一个此容器的实例。使用此选项时，你的服务将被部署到该环境中的任何主机上。如果你在调度选项卡中创建了调度规则，则Rancher将仅在符合调度规则的主机上启动容器。

你还需要输入名称，如果需要，还可以输入服务描述。

为服务设置所需的镜像。你可以使用DockerHub上的任何镜像，以及已添加到你的环境中的任何镜像仓库。镜像名称的语法与docker run命令中使用的语法相同。

镜像名称的语法。默认情况下，我们从Dockerhub中拉取。如果没有指定标签，我们将拉取标签为tag的镜像。

[registry-name]/[namespace]/[imagename]:[version]

在镜像名称下方，有一个复选框创建前总是拉取镜像。默认情况下，这是被勾选的。选择此选项后，每次在主机上启动容器的时候，都将始终尝试拉取镜像，即使该镜像已被缓存在了该主机上。

####选项
Rancher努力与Docker保持一致，我们的目标是，支持任何docker run所支持的选项。端口映射和服务链接显示在主页面上，但所有其他选项都在不同的选项卡中。

默认情况下，服务中的所有容器都以分离模式运行，例如：docker run命令中的-d。

#####端口映射
当配置了映射端口后，你可以通过主机上的公共端口访问容器暴露的端口。在端口映射部分中，需要设置暴露在主机上的端口。该端口将流量指向你设置的私有端口。私有端口通常是容器上暴露的端口（例如：镜像的Dockerfile中的EXPOSE）。当你映射一个端口时，Rancher将会在启动容器之前检查主机是否有端口冲突。

当使用端口映射时，如果服务的容器规模大于具有可用端口的主机数量时，你的服务将被阻塞在正在激活状态。如果你查看服务的详细信息，你将可以看到Error状态的容器，这表明容器由于无法在主机上找到未被占用的端口而失败。该服务将继续尝试，如果发现有主机/端口可用，则该服务将在该主机上启动一个容器。

> 注意：
当在Rancher中暴露端口时，它只会显示创建时暴露端口。如果端口映射有任何改变，它不会在docker ps中更新，因为Rancher通过管理iptable规则，来实现端口动态变更的。

#####随机端口映射
如果你想要利用Rancher的随机端口映射，公共端口可以留空，你只需要定义私有端口。

#####链接服务
如果你的环境中已经创建了其他服务，则可以将已有服务链接到你正在创建的服务。正在创建的服务中的所有容器都会链接到目标服务中的所有容器。链接就像docker run命令中的--link功能一样。

链接是基于Rancher内部DNS的附加功能，当你不需要按服务名称解析服务时，可以使用链接。

####RANCHER 选项
除了提供docker run支持的所有选项之外，Rancher还通过UI提供了额外选项。

#####健康检查
如果Rancher中主机不能正常工作来（例如：处于reconnecting或inactive状态），你需要配置健康检查，以使Rancher将服务中的容器调度到其他的主机上。

> 注意：
健康检查仅适用于托管网络的服务。如果你选择任何其他网络，则不能被监察到。

在健康检查选项卡中，你可以选择检查服务的TCP连接或HTTP响应。

阅读有关Rancher如何处理健康检查的更多详细信息。

#####标签/调度
在标签选项卡中，Rancher允许将任何标签添加到服务的容器中。标签在创建调度规则时非常有用。在调度选项卡中，你可以使用主机标签，容器/服务标签，和容器/服务名称来创建你服务需要的调度规则。

阅读有关标签与调度的更多细节。

###在UI中添加服务
首先，我们通过设置数量为1个容器的服务来创建我们的数据库，给它设置名称database，并使用mongo:latest镜像。不需要其他的配置，点击创建。该服务将立即启动。

现在我们已经启动了我们的数据库服务，我们将把web服务添加到我们的应用中。这一次，我们将服务规模设置为2个容器，创建一个名称为web并使用sdelements/lets-chat作为镜像的服务。我们没有暴露Web服务中的任何端口，因为我们将添加负载均衡来实现服务访问。我们已经创建了数据库服务，我们将在服务链接的目标服务选择数据库服务，在名称中填写mongo。点击创建，我们的LetsChat应用程序已准备好了，我们马上可以用负载均衡服务来暴露端口了。

###RANCHER COMPOSE 中的服务选项
阅读更多关于配置Rancher Compose的细节。

Rancher Compose工具的工作方式和Docker Compose一样，并支持V1和V2版本的docker-compose.yml文件。要启用Rancher支持的功能，你还可以使用扩展或重写了docker-compose.yml的rancher-compose.yml文档。例如，rancher-compose.yml文档包含了服务的scale和healthcheck。

如果你不熟悉Docker Compose或Rancher Compose，我们建议你使用UI来启动你的服务。你可以通过单击应用的下拉列表中的查看配置来查看整个应用的配置（例如：与你的应用等效的docker-compose.yml文件和rancher-compose.yml文件）。

####链接服务
在Rancher中，环境中的所有服务都是可以通过DNS解析的，因此不需要明确设置服务链接，除非你希望使用特定的别名进行DNS解析。

> 注意：
我们目前不支持将从服务与主服务相关联，反之亦然。阅读更多关于Rancher内部DNS工作原理。

应用中的服务都是可以通过服务名称service_name来解析的，当然，你也可以通过链接来使用其他名称进行解析。

#####例子 DOCKER-COMPOSE.YML

```
version: '2'
services:
  web:
    labels:
      io.rancher.container.pull_image: always
    tty: true
    image: sdelements/lets-chat
    links:
    - database:mongo
    stdin_open: true
  database:
    labels:
      io.rancher.container.pull_image: always
    tty: true
    image: mongo
    stdin_open: true
```

在这个例子中，mongo可以解析为database。如果没有链接，web服务需要通过服务名称database来解析数据库服务。

对于不同应用中的服务，可以使用service_name.stack_name对服务进行解析。如果你希望使用特定别名进行DNS解析，则可以在docker-compose.yml中使用external_links。

#####例子 DOCKER-COMPOSE.YML
```
version: '2'
services:
  web:
    image: sdelements/lets-chat
    external_links:
    - alldbs/db1:mongo
```

在此示例中，alldbs应用中的db1服务将链接到web服务。在web服务中，mongo将可解析为db1。没有外部链接时，db1.alldbs将可解析为db1。

> 注意：
跨应用的服务发现受环境的限制（特意设计的）。不支持应用的跨环境发现。

###使用 RANCHER COMPOSE 添加服务
阅读更多关于配置Rancher Compose的详情.

我们将创建与上面通过UI创建的相同示例。首先，你将需要创建一个docker-compose.yml文件和一个rancher-compose.yml文件。使用Rancher Compose，我们可以一次启动应用程序中的所有服务。如果没有rancher-compose.yml文件，则所有服务将以1个容器的规模启动。

####例子 DOCKER-COMPOSE.YML

```
version: '2'
services:
  web:
    labels:
      io.rancher.container.pull_image: always
    tty: true
    image: sdelements/lets-chat
    links:
    - database:mongo
    stdin_open: true
  database:
    labels:
      io.rancher.container.pull_image: always
    tty: true
    image: mongo
    stdin_open: true
```

####例子 RANCHER-COMPOSE.YML

```
# 你想要拓展的效果服务
version: '2'
services:
  web:
    scale: 2
  database:
    scale: 1
```

创建文件后，可以将服务部署到Rancher Server。

```
#创建并启动一个没有环境变量的服务并选择一个应用
#如果没有提供应用名称，应用的名称将是命令运行的文件夹名称
#如果该应用没有存在于Rancher中，它将会被创建
$ rancher-compose --url URL_of_Rancher --access-key <username_of_environment_api_key> --secret-key <password_of_environment_api_key> -p LetsChatApp up -d

#创建并运行一个已经设置好环境变量的服务
$ rancher-compose -p LetsChatApp up -d
```

###从服务
Rancher支持通过使用从服务的概念对服务进行分组，从而使一组服务可以同时进行调度和扩缩容。通常创建具有一个或多个从服务的服务，来支持容器之间共享卷（即--volumes_from）和网络（即--net=container）。

你可能希望你的服务的使用volumes_from和net去连接其他服务。为了实现这一点，你需要在服务直接建立一个从属关系。通过从属关系，Rancher可以将这些服务作为一个单元进行扩容和调度。例如：B是A的从服务，Rancher始终将A和B作为一对进行部署，服务的数量规模将始终保持一致。

如果你有多个服务总需要部署在同一主机上，你也可以通过定义从属关系来实现它。

当给一个服务定义一个从服务时，你不需要链接该服务，因为从服务会自动被DNS解析到。

当在服务中使用负载均衡时，而该服务又拥有从服务的时候，你需要使用主服务作为负载均衡器的目标。从服务不能成为目标。
了解更多关于Rancher内部DNS的详情。

####在UI中添加从服务
要设置一个从服务，你可以点击+添加从容器按钮，按钮位于页面的数量那部分。第一个服务被认为是主服务，后面每个附加的从服务都是辅助服务。

####通过RANCHER COMPOSE添加从服务
要设置sidekick关系，请向其中一个服务添加标签。标签的键是io.rancher.sidekicks，该值是从服务。如果你要将多个服务添加为从服务，可以用逗号分隔。例：io.rancher.sidekicks: sidekick1, sidekick2, sidekick3

#####主服务
无论哪个服务包含sidekick标签都被认为是主服务，而各个sidekicks被视为从服务。主服务的数量将用作sidekick标签中所有从服务的数量。如果你的所有服务中的数量不同，则主服务的数量将用于所有服务。

当使用负载均衡器指向带有从服务的服务时，你只能指向主服务，从服务不能成为目标。

#####RANCHER COMPOSE里面的从容器例子:
例子docker-compose.yml

```
version: '2'
services:
  test:
    tty: true
    image: ubuntu:14.04.2
    stdin_open: true
    volumes_from:
    - test-data
    labels:
      io.rancher.sidekicks: test-data
  test-data:
    tty: true
    command:
    - cat
    image: ubuntu:14.04.2
    stdin_open: true
```

例子 rancher-compose.yml
```
version: '2'
services:
  test:
    scale: 2
  test-data:
    scale: 2
```

#####RANCHER COMPOSE里面的从服务例子:多服务使用来自同一个服务VOLUMES_FROM

如果你有多个服务，他们将使用相同的容器去做一个volumes_from，你可以添加第二个服务作为主服务的从服务，并使用相同的数据容器。由于只有主服务可以作为负载均衡的目标，请确保选择了正确的服务作为主服务（即，具有sidekick标签的服务）。
示例 docker-compose.yml

```
version: '2'
services:
  test-data:
    tty: true
    command:
    - cat
    image: ubuntu:14.04.2
    stdin_open: true
  test1:
    tty: true
    image: ubuntu:14.04.2
    stdin_open: true
    labels:
      io.rancher.sidekicks: test-data, test2
    volumes_from:
    - test-data
  test2:
    tty: true
    image: ubuntu:14.04.2
    stdin_open: true
    volumes_from:
    - test-data
```