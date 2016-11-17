# -*- coding: utf-8 -*-

# 慕课网python进阶所有代码
print u'慕课网python进阶所有代码'

# 第1章 课程介绍
#python基础回顾
"""
安装python环境
变量和数据类型：python内置的基本类型
list和tuple：顺序的集合类型
条件判断和循环：控制程序流程
dict和set：根据key访问的集合类型
函数：定义和调用函数
切片：如何对list进行切片
迭代：如何用for循环迭代集合类型
列表生成式：如何快速的生成列表
"""

#本课程将要学习的内容
"""
函数式编程：注意，不是函数编程
模块：如何使用模块
面向对象编程：面向对象的概念、属性、方法、继承、多态等
定制类：利用python的特殊方法定制类
"""

#学习目标
"""
掌握函数式编程
掌握面向对象编程
能够编写模块化的程序
"""


# 第2章 函数式编程

## 2-1 python中函数式编程简介
#什么是函数式编程
#函数:function,在入门课程已学习
#函数式:functional,一种编程规范

#函数式编程的特点
"""
把计算机视为函数而非指令
纯函数式编程：不需要变量，没有副作用，测试简单
支持高级函数，代码简洁
"""

#python支持的函数式编程
"""
不是纯函数式编程：允许有变量
支持高阶函数：函数也可以作为变量传入
支持闭包：有了闭包就能返回函数
有限度的支持匿名函数
"""

# 2-2 python中高阶函数

"""
变量可以指向函数
函数名其实就是指向函数的变量
高阶函数：能接收函数做函数的函数
    变量可以指向函数
    函数的参数可以接收变量
    一个函数可以接收另一个函数作为参数
    能接收函数作为参数的函数就是高阶函数
"""

'''
def add(x,y,s):
    return s(x)+s(y)
print add(-4,5,abs)
'''

## 2-3 python把函数作为参数
#根据函数的定义，函数执行的代码实际上是
'''
abs(-5) + abs(9)
'''


# 计算平方根可以用函数math.sqrt()

'''
import math
def add(x, y, f):
    return f(x) + f(y)
print add(25, 9, math.sqrt)
'''

## 2-4 python中map()函数
#map()是 Python 内置的高阶函数，它接收一个函数 f 和一个 list，并通过把函数 f 依次作用在 list 的每个元素上，得到一个新的 list 并返回

'''
def f(x):
    return x*x
print map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])
'''

#upper()函数把小写转换为大写
#lower()函数把大写转换为小写

'''
def format_name(s):
    return s[0].upper() + s[1:].lower()
print map(format_name, ['adam', 'LISA', 'barT'])
'''


## 2-5 python中reduce()函数
#reduce()函数也是Python内置的一个高阶函数。reduce()函数接收的参数和 map()类似，一个函数 f，一个list，但行为和 map()不同，reduce()传入的函数 f 必须接收两个参数，reduce()对list的每个元素反复调用函数f，并返回最终结果值。

#利用recude()来求积
'''
def prod(x, y):
    return x * y
print reduce(prod, [2, 4, 5, 7, 12])
'''

## 2-6 python中filter()函数
#filter()函数是 Python 内置的另一个有用的高阶函数，filter()函数接收一个函数 f 和一个list，这个函数 f 的作用是对每个元素进行判断，返回 True或 False，filter()根据判断结果自动过滤掉不符合条件的元素，返回由符合条件元素组成的新list

#删除偶数，保留基数

'''
def is_odd(x):
    return x % 2 == 1
print filter(is_odd, [1, 4, 6, 7, 9, 12, 17])
'''


#删除None和空字符串

'''
def is_not_empty(s):
    return s and len(s.strip()) > 0
print filter(is_not_empty, ['test', None, '', 'str', '  ', 'END'])
'''

#s.strip(rm) 删除 s 字符串中开头、结尾处的 rm 序列的字符
#当rm为空时，默认删除空白符（包括'\n', '\r', '\t', ' ')

'''
a = '     123'
print a.strip()
a='\t\t123\r\n'
print a.strip()
'''

#利用filter()过滤出1~100中平方根是整数的数
#math.sqrt()返回结果是浮点数
#int()函数转换为整数
'''
import math
def is_sqr(x):
    r = int(math.sqrt(x))
    return r*r==x
print filter(is_sqr, range(1, 101))
'''

