# Python爬虫利器六之PyQuery的用法

## 前言

你是否觉得 XPath 的用法多少有点晦涩难记呢？

你是否觉得 BeautifulSoup 的语法多少有些悭吝难懂呢？

你是否甚至还在苦苦研究正则表达式却因为少些了一个点而抓狂呢？

你是否已经有了一些前端基础了解选择器却与另外一些奇怪的选择器语法混淆了呢？

嗯，那么，前端大大们的福音来了，PyQuery 来了，乍听名字，你一定联想到了 jQuery，如果你对 jQuery 熟悉，那么 PyQuery 来解析文档就是不二之选！包括我在内！

PyQuery 是 Python 仿照 jQuery 的严格实现。语法与 jQuery 几乎完全相同，所以不用再去费心去记一些奇怪的方法了。

天下竟然有这等好事？我都等不及了！

## 安装

有这等神器还不赶紧安装了！来！

```
pip install pyquery
```

还是原来的配方，还是熟悉的味道。

## 参考来源

本文内容参考[官方文档](https://pythonhosted.org/pyquery/)，更多内容，大家可以去官方文档学习，毕竟那里才是最原汁原味的。

目前版本 1.2.4 (2016/3/24)


## 简介

> pyquery allows you to make jquery queries on xml documents. The API is as much as possible the similar to jquery. pyquery uses lxml for fast xml and html manipulation.

> This is not (or at least not yet) a library to produce or interact with javascript code. I just liked the jquery API and I missed it in python so I told myself “Hey let’s make jquery in python”. This is the result.

> It can be used for many purposes, one idea that I might try in the future is to use it for templating with pure http templates that you modify using pyquery. I can also be used for web scrapping or for theming applications with Deliverance.

pyquery 可让你用 jQuery 的语法来对 xml 进行操作。这I和 jQuery 十分类似。如果利用 lxml，pyquery 对 xml 和 html 的处理将更快。

这个库不是（至少还不是）一个可以和 JavaScript交互的代码库，它只是非常像 jQuery API 而已。

## 初始化

在这里介绍四种初始化方式。

（1）直接字符串

```
from pyquery import PyQuery as pq
doc = pq("<html></html>")
```

pq 参数可以直接传入 HTML 代码，doc 现在就相当于 jQuery 里面的 $ 符号了。

（2）lxml.etree

```
from lxml import etree
doc = pq(etree.fromstring("<html></html>"))
```

可以首先用 lxml 的 etree 处理一下代码，这样如果你的 HTML 代码出现一些不完整或者疏漏，都会自动转化为完整清晰结构的 HTML代码。

（3）直接传URL

```
from pyquery import PyQuery as pq
doc = pq('http://www.baidu.com')
```

这里就像直接请求了一个网页一样，类似用 urllib2 来直接请求这个链接，得到 HTML 代码。

（4）传文件

```
from pyquery import PyQuery as pq
doc = pq(filename='hello.html')
```

可以直接传某个路径的文件名。

## 快速体验

现在我们以本地文件为例，传入一个名字为 hello.html 的文件，文件内容为

```
<div>
    <ul>
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
```

编写如下程序

```
from pyquery import PyQuery as pq
doc = pq(filename='hello.html')
print doc.html()
print type(doc)
li = doc('li')
print type(li)
print li.text()
```

运行结果

```
    <ul>
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 
<class 'pyquery.pyquery.PyQuery'>
<class 'pyquery.pyquery.PyQuery'>
first item second item third item fourth item fifth item
```

看，回忆一下 jQuery 的语法，是不是运行结果都是一样的呢？

在这里我们注意到了一点，PyQuery 初始化之后，返回类型是 PyQuery，利用了选择器筛选一次之后，返回结果的类型依然还是 PyQuery，这简直和 jQuery 如出一辙，不能更赞！然而想一下 BeautifulSoup 和 XPath 返回的是什么？列表！一种不能再进行二次筛选（在这里指依然利用 BeautifulSoup 或者 XPath 语法）的对象！

然而比比 PyQuery，哦我简直太爱它了！

## 属性操作

你可以完全按照 jQuery 的语法来进行 PyQuery 的操作。

```
from pyquery import PyQuery as pq

p = pq('<p id="hello" class="hello"></p>')('p')
print p.attr("id")
print p.attr("id", "plop")
print p.attr("id", "hello")
```

运行结果

```
hello
<p id="plop" class="hello"/>
<p id="hello" class="hello"/>
```

再来一发

```
from pyquery import PyQuery as pq

p = pq('<p id="hello" class="hello"></p>')('p')
print p.addClass('beauty')
print p.removeClass('hello')
print p.css('font-size', '16px')
print p.css({'background-color': 'yellow'})
```

运行结果

```
<p id="hello" class="hello beauty"/>
<p id="hello" class="beauty"/>
<p id="hello" class="beauty" style="font-size: 16px"/>
<p id="hello" class="beauty" style="font-size: 16px; background-color: yellow"/>
```

依旧是那么优雅与自信！

在这里我们发现了，这是一连串的操作，而 p 是一直在原来的结果上变化的。

因此执行上述操作之后，p 本身也发生了变化。

## DOM操作

同样的原汁原味的 jQuery 语法

```
from pyquery import PyQuery as pq

p = pq('<p id="hello" class="hello"></p>')('p')
print p.append(' check out <a href="http://reddit.com/r/python"><span>reddit</span></a>')
print p.prepend('Oh yes!')
d = pq('<div class="wrap"><div id="test"><a href="http://cuiqingcai.com">Germy</a></div></div>')
p.prependTo(d('#test'))
print p
print d
d.empty()
print d
```

运行结果

```
<p id="hello" class="hello"> check out <a href="http://reddit.com/r/python"><span>reddit</span></a></p>
<p id="hello" class="hello">Oh yes! check out <a href="http://reddit.com/r/python"><span>reddit</span></a></p>
<p id="hello" class="hello">Oh yes! check out <a href="http://reddit.com/r/python"><span>reddit</span></a></p>
<div class="wrap"><div id="test"><p id="hello" class="hello">Oh yes! check out <a href="http://reddit.com/r/python"><span>reddit</span></a></p><a href="http://cuiqingcai.com">Germy</a></div></div>
<div class="wrap"/>
```

这不需要多解释了吧。

DOM 操作也是与 jQuery 如出一辙。

## 遍历

遍历用到 items 方法返回对象列表，或者用 lambda

```
from pyquery import PyQuery as pq
doc = pq(filename='hello.html')
lis = doc('li')
for li in lis.items():
    print li.html()

print lis.each(lambda e: e)
```

运行结果

```
first item
<a href="link2.html">second item</a>
<a href="link3.html"><span class="bold">third item</span></a>
<a href="link4.html">fourth item</a>
<a href="link5.html">fifth item</a>
<li class="item-0">first item</li>
 <li class="item-1"><a href="link2.html">second item</a></li>
 <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
 <li class="item-1 active"><a href="link4.html">fourth item</a></li>
 <li class="item-0"><a href="link5.html">fifth item</a></li>
```

不过最常用的还是 items 方法

## 网页请求

PyQuery 本身还有网页请求功能，而且会把请求下来的网页代码转为 PyQuery 对象。

```
from pyquery import PyQuery as pq
print pq('http://cuiqingcai.com/', headers={'user-agent': 'pyquery'})
print pq('http://httpbin.org/post', {'foo': 'bar'}, method='post', verify=True)
```

感受一下，GET，POST，样样通。

## Ajax

PyQuery 同样支持 Ajax 操作，带有 get 和 post 方法，不过不常用，一般我们不会用 PyQuery 来做网络请求，仅仅是用来解析。

[PyQueryAjax](https://pythonhosted.org/pyquery/ajax.html)

## API

最后少不了的，[API](https://pythonhosted.org/pyquery/api.html)大放送。


原汁原味最全的API，都在里面了！如果你对 jQuery 语法不熟，强烈建议先学习下 jQuery，再回来看 PyQuery，你会感到异常亲切！

## 结语

用完了 PyQuery，我已经深深爱上了他！

你呢？