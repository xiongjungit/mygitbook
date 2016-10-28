#6-2 操作DOM


由于HTML文档被浏览器解析后就是一棵DOM树，要改变HTML的结构，就需要通过JavaScript来操作DOM。

始终记住DOM是一个树形结构。操作一个DOM节点实际上就是这么几个操作：

- 更新：更新该DOM节点的内容，相当于更新了该DOM节点表示的HTML的内容；

- 遍历：遍历该DOM节点下的子节点，以便进行进一步操作；

- 添加：在该DOM节点下新增一个子节点，相当于动态增加了一个HTML节点；

- 删除：将该节点从HTML中删除，相当于删掉了该DOM节点的内容以及它包含的所有子节点。

在操作一个DOM节点前，我们需要通过各种方式先拿到这个DOM节点。最常用的方法是document.getElementById()和document.getElementsByTagName()，以及CSS选择器document.getElementsByClassName()。

由于ID在HTML文档中是唯一的，所以document.getElementById()可以直接定位唯一的一个DOM节点。document.getElementsByTagName()和document.getElementsByClassName()总是返回一组DOM节点。要精确地选择DOM，可以先定位父节点，再从父节点开始选择，以缩小范围。

例如：

	// 返回ID为'test'的节点：
	var test = document.getElementById('test');
	
	// 先定位ID为'test-table'的节点，再返回其内部所有tr节点：
	var trs = document.getElementById('test-table').getElementsByTagName('tr');
	
	// 先定位ID为'test-div'的节点，再返回其内部所有class包含red的节点：
	var reds = document.getElementById('test-div').getElementsByClassName('red');
	
	// 获取节点test下的所有直属子节点:
	var cs = test.children;
	
	// 获取节点test下第一个、最后一个子节点：
	var first = test.firstElementChild;
	var last = test.lastElementChild;
第二种方法是使用querySelector()和querySelectorAll()，需要了解selector语法，然后使用条件来获取节点，更加方便：

	// 通过querySelector获取ID为q1的节点：
	var q1 = document.querySelector('#q1');
	
	// 通过querySelectorAll获取q1节点内的符合条件的所有节点：
	var ps = q1.querySelectorAll('div.highlighted > p');
注意：低版本的IE<8不支持querySelector和querySelectorAll。IE8仅有限支持。

严格地讲，我们这里的DOM节点是指Element，但是DOM节点实际上是Node，在HTML中，Node包括Element、Comment、CDATA_SECTION等很多种，以及根节点Document类型，但是，绝大多数时候我们只关心Element，也就是实际控制页面结构的Node，其他类型的Node忽略即可。根节点Document已经自动绑定为全局变量document。

##练习

如下的HTML结构：

JavaScript

Java

Python

Ruby

Swift

Scheme

Haskell

	<!-- HTML结构 -->
	<div id="test-div">
	<div class="c-red">
	    <p id="test-p">JavaScript</p>
	    <p>Java</p>
	  </div>
	  <div class="c-red c-green">
	    <p>Python</p>
	    <p>Ruby</p>
	    <p>Swift</p>
	  </div>
	  <div class="c-green">
	    <p>Scheme</p>
	    <p>Haskell</p>
	  </div>
	</div>
请选择出指定条件的节点：

	'use strict';
	
	// 选择<p>JavaScript</p>:
	var js = ???;
	
	// 选择<p>Python</p>,<p>Ruby</p>,<p>Swift</p>:
	var arr = ???;
	
	// 选择<p>Haskell</p>:
	var haskell = ???;
	
	// 测试:
	if (!js || js.innerText !== 'JavaScript') {
	    alert('选择JavaScript失败!');
	} else if (!arr || arr.length !== 3 || !arr[0] || !arr[1] || !arr[2] || arr[0].innerText !== 'Python' || arr[1].innerText !== 'Ruby' || arr[2].innerText !== 'Swift') {
	    alert('选择Python,Ruby,Swift失败!');
	} else if (!haskell || haskell.innerText !== 'Haskell') {
	    alert('选择Haskell失败!');
	} else {
	    alert('测试通过!');
	}