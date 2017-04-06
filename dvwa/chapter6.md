#dvwacn之六暴力破解

dvwacn之暴力破解物理路径

```
root@webserver:/var/www/dvwacn/vulnerabilities/brute/source# ls
high.php  low.php  medium.php
```


##安全级别

- low.php

```
<?php

if( isset( $_GET['Login'] ) ) {

	$user = $_GET['username'];
	
	$pass = $_GET['password'];
	$pass = md5($pass);

	$qry = "SELECT * FROM `users` WHERE user='$user' AND password='$pass';";
	$result = mysql_query( $qry ) or die( '<pre>' . mysql_error() . '</pre>' );

	if( $result && mysql_num_rows( $result ) == 1 ) {
		// Get users details
		$i=0; // Bug fix.
		$avatar = mysql_result( $result, $i, "avatar" );

		// Login Successful
		$html .= "<p>µȂ½³ɹ¦£¬ź¿ʒԽ񑇤̼²ڗ󡡠" . $user . "</p>";
		$html .= '<img src="' . $avatar . '" />';
	} else {
		//Login failed
		$html .= "<pre><br>ԃ»§Ļ»󖠃݂뵭ϳ¡£</pre>";
	}

	mysql_close();
}

?>
```

- medium.php 

```
<?php

if( isset( $_GET[ 'Login' ] ) ) {

	// Sanitise username input
	$user = $_GET[ 'username' ];
	$user = mysql_real_escape_string( $user );

	// Sanitise password input
	$pass = $_GET[ 'password' ];
	$pass = mysql_real_escape_string( $pass );
	$pass = md5( $pass );

	$qry = "SELECT * FROM `users` WHERE user='$user' AND password='$pass';";
	$result = mysql_query( $qry ) or die( '<pre>' . mysql_error() . '</pre>' );

	if( $result && mysql_num_rows($result) == 1 ) {
		// Get users details
		$i=0; // Bug fix.
		$avatar = mysql_result( $result, $i, "avatar" );

		// Login Successful
		$html .= "<p>µȂ½³ɹ¦£¬ź¿ʒԽ񑇤̼²ڗ󡡢 . $user . "</p>";
		$html .= '<img src="' . $avatar . '" />';
	} else {
		//Login failed
		$html .= "<pre><br>ԃ»§Ļ»󖠃݂뵭ϳ¡£</pre>";
	}

	mysql_close();
}

?>
```


- high.php

``` 
<?php

if( isset( $_GET[ 'Login' ] ) ) {

	// Sanitise username input
	$user = $_GET[ 'username' ];
	$user = stripslashes( $user );
	$user = mysql_real_escape_string( $user );

	// Sanitise password input
	$pass = $_GET[ 'password' ];
	$pass = stripslashes( $pass );
	$pass = mysql_real_escape_string( $pass );
	$pass = md5( $pass );

	$qry = "SELECT * FROM `users` WHERE user='$user' AND password='$pass';";
	$result = mysql_query($qry) or die('<pre>' . mysql_error() . '</pre>' );

	if( $result && mysql_num_rows( $result ) == 1 ) {
		// Get users details
		$i=0; // Bug fix.
		$avatar = mysql_result( $result, $i, "avatar" );

		// Login Successful
		$html .= "<p>µȂ½³ɹ¦£¬ź¿ʒԽ񑇤̼²ڗ󡡢 . $user . "</p>";
		$html .= '<img src="' . $avatar . '" />';
	} else {
		// Login failed
		sleep(3);
		$html .= "<pre><br>ԃ»§Ļ»󖠃݂뵭ϳ¡£</pre>";
		}

	mysql_close();
}

?>
```

##暴力破解过程

###设置http代理

火狐浏览器中安装FoxyProxy插件

```
新建代理服务器-->代理名称:Burp Suite-->主机或IP地址:127.0.0.1-->端口:8080-->为全部Urls启用代理服务器Burp Suite
```

###设置Burp Suite

打开Burp Suite

```
Proxy-->Options-->Add-->Bind to Port:8080|Blind to Address:127.0.0.1

Intercept-->Intercept is off
```

http://192.168.56.80/dvwacn/vulnerabilities/brute

用户点击暴力破解，输入

```
用户名：admin
密码：123456
```

接着到Burp Suite中查看抓到的http包内容

```
GET /dvwacn/vulnerabilities/brute/?username=admin&password=123456&Login=%B5%C7%C2%BD HTTP/1.1
Host: 192.168.56.80
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://192.168.56.80/dvwacn/vulnerabilities/brute/
Cookie: security=high; PHPSESSID=b066ao156vs6s2qhh0kr60sha4
Connection: close
```

把抓到的http包发送到Intruder，设置Positions如下

```
GET /dvwacn/vulnerabilities/brute/?username=admin&password=§123456§&Login=%B5%C7%C2%BD HTTP/1.1
Host: 192.168.56.80
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://192.168.56.80/dvwacn/vulnerabilities/brute/
Cookie: security=high; PHPSESSID=b066ao156vs6s2qhh0kr60sha4
Connection: close
```

设置Payloads，从Payload Options中选中Load...选择一个字典文件/tmp/dic.txt

dic.txt内容如下

```
123456
root
admin888
password
admin
```

设置Options匹配规则，从Grep - Match中选择Add添加`用户名或者密码错误。`

然后点击Positions中的Start attack进行暴力破解

查看运行结果，按Length排序，选中字节数大小跟其他不一样的那一条,查看Response中的Render,你会发现已经登录成功了。

当然，你也可以查看录像文件，更直观的观察暴力破解过程。

http://192.168.56.80/dvwacn/vulnerabilities/brute/Bruteforce/Bruteforce_controller.swf
