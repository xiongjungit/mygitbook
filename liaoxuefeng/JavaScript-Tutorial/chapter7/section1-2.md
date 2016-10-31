#7-1-2 查找和过滤

通常情况下选择器可以直接定位到我们想要的元素，但是，当我们拿到一个jQuery对象后，还可以以这个对象为基准，进行查找和过滤。

最常见的查找是在某个节点的所有子节点中查找，使用find()方法，它本身又接收一个任意的选择器。例如如下的HTML结构：

	<!-- HTML结构 -->
	<ul class="lang">
	    <li class="js dy">JavaScript</li>
	    <li class="dy">Python</li>
	    <li id="swift">Swift</li>
	    <li class="dy">Scheme</li>
	    <li name="haskell">Haskell</li>
	</ul>
用find()查找：

	var ul = $('ul.lang'); // 获得<ul>
	var dy = ul.find('.dy'); // 获得JavaScript, Python, Scheme
	var swf = ul.find('#swift'); // 获得Swift
	var hsk = ul.find('[name=haskell]'); // 获得Haskell
如果要从当前节点开始向上查找，使用parent()方法：

	var swf = $('#swift'); // 获得Swift
	var parent = swf.parent(); // 获得Swift的上层节点<ul>
	var a = swf.parent('div.red'); // 从Swift的父节点开始向上查找，直到找到某个符合条件的节点并返回
对于位于同一层级的节点，可以通过next()和prev()方法，例如：

当我们已经拿到Swift节点后：

	var swift = $('#swift');
	
	swift.next(); // Scheme
	swift.next('[name=haskell]'); // Haskell，因为Haskell是后续第一个符合选择器条件的节点
	
	swift.prev(); // Python
	swift.prev('.js'); // JavaScript，因为JavaScript是往前第一个符合选择器条件的节点
##过滤

和函数式编程的map、filter类似，jQuery对象也有类似的方法。

filter()方法可以过滤掉不符合选择器条件的节点：
	
	var langs = $('ul.lang li'); // 拿到JavaScript, Python, Swift, Scheme和Haskell
	var a = langs.filter('.dy'); // 拿到JavaScript, Python, Scheme
或者传入一个函数，要特别注意函数内部的this被绑定为DOM对象，不是jQuery对象：

	var langs = $('ul.lang li'); // 拿到JavaScript, Python, Swift, Scheme和Haskell
	langs.filter(function () {
	    return this.innerHTML.indexOf('S') === 0; // 返回S开头的节点
	}); // 拿到Swift, Scheme
map()方法把一个jQuery对象包含的若干DOM节点转化为其他对象：

	var langs = $('ul.lang li'); // 拿到JavaScript, Python, Swift, Scheme和Haskell
	var arr = langs.map(function () {
	    return this.innerHTML;
	}).get(); // 用get()拿到包含string的Array：['JavaScript', 'Python', 'Swift', 'Scheme', 'Haskell']
此外，一个jQuery对象如果包含了不止一个DOM节点，first()、last()和slice()方法可以返回一个新的jQuery对象，把不需要的DOM节点去掉：

	var langs = $('ul.lang li'); // 拿到JavaScript, Python, Swift, Scheme和Haskell
	var js = langs.first(); // JavaScript，相当于$('ul.lang li:first-child')
	var haskell = langs.last(); // Haskell, 相当于$('ul.lang li:last-child')
	var sub = langs.slice(2, 4); // Swift, Scheme, 参数和数组的slice()方法一致
##练习

对于下面的表单：

	<form id="test-form" action="#0" onsubmit="return false;">
	    <p><label>Name: <input name="name"></label></p>
	    <p><label>Email: <input name="email"></label></p>
	    <p><label>Password: <input name="password" type="password"></label></p>
	    <p>Gender: <label><input name="gender" type="radio" value="m" checked> Male</label> <label><input name="gender" type="radio" value="f"> Female</label></p>
	    <p><label>City: <select name="city">
	        <option value="BJ" selected>Beijing</option>
	        <option value="SH">Shanghai</option>
	        <option value="CD">Chengdu</option>
	        <option value="XM">Xiamen</option>
	    </select></label></p>
	    <p><button type="submit">Submit</button></p>
	</form>
输入值后，用jQuery获取表单的JSON字符串，key和value分别对应每个输入的name和相应的value，例如：{"name":"Michael","email":...}

	'use strict';
	var json = null;
	
	json = ???;
	
	// 显示结果:
	if (typeof(json) === 'string') {
	    alert(json);
	}
	else {
	    alert('json变量不是string!');
	}





<form id="test-form" action="#0" onsubmit="return false;">
    <p><label>Name: <input name="name"></label></p>
    <p><label>Email: <input name="email"></label></p>
    <p><label>Password: <input name="password" type="password"></label></p>
    <p>Gender: <label><input name="gender" type="radio" value="m" checked=""> Male</label> <label><input name="gender" type="radio" value="f"> Female</label></p>
    <p><label>City: <select name="city">
        <option value="BJ" selected="">Beijing</option>
        <option value="SH">Shanghai</option>
        <option value="CD">Chengdu</option>
        <option value="XM">Xiamen</option>
    </select></label></p>
    <p><button type="submit">Submit</button></p>
</form>