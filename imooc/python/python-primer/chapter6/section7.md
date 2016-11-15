#6-7 Python之访问set
由于**set存储的是无序集合**，所以我们没法通过索引来访问。

访问 set中的某个元素实际上就是判断一个元素是否在set中。

例如，存储了班里同学名字的set：

	>>> s = set(['Adam', 'Lisa', 'Bart', 'Paul'])
我们可以用 in 操作符判断：

Bart是该班的同学吗？

	>>> 'Bart' in s
	True
Bill是该班的同学吗？

	>>> 'Bill' in s
	False
bart是该班的同学吗？

	>>> 'bart' in s
	False
看来大小写很重要，'Bart' 和 'bart'被认为是两个不同的元素。

##任务
由于上述set不能识别小写的名字，请改进set，使得 'adam' 和 'bart'都能返回True。

?不会了怎么办
在list中，需要把两个名字同时放进去。

参考代码:

	s = set(['Adam', 'adam', 'Lisa', 'lisa', 'Bart', 'bart', 'Paul', 'paul'])
	print 'adam' in s
	print 'bart' in s
