#6-2 python中 `__str__`和`__repr__`
如果要把一个类的实例变成 str，就需要实现特殊方法`__str__()`：

	class Person(object):
	    def __init__(self, name, gender):
	        self.name = name
	        self.gender = gender
	    def __str__(self):
	        return '(Person: %s, %s)' % (self.name, self.gender)
现在，在交互式命令行下用 print 试试：

	>>> p = Person('Bob', 'male')
	>>> print p
	(Person: Bob, male)
但是，如果直接敲变量 p：

	>>> p
	<main.Person object at 0x10c941890>
似乎`__str__() `不会被调用。

因为 Python 定义了`__str__()`和`__repr__()`两种方法，`__str__()`用于显示给用户，而`__repr__()`用于显示给开发人员。

有一个偷懒的定义`__repr__`的方法：

	class Person(object):
	    def __init__(self, name, gender):
	        self.name = name
	        self.gender = gender
	    def __str__(self):
	        return '(Person: %s, %s)' % (self.name, self.gender)
	    __repr__ = __str__
##任务
请给Student 类定义`__str__`和`__repr__`方法，使得能打印出<Student: name, gender, score>：

	class Student(Person):
	    def __init__(self, name, gender, score):
	        super(Student, self).__init__(name, gender)
	        self.score = score
?不会了怎么办
只要为Students 类加上`__str__()`和`__repr__()`方法即可。

参考代码:

	class Person(object):
	    def __init__(self, name, gender):
	        self.name = name
	        self.gender = gender
	
	class Student(Person):
	    def __init__(self, name, gender, score):
	        super(Student, self).__init__(name, gender)
	        self.score = score
	    def __str__(self):
	        return '(Student: %s, %s, %s)' % (self.name, self.gender, self.score)
	    __repr__ = __str__
	
	s = Student('Bob', 'male', 88)
	print s