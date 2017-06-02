# Python爬虫利器一之Requests库的用法


## 前言

之前我们用了 urllib 库，这个作为入门的工具还是不错的，对了解一些爬虫的基本理念，掌握爬虫爬取的流程有所帮助。入门之后，我们就需要学习一些更加高级的内容和工具来方便我们的爬取。那么这一节来简单介绍一下 requests 库的基本用法。

注：Python 版本依然基于 2.7

## 官方文档

以下内容大多来自于官方文档，本文进行了一些修改和总结。要了解更多可以参考[官方文档](http://docs.python-requests.org/en/master/)

## 安装

利用 pip 安装

```
$ pip install requests
```

或者利用 easy_install

```
$ easy_install requests
```

通过以上两种方法均可以完成安装。

## 引入

首先我们引入一个小例子来感受一下

```
import requests

r = requests.get('http://cuiqingcai.com')
print type(r)
print r.status_code
print r.encoding
#print r.text
print r.cookies
```

以上代码我们请求了本站点的网址，然后打印出了返回结果的类型，状态码，编码方式，Cookies等内容。

运行结果如下

```
<class 'requests.models.Response'>
200
UTF-8
<RequestsCookieJar[]>
```

怎样，是不是很方便。别急，更方便的在后面呢。

## 基本请求

requests库提供了http所有的基本请求方式。例如

```
r = requests.post("http://httpbin.org/post")
r = requests.put("http://httpbin.org/put")
r = requests.delete("http://httpbin.org/delete")
r = requests.head("http://httpbin.org/get")
r = requests.options("http://httpbin.org/get")
```

嗯，一句话搞定。

## 基本GET请求

最基本的GET请求可以直接用get方法

```
r = requests.get("http://httpbin.org/get")
```

如果想要加参数，可以利用 params 参数

```
import requests

payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.get("http://httpbin.org/get", params=payload)
print r.url
```

运行结果

```
http://httpbin.org/get?key2=value2&key1=value1
```

如果想请求JSON文件，可以利用 json() 方法解析

例如自己写一个JSON文件命名为a.json，内容如下

```
["foo", "bar", {
  "foo": "bar"
}]
```

利用如下程序请求并解析

```
import requests

r = requests.get("a.json")
print r.text
print r.json()
```

运行结果如下，其中一个是直接输出内容，另外一个方法是利用 json() 方法解析，感受下它们的不同

```
["foo", "bar", {
 "foo": "bar"
 }]
 [u'foo', u'bar', {u'foo': u'bar'}]
```

如果想获取来自服务器的原始套接字响应，可以取得 r.raw 。 不过需要在初始请求中设置 stream=True 。

```
r = requests.get('https://github.com/timeline.json', stream=True)
r.raw
<requests.packages.urllib3.response.HTTPResponse object at 0x101194810>
r.raw.read(10)
'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03'
```

这样就获取了网页原始套接字内容。

如果想添加 headers，可以传 headers 参数

```
import requests

payload = {'key1': 'value1', 'key2': 'value2'}
headers = {'content-type': 'application/json'}
r = requests.get("http://httpbin.org/get", params=payload, headers=headers)
print r.url
```

通过headers参数可以增加请求头中的headers信息

## 基本POST请求

对于 POST 请求来说，我们一般需要为它增加一些参数。那么最基本的传参方法可以利用 data 这个参数。

```
import requests

payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.post("http://httpbin.org/post", data=payload)
print r.text
```

运行结果

```
{
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {
    "key1": "value1", 
    "key2": "value2"
  }, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Content-Length": "23", 
    "Content-Type": "application/x-www-form-urlencoded", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.9.1"
  }, 
  "json": null, 
  "url": "http://httpbin.org/post"
}
```

可以看到参数传成功了，然后服务器返回了我们传的数据。

有时候我们需要传送的信息不是表单形式的，需要我们传JSON格式的数据过去，所以我们可以用 json.dumps() 方法把表单数据序列化。

```
import json
import requests

url = 'http://httpbin.org/post'
payload = {'some': 'data'}
r = requests.post(url, data=json.dumps(payload))
print r.text
```

运行结果

```
{
  "args": {}, 
  "data": "{\"some\": \"data\"}", 
  "files": {}, 
  "form": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Content-Length": "16", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.9.1"
  }, 
  "json": {
    "some": "data"
  },  
  "url": "http://httpbin.org/post"
}
```

通过上述方法，我们可以POST JSON格式的数据

如果想要上传文件，那么直接用 file 参数即可

新建一个 a.txt 的文件，内容写上 Hello World!

```
import requests

url = 'http://httpbin.org/post'
files = {'file': open('test.txt', 'rb')}
r = requests.post(url, files=files)
print r.text
```

可以看到运行结果如下

```
{
  "args": {}, 
  "data": "", 
  "files": {
    "file": "Hello World!"
  }, 
  "form": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Content-Length": "156", 
    "Content-Type": "multipart/form-data; boundary=7d8eb5ff99a04c11bb3e862ce78d7000", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.9.1"
  }, 
  "json": null, 
  "url": "http://httpbin.org/post"
}
```

这样我们便成功完成了一个文件的上传。

requests 是支持流式上传的，这允许你发送大的数据流或文件而无需先把它们读入内存。要使用流式上传，仅需为你的请求体提供一个类文件对象即可

```
with open('massive-body') as f:
    requests.post('http://some.url/streamed', data=f)
```

这是一个非常实用方便的功能。

## Cookies

如果一个响应中包含了cookie，那么我们可以利用 cookies 变量来拿到

```
import requests

url = 'http://example.com'
r = requests.get(url)
print r.cookies
print r.cookies['example_cookie_name']
```

以上程序仅是样例，可以用 cookies 变量来得到站点的 cookies

另外可以利用 cookies 变量来向服务器发送 cookies 信息

```
import requests

url = 'http://httpbin.org/cookies'
cookies = dict(cookies_are='working')
r = requests.get(url, cookies=cookies)
print r.text
```

运行结果

```
'{"cookies": {"cookies_are": "working"}}'
```

可以已经成功向服务器发送了 cookies

## 超时配置

可以利用 timeout 变量来配置最大请求时间

```
requests.get('http://github.com', timeout=0.001)
```

注：timeout 仅对连接过程有效，与响应体的下载无关。

也就是说，这个时间只限制请求的时间。即使返回的 response 包含很大内容，下载需要一定时间，然而这并没有什么卵用。

## 会话对象

在以上的请求中，每次请求其实都相当于发起了一个新的请求。也就是相当于我们每个请求都用了不同的浏览器单独打开的效果。也就是它并不是指的一个会话，即使请求的是同一个网址。比如

```
import requests

requests.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = requests.get("http://httpbin.org/cookies")
print(r.text)
```

结果是

```
{
  "cookies": {}
}
```

很明显，这不在一个会话中，无法获取 cookies，那么在一些站点中，我们需要保持一个持久的会话怎么办呢？就像用一个浏览器逛淘宝一样，在不同的选项卡之间跳转，这样其实就是建立了一个长久会话。

解决方案如下

```
import requests

s = requests.Session()
s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get("http://httpbin.org/cookies")
print(r.text)
```

在这里我们请求了两次，一次是设置 cookies，一次是获得 cookies

运行结果

```
{
  "cookies": {
    "sessioncookie": "123456789"
  }
}
```

发现可以成功获取到 cookies 了，这就是建立一个会话到作用。体会一下。

那么既然会话是一个全局的变量，那么我们肯定可以用来全局的配置了。

```
import requests

s = requests.Session()
s.headers.update({'x-test': 'true'})
r = s.get('http://httpbin.org/headers', headers={'x-test2': 'true'})
print r.text
```

通过 s.headers.update 方法设置了 headers 的变量。然后我们又在请求中设置了一个 headers，那么会出现什么结果？

很简单，两个变量都传送过去了。

运行结果

```
{
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.9.1", 
    "X-Test": "true", 
    "X-Test2": "true"
  }
}
```

如果get方法传的headers 同样也是 x-test 呢？

```
r = s.get('http://httpbin.org/headers', headers={'x-test': 'true'})
```

嗯，它会覆盖掉全局的配置

```
{
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.9.1", 
    "X-Test": "true"
  }
}
```

那如果不想要全局配置中的一个变量了呢？很简单，设置为 None 即可

```
r = s.get('http://httpbin.org/headers', headers={'x-test': None})
```


运行结果

```
{
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.9.1"
  }
}
```

嗯，以上就是 session 会话的基本用法

## SSL证书验证

现在随处可见 https 开头的网站，Requests可以为HTTPS请求验证SSL证书，就像web浏览器一样。要想检查某个主机的SSL证书，你可以使用 verify 参数

现在 12306 证书不是无效的嘛，来测试一下

```
import requests

r = requests.get('https://kyfw.12306.cn/otn/', verify=True)
print r.text
```

结果

```
requests.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:590)
```

果真如此

来试下 github 的

```
import requests

r = requests.get('https://github.com', verify=True)
print r.text
```

嗯，正常请求，内容我就不输出了。

如果我们想跳过刚才 12306 的证书验证，把 verify 设置为 False 即可

```
import requests

r = requests.get('https://kyfw.12306.cn/otn/', verify=False)
print r.text
```

发现就可以正常请求了。在默认情况下 verify 是 True，所以如果需要的话，需要手动设置下这个变量。

## 代理

如果需要使用代理，你可以通过为任意请求方法提供 proxies 参数来配置单个请求

```
import requests

proxies = {
  "https": "http://41.118.132.69:4433"
}
r = requests.post("http://httpbin.org/post", proxies=proxies)
print r.text
```

也可以通过环境变量 HTTP_PROXY 和 HTTPS_PROXY 来配置代理

```
export HTTP_PROXY="http://10.10.1.10:3128"
export HTTPS_PROXY="http://10.10.1.10:1080"
```

通过以上方式，可以方便地设置代理。

## API

以上讲解了 requests 中最常用的参数，如果需要用到更多，请参考官方文档 [API](http://docs.python-requests.org/en/master/api/)


## 结语

以上总结了一下 requests 的基本用法，如果你对爬虫有了一定的基础，那么肯定可以很快上手，在此就不多赘述了。

练习才是王道，大家尽快投注于实践中吧。