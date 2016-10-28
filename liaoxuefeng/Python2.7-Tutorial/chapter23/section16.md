#23-16 Day 16 - 编写移动App


网站部署上线后，还缺点啥呢？

在移动互联网浪潮席卷而来的今天，一个网站没有上线移动App，出门根本不好意思跟人打招呼。

所以，awesome-python-webapp必须得有一个移动App版本！

##开发iPhone版本

我们首先来看看如何开发iPhone App。前置条件：一台Mac电脑，安装XCode和最新的iOS SDK。

在使用MVVM编写前端页面时，我们就能感受到，用REST API封装网站后台的功能，不但能清晰地分离前端页面和后台逻辑，现在这个好处更加明显，移动App也可以通过REST API从后端拿到数据。

我们来设计一个简化版的iPhone App，包含两个屏幕：列出最新日志和阅读日志的详细内容：

![awesomepy-iphone-app](../image/chapter23/23-16-1.jpg)

只需要调用API：/api/blogs。

在XCode中完成App编写：

![awesomepy-iphone-app-xcode](../image/chapter23/23-16-2.jpg)

由于我们的教程是Python，关于如何开发iOS，请移步Develop Apps for iOS。

[点击下载iOS App源码](https://github.com/michaelliao/awesome-python-webapp/tree/day-16/ios)。

如何编写Android App？这个当成作业了。