#6-5 Python之 遍历dict
由于dict也是一个集合，所以，遍历dict和遍历list类似，都可以通过 for 循环实现。

直接使用for循环可以遍历 dict 的 key：

	>>> d = { 'Adam': 95, 'Lisa': 85, 'Bart': 59 }
	>>> for key in d:
	...     print key
	... 
	Lisa
	Adam
	Bart
由于通过 key 可以获取对应的 value，因此，在循环体内，可以获取到value的值。

##s任务
请用 for 循环遍历如下的dict，打印出 name: score 来。

	d = {
	    'Adam': 95,
	    'Lisa': 85,
	    'Bart': 59
	}
?不会了怎么办
通过d[key]获取对应的value。

参考代码:

	d= {
	    'Adam': 95,
	    'Lisa': 85,
	    'Bart': 59
	}
	for key in d:
	    print key + ':', d[key]