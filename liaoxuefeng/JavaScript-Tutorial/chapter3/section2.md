#3-2 变量作用域


在JavaScript中，用var申明的变量实际上是有作用域的。

如果一个变量在函数体内部申明，则该变量的作用域为整个函数体，在函数体外不可引用该变量：

	'use strict';
	
	function foo() {
	    var x = 1;
	    x = x + 1;
	}
	
	x = x + 2; // ReferenceError! 无法在函数体外引用变量x
如果两个不同的函数各自申明了同一个变量，那么该变量只在各自的函数体内起作用。换句话说，不同函数内部的同名变量互相独立，互不影响：

	'use strict';
	
	function foo() {
	    var x = 1;
	    x = x + 1;
	}
	
	function bar() {
	    var x = 'A';
	    x = x + 'B';
	}
由于JavaScript的函数可以嵌套，此时，内部函数可以访问外部函数定义的变量，反过来则不行：

	'use strict';
	
	function foo() {
	    var x = 1;
	    function bar() {
	        var y = x + 1; // bar可以访问foo的变量x!
	    }
	    var z = y + 1; // ReferenceError! foo不可以访问bar的变量y!
	}
如果内部函数和外部函数的变量名重名怎么办？

	'use strict';
	
	function foo() {
	    var x = 1;
	    function bar() {
	        var x = 'A';
	        alert('x in bar() = ' + x); // 'A'
	    }
	    alert('x in foo() = ' + x); // 1
	    bar();
	}
这说明JavaScript的函数在查找变量时从自身函数定义开始，从“内”向“外”查找。如果内部函数定义了与外部函数重名的变量，则内部函数的变量将“屏蔽”外部函数的变量。

##变量提升

JavaScript的函数定义有个特点，它会先扫描整个函数体的语句，把所有申明的变量“提升”到函数顶部：

	'use strict';
	
	function foo() {
	    var x = 'Hello, ' + y;
	    alert(x);
	    var y = 'Bob';
	}
	
	foo();
虽然是strict模式，但语句var x = 'Hello, ' + y;并不报错，原因是变量y在稍后申明了。但是alert显示Hello, undefined，说明变量y的值为undefined。这正是因为JavaScript引擎自动提升了变量y的声明，但不会提升变量y的赋值。

对于上述foo()函数，JavaScript引擎看到的代码相当于：

	function foo() {
	    var y; // 提升变量y的申明
	    var x = 'Hello, ' + y;
	    alert(x);
	    y = 'Bob';
	}
由于JavaScript的这一怪异的“特性”，我们在函数内部定义变量时，请严格遵守“在函数内部首先申明所有变量”这一规则。最常见的做法是用一个var申明函数内部用到的所有变量：

	function foo() {
	    var
	        x = 1, // x初始化为1
	        y = x + 1, // y初始化为2
	        z, i; // z和i为undefined
	    // 其他语句:
	    for (i=0; i<100; i++) {
	        ...
	    }
	}
##全局作用域

不在任何函数内定义的变量就具有全局作用域。实际上，JavaScript默认有一个全局对象window，全局作用域的变量实际上被绑定到window的一个属性：

	'use strict';
	
	var course = 'Learn JavaScript';
	alert(course); // 'Learn JavaScript'
	alert(window.course); // 'Learn JavaScript'
因此，直接访问全局变量course和访问window.course是完全一样的。

你可能猜到了，由于函数定义有两种方式，以变量方式var foo = function () {}定义的函数实际上也是一个全局变量，因此，顶层函数的定义也被视为一个全局变量，并绑定到window对象：

	'use strict';
	
	function foo() {
	    alert('foo');
	}
	
	foo(); // 直接调用foo()
	window.foo(); // 通过window.foo()调用
进一步大胆地猜测，我们每次直接调用的alert()函数其实也是window的一个变量：

	'use strict';
	
	window.alert('调用window.alert()');
	// 把alert保存到另一个变量:
	var old_alert = window.alert;
	// 给alert赋一个新函数:
	window.alert = function () {}
	
	alert('无法用alert()显示了!');
	
	// 恢复alert:
	window.alert = old_alert;
	alert('又可以用alert()了!');

这说明JavaScript实际上只有一个全局作用域。任何变量（函数也视为变量），如果没有在当前函数作用域中找到，就会继续往上查找，最后如果在全局作用域中也没有找到，则报ReferenceError错误。

##名字空间

全局变量会绑定到window上，不同的JavaScript文件如果使用了相同的全局变量，或者定义了相同名字的顶层函数，都会造成命名冲突，并且很难被发现。

减少冲突的一个方法是把自己的所有变量和函数全部绑定到一个全局变量中。例如：

	// 唯一的全局变量MYAPP:
	var MYAPP = {};
	
	// 其他变量:
	MYAPP.name = 'myapp';
	MYAPP.version = 1.0;
	
	// 其他函数:
	MYAPP.foo = function () {
	    return 'foo';
	};
把自己的代码全部放入唯一的名字空间MYAPP中，会大大减少全局变量冲突的可能。

许多著名的JavaScript库都是这么干的：jQuery，YUI，underscore等等。

##局部作用域

由于JavaScript的变量作用域实际上是函数内部，我们在for循环等语句块中是无法定义具有局部作用域的变量的：

	'use strict';
	
	function foo() {
	    for (var i=0; i<100; i++) {
	        //
	    }
	    i += 100; // 仍然可以引用变量i
	}
为了解决块级作用域，ES6引入了新的关键字let，用let替代var可以申明一个块级作用域的变量：

	'use strict';
	
	function foo() {
	    var sum = 0;
	    for (let i=0; i<100; i++) {
	        sum += i;
	    }
	    i += 1; // SyntaxError
	}
##常量

由于var和let申明的是变量，如果要申明一个常量，在ES6之前是不行的，我们通常用全部大写的变量来表示“这是一个常量，不要修改它的值”：

	var PI = 3.14;
ES6标准引入了新的关键字const来定义常量，const与let都具有块级作用域：

	'use strict';
	
	const PI = 3.14;
	PI = 3; // 某些浏览器不报错，但是无效果！
	PI; // 3.14