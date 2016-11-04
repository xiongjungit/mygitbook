#6-8 python中 `__slots__`
由于Python是动态语言，任何实例在运行期都可以动态地添加属性。

如果要限制添加的属性，例如，Student类只允许添加 name、gender和score 这3个属性，就可以利用Python的一个特殊的`__slots__`来实现。

顾名思义，`__slots__`是指一个类允许的属性列表：

	class Student(object):
	    __slots__ = ('name', 'gender', 'score')
	    def __init__(self, name, gender, score):
	        self.name = name
	        self.gender = gender
	        self.score = score
现在，对实例进行操作：

	>>> s = Student('Bob', 'male', 59)
	>>> s.name = 'Tim' # OK
	>>> s.score = 99 # OK
	>>> s.grade = 'A'
	Traceback (most recent call last):
	  ...
	AttributeError: 'Student' object has no attribute 'grade'
`__slots__`的目的是限制当前类所能拥有的属性，如果不需要添加任意动态的属性，使用`__slots__`也能节省内存。

##任务
假设Person类通过`__slots__`定义了name和gender，请在派生类Student中通过`__slots__`继续添加score的定义，使Student类可以实现name、gender和score 3个属性。

 

?不会了怎么办
Student类的`__slots__`只需要包含Person类不包含的score属性即可。

参考代码:

	class Person(object):
	    __slots__ = ('name', 'gender')
	    def __init__(self, name, gender):
	        self.name = name
	        self.gender = gender
	
	class Student(Person):
	    __slots__ = ('score',)
	    def __init__(self, name, gender, score):
	        super(Student, self).__init__(name, gender)
	        self.score = score
	
	s = Student('Bob', 'male', 59)
	s.name = 'Tim'
	s.score = 99
	print s.score