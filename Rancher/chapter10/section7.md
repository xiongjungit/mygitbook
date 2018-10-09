##存储服务
Rancher提供了不同的存储服务，从而使用户可以将存储卷映射到容器中。

###配置存储服务
当我们创建环境模板时，用户可以从应用商店选择需要在环境中的使用存储服务。

或者，如果用户已经创建了一个环境，你可以从 应用商店中选择并启动一个存储服务。

> 注意：
某些存储服务可能无法和一些容器编排调度引擎（例如，kubernetes）兼容。环境模板可以根据当前的编排调度框架限定可以使用的存储服务，而应用商店中则会显示全部的存储服务。

###查看存储驱动
在存储服务启动后，在基础架构 -> 存储的界面中可以看到一个存储驱动已经被创建出来。在这个界面中，用户可以查看当前环境中所有可用的存储驱动。存储驱动的名称和刚刚启动的存储服务所在的应用的名称保持一致。

对于每一种存储驱动，主机上运行的存储服务都会被显示出来。正常情况下，环境里的所有主机都会出现在该页面。同时，存储驱动提供的卷列表以及卷的状态也会被显示出来。你可以看到每个卷的名称（比如，主机上的卷名称），以及每个卷的挂载点。对于每个挂载点，其容器信息以及该挂载点在容器中映射的路径都会被显示出来。

###卷的作用域
Rancher的存储服务中，卷的作用域可以在不同的级别生效。目前，只有Rancher Compose支持创建不同的存储作用域。UI上仅仅支持环境级别的卷创建操作。

####应用级别
应用级别的存储卷，应用中的服务如果引用了相同的卷都将共享同一个存储卷。不在该应用内的服务则无法使用此存储卷。

Rancher中，应用级别的存储卷的命名规则为使用应用名称为前缀来表明该卷为此应用独有，且会以随机生成的一组数字结尾以确保没有重名。在引用该存储卷时，你依然可以使用原来的卷名称。比如，如果你在应用 stackA中创建了一个名为foo 的卷， 你的主机上显示的卷名称将为`stackA_foo_<randomNumber>`，但在你的服务中，你依然可以使用foo。

####环境级别
环境级别的存储卷，该环境中的所有服务如果 引用了相同的卷将共享同一个存储卷。不同应用中的不同服务也可以共享同一个存储卷。目前，通过UI只可以创建环境级别的卷。

###在UI中使用存储驱动
在你的存储服务启动后且状态为active，使用共享存储卷的服务就可以被创建了。在创建服务时，在卷选项卡中，输入卷以及卷驱动

卷 语法和Docker语法相同，`<volume_name>:</path/in/container>`。Docker卷默认挂载为读写模式，但是你可以通过在卷的末尾添加:ro将其挂载为只读模式。

卷驱动和存储驱动的名字一致，为存储驱动的应用名。

如果 `<volume_name>`在存储驱动中已经存在，在存储卷作用域范围内，将使用相同的存储卷。

####创建新卷
一个卷可以被分为两部分创建：

1. 创建服务时，如果 卷选项卡中的卷在存储驱动中还不存在，环境级别的存储卷将被创建。如果卷已经存储，将不会再创建新卷。
> 注意：该设定并不适用于Rancher EBS，使用Rancher EBS时，必须首先定义一个卷。

2. 在基础架构 -> 存储界面中，选择添加卷。输入卷名称以及驱动信息如果你需要的话。该卷在被一个服务使用之前将一直保持 inactive 状态。

###在RANCHER COMPOSE中使用存储驱动
在基础设施应用中的存储服务启动后，你可以开始创建卷了。在下面的例子中，我们将使用Rancher NFS 存储服务。
在Docker Compose文件中volumes下可以定义卷。在同一个Docker Compose中每个卷可以和多个服务关联。此功能只在Compose v2格式下生效。

```
version: '2'
services:
  foo:
    image: busybox
    stdin_open: true
    volumes:
    - bar:/var/lib/storage
volumes:
  bar:
    driver: rancher-nfs
```

####应用级别
默认情况下，所有的卷将为应用级别。在同一个Compose文件中所有引用同一个卷的服务或应用将共享同一个卷。

如果再同一个Compose文件中创建了一个新应用，一个新卷也会被创建。当应用被删除时，卷也会被删除。
在上面的例子上，卷bar即为应用级别。

####环境级别
如果需要多个应用共享卷，你需要使用一个环境级别的卷。在这个例子里，必须先创建好卷，之后才可以启动使用这个卷对服务或应用。为了使用环境级别的卷，你需要添加external选项到这个卷里。

```
version: '2'
services:
  foo:
    image: busybox
    stdin_open: true
    volumes:
    - bar:/var/lib/storage
volumes:
  bar:
    driver: rancher-nfs
    external: true
```