## 2-7 python中自定义排序函数
#Python内置的 sorted()函数可对list进行排序
#sorted()也是一个高阶函数，它可以接收一个比较函数来实现自定义排序，比较函数的定义是，传入两个待比较的元素 x, y，如果 x 应该排在 y 的前面，返回 -1，如果 x 应该排在 y 的后面，返回 1。如果 x 和 y 相等，返回 0
#sorted()也可以对字符串进行排序，字符串默认按照ASCII大小来比较

#利用sorted()高阶函数，实现忽略大小写排序的算法
#输入：['bob', 'about', 'Zoo', 'Credit'] 输出：['about', 'bob', 'Credit', 'Zoo']

'''
def cmp_ignore_case(s1, s2):
    u1 = s1.upper()
    u2 = s2.upper()
    if u1 < u2:
        return -1
    if u1 > u2:
        return 1
    return 0
print sorted(['bob', 'about', 'Zoo', 'Credit'], cmp_ignore_case)
'''

## 2-8 python中返回函数
#Python的函数不但可以返回int、str、list、dict等数据类型，还可以返回函数

#编写一个函数calc_prod(lst)，它接收一个list，返回一个函数，返回函数可以计算参数的乘积
'''
def calc_prod(lst):
    def lazy_prod():
        def f(x, y):
            return x * y
        return reduce(f, lst, 1)
    return lazy_prod
f = calc_prod([1, 2, 3, 4])
print f()
'''

# 2-9 python中闭包
#在函数内部定义的函数和外部定义的函数是一样的，只是他们无法被外部访问
#内层函数引用了外层函数的变量（参数也算变量），然后返回内层函数的情况，称为闭包
#闭包的特点是返回的函数还引用了外层函数的局部变量，所以，要正确使用闭包，就要确保引用的局部变量在函数返回后不能变。

#编写count()函数，让它正确返回能计算1x1、2x2、3x3的函数
'''
def count():
    fs = []
    for i in range(1, 4):
        def f(j):
            def g():
                return j*j
            return g
        r = f(i)
        fs.append(r)
    return fs
f1, f2, f3 = count()
print f1(), f2(), f3()
'''

## 2-10 python中匿名函数

"""
print map(lambda x: x * x, [1, 2, 3, 4, 5, 6, 7, 8, 9])
关键字lambda 表示匿名函数，冒号前面的 x 表示函数参数
匿名函数 lambda x: x * x 实际上就是

def f(x):
    return x * x
"""

#利用匿名函数简化以下代码：

'''
def is_not_empty(s):
    return s and len(s.strip()) > 0
print filter(is_not_empty, ['test', None, '', 'str', '  ', 'END'])
'''
#定义匿名函数时，没有return关键字，且表达式的值就是函数返回值。

'''
print filter(lambda s: s and len(s.strip())>0, ['test', None, '', 'str', '  ', 'END'])
'''


## 2-11 python中decorator装饰器
#什么是装饰器@decotator
"""
定义了一个函数
想在运行时动态增加功能
又不想改动函数本身的代码
"""

"""
高阶函数
    可以接收函数作为参数
    可以返回函数
    可以接收一个函数，对其包装，然后返回一个新函数
"""

'''
def f1(x):
    return x*2
def new_fn(f): #装饰器函数
    def fn(x):
        print '调用' + ' ' + f.__name__ + '()' + ' ' +'函数'
        return f(x)
    return fn
f1 = new_fn(f1)
print f1(5)
'''

#python内置的@语法就是为了简化装饰器的调用

"""
装饰器的作用
    可以极大的简化代码
        打印日志：@log
        检测性能：@performance
        数据库事务：@transaction
        URL路由：@post('/register')
"""

## 2-12 python中编写无参数decorator
#使用 decorator 用Python提供的 @ 语法，这样可以避免手动编写 f = decorate(f) 这样的代码

'''
def log(f):
    def fn(x):
        print '调用' + ' ' + f.__name__ + '()' + ' ' +'函数'
        return f(x)
    return fn
@log #装饰器
def factorial(n):
    return reduce(lambda x,y: x*y, range(1, n+1))
print factorial(10)
#对于参数不是一个的函数，调用将报错
#add() 函数需要传入两个参数，但是 @log 写死了只含一个参数的返回函数
@log #装饰器
def add(x, y):
    return x + y
print add(1, 2)
'''

