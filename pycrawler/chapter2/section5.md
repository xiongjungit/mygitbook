# Python爬虫实战五之模拟登录淘宝并获取所有订单

经过多次尝试，模拟登录淘宝终于成功了，实在是不容易，淘宝的登录加密和验证太复杂了，煞费苦心，在此写出来和大家一起分享，希望大家支持。

## 温馨提示

更新时间，2016-02-01，现在淘宝换成了滑块验证了，比较难解决这个问题，以下的代码没法用了，仅作学习参考研究之用吧。

## 本篇内容

1. python模拟登录淘宝网页

2. 获取登录用户的所有订单详情

3. 学会应对出现验证码的情况

4. 体会一下复杂的模拟登录机制

## 探索部分成果

1. 淘宝的密码用了AES加密算法，最终将密码转化为256位，在POST时，传输的是256位长度的密码。

2. 淘宝在登录时必须要输入验证码，在经过几次尝试失败后最终获取了验证码图片让用户手动输入来验证。

3. 淘宝另外有复杂且每天在变的 ua 加密算法，在程序中我们需要提前获取某一 ua 码才可进行模拟登录。

4. 在获取最后的登录 st 码时，历经了多次请求和正则表达式提取，且 st 码只可使用一次。

## 整体思路梳理

1. 手动到浏览器获取 ua 码以及 加密后的密码，只获取一次即可，一劳永逸。

2. 向登录界面发送登录请求，POST 一系列参数，包括 ua 码以及密码等等，获得响应，提取验证码图像。

3. 用户输入手动验证码，重新加入验证码数据再次用 POST 方式发出请求，获得响应，提取 J_Htoken。

4. 利用 J_Htoken 向 alipay 发出请求，获得响应，提取 st 码。

5. 利用 st 码和用户名，重新发出登录请求，获得响应，提取重定向网址，存储 cookie。

6. 利用 cookie 向其他个人页面如订单页面发出请求，获得响应，提取订单详情。

是不是没看懂？没事，下面我将一点点说明自己模拟登录的过程，希望大家可以理解。

## 前期准备

由于淘宝的 ua 算法和 aes 密码加密算法太复杂了，ua 算法在淘宝每天都是在变化的，不过，这个内容你获取之后一直用即可，经过测试之后没有问题，一劳永逸。

那么 ua 和 aes 密码怎样获取呢？

我们就从浏览器里面直接获取吧，打开浏览器，找到淘宝的登录界面，按 F12 或者浏览器右键审查元素。

在这里我用的是火狐浏览器，首先记得在浏览器中设置一下显示持续日志，要不然页面跳转了你就看不到之前抓取的信息了。在这里截图如下：

