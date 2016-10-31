#3-4-2 filter

filter也是一个常用的操作，它用于把Array的某些元素过滤掉，然后返回剩下的元素。

和map()类似，Array的filter()也接收一个函数。和map()不同的是，filter()把传入的函数依次作用于每个元素，然后根据返回值是true还是false决定保留还是丢弃该元素。

例如，在一个Array中，删掉偶数，只保留奇数，可以这么写：

	var arr = [1, 2, 4, 5, 6, 9, 10, 15];
	var r = arr.filter(function (x) {
	    return x % 2 !== 0;
	});
	r; // [1, 5, 9, 15]
把一个Array中的空字符串删掉，可以这么写：

	var arr = ['A', '', 'B', null, undefined, 'C', '  '];
	var r = arr.filter(function (s) {
	    return s && s.trim(); // 注意：IE9以下的版本没有trim()方法
	});
	r; // ['A', 'B', 'C']
	可见用filter()这个高阶函数，关键在于正确实现一个“筛选”函数。

##练习

请尝试用filter()筛选出素数：

	'use strict';
	
	function get_primes(arr) {
	
	    return [];
	
	}
	
	// 测试:
	var
	    x,
	    r,
	    arr = [];
	for (x = 1; x < 100; x++) {
	    arr.push(x);
	}
	r = get_primes(arr);
	if (r.toString() === [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97].toString()) {
	    alert('测试通过!');
	} else {
	    alert('测试失败: ' + r.toString());
	}