#要让 @log 自适应任何参数定义的函数，可以利用Python的 args 和 *kw，保证任意个数的参数总是能正常调用

'''
def log(f):
    def fn(*args, **kw):
        print '调用' + ' ' + f.__name__ + '()' + ' ' +'函数'
        return f(*args, **kw)
    return fn
@log #装饰器
def factorial(n):
    return reduce(lambda x,y: x*y, range(1, n+1))
print factorial(10)
@log #装饰器
def add(x, y):
    return x + y
print add(1, 2)
'''


#编写一个@performance，它可以打印出函数调用的时间
#计算函数调用的时间可以记录调用前后的当前时间戳，然后计算两个时间戳的差

'''
import time
def performance(f):
    def fn(*args, **kw):
        t1 = time.time()
        r = f(*args, **kw)
        t2 = time.time()
        print '调用函数 %s() 时间是 %fs' % (f.__name__, (t2 - t1))
        return r
    return fn

@performance
def factorial(n):
    return reduce(lambda x,y: x*y, range(1, n+1))
print factorial(10)
'''


## 2-13 python中编写带参数decorator
#上一节的@performance只能打印秒，请给 @performace 增加一个参数，允许传入's'或'ms'
#要实现带参数的@performance，就需要实现my_func = performance('ms')(my_func),需要3层嵌套的decorator来实现

'''
import time
def performance(unit):
    def perf_decorator(f):
        def wrapper(*args, **kw):
            t1 = time.time()
            r = f(*args, **kw)
            t2 = time.time()
            t = (t2 - t1) * 1000 if unit=='ms' else (t2 - t1)
            print '调用函数 %s() 时间是 %f %s' % (f.__name__, t, unit)
            return r
        return wrapper
    return perf_decorator

@performance('毫秒')
def factorial(n):
    return reduce(lambda x,y: x*y, range(1, n+1))
print factorial(10)
'''

## 2-14 python中完善decorator
#Python内置的functools可以用来自动化完成把原函数的所有必要属性都一个一个复制到新函数上

'''
import functools
def log(f):
    @functools.wraps(f)
    def wrapper(*args, **kw):
        print 'call...'
        return f(*args, **kw)
    return wrapper
@log
def f2(x):
    pass
print f2.__name__
'''

#带参数的@decorator，@functools.wraps应该放置在哪
#@functools.wraps应该作用在返回的新函数上
'''
import time, functools
def performance(unit):
    def perf_decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kw):
            t1 = time.time()
            r = f(*args, **kw)
            t2 = time.time()
            t = (t2 - t1) * 1000 if unit=='ms' else (t2 - t1)
            print '调用函数 %s() 时间是 %f %s' % (f.__name__, t, unit)
            return r
        return wrapper
    return perf_decorator

@performance('毫秒')
def factorial(n):
    return reduce(lambda x,y: x*y, range(1, n+1))
print factorial.__name__
print factorial(3)
'''

##2-15 python中偏函数
#定义一个int2()的函数，默认把base=2传进去

'''
def int2(x, base=2):
    return int(x, base)
print int2('11111111')
'''

#functools.partial就是帮助我们创建一个偏函数的，不需要我们自己定义int2()，可以直接使用下面的代码创建一个新的函数int2

'''
import functools
int2 = functools.partial(int,base=2)
print int2('11111111')
'''

#functools.partial可以把一个参数多的函数变成一个参数少的新函数，少的参数需要在创建时指定默认值
#functools.partial实现忽略大小写排序

'''
import functools
sorted_ignore_case = functools.partial(sorted, cmp=lambda s1, s2: cmp(s1.upper(), s2.upper()))
print sorted_ignore_case(['bob', 'about', 'Zoo', 'Credit'])
'''

# 第三章 模块
# 3-1 python中模块和包的概念
#包就是文件夹,可以有多级,模块就是py文件
#包下面有个__init__.py,每层都必须有

# 3-2 python之导入模块
#要使用一个模块，我们必须首先导入该模块。Python使用import语句导入一个模块
#你可以认为math就是一个指向已导入模块的变量，通过该变量，我们可以访问math模块中所定义的所有公开的函数、变量和类