如果在当前环境中找不到一个叫bar的环境级别的卷，那么将会有报错提示。环境级别的卷只能通过UI进行删除。

##Rancher NFS
Rancher支持将NFS卷作为容器的一个存储选项

使用NFS之前的准备工作
在部署Rancher NFS驱动之前，你需要先准备一个NFS服务器。例如，你可以使用如下命令在Ubuntu 16.04上安装NFS服务器。

```
sudo apt-get update
sudo apt-get install nfs-kernel-server
```

在这个服务器上，你需要设置一个基础目录。首选，你需要创建一个共享目录。

```
sudo mkdir /nfs
sudo chown nobody:nogroup /nfs
```

修改exports文件(/etc/exports).

```
/nfs    *(rw,sync,no_subtree_check,no_root_squash)
```

在全部修改完成后，你需要重新启动NFS内核服务器。

```
sudo systemctl restart nfs-kernel-server
```

###在AMAZON EFS上使用RANCHER NFS驱动
Rancher的NFS驱动可以连接Amazon的EFS。当我们在Amazon EFS上使用Rancher NFS驱动时，环境内全部的主机都需要是EC2主机，并且这些主机要部署在与EFS所在区域相同的同一个可用区内。

###配置RANCHER NFS
当设置一个环境模版的时候，你可以选择启用Rancher NFS应用，这样以后用这个模版创建的环境都会包括Rancher的NFS服务。

或者，如果你已经设置好了一个环境，你可以在应用商店中找到并部署Rancher NFS服务。

> 注意：
某些存储服务可能与容器编排引擎不兼容(例如 Kubernetes)。环境模版会根据你选择的编排引擎显示其兼容的存储服务。但是在应用商店中可以看到全部的应用，不会按照编排引擎进行过滤。

为了部署Rancher NFS，你需要指定如下配置：

- NFS Server: NFS服务器的IP地址或者主机名称
- Export Base Directory: NFS服务器输出的共享目录
- NFS Version: 你所用的NFS版本，当前使用的是版本4
- Mount Options: 用逗号分隔的默认挂载选项， 例如: ‘proto=udp’. 不要配置nfsvers选项，这个选项会被忽略。
- On Remove: 当移除Rancher NFS卷的时候，底层数据是否应该被保留或者清理。选项有purge和retain，默认值为purge。从Rancher 1.6.6开始支持。

###RANCHER NFS驱动选项
当通过Rancher NFS驱动创建卷时，你可以通过一些选项来自定义自己的卷。这些选项是一些键值对，可以通过UI的驱动选项添加，也可以通过compose文件的driver_opts属性来添加。

####驱动选项
- Host - (host): NFS主机
- Export - (export): 当一个卷配置了host和export，将不会创建子文件夹，export的根目录将会被挂载。
- Export Base - (exportBase): 默认情况下，卷可以配置host和export base，这样会在NFS服务器上创建一个名字唯一的子文件夹。
- Mount Options - (mntOptions): 用逗号分隔的默认挂载选项。
- On Remove - (onRemove): 当移除Rancher NFS卷的时候，底层数据是否应该被保留或者清理。选项有purge和retain，默认值为purge。从Rancher 1.6.6开始支持。

###在UI中使用RANCHER NFS
####创建卷
当Rancher NFS在Rancher中部署成功后，你还需要在基础架构 -> 存储里创建NFS卷，之后才可以在服务中使用NFS卷。

1. 点击添加卷。
2. 输入在服务中使用的卷的名称。
3. 可选: 添加额外的驱动选项。

####在服务中使用卷
一旦卷在UI中被创建成功，你可以在服务中使用这个共享存储了。当创建一个服务时，在卷页签，可以输入卷和卷驱动。

volume的语法格式与Docker相同，`<volume_name>:</path/in/container>`。Docker的卷默认是以读写模式进行挂载的，但是你可以通过在卷结尾处添加:ro使其以只读的模式进行挂载。

卷驱动和存储驱动的名字一致，为存储驱动的应用名。默认情况下，Rancher NFS 存储驱动名称为rancher-nfs。

###在COMPOSE文件中使用RANCHER NFS
在基础设施应用中的Rancher NFS启动后，你可以开始在Compose文件中创建卷了。

在Docker Compose文件中volumes下可以定义卷。在同一个Docker Compose中每个卷可以和多个服务关联。

> 注意：
此功能只在Compose v2格式下生效。

####NFS卷示例
在这里例子中，我们将创建一个NFS卷同时创建使用这个卷的服务。所有该应用中的服务将共享同一个卷。

```
version: '2'
services:
  foo:
    image: alpine
    stdin_open: true
    volumes:
    - bar:/data
volumes:
  bar:
    driver: rancher-nfs
```

