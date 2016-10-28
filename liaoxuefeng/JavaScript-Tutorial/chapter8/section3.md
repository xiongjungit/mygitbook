#8-3 Functions


因为underscore本来就是为了充分发挥JavaScript的函数式编程特性，所以也提供了大量JavaScript本身没有的高阶函数。

##bind

bind()有什么用？我们先看一个常见的错误用法：

	'use strict';
	
	console.log('Hello, world!');
	// 输出'Hello, world!'
	
	var log = console.log;
	log('Hello, world!');
	// Uncaught TypeError: Illegal invocation
如果你想用log()取代console.log()，按照上面的做法是不行的，因为直接调用log()传入的this指针是undefined，必须这么用：

	'use strict';
	
	var log = console.log;
	// 调用call并传入console对象作为this:
	log.call(console, 'Hello, world!')
	// 输出Hello, world!
这样搞多麻烦！还不如直接用console.log()。但是，bind()可以帮我们把console对象直接绑定在log()的this指针上，以后调用log()就可以直接正常调用了：

	'use strict';
	
	var log = _.bind(console.log, console);
	log('Hello, world!');
	// 输出Hello, world!
##partial

partial()就是为一个函数创建偏函数。偏函数是什么东东？看例子：

假设我们要计算xy，这时只需要调用Math.pow(x, y)就可以了。

假设我们经常计算2y，每次都写Math.pow(2, y)就比较麻烦，如果创建一个新的函数能直接这样写pow2N(y)就好了，这个新函数pow2N(y)就是根据Math.pow(x, y)创建出来的偏函数，它固定住了原函数的第一个参数（始终为2）：

	'use strict';
	
	var pow2N = _.partial(Math.pow, 2);
	pow2N(3); // 8
	pow2N(5); // 32
	pow2N(10); // 1024
如果我们不想固定第一个参数，想固定第二个参数怎么办？比如，希望创建一个偏函数cube(x)，计算x3，可以用_作占位符，固定住第二个参数：

	'use strict';
	
	var cube = _.partial(Math.pow, _, 3);
	cube(3); // 27
	cube(5); // 125
	cube(10); // 1000
可见，创建偏函数的目的是将原函数的某些参数固定住，可以降低新函数调用的难度。

##memoize

如果一个函数调用开销很大，我们就可能希望能把结果缓存下来，以便后续调用时直接获得结果。举个例子，计算阶乘就比较耗时：

	'use strict';
	
	function factorial(n) {
	    console.log('start calculate ' + n + '!...');
	    var s = 1, i = n;
	    while (i > 1) {
	        s = s * i;
	        i --;
	    }
	    console.log(n + '! = ' + s);
	    return s;
	}
	
	factorial(10); // 3628800
	// 注意控制台输出:
	// start calculate 10!...
	// 10! = 3628800
用memoize()就可以自动缓存函数计算的结果：

	'use strict';
	
	var factorial = _.memoize(function(n) {
	    console.log('start calculate ' + n + '!...');
	    var s = 1, i = n;
	    while (i > 1) {
	        s = s * i;
	        i --;
	    }
	    console.log(n + '! = ' + s);
	    return s;
	});
	
	// 第一次调用:
	factorial(10); // 3628800
	// 注意控制台输出:
	// start calculate 10!...
	// 10! = 3628800
	
	// 第二次调用:
	factorial(10); // 3628800
	// 控制台没有输出
对于相同的调用，比如连续两次调用factorial(10)，第二次调用并没有计算，而是直接返回上次计算后缓存的结果。不过，当你计算factorial(9)的时候，仍然会重新计算。

可以对factorial()进行改进，让其递归调用：

	'use strict';
	
	var factorial = _.memoize(function(n) {
	    console.log('start calculate ' + n + '!...');
	    if (n < 2) {
	        return 1;
	    }
	    return n * factorial(n - 1);
	});
	
	factorial(10); // 3628800
	// 输出结果说明factorial(1)~factorial(10)都已经缓存了:
	// start calculate 10!...
	// start calculate 9!...
	// start calculate 8!...
	// start calculate 7!...
	// start calculate 6!...
	// start calculate 5!...
	// start calculate 4!...
	// start calculate 3!...
	// start calculate 2!...
	// start calculate 1!...
	
	factorial(9); // 362880
	// console无输出
##once

顾名思义，once()保证某个函数执行且仅执行一次。如果你有一个方法叫register()，用户在页面上点两个按钮的任何一个都可以执行的话，就可以用once()保证函数仅调用一次，无论用户点击多少次：

	'use strict';
	
	var register = _.once(function () {
	    alert('Register ok!');
	});
	
	// 测试效果:
	register();
	register();
	register();

##delay

delay()可以让一个函数延迟执行，效果和setTimeout()是一样的，但是代码明显简单了：

	'use strict';
	
	// 2秒后调用alert():
	_.delay(alert, 2000);
如果要延迟调用的函数有参数，把参数也传进去：

	'use strict';
	
	var log = _.bind(console.log, console);
	_.delay(log, 2000, 'Hello,', 'world!');
	// 2秒后打印'Hello, world!':
更多完整的函数请参考underscore的文档：http://underscorejs.org/#functions