'''
import math
print math.pow(2, 0.5) # pow是函数
print math.pi # pi是变量
'''

#如果我们只希望导入用到的math模块的某几个函数，而不是所有函数，可以用下面的语句

'''
from math import pow, sin, log
print pow(2, 10)
print sin(3.14)
print int(log(8))
'''



#如果使用import导入模块名，由于必须通过模块名引用函数名，因此不存在冲突
'''
import math, logging
print math.log(10)   # 调用的是math的log函数
print logging.log(10, 'something')   # 调用的是logging的log函数
'''

#如果使用 from...import 导入 log 函数，势必引起冲突。这时，可以给函数起个“别名”来避免冲突

'''
from math import log
from logging import log as logger   # logging的log现在变成了logger
print log(10)   # 调用的是math的log
print logger(10, 'import from logging')   # 调用的是logging的log
'''


#Python的os.path模块提供了 isdir() 和 isfile()函数，请导入该模块，并调用函数判断指定的目录和文件是否存在。

'''
import os
print os.path.isdir(r'C:\Windows')
print os.path.isfile(r'C:\Windows\notepad.exe')
print os.path.isfile(r'C:\Windows\word.exe')
'''

## 3-3 python中动态导入模块

#如果导入的模块不存在，Python解释器会报 ImportError 错误
#利用ImportError错误，我们经常在Python中动态导入模块

'''
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
'''

#try 的作用是捕获错误，并在捕获到指定错误时执行 except 语句

#先尝试导入json，如果失败，再尝试导入simplejson as json

'''
try:
    import json
except ImportError:
    import simplejson as json
print json.dumps({'python':2.7})
'''

## 3-4 python之使用__future__
#要“试用”某一新的特性，就可以通过导入__future__模块的某些功能来实现
#使用from __future__ import unicode_literals将把Python 3.x的unicode规则带入Python 2.7中
'''
from __future__ import unicode_literals
s = 'am I an unicode?'
print isinstance(s, unicode)
'''


## 3-5 python之安装第三方模块
"""
python提供的模块管理工具
    easy_install
    pip #推荐，已内置到python 2.7.9
"""

#第4章 面向对象编程基础
#本章讲解Python面向对象编程的概念，如何创建类和实例，如何定义类的属性和方法。

## 4-1 python之面向对象编程

"""
什么是面向对象编程
    面向对象编程是一种程序设计范式
    吧程序看做不同对象的相互调用
    对现实世界建立对象模型
面向对象编程的基本思想
    类和实例
        类用于定义抽象类型
        实例根据类的定义被创建出来
    数据封装
"""

'''
class Person: #类
    pass
xiaoming = Person() #实例
xiaojun = Person() #实例
'''


#数据封装
'''
class Person:
    def __init__(self, name):
        self.name = name

p1 = Person('xiaoming')
p2 = Person('xiaojun')
'''


## 4-2 python之定义类并创建实例
#在Python中，类通过 class 关键字定义。以 Person 为例，定义一个Person类如下
#按照 Python 的编程习惯，类名以大写字母开头，紧接着是(object),表示该类是从哪个类继承下来的

'''
class Person(object):
    pass
'''

#有了Person类的定义，就可以创建出具体的xiaoming、xiaohong等实例。创建实例使用 类名+()，类似函数调用的形式创建

'''
xiaoming = Person()
xiaohong = Person()
'''


#定义Person类，并创建出两个实例，打印实例，再比较两个实例是否相等
'''
class Person(object):
    pass
xiaoming = Person()
xiaohong = Person()
print xiaoming
print xiaohong
print xiaoming == xiaohong
'''

## 4-3 python中创建实例属性
#Python是动态语言，对每一个实例，都可以直接给他们的属性赋值，例如，给xiaoming这个实例加上name、gender和birth属性
'''
xiaoming = Person()
xiaoming.name = 'Xiao Ming'
xiaoming.gender = 'Male'
xiaoming.birth = '1990-1-1'
'''

#实例的属性可以像普通变量一样进行操作：
'''
xiaohong.grade = xiaohong.grade + 1
'''

#创建包含两个 Person 类的实例的 list，并给两个实例的 name 赋值，然后按照 name 进行排序

