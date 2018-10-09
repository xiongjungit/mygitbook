##升级Kubernetes
如果希望升级一个已有的Kubernetes部署为平面隔离部署, 请参考迁移部分的说明。

整个迁移流程由两个阶段组成。

1. 确保你的环境中拥有足够数量具备合适标签的主机。
2. 升级Kubernetes基础设施应用栈。

###主机与标签
确认环境中拥有足够数量具备各平面标签的主机。你可以添加新的主机或使用已有主机。

1. 计算平面主机: 对于全部已存在的运行有kubelet和proxy容器的主机, 添加标签compute=true。 这些是当你运行kubectl get node命令时显示的已经注册到Kubernetes的节点。此步骤非常重要 ，如果主机没有这个标签，运行在主机上的Kubernetes pods将变为孤儿pods。如果环境中有运行kubelet和proxy容器的主机，你可以按照从计算平面移除主机中的步骤操作将其移除。你也可以增加更多的主机并按照为主机设置标签中的步骤为主机设置compute=true标签。
2. 数据平面主机: 拥有至少3台具有1 CPU, >=1.5GB RAM, >=20GB DISK的主机。如果你有一个已经运行的Kubernetes环境中包含etcd服务运行，请确保运行etcd服务的主机具有etcd=true标签。
3. 编排平面主机: 添加至少2台具有大于等于1 CPU且大于等于2GB RAM的主机。添加主机时，按照为主机设置标签中的步骤为主机设置orchestration=true标签。 你也可以仅使用一台主机进行部署，但这样将牺牲高可用性。当仅有的一台主机发生故障时，一些K8s功能例如API、在pods发生故障时进行重新调度等，将不会正常工作，直到一台新的主机被加入。

###升级KUBERNETES
1. 在Kubernetes -> 基础设施应用下, 找到Kubernetes基础设施应用栈。点击有可用更新或已经是最新版本按钮。
2. 确认Kubernetes模板版本是你希望使用的版本。
3. 将Plane Isolation设置为required。
4. 选择cloud providers, backups, add-ons等的设置选项。
5. 点击升级以启动新版本的Kubernetes基础设施应用。
6. 在Kubernetes应用栈下的所有服务完成升级并显示为已升级状态后, 点击已升级: 完成升级按钮。

####将运行PODS的主机从计算平面删除
警告: 如果你计划从计算平面删除任何主机，不属于任何replication controller或类似对象的裸pod将 不会 被重新调度。这是正常行为。

计算平面的主机运行kubelet和proxy容器。

1. 如果主机具有compute=true标签, 从主机上移除此标签。此操作将阻止kubelet和proxy容器被删除后重新被调度到这些主机。
2. 通过shell或者远程客户端使用kubectl工具, 运行kubectl delete node <HOST>。 你可以从Rancher用户界面或通过kubectl工具运行kubectl get node获取主机名 (也就是：<HOST>)。在进行下一步可选操作之前，请等待所有pods被删除。
3. 可选: 如果你希望从主机中删除kubelet和proxy容器，你可以对kubelet和proxy服务进行一次升级，升级过程中无需修改任何设置。 在进行升级操作之前，确保主机上的所有pods都已经被删除。