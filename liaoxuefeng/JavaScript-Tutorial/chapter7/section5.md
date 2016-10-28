#7-5 AJAX


用JavaScript写AJAX前面已经介绍过了，主要问题就是不同浏览器需要写不同代码，并且状态和错误处理写起来很麻烦。

用jQuery的相关对象来处理AJAX，不但不需要考虑浏览器问题，代码也能大大简化。

##ajax

jQuery在全局对象jQuery（也就是$）绑定了ajax()函数，可以处理AJAX请求。ajax(url, settings)函数需要接收一个URL和一个可选的settings对象，常用的选项如下：

- async：是否异步执行AJAX请求，默认为true，千万不要指定为false；

- method：发送的Method，缺省为'GET'，可指定为'POST'、'PUT'等；

- contentType：发送POST请求的格式，默认值为'application/x-www-form-urlencoded; charset=UTF-8'，也可以指定为text/plain、application/json；

- data：发送的数据，可以是字符串、数组或object。如果是GET请求，data将被转换成query附加到URL上，如果是POST请求，根据contentType把data序列化成合适的格式；

- headers：发送的额外的HTTP头，必须是一个object；

- dataType：接收的数据格式，可以指定为'html'、'xml'、'json'、'text'等，缺省情况下根据响应的Content-Type猜测。

下面的例子发送一个GET请求，并返回一个JSON格式的数据：

	var jqxhr = $.ajax('/api/categories', {
	    dataType: 'json'
	});
	// 请求已经发送了
不过，如何用回调函数处理返回的数据和出错时的响应呢？

还记得Promise对象吗？jQuery的jqXHR对象类似一个Promise对象，我们可以用链式写法来处理各种回调：

	'use strict';
	
	function ajaxLog(s) {
	    var txt = $('#test-response-text');
	    txt.val(txt.val() + '\n' + s);
	}
	
	$('#test-response-text').val('');
	
	var jqxhr = $.ajax('/api/categories', {
	    dataType: 'json'
	}).done(function (data) {
	    ajaxLog('成功, 收到的数据: ' + JSON.stringify(data));
	}).fail(function (xhr, status) {
	    ajaxLog('失败: ' + xhr.status + ', 原因: ' + status);
	}).always(function () {
	    ajaxLog('请求完成: 无论成功或失败都会调用');
	});


<textarea id="test-response-text" rows="10" style="width: 90%; margin: 15px 0; resize: none;">响应结果：</textarea>

##get

对常用的AJAX操作，jQuery提供了一些辅助方法。由于GET请求最常见，所以jQuery提供了get()方法，可以这么写：

	var jqxhr = $.get('/path/to/resource', {
	    name: 'Bob Lee',
	    check: 1
	});
第二个参数如果是object，jQuery自动把它变成query string然后加到URL后面，实际的URL是：

	/path/to/resource?name=Bob%20Lee&check=1
这样我们就不用关心如何用URL编码并构造一个query string了。

##post

post()和get()类似，但是传入的第二个参数默认被序列化为application/x-www-form-urlencoded：

	var jqxhr = $.post('/path/to/resource', {
	    name: 'Bob Lee',
	    check: 1
	});
实际构造的数据name=Bob%20Lee&check=1作为POST的body被发送。

##getJSON

由于JSON用得越来越普遍，所以jQuery也提供了getJSON()方法来快速通过GET获取一个JSON对象：

	var jqxhr = $.getJSON('/path/to/resource', {
	    name: 'Bob Lee',
	    check: 1
	}).done(function (data) {
	    // data已经被解析为JSON对象了
	});
##安全限制

jQuery的AJAX完全封装的是JavaScript的AJAX操作，所以它的安全限制和前面讲的用JavaScript写AJAX完全一样。

如果需要使用JSONP，可以在ajax()中设置jsonp: 'callback'，让jQuery实现JSONP跨域加载数据。

关于跨域的设置请参考浏览器 - AJAX一节中CORS的设置。