'''
class Person(object):
    pass
p1 = Person()
p1.name = 'Bart'

p2 = Person()
p2.name = 'Adam'

p3 = Person()
p3.name = 'Lisa'

L1 = [p1, p2, p3]
L2 = sorted(L1, lambda p1, p2: cmp(p1.name, p2.name))

print L2[0].name
print L2[1].name
print L2[2].name
'''

## 4-4 python中初始化实例属性
#在定义 Person 类时，可以为Person类添加一个特殊的__init__()方法，当创建实例时，__init__()方法被自动调用，我们就能在此为每个实例都统一加上以下属性

'''
class Person(object):
    def __init__(self, name, gender, birth):
        self.name = name
        self.gender = gender
        self.birth = birth

xiaoming = Person('Xiao Ming', 'Male', '1991-1-1')
xiaohong = Person('Xiao Hong', 'Female', '1992-2-2')

#有了__init__()方法，每个Person实例在创建时，都会有 name、gender 和 birth 这3个属性，并且，被赋予不同的属性值，访问属性使用.操作符
print xiaoming.name
print xiaohong.birth
'''


#定义Person类的__init__方法，除了接受 name、gender 和 birth 外，还可接受任意关键字参数，并把他们都作为属性赋值给实例
#要定义关键字参数，使用 **kw
#除了可以直接使用self.name = 'xxx'设置一个属性外，还可以通过 setattr(self, 'name', 'xxx') 设置属性

'''
class Person(object):
    def __init__(self, name, gender, birth, **kw):
        self.name = name
        self.gender = gender
        self.birth = birth
        for k, v in kw.iteritems():
            setattr(self, k, v)
xiaoming = Person('Xiao Ming', 'Male', '1990-1-1', job='Student')
print xiaoming.name
print xiaoming.job
'''

## 4-5 python中访问限制
#Python对属性权限的控制是通过属性名来实现的，如果一个属性由双下划线开头(__)，该属性就无法被外部访问
#如果一个属性以"__xxx__"的形式定义，那它又可以被外部访问了，以"__xxx__"定义的属性在Python的类中被称为特殊属性，有很多预定义的特殊属性可以使用，通常我们不要把普通属性用"__xxx__"定义

#给Person类的__init__方法中添加name和score参数，并把score绑定到__score属性上，看看外部是否能访问到

'''
class Person(object):
    def __init__(self, name, score):
        self.name = name
        self.__score = score

p = Person('Bob', 59)

print p.name
print p.__score
'''

## 4-6 python中创建类属性
#类是模板，而实例则是根据类创建的对象。
#绑定在一个实例上的属性不会影响其他实例，但是，类本身也是一个对象，如果在类上绑定一个属性，则所有实例都可以访问类的属性，并且，所有实例访问的类属性都是同一个

#定义类属性可以直接在 class 中定义：


'''
class Person(object):
    address = 'Earth'
    def __init__(self, name):
        self.name = name

print Person.address
p1 = Person('Bob')
p2 = Person('Alice')

print p1.name,p1.address
print p2.name,p2.address

Person.address = 'China'

print p1.name,p1.address
print p2.name,p2.address
'''

#给 Person 类添加一个类属性 count，每创建一个实例，count 属性就加 1，这样就可以统计出一共创建了多少个 Person 的实例
#由于创建实例必定会调用__init__()方法，所以在这里修改类属性 count 很合适

'''
class Person(object):
    count = 0
    def __init__(self, name):
        Person.count = Person.count + 1
        self.name = name
p1 = Person('Bob')
print Person.count
p2 = Person('Alice')
print Person.count
p3 = Person('Tim')
print Person.count
'''

## 4-7 python中类属性和实例属性名字冲突怎么办
#当实例属性和类属性重名时，实例属性优先级高，它将屏蔽掉对类属性的访问

#把上节的 Person 类属性 count 改为 __count，再试试能否从实例和类访问该属性

'''
class Person(object):
    __count = 0
    def __init__(self, name):
        Person.__count = Person.__count + 1
        self.name = name
        print Person.__count

p1 = Person('Bob')
p2 = Person('Alice')

print Person.__count
'''

## 4-8 python中定义实例方法
#一个实例的私有属性就是以__开头的属性，无法被外部访问
#实例的方法就是在类中定义的函数，它的第一个参数永远是 self，指向调用该方法的实例本身，其他参数和一个普通函数是完全一样的