![](http://qiniu.cuiqingcai.com/wp-content/uploads/2015/02/20150225013600-1024x560.jpg)


好，那么接下来我们就从浏览器中获取 ua 和 aes 密码

点击网络选项卡，这时都是空的，什么数据也没有截取。这时你就在网页上登录一下试试吧，输入用户名啊，密码啊，有必要时需要输入验证码，点击登录。

![](http://qiniu.cuiqingcai.com/wp-content/uploads/2015/02/QQ%E6%88%AA%E5%9B%BE20150225014124-1024x392.jpg)

等跳转成功后，你就可以看到好多日志记录了，点击图中的那一行 login.taobo.com，然后查看参数，你就会发现表单数据了，其中就包括 ua 还有下面的 password2，把这俩复制下来，我们之后要用到的。这就是我们需要的 ua 还有 aes 加密后的密码。

![](http://qiniu.cuiqingcai.com/wp-content/uploads/2015/02/QQ%E6%88%AA%E5%9B%BE20150225014019-1024x305.jpg)

恩，读到这里，你应该获取到了属于自己的 ua 和 password2 两个内容。

## 输入验证码并获取J_HToken

经过博主本人亲自验证，有时候，在模拟登录时你并不需要输入验证码，它直接返回的结果就是前面所说的下一步用到的 J_Token，而有时候你则会需要输入验证码，等你手动输入验证码之后，重新请求登录一次。

博主是边写程序边更新文章的，现在写完了是否有必要输入验证码的检验以及在浏览器中呈现验证码。

代码如下

```
__author__ = 'CQC'
# -*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
import re
import webbrowser

#模拟登录淘宝类
class Taobao:

    #初始化方法
    def __init__(self):
        #登录的URL
        self.loginURL = "https://login.taobao.com/member/login.jhtml"
        #代理IP地址，防止自己的IP被封禁
        self.proxyURL = 'http://120.193.146.97:843'
        #登录POST数据时发送的头部信息
        self.loginHeaders =  {
            'Host':'login.taobao.com',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Referer' : 'https://login.taobao.com/member/login.jhtml',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection' : 'Keep-Alive'
        }
        #用户名
        self.username = 'cqcre'
        #ua字符串，经过淘宝ua算法计算得出，包含了时间戳,浏览器,屏幕分辨率,随机数,鼠标移动,鼠标点击,其实还有键盘输入记录,鼠标移动的记录、点击的记录等等的信息
        self.ua = '191UW5TcyMNYQwiAiwTR3tCf0J/QnhEcUpkMmQ=|Um5Ockt0TXdPc011TXVKdyE=|U2xMHDJ+H2QJZwBxX39Rb1d5WXcrSixAJ1kjDVsN|VGhXd1llXGNaYFhkWmJaYl1gV2pIdUtyTXRKfkN4Qn1FeEF6R31TBQ==|VWldfS0TMw8xDjYWKhAwHiUdOA9wCDEVaxgkATdcNU8iDFoM|VmNDbUMV|V2NDbUMV|WGRYeCgGZhtmH2VScVI2UT5fORtmD2gCawwuRSJHZAFsCWMOdVYyVTpbPR99HWAFYVMpUDUFORshHiQdJR0jAT0JPQc/BDoFPgooFDZtVBR5Fn9VOwt2EWhCOVQ4WSJPJFkHXhgoSDVIMRgnHyFqQ3xEezceIRkmahRqFDZLIkUvRiEDaA9qQ3xEezcZORc5bzk=|WWdHFy0TMw8vEy0UIQE0ADgYJBohGjoAOw4uEiwXLAw2DThu9a==|WmBAED5+KnIbdRh1GXgFQSZbGFdrUm1UblZqVGxQa1ZiTGxQcEp1I3U=|W2NDEz19KXENZwJjHkY7Ui9OJQsre09zSWlXY1oMLBExHzERLxsuE0UT|XGZGFjh4LHQdcx5zH34DRyBdHlFtVGtSaFBsUmpWbVBkSmpXd05zTnMlcw==|XWdHFzl5LXUJYwZnGkI/VitKIQ8vEzMKNws3YTc=|XmdaZ0d6WmVFeUB8XGJaYEB4TGxWbk5yTndXa0tyT29Ta0t1QGBeZDI='
        #密码，在这里不能输入真实密码，淘宝对此密码进行了加密处理，256位，此处为加密后的密码
        self.password2 = '7511aa68sx629e45de220d29174f1066537a73420ef6dbb5b46f202396703a2d56b0312df8769d886e6ca63d587fdbb99ee73927e8c07d9c88cd02182e1a21edc13fb8e140a4a2a4b5c253bf38484bd0e08199e03eb9bf7b365a5c673c03407d812b91394f0d3c7564042e3f2b11d156aeea37ad6460118914125ab8f8ac466f'
        self.post = post = {
            'ua':self.ua,
            'TPL_checkcode':'',
            'CtrlVersion': '1,0,0,7',
            'TPL_password':'',
            'TPL_redirect_url':'http://i.taobao.com/my_taobao.htm?nekot=udm8087E1424147022443',
            'TPL_username':self.username,
            'loginsite':'0',
            'newlogin':'0',
            'from':'tb',
            'fc':'default',
            'style':'default',
            'css_style':'',
            'tid':'XOR_1_000000000000000000000000000000_625C4720470A0A050976770A',
            'support':'000001',
            'loginType':'4',
            'minititle':'',
            'minipara':'',
            'umto':'NaN',
            'pstrong':'3',
            'llnick':'',
            'sign':'',
            'need_sign':'',
            'isIgnore':'',
            'full_redirect':'',
            'popid':'',
            'callback':'',
            'guf':'',
            'not_duplite_str':'',
            'need_user_id':'',
            'poy':'',
            'gvfdcname':'10',
            'gvfdcre':'',
            'from_encoding ':'',
            'sub':'',
            'TPL_password_2':self.password2,
            'loginASR':'1',
            'loginASRSuc':'1',
            'allp':'',
            'oslanguage':'zh-CN',
            'sr':'1366*768',
            'osVer':'windows|6.1',
            'naviVer':'firefox|35'
        }
        #将POST的数据进行编码转换
        self.postData = urllib.urlencode(self.post)
        #设置代理
        self.proxy = urllib2.ProxyHandler({'http':self.proxyURL})
        #设置cookie
        self.cookie = cookielib.LWPCookieJar()
        #设置cookie处理器
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
        #设置登录时用到的opener，它的open方法相当于urllib2.urlopen
        self.opener = urllib2.build_opener(self.cookieHandler,self.proxy,urllib2.HTTPHandler)


    #得到是否需要输入验证码，这次请求的相应有时会不同，有时需要验证有时不需要
    def needIdenCode(self):
        #第一次登录获取验证码尝试，构建request
        request = urllib2.Request(self.loginURL,self.postData,self.loginHeaders)
        #得到第一次登录尝试的相应
        response = self.opener.open(request)
        #获取其中的内容
        content = response.read().decode('gbk')
        #获取状态吗
        status = response.getcode()
        #状态码为200，获取成功
        if status == 200:
            print u"获取请求成功"
            #\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801这六个字是请输入验证码的utf-8编码
            pattern = re.compile(u'\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801',re.S)
            result = re.search(pattern,content)
            #如果找到该字符，代表需要输入验证码
            if result:
                print u"此次安全验证异常，您需要输入验证码"
                return content
            #否则不需要
            else:
                print u"此次安全验证通过，您这次不需要输入验证码"
                return False
        else:
            print u"获取请求失败"

    #得到验证码图片
    def getIdenCode(self,page):
        #得到验证码的图片
        pattern = re.compile('<img id="J_StandardCode_m.*?data-src="(.*?)"',re.S)
        #匹配的结果
        matchResult = re.search(pattern,page)
        #已经匹配得到内容，并且验证码图片链接不为空
        if matchResult and matchResult.group(1):
            print matchResult.group(1)
            return matchResult.group(1)
        else:
            print u"没有找到验证码内容"
            return False

    #程序运行主干
    def main(self):
        #是否需要验证码，是则得到页面内容，不是则返回False
        needResult = self.needIdenCode()
        if not needResult == False:
            print u"您需要手动输入验证码"
            idenCode = self.getIdenCode(needResult)
            #得到了验证码的链接
            if not idenCode == False:
                print u"验证码获取成功"
                print u"请在浏览器中输入您看到的验证码"
                webbrowser.open_new_tab(idenCode)
            #验证码链接为空，无效验证码
            else:
                print u"验证码获取失败，请重试"
        else:
            print u"不需要输入验证码"



taobao = Taobao()
taobao.main()
```

恩，请把里面的 ua 和 password2 还有用户名换成自己的进行尝试，用我的可能会产生错误的。

运行结果

![](http://qiniu.cuiqingcai.com/wp-content/uploads/2015/02/QQ%E6%88%AA%E5%9B%BE20150225015508.jpg)

然后会蹦出浏览器，显示了验证码的内容，这个需要你来手动输入。

在这里有小伙伴向我反映有这么个错误

![](http://qiniu.cuiqingcai.com/wp-content/uploads/2015/02/QQ%E5%9B%BE%E7%89%8720150227181617.png)

经过查证，竟然是版本问题，博主本人用的是 2.7.7，而小伙伴用的是 2.7.9。后来换成 2.7.7 就好了…，我也是醉了，希望有相同错误的小伙伴，可以尝试换一下版本…

好啦，运行时会弹出浏览器，如图

![](http://qiniu.cuiqingcai.com/wp-content/uploads/2015/02/QQ%E6%88%AA%E5%9B%BE20150225015717.jpg)

那么，我们现在需要手动输入验证码，重新向登录界面发出登录请求，之前的post数据内容加入验证码这一项，重新请求一次，如果请求成功，则会返回下一步我们需要的 J_HToken，如果验证码输入错误，则会返回验证码输入错误的选项。好，下面，我已经写到了获取J_HToken的进度，代码如下，现在运行程序，会蹦出浏览器，然后提示你输入验证码，用户手动输入之后，则会返回一个页面，我们提取出 J_Htoken即可。

注意，到现在为止，你还没有登录成功，只是获取到了J_HToken的值。

目前写到的代码如下

```
__author__ = 'CQC'
# -*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
import re
import webbrowser

#模拟登录淘宝类
class Taobao:

    #初始化方法
    def __init__(self):
        #登录的URL
        self.loginURL = "https://login.taobao.com/member/login.jhtml"
        #代理IP地址，防止自己的IP被封禁
        self.proxyURL = 'http://120.193.146.97:843'
        #登录POST数据时发送的头部信息
        self.loginHeaders =  {
            'Host':'login.taobao.com',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Referer' : 'https://login.taobao.com/member/login.jhtml',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection' : 'Keep-Alive'
        }
        #用户名
        self.username = 'cqcre'
        #ua字符串，经过淘宝ua算法计算得出，包含了时间戳,浏览器,屏幕分辨率,随机数,鼠标移动,鼠标点击,其实还有键盘输入记录,鼠标移动的记录、点击的记录等等的信息
        self.ua = '191UW5TcyMNYQwiAiwTR3tCf0J/QnhEcUpkMmQ=|Um5Ockt0TXdPc011TXVKdyE=|U2xMHDJ+H2QJZwBxX39Rb1d5WXcrSixAJ1kjDVsN|VGhXd1llXGNaYFhkWmJaYl1gV2pIdUtyTXRKfkN4Qn1FeEF6R31TBQ==|VWldfS0TMw8xDjYWKhAwHiUdOA9wCDEVaxgkATdcNU8iDFoM|VmNDbUMV|V2NDbUMV|WGRYeCgGZhtmH2VScVI2UT5fORtmD2gCawwuRSJHZAFsCWMOdVYyVTpbPR99HWAFYVMpUDUFORshHiQdJR0jAT0JPQc/BDoFPgooFDZtVBR5Fn9VOwt2EWhCOVQ4WSJPJFkHXhgoSDVIMRgnHyFqQ3xEezceIRkmahRqFDZLIkUvRiEDaA9qQ3xEezcZORc5bzk=|WWdHFy0TMw8vEy0UIQE0ADgYJBohGjoAOw4uEiwXLAw2DThuOA==|WmBAED5+KnIbdRh1GXgFQSZbGFdrUm1UblZqVGxQa1ZiTGxQcEp1I3U=|W2NDEz19KXENZwJjHkY7Ui9OJQsre09zSWlXY1oMLBExHzERLxsuE0UT|XGZGFjh4LHQdcx5zH34DRyBdHlFtVGtSaFBsUmpWbVBkSmpXd05zTnMlcw==|XWdHFzl5LXUJYwZnGkI/VitKIQ8vEzMKNws3YTc=|XmdaZ0d6WmVFeUB8XGJaYEB4TGxWbk5yTndXa0tyT29Ta0t1QGBeZDI='
        #密码，在这里不能输入真实密码，淘宝对此密码进行了加密处理，256位，此处为加密后的密码
        self.password2 = '7511aa6854629e45de220d29174f1066537a73420ef6dbb5b46f202396703a2d56b0312df8769d886e6ca63d587fdbb99ee73927e8c07d9c88cd02182e1a21edc13fb8e0a4a2a4b5c253bf38484bd0e08199e03eb9bf7b365a5c673c03407d812b91394f0d3c7564042e3f2b11d156aeea37ad6460118914125ab8f8ac466f'
        self.post = post = {
            'ua':self.ua,
            'TPL_checkcode':'',
            'CtrlVersion': '1,0,0,7',
            'TPL_password':'',
            'TPL_redirect_url':'http://i.taobao.com/my_taobao.htm?nekot=udm8087E1424147022443',
            'TPL_username':self.username,
            'loginsite':'0',
            'newlogin':'0',
            'from':'tb',
            'fc':'default',
            'style':'default',
            'css_style':'',
            'tid':'XOR_1_000000000000000000000000000000_625C4720470A0A050976770A',
            'support':'000001',
            'loginType':'4',
            'minititle':'',
            'minipara':'',
            'umto':'NaN',
            'pstrong':'3',
            'llnick':'',
            'sign':'',
            'need_sign':'',
            'isIgnore':'',
            'full_redirect':'',
            'popid':'',
            'callback':'',
            'guf':'',
            'not_duplite_str':'',
            'need_user_id':'',
            'poy':'',
            'gvfdcname':'10',
            'gvfdcre':'',
            'from_encoding ':'',
            'sub':'',
            'TPL_password_2':self.password2,
            'loginASR':'1',
            'loginASRSuc':'1',
            'allp':'',
            'oslanguage':'zh-CN',
            'sr':'1366*768',
            'osVer':'windows|6.1',
            'naviVer':'firefox|35'
        }
        #将POST的数据进行编码转换
        self.postData = urllib.urlencode(self.post)
        #设置代理
        self.proxy = urllib2.ProxyHandler({'http':self.proxyURL})
        #设置cookie
        self.cookie = cookielib.LWPCookieJar()
        #设置cookie处理器
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
        #设置登录时用到的opener，它的open方法相当于urllib2.urlopen
        self.opener = urllib2.build_opener(self.cookieHandler,self.proxy,urllib2.HTTPHandler)


    #得到是否需要输入验证码，这次请求的相应有时会不同，有时需要验证有时不需要
    def needCheckCode(self):
        #第一次登录获取验证码尝试，构建request
        request = urllib2.Request(self.loginURL,self.postData,self.loginHeaders)
        #得到第一次登录尝试的相应
        response = self.opener.open(request)
        #获取其中的内容
        content = response.read().decode('gbk')
        #获取状态吗
        status = response.getcode()
        #状态码为200，获取成功
        if status == 200:
            print u"获取请求成功"
            #\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801这六个字是请输入验证码的utf-8编码
            pattern = re.compile(u'\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801',re.S)
            result = re.search(pattern,content)
            print content
            #如果找到该字符，代表需要输入验证码
            if result:
                print u"此次安全验证异常，您需要输入验证码"
                return content
            #否则不需要
            else:
                #返回结果直接带有J_HToken字样，表明直接验证通过
                tokenPattern = re.compile('id="J_HToken"')
                tokenMatch = re.search(tokenPattern,content)
                if tokenMatch:
                    print u"此次安全验证通过，您这次不需要输入验证码"
                    return False
        else:
            print u"获取请求失败"
            return None

    #得到验证码图片
    def getCheckCode(self,page):
        #得到验证码的图片
        pattern = re.compile('<img id="J_StandardCode_m.*?data-src="(.*?)"',re.S)
        #匹配的结果
        matchResult = re.search(pattern,page)
        #已经匹配得到内容，并且验证码图片链接不为空
        if matchResult and matchResult.group(1):
            print matchResult.group(1)
            return matchResult.group(1)
        else:
            print u"没有找到验证码内容"
            return False


    #输入验证码，重新请求，如果验证成功，则返回J_HToken
    def loginWithCheckCode(self):
        #提示用户输入验证码
        checkcode = raw_input('请输入验证码:')
        #将验证码重新添加到post的数据中
        self.post['TPL_checkcode'] = checkcode
        #对post数据重新进行编码
        self.postData = urllib.urlencode(self.post)
        try:
            #再次构建请求，加入验证码之后的第二次登录尝试
            request = urllib2.Request(self.loginURL,self.postData,self.loginHeaders)
            #得到第一次登录尝试的相应
            response = self.opener.open(request)
            #获取其中的内容
            content = response.read().decode('gbk')
            #检测验证码错误的正则表达式，\u9a8c\u8bc1\u7801\u9519\u8bef 是验证码错误五个字的编码
            pattern = re.compile(u'\u9a8c\u8bc1\u7801\u9519\u8bef',re.S)
            result = re.search(pattern,content)
            #如果返回页面包括了，验证码错误五个字
            if result:
                print u"验证码输入错误"
                return False
            else:
                #返回结果直接带有J_HToken字样，说明验证码输入成功，成功跳转到了获取HToken的界面
                tokenPattern = re.compile('id="J_HToken" value="(.*?)"')
                tokenMatch = re.search(tokenPattern,content)
                #如果匹配成功，找到了J_HToken
                if tokenMatch:
                    print u"验证码输入正确"
                    print tokenMatch.group(1)
                    return tokenMatch.group(1)
                else:
                    #匹配失败，J_Token获取失败
                    print u"J_Token获取失败"
                    return False
        except urllib2.HTTPError, e:
            print u"连接服务器出错，错误原因",e.reason
            return False

    #程序运行主干
    def main(self):
        #是否需要验证码，是则得到页面内容，不是则返回False
        needResult = self.needCheckCode()
        #请求获取失败，得到的结果是None
        if not needResult ==None:
            if not needResult == False:
                print u"您需要手动输入验证码"
                idenCode = self.getCheckCode(needResult)
                #得到了验证码的链接
                if not idenCode == False:
                    print u"验证码获取成功"
                    print u"请在浏览器中输入您看到的验证码"
                    webbrowser.open_new_tab(idenCode)
                    J_HToken = self.loginWithCheckCode()
                    print "J_HToken",J_HToken
                #验证码链接为空，无效验证码
                else:
                    print u"验证码获取失败，请重试"
            else:
                print u"不需要输入验证码"
        else:
            print u"请求登录页面失败，无法确认是否需要验证码"



taobao = Taobao()
taobao.main()
```

现在的运行结果是这样的，我们已经可以得到 J_HToken 了，离成功又迈进了一步。

![](http://qiniu.cuiqingcai.com/wp-content/uploads/2015/02/QQ%E6%88%AA%E5%9B%BE20150225200329.jpg)

好，到现在为止，我们应该可以获取到J_HToken的值啦。

## 利用J_HToken获取st

st也是一个经计算得到的code，可以这么理解，st是淘宝后台利用J_HToken以及其他数据经过计算之后得到的，可以利用st和用户名直接用get方式登录，所以st可以理解为一个秘钥。这个st值只会使用一次，如果第二次用get方式登录则会失效。所以它是一次性使用的。

下面J_HToken计算st的方法如下

```
#通过token获得st
def getSTbyToken(self,token):
    tokenURL = 'https://passport.alipay.com/mini_apply_st.js?site=0&token=%s&callback=stCallback6' % token
    request = urllib2.Request(tokenURL)
    response = urllib2.urlopen(request)
    #处理st，获得用户淘宝主页的登录地址
    pattern = re.compile('{"st":"(.*?)"}',re.S)
    result = re.search(pattern,response.read())
    #如果成功匹配
    if result:
        print u"成功获取st码"
        #获取st的值
        st = result.group(1)
        return st
    else:
        print u"未匹配到st"
        return False
```

## 直接利用st登录

得到st之后，基本上就大功告成啦，一段辛苦终于没有白费，你可以直接构建get方式请求的URL，直接访问这个URL便可以实现登录。

```
stURL = 'https://login.taobao.com/member/vst.htm?st=%s&TPL_username=%s' % (st,username)
```

比如

```
 https://login.taobao.com/member/vst.htm?st=1uynJELa4hKfsfWU3OjPJCw&TPL_username=cqcre
```

直接访问该链接即可实现登录，不过我这个应该已经失效了吧~

代码在这先不贴了，剩下的一起贴了~

## 获取已买到的宝贝页面

已买到的宝贝的页面地址是

```
http://buyer.trade.taobao.com/trade/itemlist/list_bought_items.htm
```

另外还有页码的参数。

重新构建一个带有cookie的opener，将上面的带有st的URL打开，保存它的cookie，然后再利用这个opener打开已买到的宝贝的页面，你就会得到已买到的宝贝页面详情了。

```
#获得已买到的宝贝页面
def getGoodsPage(self,pageIndex):
    goodsURL = 'http://buyer.trade.taobao.com/trade/itemlist/listBoughtItems.htm?action=itemlist/QueryAction&event_submit_do_query=1&pageNum=' + str(pageIndex)
    response = self.newOpener.open(goodsURL)
    page =  response.read().decode('gbk')
    return page
```

正则表达式提取信息

这是我的已买到的宝贝界面，审查元素可以看到，每一个宝贝都是tbody标签包围着。

![](http://qiniu.cuiqingcai.com/wp-content/uploads/2015/02/QQ%E6%88%AA%E5%9B%BE20150225223302.jpg)

我们现在想获取订单时间，订单号，卖家店铺名称，宝贝名称，原价，购买数量，最后付款多少，交易状态这几个量，具体就不再分析啦，正则表达式还不熟悉的同学请参考前面所说的正则表达式的用法，在这里，正则表达式匹配的代码是

```
#u'\u8ba2\u5355\u53f7'是订单号的编码
pattern = re.compile(u'dealtime.*?>(.*?)</span>.*?\u8ba2\u5355\u53f7.*?<em>(.*?)</em>.*?shopname.*?title="(.*?)".*?baobei-name">.*?<a.*?>(.*?)</a>.*?'
                     u'price.*?title="(.*?)".*?quantity.*?title="(.*?)".*?amount.*?em.*?>(.*?)</em>.*?trade-status.*?<a.*?>(.*?)</a>',re.S)
result = re.findall(pattern,page)
for item in result:
    print '------------------------------------------------------------'
    print "购买日期:",item[0].strip(), '订单号:',item[1].strip(),'卖家店铺:',item[2].strip()
    print '宝贝名称:',item[3].strip()
    print '原价:',item[4].strip(),'购买数量:',item[5].strip(),'实际支付:',item[6].strip(),'交易状态',item[7].strip()
```

## 最终代码整理

恩，你懂得，最重要的东西来了，经过博主2天多的奋战，代码基本就构建完成。写了两个类，其中提取页面信息的方法我单独放到了一个类中，叫 tool.py，类名为 Tool。

先看一下运行结果吧~

![](http://qiniu.cuiqingcai.com/wp-content/uploads/2015/02/QQ%E6%88%AA%E5%9B%BE20150225234414.jpg)

最终代码如下

```
tool.py
```

```
__author__ = 'CQC'
# -*- coding:utf-8 -*-

import re

#处理获得的宝贝页面
class Tool:

    #初始化
    def __init__(self):
        pass


    #获得页码数
    def getPageNum(self,page):
        pattern = re.compile(u'<div class="total">.*?\u5171(.*?)\u9875',re.S)
        result = re.search(pattern,page)
        if result:
            print "找到了共多少页"
            pageNum = result.group(1).strip()
            print '共',pageNum,'页'
            return pageNum

    def getGoodsInfo(self,page):
        #u'\u8ba2\u5355\u53f7'是订单号的编码
        pattern = re.compile(u'dealtime.*?>(.*?)</span>.*?\u8ba2\u5355\u53f7.*?<em>(.*?)</em>.*?shopname.*?title="(.*?)".*?baobei-name">.*?<a.*?>(.*?)</a>.*?'
                             u'price.*?title="(.*?)".*?quantity.*?title="(.*?)".*?amount.*?em.*?>(.*?)</em>.*?trade-status.*?<a.*?>(.*?)</a>',re.S)
        result = re.findall(pattern,page)
        for item in result:
            print '------------------------------------------------------------'
            print "购买日期:",item[0].strip(), '订单号:',item[1].strip(),'卖家店铺:',item[2].strip()
            print '宝贝名称:',item[3].strip()
            print '原价:',item[4].strip(),'购买数量:',item[5].strip(),'实际支付:',item[6].strip(),'交易状态',item[7].strip()
```

```
taobao.py
```

```
__author__ = 'CQC'
# -*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
import re
import webbrowser
import tool

#模拟登录淘宝类
class Taobao:

    #初始化方法
    def __init__(self):
        #登录的URL
        self.loginURL = "https://login.taobao.com/member/login.jhtml"
        #代理IP地址，防止自己的IP被封禁
        self.proxyURL = 'http://120.193.146.97:843'
        #登录POST数据时发送的头部信息
        self.loginHeaders =  {
            'Host':'login.taobao.com',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Referer' : 'https://login.taobao.com/member/login.jhtml',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection' : 'Keep-Alive'
        }
        #用户名
        self.username = 'cqcre'
        #ua字符串，经过淘宝ua算法计算得出，包含了时间戳,浏览器,屏幕分辨率,随机数,鼠标移动,鼠标点击,其实还有键盘输入记录,鼠标移动的记录、点击的记录等等的信息
        self.ua = '191UW5TcyMNYQwiAiwTR3tCf0J/QnhEcUpkMmQ=|Um5Ockt0TXdPc011TXVKdyE=|U2xMHDJ+H2QJZwBxX39Rb1d5WXcrSixAJ1kjDVsN|VGhXd1llXGNaYFhkWmJaYl1gV2pIdUtyTXRKfkN4Qn1FeEF6R31TBQ==|VWldfS0TMw8xDjYWKhAwHiUdOA9wCDEVaxgkATdcNU8iDFoM|VmNDbUMV|V2NDbUMV|WGRYeCgGZhtmH2VScVI2UT5fORtmD2gCawwuRSJHZAFsCWMOdVYyVTpbPR99HWAFYVMpUDUFORshHiQdJR0jAT0JPQc/BDoFPgooFDZtVBR5Fn9VOwt2EWhCOVQ4WSJPJFkHXhgoSDVIMRgnHyFqQ3xEezceIRkmahRqFDZLIkUvRiEDaA9qQ3xEezcZORc5bzk=|WWdHFy0TMw8vEy0UIQE0ADgYJBohGjoAOw4uEiwXLAw2DThuOA==|WmBAED5+KnIbdRh1GXgFQSZbGFdrUm1UblZqVGxQa1ZiTGxQcEp1I3U=|W2NDEz19KXENZwJjHkY7Ui9OJQsre09zSWlXY1oMLBExHzERLxsuE0UT|XGZGFjh4LHQdcx5zH34DRyBdHlFtVGtSaFBsUmpWbVBkSmpXd05zTnMlcw==|XWdHFzl5LXUJYwZnGkI/VitKIQ8vEzMKNws3YTc=|XmdaZ0d6WmVFeUB8XGJaYEB4TGxWbk5yTndXa0tyT29Ta0t1QGBeZDI='
        #密码，在这里不能输入真实密码，淘宝对此密码进行了加密处理，256位，此处为加密后的密码
        self.password2 = '7511aa6854629e45de220d29174f1066537a73420ef6dbb5b46f202396703a2d56b0312df8769d886e6ca63d587fdbb99ee73927e8c07d9c88cd02182e1a21edc13fb8e140a4a2a4b53bf38484bd0e08199e03eb9bf7b365a5c673c03407d812b91394f0d3c7564042e3f2b11d156aeea37ad6460118914125ab8f8ac466f'
        self.post = post = {
            'ua':self.ua,
            'TPL_checkcode':'',
            'CtrlVersion': '1,0,0,7',
            'TPL_password':'',
            'TPL_redirect_url':'http://i.taobao.com/my_taobao.htm?nekot=udm8087E1424147022443',
            'TPL_username':self.username,
            'loginsite':'0',
            'newlogin':'0',
            'from':'tb',
            'fc':'default',
            'style':'default',
            'css_style':'',
            'tid':'XOR_1_000000000000000000000000000000_625C4720470A0A050976770A',
            'support':'000001',
            'loginType':'4',
            'minititle':'',
            'minipara':'',
            'umto':'NaN',
            'pstrong':'3',
            'llnick':'',
            'sign':'',
            'need_sign':'',
            'isIgnore':'',
            'full_redirect':'',
            'popid':'',
            'callback':'',
            'guf':'',
            'not_duplite_str':'',
            'need_user_id':'',
            'poy':'',
            'gvfdcname':'10',
            'gvfdcre':'',
            'from_encoding ':'',
            'sub':'',
            'TPL_password_2':self.password2,
            'loginASR':'1',
            'loginASRSuc':'1',
            'allp':'',
            'oslanguage':'zh-CN',
            'sr':'1366*768',
            'osVer':'windows|6.1',
            'naviVer':'firefox|35'
        }
        #将POST的数据进行编码转换
        self.postData = urllib.urlencode(self.post)
        #设置代理
        self.proxy = urllib2.ProxyHandler({'http':self.proxyURL})
        #设置cookie
        self.cookie = cookielib.LWPCookieJar()
        #设置cookie处理器
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
        #设置登录时用到的opener，它的open方法相当于urllib2.urlopen
        self.opener = urllib2.build_opener(self.cookieHandler,self.proxy,urllib2.HTTPHandler)
        #赋值J_HToken
        self.J_HToken = ''
        #登录成功时，需要的Cookie
        self.newCookie = cookielib.CookieJar()
        #登陆成功时，需要的一个新的opener
        self.newOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.newCookie))
        #引入工具类
        self.tool = tool.Tool()


    #得到是否需要输入验证码，这次请求的相应有时会不同，有时需要验证有时不需要
    def needCheckCode(self):
        #第一次登录获取验证码尝试，构建request
        request = urllib2.Request(self.loginURL,self.postData,self.loginHeaders)
        #得到第一次登录尝试的相应
        response = self.opener.open(request)
        #获取其中的内容
        content = response.read().decode('gbk')
        #获取状态吗
        status = response.getcode()
        #状态码为200，获取成功
        if status == 200:
            print u"获取请求成功"
            #\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801这六个字是请输入验证码的utf-8编码
            pattern = re.compile(u'\u8bf7\u8f93\u5165\u9a8c\u8bc1\u7801',re.S)
            result = re.search(pattern,content)
            #如果找到该字符，代表需要输入验证码
            if result:
                print u"此次安全验证异常，您需要输入验证码"
                return content
            #否则不需要
            else:
                #返回结果直接带有J_HToken字样，表明直接验证通过
                tokenPattern = re.compile('id="J_HToken" value="(.*?)"')
                tokenMatch = re.search(tokenPattern,content)
                if tokenMatch:
                    self.J_HToken = tokenMatch.group(1)
                    print u"此次安全验证通过，您这次不需要输入验证码"
                    return False
        else:
            print u"获取请求失败"
            return None

    #得到验证码图片
    def getCheckCode(self,page):
        #得到验证码的图片
        pattern = re.compile('<img id="J_StandardCode_m.*?data-src="(.*?)"',re.S)
        #匹配的结果
        matchResult = re.search(pattern,page)
        #已经匹配得到内容，并且验证码图片链接不为空
        if matchResult and matchResult.group(1):
            return matchResult.group(1)
        else:
            print u"没有找到验证码内容"
            return False


    #输入验证码，重新请求，如果验证成功，则返回J_HToken
    def loginWithCheckCode(self):
        #提示用户输入验证码
        checkcode = raw_input('请输入验证码:')
        #将验证码重新添加到post的数据中
        self.post['TPL_checkcode'] = checkcode
        #对post数据重新进行编码
        self.postData = urllib.urlencode(self.post)
        try:
            #再次构建请求，加入验证码之后的第二次登录尝试
            request = urllib2.Request(self.loginURL,self.postData,self.loginHeaders)
            #得到第一次登录尝试的相应
            response = self.opener.open(request)
            #获取其中的内容
            content = response.read().decode('gbk')
            #检测验证码错误的正则表达式，\u9a8c\u8bc1\u7801\u9519\u8bef 是验证码错误五个字的编码
            pattern = re.compile(u'\u9a8c\u8bc1\u7801\u9519\u8bef',re.S)
            result = re.search(pattern,content)
            #如果返回页面包括了，验证码错误五个字
            if result:
                print u"验证码输入错误"
                return False
            else:
                #返回结果直接带有J_HToken字样，说明验证码输入成功，成功跳转到了获取HToken的界面
                tokenPattern = re.compile('id="J_HToken" value="(.*?)"')
                tokenMatch = re.search(tokenPattern,content)
                #如果匹配成功，找到了J_HToken
                if tokenMatch:
                    print u"验证码输入正确"
                    self.J_HToken = tokenMatch.group(1)
                    return tokenMatch.group(1)
                else:
                    #匹配失败，J_Token获取失败
                    print u"J_Token获取失败"
                    return False
        except urllib2.HTTPError, e:
            print u"连接服务器出错，错误原因",e.reason
            return False


    #通过token获得st
    def getSTbyToken(self,token):
        tokenURL = 'https://passport.alipay.com/mini_apply_st.js?site=0&token=%s&callback=stCallback6' % token
        request = urllib2.Request(tokenURL)
        response = urllib2.urlopen(request)
        #处理st，获得用户淘宝主页的登录地址
        pattern = re.compile('{"st":"(.*?)"}',re.S)
        result = re.search(pattern,response.read())
        #如果成功匹配
        if result:
            print u"成功获取st码"
            #获取st的值
            st = result.group(1)
            return st
        else:
            print u"未匹配到st"
            return False

    #利用st码进行登录,获取重定向网址
    def loginByST(self,st,username):
        stURL = 'https://login.taobao.com/member/vst.htm?st=%s&TPL_username=%s' % (st,username)
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Host':'login.taobao.com',
            'Connection' : 'Keep-Alive'
        }
        request = urllib2.Request(stURL,headers = headers)
        response = self.newOpener.open(request)
        content =  response.read().decode('gbk')
        #检测结果，看是否登录成功
        pattern = re.compile('top.location = "(.*?)"',re.S)
        match = re.search(pattern,content)
        if match:
            print u"登录网址成功"
            location = match.group(1)
            return True
        else:
            print "登录失败"
            return False


    #获得已买到的宝贝页面
    def getGoodsPage(self,pageIndex):
        goodsURL = 'http://buyer.trade.taobao.com/trade/itemlist/listBoughtItems.htm?action=itemlist/QueryAction&event_submit_do_query=1' + '&pageNum=' + str(pageIndex)
        response = self.newOpener.open(goodsURL)
        page =  response.read().decode('gbk')
        return page

    #获取所有已买到的宝贝信息
    def getAllGoods(self,pageNum):
        print u"获取到的商品列表如下"
        for x in range(1,int(pageNum)+1):
            page = self.getGoodsPage(x)
            self.tool.getGoodsInfo(page)



    #程序运行主干
    def main(self):
        #是否需要验证码，是则得到页面内容，不是则返回False
        needResult = self.needCheckCode()
        #请求获取失败，得到的结果是None
        if not needResult ==None:
            if not needResult == False:
                print u"您需要手动输入验证码"
                checkCode = self.getCheckCode(needResult)
                #得到了验证码的链接
                if not checkCode == False:
                    print u"验证码获取成功"
                    print u"请在浏览器中输入您看到的验证码"
                    webbrowser.open_new_tab(checkCode)
                    self.loginWithCheckCode()
                #验证码链接为空，无效验证码
                else:
                    print u"验证码获取失败，请重试"
            else:
                print u"不需要输入验证码"
        else:
            print u"请求登录页面失败，无法确认是否需要验证码"


        #判断token是否正常获取到
        if not self.J_HToken:
            print "获取Token失败，请重试"
            return
        #获取st码
        st = self.getSTbyToken(self.J_HToken)
        #利用st进行登录
        result = self.loginByST(st,self.username)
        if result:
            #获得所有宝贝的页面
            page = self.getGoodsPage(1)
            pageNum = self.tool.getPageNum(page)
            self.getAllGoods(pageNum)
        else:
            print u"登录失败"



taobao = Taobao()
taobao.main()
```

好啦，运行结果就是上面贴的图片，可以成功获取到自己的商品列表，前提是把你们的 用户名，ua，password2这三个设置好。

以上均为博主亲身所敲，代码写的不好，谨在此贴出和大家一起分享经验~

小伙伴们试一下吧，希望对大家有帮助~