##主机驱动
[Docker-machine](https://docs.docker.com/machine/)驱动可被添加到Rancher中，以便这些驱动可以将主机添加到Rancher中。只有管理员可以设置哪些主机驱动可见，这个在系统管理 -> 主机驱动。

只有启用的主机驱动才能在基础架构 -> 添加主机的页面上显示出来。默认情况下，Rancher提供了许多主机驱动，但是只有一些是启用状态。

####添加主机驱动
你可以通过点击添加主机驱动轻松添加自己的主机驱动。

1. 提供下载URL。这个地址是64位Linux驱动的二进制文件的地址。
2. (可选) 为驱动提供自定义添加主机界面的自定义UI的URL。参考[ui-driver-skel repository](https://github.com/rancher/ui-driver-skel)以了解更多信息。
3. (可选) 提供一个校验和以检验下载的驱动是否匹配期望的校验和。
4. 完成之后，点击创建。

点击创建后，Rancher就会添加这个额外的驱动，并将其显示在添加主机页面的驱动选项里。