#给 Person 类增加一个私有属性 __score，表示分数，再增加一个实例方法 get_grade()，能根据 __score 的值分别返回 A-优秀, B-及格, C-不及格三档


'''
class Person(object):

    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def get_grade(self):
        if self.__score >= 80:
            return 'A-优秀'
        if self.__score >= 60:
            return 'B-及格'
        return 'C-不及格'

p1 = Person('Bob', 90)
p2 = Person('Alice', 65)
p3 = Person('Tim', 48)

print p1.get_grade()
print p2.get_grade()
print p3.get_grade()
'''


## 4-9 python中方法也是属性
#我们在 class 中定义的实例方法其实也是属性，它实际上是一个函数对象

#属性可以是普通的值对象，如 str，int 等，也可以是方法，还可以是函数

'''
class Person(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score
        self.get_grade = lambda: 'A'

p1 = Person('Bob', 90)
print p1.get_grade
print p1.get_grade()
'''

#直接把 lambda 函数赋值给 self.get_grade 和绑定方法有所不同，函数调用不需要传入 self，但是方法调用需要传入 self

## 4-10 python中定义类方法
#和属性类似，方法也分实例方法和类方法
#在class中定义的全部是实例方法，实例方法第一个参数 self 是实例本身
#要在class中定义类方法，需要这么写

'''
class Person(object):
    count = 0
    @classmethod
    def how_many(cls):
        return cls.count
    def __init__(self, name):
        self.name = name
        Person.count = Person.count + 1

print Person.how_many()
p1 = Person('Bob')
print Person.how_many()
'''

#通过标记一个 @classmethod，该方法将绑定到 Person 类上，而非类的实例。类方法的第一个参数将传入类本身，通常将参数名命名为 cls，上面的 cls.count 实际上相当于 Person.count

#如果将类属性 count 改为私有属性__count，则外部无法读取__score，但可以通过一个类方法获取，请编写类方法获得__count值

'''
class Person(object):
    __count = 0
    @classmethod
    def how_many(cls):
        return cls.__count
    def __init__(self, name):
        self.name = name
        Person.__count = Person.__count + 1

print Person.how_many()
p1 = Person('Bob')
print Person.how_many()
'''

#第5章 类的继承
#本章讲解Python类的继承，如何判断实例类型，多态以及如何获取对象信息

## 5-1 python中什么是继承(mp4)
"""
print u'''什么是继承
    新类不必从头编写
    新类从现有的类继承，就自动拥有了现有类的所有功能
    新类只需要编写现有类缺少的新功能
继承的好处
    复用已有代码
    自动拥有了现有类的所有功能
    只需要编写缺少的新功能
父类和子类
    父类，基类，超类
    子类，派生类，继承类
继承树
继承的特点
    子类和父类是is关系
错误的继承
    Student类和Book类是has关系
    has关系应该使用组合而非继承
python的继承
    总是从某个类继承
    不要忘记调用super().__init__
"""

## 5-2 python中继承一个类

"""
如果已经定义了Person类，需要定义新的Student和Teacher类时，可以直接从Person类继承：

class Person(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
定义Student类时，只需要把额外的属性加上，例如score：

class Student(Person):
    def __init__(self, name, gender, score):
        super(Student, self).__init__(name, gender)
        self.score = score
一定要用 super(Student, self).init(name, gender) 去初始化父类，否则，继承自 Person 的 Student 将没有 name 和 gender。

函数super(Student, self)将返回当前类继承的父类，即 Person ，然后调用__init__()方法，注意self参数已在super()中传入，在__init__()中将隐式传递，不需要写出（也不能写）。
"""

#参考 Student 类，编写一个 Teacher类，也继承自 Person

'''
class Person(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
class Teacher(Person):
    def __init__(self, name, gender, course):
        super(Teacher, self).__init__(name, gender)
        self.course = course

t = Teacher('Alice', 'Female', 'English')
print t.name
print t.course
'''

## 5-3 python中判断类型
#函数isinstance()可以判断一个变量的类型，既可以用在Python内置的数据类型如str、list、dict，也可以用在我们自定义的类，它们本质上都是数据类型
#在继承链上，一个父类的实例不能是子类类型，因为子类比父类多了一些属性和方法