####使用HOST，EXPORTBASE和EXPORT的示例
下面的例子展示了如何在某个服务中，覆盖host和exportBase。

```
version: '2'
services:
  foo:
    image: alpine
    stdin_open: true
    volumes:
    - bar:/data
volumes:
  bar:
    driver: rancher-nfs
    driver_opts:
      host: 192.168.0.1
      exportBase: /thisisanothershare
```

你也可以给每个卷使用不同的exportBase，请看下面的例子。

```
version: '2'
services:
  foo:
    image: alpine
    stdin_open: true
    volumes:
    - bar:/bardata
    - baz:/bazdata
volumes:
  bar:
    driver: rancher-nfs
    driver_opts:
      host: 192.168.0.1
      exportBase: /thisisanothershare
  baz:
    driver: rancher-nfs
    driver_opts:
      host: 192.168.0.1
      exportBase: /evenanothershare
```

###RANCHER NFS使用AWS EFS
在AWS上创建EFS文件系统之后，你可以部署Rancher NFS驱动来使用这个EFS文件系统。因为亚马逊EFS只在内部可达，所以只有与EFS在同一个可用区内的EC2主机可以访问EFS。因此，在创建存储驱动之前，你需要先添加EC2主机到Rancher环境中。

你可以使用下面的选项来部署Rancher NFS:

- NFS Server: xxxxxxx.efs.us-west-2.amazonaws.com
- Export Base Directory: /
- NFS Version: nfsvers=4

###在移除卷时保留数据
驱动选项onRemove的默认值为purge。这意味着，当从Rancher中删除这个卷的时候，底层的数据也会被删除。如果你想要保留底层数据，你可以将这个选项设置为retain。你也可以给每个卷设置不同的onRemove值。如果nfs-driver选项onRemove被设置为retain，但是你想要在某个卷在Rancher中被删除时清理掉这个卷的底层数据，你可以通过docker-compose.yml在这个卷的driver_opts下面设置onRemove: purge。示例入下。

```
services:
  foo:
    image: alpine
    stdin_open: true
    volumes:
    - bar:/data
volumes:
  bar:
    driver: rancher-nfs
    driver_opts:
      onRemove: purge
```

如果nfs-driver选项onRemove被设置为purge，你可以在卷的driver_opts里设置onRemove: retain来保留数据，这样当这个卷在Rancher中被移除时，数据将会被保留下来。

```
services:
  foo:
    image: alpine
    stdin_open: true
    volumes:
    - bar:/data
volumes:
  bar:
    driver: rancher-nfs
    driver_opts:
      onRemove: retain
```

> 注意：
创建一个外部卷的时候，如果卷的名称和之前被删除的卷的名称相同，并且这个被删除的卷的数据被保留着，这时使用这个卷的容器可以访问被先前保留的数据。


##Rancher EBS
Rancher提供对AWS EBS卷的支持，用户可以选择为容器选择AWS EBS存储。

###使用EBS的限制
一个AWS EBS卷只可以挂载到一个AWS EC2实例中。因此，所有使用同一个AWS EBS卷的所有容器将会被调度到同一台主机上。

###配置RANCHER EBS
当配置一个环境模板时，你可以选择启用Rancher EBS。这样从该环境模板创建的环境都会自动启动该存储驱动。

又或者，你已经创建了一个环境，你可以选择从应用商店中直接启动Rancher EBS。

> 注意：
某些存储服务可能无法和一些容器或编排调度系统（例如，kubernetes）所兼容。环境模板可以根据当前的编排调度系统限定可以使用的存储服务，而应用商店中则会显示全部的存储服务。

要启动Rancher EBS，你需要一个AWS Access Key以及Secret Key 以确保你有权限创建AWS EBS卷。同时，不同的驱动选项可能还需要其他额外的权限。

###RANCHER EBS 驱动选项
当创建AWS EBS卷时，有一些其他的选项可以用于自定义卷。这些选项是一些键值对，可以通过UI的驱动选项添加，也可以通过compose文件的driver_opts属性来添加。

####必填驱动选项
- 大小 - (size): EBS卷大小

####可选驱动选项
- 卷类型 - (volumeType): 卷类型
- IOPS - (iops): IOPS 选项
- 指定的可用区 (ec2_az): 在指定的可用区中创建容器以及EBS卷。(比如. us-west-1a)

对于以下选项，你必须指定和ID绑定的可用区(ec2_az)

- Encrypted (encrypted): 卷是否需要被加密。注：如果需要启动此选项，则需要提供AWS KMS ID。
- AWS KMS ID (kmsKeyId): 用于创建加密卷的AWS Key Management Service customer master key (CMK) 的完整资源名称-ARN（Amazon Resource Name）
- Snapshot ID (snapshotID): 用于创建卷的快照。
- Volume ID (volumeID): 已创建的卷ID。

