# Python爬虫进阶二之PySpider框架安装配置

## 关于

首先，在此附上[PySpider项目地址](https://github.com/binux/pyspider)，以及[官方文档](http://docs.pyspider.org/en/latest/)


## 安装

### 1. pip

首先确保你已经安装了pip，若没有安装，请参照[pip安装](http://pip-cn.readthedocs.org/en/latest/installing.html)

### 2. phantomjs

PhantomJS 是一个基于 WebKit 的服务器端 JavaScript API。它全面支持web而不需浏览器支持，其快速、原生支持各种Web标准：DOM 处理、CSS 选择器、JSON、Canvas 和 SVG。 PhantomJS 可以用于页面自动化、网络监测、网页截屏以及无界面测试等。[安装](http://phantomjs.org/download.html)

以上附有官方安装方式，如果你是 Ubuntu 或 Mac OS X用户，可以直接用命令来安装

Ubuntu:

```
sudo apt-get install phantomjs
```

Mac OS X:

```
brew install phantomjs
```

### 3. pyspider

直接利用 pip 安装即可

```
pip install pyspider
```

如果你是 Ubuntu 用户，请提前安装好以下支持类库

```
sudo apt-get install python python-dev python-distribute python-pip libcurl4-openssl-dev libxml2-dev libxslt1-dev python-lxml
```

测试

如果安装过程没有提示任何错误，那就证明一些OK。

命令行输入

```
pyspider all
```

然后浏览器访问 http://localhost:5000

观察一下效果，如果可以正常出现 PySpider 的页面，那证明一切OK

在此附图一张，这是我写了几个爬虫之后的界面。

![](http://qiniu.cuiqingcai.com/wp-content/uploads/2016/02/2016-02-11-20.55.36-1024x355.png)

好，接下来我会进一步介绍这个框架的使用。

## 常见错误

我曾遇到过的一个错误：

[PySpider HTTP 599: SSL certificate problem错误的解决方法](http://cuiqingcai.com/2703.html) ，后来在作者那发了issue得到了答案，其他的暂时没什么问题。

不过发现有的小伙伴提了各种各样的问题啊，不过我确实都没遇到过，我再Win10，Linux Ubuntu，Linux CentOS，Mac OS X都成功运行。不过确实有些奇怪的问题，跑着跑着崩了，一点就崩了我也就比较纳闷了。

如果大家有问题，可以看看作者项目里面有没有类似的issue，另外也推荐大家直接到作者的GitHub上发issue。

毕竟，这个框架不是我写的。

在此附上[PySpider Issue地址](https://github.com/binux/pyspider/issues)