'''
class Person(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

class Student(Person):
    def __init__(self, name, gender, score):
        super(Student, self).__init__(name, gender)
        self.score = score

class Teacher(Person):
    def __init__(self, name, gender, course):
        super(Teacher, self).__init__(name, gender)
        self.course = course

t = Teacher('Alice', 'Female', 'English')

print isinstance(t, Person)
print isinstance(t, Student)
print isinstance(t, Teacher)
print isinstance(t, object)
'''

## 5-4 python中多态

'''
class Person(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
    def whoAmI(self):
        return 'I am a Person, my name is %s' % self.name

class Student(Person):
    def __init__(self, name, gender, score):
        super(Student, self).__init__(name, gender)
        self.score = score
    def whoAmI(self):
        return 'I am a Student, my name is %s' % self.name

class Teacher(Person):
    def __init__(self, name, gender, course):
        super(Teacher, self).__init__(name, gender)
        self.course = course
    def whoAmI(self):
        return 'I am a Teacher, my name is %s' % self.name

def who_am_i(x):
    print x.whoAmI()

p = Person('Tim', 'Male')
s = Student('Bob', 'Male', 88)
t = Teacher('Alice', 'Female', 'English')

who_am_i(p)
who_am_i(s)
who_am_i(t)
'''

#在一个函数中，如果我们接收一个变量 x，则无论该 x 是 Person、Student还是 Teacher，都可以正确打印出结果,这种行为称为多态
#任何对象，只要有read()方法，就称为File-like Object
'''
import json
class Students(object):
    def read(self):
        return r'["Tim", "Bob", "Alice"]'
s = Students()
print json.load(s)
'''

## 5-5 python中多重继承
#除了从一个父类继承外，Python允许从多个父类继承，称为多重继承。


'''
class Person(object):
    pass

class Student(Person):
    pass

class Teacher(Person):
    pass

class SkillMixin(object):
    pass

class BasketballMixin(SkillMixin):
    def skill(self):
        return 'basketball'

class FootballMixin(SkillMixin):
    def skill(self):
        return 'football'

class BStudent(Student, BasketballMixin):
    pass

class FTeacher(Teacher, FootballMixin):
    pass

s = BStudent()
print s.skill()

t = FTeacher()
print t.skill()
'''

## 5-6 python中获取对象信息
#可以用 type() 函数获取变量的类型，它返回一个 Type 对象
#可以用 dir() 函数获取变量的所有属性

'''
class Person(object):
    def __init__(self, name, gender, **kw):
        self.name = name
        self.gender = gender
        for k, v in kw.iteritems():
            setattr(self, k, v)

p = Person('Bob', 'Male', age=18, course='Python')
print p.name
print p.gender
print p.age
print p.course
'''

# 第6章 定制类
#本章讲解Python的特殊方法，以及如何利用特殊方法定制类，实现各种强大的功能。

## 6-1 python中什么是特殊方法
#特殊方法又称为魔术方法
#特殊方法__str__(),如print lst.__str__()
"""
python的特殊方法
    用于print的__str__
    用于len的__len__
    用于cmp的__cmp__ #比较方法
    ......
特殊方法定义在class中
不需要直接调用
python的某些函数或操作符会调用对应的特殊方法

正确实现特殊方法
    只需要编写用到的特殊方法
    有关联性的特殊方法都必须实现
"""

## 6-2 python中 __str__和__repr__
#如果要把一个类的实例变成 str，就需要实现特殊方法__str__()

#给Student 类定义__str__和__repr__方法
'''
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
'''

## 6-3 python中 __cmp__
#对 int、str 等内置数据类型排序时，Python的 sorted() 按照默认的比较函数 cmp 排序，但是，如果对一组 Student 类的实例排序时，就必须提供我们自己的特殊方法__cmp__()

#修改 Student 的__cmp__方法，让它按照分数从高到底排序，分数相同的按名字排序

'''
class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __str__(self):
        return '(%s: %s)' % (self.name, self.score)

    __repr__ = __str__

    def __cmp__(self, s):
        if self.score == s.score:
            return cmp(self.name, s.name)
        return -cmp(self.score, s.score)

L = [Student('Tim', 99), Student('Bob', 88), Student('Alice', 99)]
print sorted(L)
'''

