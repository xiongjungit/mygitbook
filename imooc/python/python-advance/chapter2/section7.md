#2-7 python中自定义排序函数
Python内置的 sorted()函数可对list进行排序：

	>>>sorted([36, 5, 12, 9, 21])
	
	[5, 9, 12, 21, 36]
但 sorted()也是一个高阶函数，它可以接收一个比较函数来实现自定义排序，比较函数的定义是，传入两个待比较的元素 x, y，如果 x 应该排在 y 的前面，返回 -1，如果 x 应该排在 y 的后面，返回 1。如果 x 和 y 相等，返回 0。

因此，如果我们要实现倒序排序，只需要编写一个reversed_cmp函数：

	def reversed_cmp(x, y):
	    if x > y:
	        return -1
	    if x < y:
	        return 1
	    return 0
这样，调用 sorted() 并传入 reversed_cmp 就可以实现倒序排序：

	>>> sorted([36, 5, 12, 9, 21], reversed_cmp)
	[36, 21, 12, 9, 5]
sorted()也可以对字符串进行排序，字符串默认按照ASCII大小来比较：

	>>> sorted(['bob', 'about', 'Zoo', 'Credit'])
	['Credit', 'Zoo', 'about', 'bob']
'Zoo'排在'about'之前是因为'Z'的ASCII码比'a'小。

##任务
对字符串排序时，有时候忽略大小写排序更符合习惯。请利用sorted()高阶函数，实现忽略大小写排序的算法。

输入：['bob', 'about', 'Zoo', 'Credit']
输出：['about', 'bob', 'Credit', 'Zoo']

?不会了怎么办
对于比较函数cmp_ignore_case(s1, s2)，要忽略大小写比较，就是先把两个字符串都变成大写（或者都变成小写），再比较。

参考代码:

	def cmp_ignore_case(s1, s2):
	    u1 = s1.upper()
	    u2 = s2.upper()
	    if u1 < u2:
	        return -1
	    if u1 > u2:
	        return 1
	    return 0
	print sorted(['bob', 'about', 'Zoo', 'Credit'], cmp_ignore_case)