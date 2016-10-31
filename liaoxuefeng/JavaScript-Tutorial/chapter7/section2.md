#7-2 操作DOM

jQuery的选择器很强大，用起来又简单又灵活，但是搞了这么久，我拿到了jQuery对象，到底要干什么？

答案当然是操作对应的DOM节点啦！

回顾一下修改DOM的CSS、文本、设置HTML有多么麻烦，而且有的浏览器只有innerHTML，有的浏览器支持innerText，有了jQuery对象，不需要考虑浏览器差异了，全部统一操作！

##修改Text和HTML

jQuery对象的text()和html()方法分别获取节点的文本和原始HTML文本，例如，如下的HTML结构：

	<!-- HTML结构 -->
	<ul id="test-ul">
	    <li class="js">JavaScript</li>
	    <li name="book">Java &amp; JavaScript</li>
	</ul>
分别获取文本和HTML：

	$('#test-ul li[name=book]').text(); // 'Java & JavaScript'
	$('#test-ul li[name=book]').html(); // 'Java &amp; JavaScript'
如何设置文本或HTML？jQuery的API设计非常巧妙：无参数调用text()是获取文本，传入参数就变成设置文本，HTML也是类似操作，自己动手试试：

	'use strict';
	var j1 = $('#test-ul li.js');
	var j2 = $('#test-ul li[name=book]');
	
	j1.html('<span style="color: red">JavaScript</span>');
	j2.text('JavaScript & ECMAScript');

- JavaScript
- Java & JavaScript

一个jQuery对象可以包含0个或任意个DOM对象，它的方法实际上会作用在对应的每个DOM节点上。在上面的例子中试试：

	$('#test-ul li').text('JS'); // 是不是两个节点都变成了JS？
所以jQuery对象的另一个好处是我们可以执行一个操作，作用在对应的一组DOM节点上。即使选择器没有返回任何DOM节点，调用jQuery对象的方法仍然不会报错：

	// 如果不存在id为not-exist的节点：
	$('#not-exist').text('Hello'); // 代码不报错，没有节点被设置为'Hello'
这意味着jQuery帮你免去了许多if语句。

##修改CSS

jQuery对象有“批量操作”的特点，这用于修改CSS实在是太方便了。考虑下面的HTML结构：

	<!-- HTML结构 -->
	<ul id="test-css">
	    <li class="lang dy"><span>JavaScript</span></li>
	    <li class="lang"><span>Java</span></li>
	    <li class="lang dy"><span>Python</span></li>
	    <li class="lang"><span>Swift</span></li>
	    <li class="lang dy"><span>Scheme</span></li>
	</ul>
要高亮显示动态语言，调用jQuery对象的css('name', 'value')方法，我们用一行语句实现：

	'use strict';
	
	$('#test-css li.dy>span').css('background-color', '#ffd351').css('color', 'red');

- JavaScript
- Java
- Python
- Swift
- Scheme

注意，jQuery对象的所有方法都返回一个jQuery对象（可能是新的也可能是自身），这样我们可以进行链式调用，非常方便。

jQuery对象的css()方法可以这么用：

	var div = $('#test-div');
	div.css('color'); // '#000033', 获取CSS属性
	div.css('color', '#336699'); // 设置CSS属性
	div.css('color', ''); // 清除CSS属性
为了和JavaScript保持一致，CSS属性可以用'background-color'和'backgroundColor'两种格式。

css()方法将作用于DOM节点的style属性，具有最高优先级。如果要修改class属性，可以用jQuery提供的下列方法：

	var div = $('#test-div');
	div.hasClass('highlight'); // false， class是否包含highlight
	div.addClass('highlight'); // 添加highlight这个class
	div.removeClass('highlight'); // 删除highlight这个class
练习：分别用css()方法和addClass()方法高亮显示JavaScript：

	<!-- HTML结构 -->
	<style>
	.highlight {
	    color: #dd1144;
	    background-color: #ffd351;
	}
	</style>
	
	<div id="test-highlight-css">
	    <ul>
	        <li class="py"><span>Python</span></li>
	        <li class="js"><span>JavaScript</span></li>
	        <li class="sw"><span>Swift</span></li>
	        <li class="hk"><span>Haskell</span></li>
	    </ul>
	</div>
	'use strict';
	
	var div = $('#test-highlight-css');
	// TODO:


- Python
- JavaScript
- Swift
- Haskell

##显示和隐藏DOM

要隐藏一个DOM，我们可以设置CSS的display属性为none，利用css()方法就可以实现。不过，要显示这个DOM就需要恢复原有的display属性，这就得先记下来原有的display属性到底是block还是inline还是别的值。

考虑到显示和隐藏DOM元素使用非常普遍，jQuery直接提供show()和hide()方法，我们不用关心它是如何修改display属性的，总之它能正常工作：

	var a = $('a[target=_blank]');
	a.hide(); // 隐藏
	a.show(); // 显示
注意，隐藏DOM节点并未改变DOM树的结构，它只影响DOM节点的显示。这和删除DOM节点是不同的。

##获取DOM信息

利用jQuery对象的若干方法，我们直接可以获取DOM的高宽等信息，而无需针对不同浏览器编写特定代码：

	// 浏览器可视窗口大小:
	$(window).width(); // 800
	$(window).height(); // 600
	
	// HTML文档大小:
	$(document).width(); // 800
	$(document).height(); // 3500
	
	// 某个div的大小:
	var div = $('#test-div');
	div.width(); // 600
	div.height(); // 300
	div.width(400); // 设置CSS属性 width: 400px，是否生效要看CSS是否有效
	div.height('200px'); // 设置CSS属性 height: 200px，是否生效要看CSS是否有效
attr()和removeAttr()方法用于操作DOM节点的属性：

	// <div id="test-div" name="Test" start="1">...</div>
	var div = $('#test-div');
	div.attr('data'); // undefined, 属性不存在
	div.attr('name'); // 'Test'
	div.attr('name', 'Hello'); // div的name属性变为'Hello'
	div.removeAttr('name'); // 删除name属性
	div.attr('name'); // undefined
prop()方法和attr()类似，但是HTML5规定有一种属性在DOM节点中可以没有值，只有出现与不出现两种，例如：

	<input id="test-radio" type="radio" name="test" checked value="1">
等价于：

	<input id="test-radio" type="radio" name="test" checked="checked" value="1">
attr()和prop()对于属性checked处理有所不同：

	var radio = $('#test-radio');
	radio.attr('checked'); // 'checked'
	radio.prop('checked'); // true
prop()返回值更合理一些。不过，用is()方法判断更好：

	var radio = $('#test-radio');
	radio.is(':checked'); // true
类似的属性还有selected，处理时最好用is(':selected')。

##操作表单

对于表单元素，jQuery对象统一提供val()方法获取和设置对应的value属性：

	/*
	    <input id="test-input" name="email" value="">
	    <select id="test-select" name="city">
	        <option value="BJ" selected>Beijing</option>
	        <option value="SH">Shanghai</option>
	        <option value="SZ">Shenzhen</option>
	    </select>
	    <textarea id="test-textarea">Hello</textarea>
	*/
	var
	    input = $('#test-input'),
	    select = $('#test-select'),
	    textarea = $('#test-textarea');
	
	input.val(); // 'test'
	input.val('abc@example.com'); // 文本框的内容已变为abc@example.com
	
	select.val(); // 'BJ'
	select.val('SH'); // 选择框已变为Shanghai
	
	textarea.val(); // 'Hello'
	textarea.val('Hi'); // 文本区域已更新为'Hi'
可见，一个val()就统一了各种输入框的取值和赋值的问题。