###在界面中使用RANCHER EBS
####创建卷
当 Rancher EBS在Rancher中启动后，需要先从 基础架构 -> 存储中创建EBS卷，然后才可以在服务中使用EBS卷。

1. 点击添加卷
2. 填写卷名称
3. 必填：填写 size选项
4. 可选：添加其他额外的驱动选项。注：如果要使用加密，快照ID或者卷ID，你需要指定对应的可用区。

####在服务中使用卷
一旦卷在UI中被创建，服务就可以使用该共享存储。创建一个服务时，在 卷选项卡中，填写卷以及卷驱动信息。
卷 语法和Docker语法相同，`<volume_name>:</path/in/container>`。Docker卷默认挂载为读写模式，但是你可以通过在卷的末尾添加:ro将其挂载为只读模式。
卷驱动和存储驱动的名字一致，为存储驱动的应用名。默认情况下，Rancher EBS 存储驱动名称为rancher-ebs。

###在COMPOSE文件中使用RANCHER EBS
在基础设施应用中的Rancher EBS启动后，你可以开始在Compose文件中创建卷了。
在Docker Compose文件中volumes下可以定义卷。在同一个Docker Compose中每个卷可以和多个服务关联。

> 注意：
此功能只在Compose v2格式下生效。

####举例：应用级别存储卷，指定SIZE、卷类型以及IOPS
在这里例子中，我们将创建一个使用应用级别的存储卷的服务。所有该应用中的服务将共享同一个卷。

```
version: '2'
services:
  foo1:
    image: busybox
    stdin_open: true
    volumes:
    - bar:/var/lib/storage
  foo2:
    image: busybox
    volumes:
    - bar:/var/lib/storage

volumes:
  bar:
    driver: rancher-ebs
    driver_opts:
      size: 10
      volumeType: gp2
      iops: 1000
```

####举例：指定可用区的应用级别的存储卷
在这里例子中，我们将创建一个使用应用级别的存储卷的服务。所有该应用中的服务将共享同一个卷。
我们将指定卷的可用区，使用该AWS EBS卷的所有容器将会被调度到同一台主机上。

```
version: '2'
services:
  foo:
    image: busybox
    stdin_open: true
    volumes:
    - bar:/var/lib/storage

volumes:
  bar:
    driver: rancher-ebs
    driver_opts:
      size: 10
      ec2_az: us-west-2a
```

####举例：应用级别加密卷
在这里例子中，我们将创建一个使用应用级别的存储卷的服务。所有该应用中的服务将共享同一个卷。
为了加密该卷，你需要在驱动选项中启用加密并指定加密密钥的ID以及该密钥所在的可用区。
使用该AWS EBS卷的所有容器将会被调度到同一台主机上。

```
version: '2'
services:
  foo:
    image: busybox
    stdin_open: true
    volumes:
    - bar:/var/lib/storage

volumes:
  bar:
    driver: rancher-ebs
    driver_opts:
      size: 10
      encrypted: true
      kmsKeyId: <KMS_KEY_ID>
      # Specifying the availability zone is required when using encryption and kmsKeyId
      ec2_az: <AVAILABILITY_ZONE_WHERE_THE_KMS_KEY_IS>
```

####举例：基于快照的应用级别的存储卷
在这里例子中，我们将创建一个使用应用级别的存储卷的服务。所有该应用中的服务将共享同一个卷。
该卷将基于一个已有的AWS快照被创建出来。你需要指定快照ID以及该快照所在的可用区。
使用该AWS EBS卷的所有容器将会被调度到同一台主机上。

```
version: '2'
services:
  foo:
    image: busybox
    stdin_open: true
    volumes:
    - bar:/var/lib/storage

volumes:
  bar:
    driver: rancher-ebs
    driver_opts:
      size: 10
      snapshotID: <SNAPSHOT_ID>
      # Specifying the availability zone is required when using snapshotID
      ec2_az: <AVAILABILITY_ZONE_WHERE_THE_SNAPSHOT_IS>
```

###举例：基于已有EBS卷的的应用级别的存储卷
在这里例子中，我们将创建一个使用应用级别的存储卷的服务。所有该应用中的服务将共享同一个卷。
你需要指定卷ID以及改卷所在的可用区。
使用该AWS EBS卷的所有容器将会被调度到同一台主机上。

```
version: '2'
services:
  foo:
    image: busybox
    stdin_open: true
    volumes:
    - bar:/var/lib/storage

volumes:
  bar:
    driver: rancher-ebs
    driver_opts:
      size: 10
      volumeID: <VOLUME_ID>
      # Specifying the availability zone is required when using volumeID
      ec2_az: <AVAILABILITY_ZONE_WHERE_THE_VOLUME_IS>
```