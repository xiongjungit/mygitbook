#3-4-1 map/reduce

如果你读过Google的那篇大名鼎鼎的论文“MapReduce: Simplified Data Processing on Large Clusters”，你就能大概明白map/reduce的概念。

##smap

举例说明，比如我们有一个函数f(x)=x2，要把这个函数作用在一个数组[1, 2, 3, 4, 5, 6, 7, 8, 9]上，就可以用map实现如下：

![map](../image/chapter3/3-4-1-1.jpg)

由于map()方法定义在JavaScript的Array中，我们调用Array的map()方法，传入我们自己的函数，就得到了一个新的Array作为结果：

	function pow(x) {
	    return x * x;
	}
	
	var arr = [1, 2, 3, 4, 5, 6, 7, 8, 9];
	arr.map(pow); // [1, 4, 9, 16, 25, 36, 49, 64, 81]
map()传入的参数是pow，即函数对象本身。

你可能会想，不需要map()，写一个循环，也可以计算出结果：

	var f = function (x) {
	    return x * x;
	};
	
	var arr = [1, 2, 3, 4, 5, 6, 7, 8, 9];
	var result = [];
	for (var i=0; i<arr.length; i++) {
	    result.push(f(arr[i]));
	}
的确可以，但是，从上面的循环代码，我们无法一眼看明白“把f(x)作用在Array的每一个元素并把结果生成一个新的Array”。

所以，map()作为高阶函数，事实上它把运算规则抽象了，因此，我们不但可以计算简单的f(x)=x2，还可以计算任意复杂的函数，比如，把Array的所有数字转为字符串：

	var arr = [1, 2, 3, 4, 5, 6, 7, 8, 9];
	arr.map(String); // ['1', '2', '3', '4', '5', '6', '7', '8', '9']
只需要一行代码。

##reduce

再看reduce的用法。Array的reduce()把一个函数作用在这个Array的[x1, x2, x3...]上，这个函数必须接收两个参数，reduce()把结果继续和序列的下一个元素做累积计算，其效果就是：

	[x1, x2, x3, x4].reduce(f) = f(f(f(x1, x2), x3), x4)
比方说对一个Array求和，就可以用reduce实现：

	var arr = [1, 3, 5, 7, 9];
	arr.reduce(function (x, y) {
	    return x + y;
	}); // 25
练习：利用reduce()求积：

	'use strict';
	
	function product(arr) {
	
	    return 0;
	
	}
	
	// 测试:
	if (product([1, 2, 3, 4]) === 24 && product([0, 1, 2]) === 0 && product([99, 88, 77, 66]) === 44274384) {
	    alert('测试通过!');
	}
	else {
	    alert('测试失败!');
	}


要把[1, 3, 5, 7, 9]变换成整数13579，reduce()也能派上用场：

	var arr = [1, 3, 5, 7, 9];
	arr.reduce(function (x, y) {
	    return x * 10 + y;
	}); // 13579
如果我们继续改进这个例子，想办法把一个字符串13579先变成Array——[1, 3, 5, 7, 9]，再利用reduce()就可以写出一个把字符串转换为Number的函数。

练习：不要使用JavaScript内置的parseInt()函数，利用map和reduce操作实现一个string2int()函数：

	'use strict';
	
	function string2int(s) {
	
	    return 0;
	
	}
	
	// 测试:
	if (string2int('0') === 0 && string2int('12345') === 12345 && string2int('12300') === 12300) {
	    if (string2int.toString().indexOf('parseInt') !== -1) {
	        alert('请勿使用parseInt()!');
	    } else if (string2int.toString().indexOf('Number') !== -1) {
	        alert('请勿使用Number()!');
	    } else {
	        alert('测试通过!');
	    }
	}
	else {
	    alert('测试失败!');
	}

##练习

请把用户输入的不规范的英文名字，变为首字母大写，其他小写的规范名字。输入：['adam', 'LISA', 'barT']，输出：['Adam', 'Lisa', 'Bart']。

	'use strict';
	
	function normalize(arr) {
	
	    return [];
	
	}
	
	// 测试:
	if (normalize(['adam', 'LISA', 'barT']).toString() === ['Adam', 'Lisa', 'Bart'].toString()) {
	    alert('测试通过!');
	}
	else {
	    alert('测试失败!');
	}

小明希望利用map()把字符串变成整数，他写的代码很简洁：

	'use strict';
	
	var arr = ['1', '2', '3'];
	var r;
	
	r = arr.map(parseInt);
	
	alert('[' + r[0] + ', ' + r[1] + ', ' + r[2] + ']');

结果竟然是[1, NaN, NaN]，小明百思不得其解，请帮他找到原因并修正代码。