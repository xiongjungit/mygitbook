#9-1 安装Node.js和npm


由于Node.js平台是在后端运行JavaScript代码，所以，必须首先在本机安装Node环境。

##安装Node.js

目前Node.js的最新版本是6.2.x。首先，从[Node.js](https://nodejs.org/)官网下载对应平台的安装程序，网速慢的童鞋请移步[国内镜像](http://pan.baidu.com/s/1kU5OCOB#path=%252Fpub%252Fnodejs)。

在Windows上安装时务必选择全部组件，包括勾选Add to Path。

安装完成后，在Windows环境下，请打开命令提示符，然后输入node -v，如果安装正常，你应该看到v6.2.0这样的输出：

	C:\Users\IEUser>node -v
	v6.2.0
继续在命令提示符输入node，此刻你将进入Node.js的交互环境。在交互环境下，你可以输入任意JavaScript语句，例如100+200，回车后将得到输出结果。

要退出Node.js环境，连按两次Ctrl+C。