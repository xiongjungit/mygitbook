#3-2 Python代码运行助手


Python代码运行助手可以让你在线输入Python代码，然后通过本机运行的一个Python脚本来执行代码。原理如下：

- 在网页输入代码：
![code-input](../image/chapter3/3-2-1.jpg)

- 点击Run按钮，代码被发送到本机正在运行的Python代码运行助手；

- Python代码运行助手将代码保存为临时文件，然后调用Python解释器执行代码；

- 网页显示代码执行结果：

![code-result](../image/chapter3/3-2-2.jpg)

##下载

[本地learning.py](../code/chapter3/3-2-learning.py)

点击右键，目标另存为：[learning.py](https://raw.githubusercontent.com/michaelliao/learn-python3/master/teach/learning.py)

备用下载地址：[learning.py](http://pan.baidu.com/s/1sjNYY8P)

##运行

在存放learning.py的目录下运行命令：

C:\Users\michael\Downloads> python learning.py
如果看到Ready for Python code on port 39093...表示运行成功，不要关闭命令行窗口，最小化放到后台运行即可：

![run-learning.py](../image/chapter3/3-2-3.jpg)

##试试效果

需要支持HTML5的浏览器：

- IE >= 9
- Firefox
- Chrome
- Sarafi
# 测试代码:

	print('Hello, world')