## 6-4 python中__len__
#如果一个类表现得像一个list，要获取有多少个元素，就得用 len() 函数。
#要让 len() 函数工作正常，类必须提供一个特殊方法len()，它返回元素的个数

#斐波那契数列是由 0, 1, 1, 2, 3, 5, 8...构成。
#请编写一个Fib类，Fib(10)表示数列的前10个元素，print Fib(10) 可以打印出数列的前 10 个元素，len(Fib(10))可以正确返回数列的个数10
'''
class Fib(object):
    def __init__(self, num):
        a, b, L = 0, 1, []
        for n in range(num):
            L.append(a)
            a, b = b, a + b
        self.numbers = L

    def __str__(self):
        return str(self.numbers)

    __repr__ = __str__

    def __len__(self):
        return len(self.numbers)

f = Fib(10)
print f
print len(f)
'''

## 6-5 python中数学运算
#四则运算不局限于int和float，还可以是有理数、矩阵等
#要表示有理数，可以用一个Rational类来表示

#Rational类虽然可以做加法，但无法做减法、乘方和除法，请继续完善Rational类，实现四则运算

'''
减法运算：__sub__
乘法运算：__mul__
除法运算：__div__
'''

'''
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

class Rational(object):
    def __init__(self, p, q):
        self.p = p
        self.q = q
    def __add__(self, r):
        return Rational(self.p * r.q + self.q * r.p, self.q * r.q)
    def __sub__(self, r):
        return Rational(self.p * r.q - self.q * r.p, self.q * r.q)
    def __mul__(self, r):
        return Rational(self.p * r.p, self.q * r.q)
    def __div__(self, r):
        return Rational(self.p * r.q, self.q * r.p)
    def __str__(self):
        g = gcd(self.p, self.q)
        return '%s/%s' % (self.p / g, self.q / g)
    __repr__ = __str__

r1 = Rational(1, 2)
r2 = Rational(1, 4)
print r1 + r2
print r1 - r2
print r1 * r2
print r1 / r2
'''

## 6-6 python中类型转换

#继续完善Rational，使之可以转型为float

'''
class Rational(object):
    def __init__(self, p, q):
        self.p = p
        self.q = q

    def __int__(self):
        return self.p // self.q

    def __float__(self):
        return float(self.p) / self.q

print float(Rational(7, 2))
print float(Rational(1, 3))
'''

## 6-7 python中 @property


#给Student类加一个grade属性，根据 score 计算 A（>=80）、B、C（<60）
#用 @property 修饰 grade 的 get 方法即可实现只读属性

'''
class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.__score = score
    @property
    def score(self):
        return self.__score
    @score.setter
    def score(self, score):
        if score < 0 or score > 100:
            raise ValueError('invalid score')
        self.__score = score
    @property
    def grade(self):
        if self.score < 60:
            return 'C'
        if self.score < 80:
            return 'B'
        return 'A'
s = Student('Bob', 59)
print s.grade
s.score = 60
print s.grade
s.score = 99
print s.grade
'''

## 6-8 python中 __slots__
#__slots__是指一个类允许的属性列表
#__slots__的目的是限制当前类所能拥有的属性，如果不需要添加任意动态的属性，使用__slots__也能节省内存

'''
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
'''

## 6-9 python中 __call__
#所有的函数都是可调用对象
#一个类实例也可以变成一个可调用对象，只需要实现一个特殊方法__call__()

#加一个__call__方法，让斐波那契数列调用更简单

'''
class Fib(object):
    def __call__(self, num):
        a, b, L = 0, 1, []
        for n in range(num):
            L.append(a)
            a, b = b, a + b
        return L

f = Fib()
print f(10)
'''


# 第7章 课程总结
#对课程进行概括性总结，并对后续课程进行简单说明。

#7-1 课程总结
"""
python的函数式编程
    高阶函数
    闭包
    匿名函数
    装饰器
python的模块和包
    避免名字冲突
    引用模块
    __future__
python面向对象编程
    类和实例
    属性和方法
    区分类属性和实例属性
python类的继承
    继承的概念和目的
    多态
    多重继承
python定制类
    定制类的目的
    特殊方法
    类型转换
    __call__

下一步学习
    IO：文件和Socket
    多任务：进程和线程
    数据库
    Web开发
"""