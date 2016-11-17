# -*- coding: utf-8 -*-

# 慕课网python入门
print u'慕课网python入门所有代码'

# 第3章 python变量和数据类型
## 3-1 python中数据类型
'''
print int(0x12fd2)
print 45678 + 0x12fd2
print "Learn Python in imooc"
print 100 < 99
print 0xff == 255
'''

## 3-2 python之print语句
'''
print 'hello, python'
print 'hello,', 'python'#遇到逗号“,”会输出一个空格
'''

## 3-3 python的注释
# "#"是单行注释
# "'''"和"'''"包裹的是多行注释

## 3-4 python中什么是变量
#变量名必须是大小写英文、数字和下划线（_）的组合，且不能用数字开头
#求和 s = (x1 + x100) * n / 2
'''
x1 = 1
d = 3
n = 100
x100 = x1 + (n - 1) * d
s = (x1 + x100) * n / 2
print s
'''

## 3-5 python中定义字符串
'''
常用的转义字符
\n 表示换行
\t 表示一个制表符
\\ 表示 \ 字符本身
'''

'''
s = 'Python was started in 1989 by \"Guido\".\nPython is free and easy to learn.'
print s
'''

## 3-6 python中raw字符串与多行字符串
#在字符串前面加个前缀 r ，表示这是一个 raw 字符串
'''
print 'Line 1\nLine 2\nLine 3'
print r'Line 1\nLine 2\nLine 3'
'''

## 3-7 python中unicode字符串
#最早的Python只支持ASCII编码，普通的字符串'ABC'在Python内部都是ASCII编码的
#Python在后来添加了对Unicode的支持，以Unicode表示的字符串用u'...'表示
#开头的# -*- coding: utf-8 -*- 目的是告诉Python解释器，用UTF-8编码读取源代码。

# -*- coding: utf-8 -*-

"""
print '''静夜思

床前明月光，
疑是地上霜。
举头望明月，
低头思故乡。
'''
"""


## 3-8 python中整数和浮点数
#为什么要区分整数运算和浮点数运算呢？这是因为整数运算的结果永远是精确的，而浮点数运算的结果不一定精确
'''
print 1 + 2
print 1 + 2.0
print 11 / 4
print 11 % 4 #求余
print 11.0 / 4
print 2.5 + 10.0 / 4
'''

## 3-9 python中布尔类型
#布尔类型只有True和False两种值
#布尔类型有以下几种运算
"""
与运算：只有两个布尔值都为 True 时，计算结果才为 True。
True and True   # ==> True
True and False   # ==> False
False and True   # ==> False
False and False   # ==> False

或运算：只要有一个布尔值为 True，计算结果就是 True。
True or True   # ==> True
True or False   # ==> True
False or True   # ==> True
False or False   # ==> False

非运算：把True变为False，或者把False变为True：
not True   # ==> False
not False   # ==> True
"""

#在Python中，布尔类型还可以与其他数据类型做 and、or和not运算
#Python把0、空字符串''和None看成 False，其他数值和非空字符串都看成 True
'''
a = True
print a and 'a=T' or 'a=F'
'''

#and 和 or 运算的一条重要法则：短路计算
"""
1. 在计算 a and b 时，如果 a 是 False，则根据与运算法则，整个结果必定为 False，因此返回 a；如果 a 是 True，则整个计算结果必定取决与 b，因此返回 b。

2. 在计算 a or b 时，如果 a 是 True，则根据或运算法则，整个计算结果必定为 True，因此返回 a；如果 a 是 False，则整个计算结果必定取决于 b，因此返回 b。
"""

'''
a = 'python'
print 'hello,', a or 'world'
b = ''
print 'hello,', b or 'world'
'''


# 第4章 list和tuple类型
## 4-1 python创建list
'''
L = ['Michael', 'Bob', 'Tracy']
print L
'''

#一个元素也没有的list，就是空list：
'''
empty_list = []
print empty_list
'''

'''
L = ['Adam', 95.5, 'Lisa', 85, 'Bart', 59]
print L
'''

## 4-2 python按照索引访问list
#list是一个有序集合
'''
L = [95.5,85,59]
print L[0]
print L[1]
print L[2]
print L[-1]
'''


# 4-3 python之倒序访问list
'''
L = [95.5, 85, 59]
print L[-1]
print L[-2]
print L[-3]
'''

##4-4 Python之添加新元素
'''
L = ['Adam', 'Lisa', 'Bart']
L.append('Paul')
print L
'''
#append()总是把新的元素添加到 list 的尾部。

'''
L = ['Adam', 'Lisa', 'Bart']
L.insert(0, 'Paul')
print L
'''
#L.insert(0, 'Paul') 的意思是，'Paul'将被添加到索引为 0 的位置上

## 4-5 python从list删除元素
'''
L = ['Adam', 'Lisa', 'Bart', 'Paul']
L.pop()
print L
'''

#pop()方法总是删掉list的最后一个元素，并且它还返回这个元素
#删除索引2的元素
'''
L = ['Adam', 'Lisa', 'Bart', 'Paul']
L.pop(2)
print L
'''

'''
L = ['Adam', 'Lisa', 'Paul', 'Bart']
L.pop(3)
L.pop(2)
print L
'''

## 4-6 python中替换元素
'''
L = ['Adam', 'Lisa', 'Bart']
L[0] = 'Bart'
L[-1] = 'Adam'
print L
'''

## 4-7 python之创建tuple
#tuple是另一种有序的列表，中文翻译为“ 元组 ”。tuple 和 list 非常类似，但是，tuple一旦创建完毕，就不能修改了。
#创建tuple和创建list唯一不同之处是用( )替代了[ ]。
'''
t = (0,1, 2, 3, 4, 5, 6, 7, 8, 9)
print t
'''

## 4-8 python之创建单元素tuple
#所以 Python 规定，单元素 tuple 要多加一个逗号“,”
'''
t = (1)
print t
t = (1,)
print t
t = (1, 2, 'a',)
print t
'''

## 4-9 Python之“可变”的tuple
'''
t = ('a', 'b', ['A', 'B'])
L = t[2]
L[0] = 'X'
L[1] = 'Y'
print t
'''
#tuple所谓的“不变”是说，tuple的每个元素，指向永远不变

'''
t = ('a', 'b', ('A', 'B'))
print t
'''


# 第5章 条件判断和循环
## 5-2 python之if-else
'''
score = 55
if score >= 60:
    print 'passed'
else:
    print 'failed'
'''

## 5-3 python之if-elif-esle
'''
score = 85
if score >= 90:
    print 'excellent'
elif score >= 80:
    print 'good'
elif score >= 60:
    print 'passed'
else:
    print 'failed'
'''


## 5-4 python之for循环
'''
L = [75, 92, 59, 68,88,98]
sum = 0.0
for x in L:
    sum = sum + x
    print x
print sum / len(L)
'''

## 5-5 python之while循环
'''
sum = 0
x = 1
while x < 101:
    sum = sum + x
    print x
    x = x + 1
print sum
'''


## 5-6 python之break退出循环
'''
sum = 0
x = 1
while True:
    sum = sum + x
    x = x + 1
    if x > 100:
        break
print sum
'''

#计算 1 + 2 + 4 + 8 + 16 + ... 的前20项的和
'''
sum = 0
x = 1
n = 1
while True:
    if n > 20:
        break
    sum = sum + x
    x = x * 2
    n = n + 1
print sum
'''

## 5-7 python之continue继续循环
### 统计及格分数的平均分
'''
L = [75, 98, 59, 81, 66, 43, 69, 85]
sum = 0.0
n = 0
for x in L:
    if x < 80:
        continue
    sum = sum + x
    n = n + 1
print sum / n
'''

### 计算100以内奇数的和
'''
sum = 0
x = 0
while True:
    x = x + 1
    if x > 100:
        break
    if x % 2 == 0:
        continue
    sum = sum + x
print sum
'''

## 5-8 python之多重循环
### 打印100以内十位比个位小的数字
'''
for x in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
    for y in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        if x < y:
            print x * 10 + y
'''

# 第6章 Dict和Set类型
#讲解Python的另外两种重要的数据类型Dict和Set，可以快速按照关键字检索信息。

## 6-1 python之什么是dict
#要根据名字找到对应的成绩,Python的 dict 就是专门干这件事的。用 dict 表示“名字”-“成绩”的查找表如下：

'''
d = {
    'Adam': 95,
    'Lisa': 85,
    'Bart': 59
}
print d
print len(d)
'''

#我们把名字称为key，对应的成绩称为value，dict就是通过 key 来查找 value。
#花括号 {} 表示这是一个dict，然后按照 key: value, 写出来即可。最后一个 key: value 的逗号可以省略。
#由于dict也是集合，len() 函数可以计算任意集合的大小：

## 6-2 python之访问dict
'''
d = {
    'Adam': 95,
    'Lisa': 85,
    'Bart': 59
}
print d['Adam']
'''

#一是先判断一下 key 是否存在，用 in 操作符：
"""
if 'Paul' in d:
    print d['Paul']
"""
#二是使用dict本身提供的一个 get 方法，在Key不存在的时候，返回None：
"""
print d.get('Bart')
print d.get('Paul')
"""


'''
d = {
    'Adam': 95,
    'Lisa': 85,
    'Bart': 59
}
print 'Adam:', d['Adam']
print 'Lisa:', d['Lisa']
print 'Bart:', d['Bart']
'''


## 6-3 python中dict的特点
#dict的第一个特点是查找速度快
#dict的第二个特点就是存储的key-value序对是没有顺序的！这和list不一样
#dict的第三个特点是作为 key 的元素必须不可变，Python的基本类型如字符串、整数、浮点数都是不可变的，都可以作为 key。但是list是可变的，就不能作为 key。

'''
d = {
    95: 'Adam',
    85: 'Lisa',
    59: 'Bart'
}
print d
'''

## 6-4 python更新dict
#dict是可变的，我们可以随时往dict中添加新的 key-value。
'''
d = {
    'Adam': 95,
    'Lisa': 85,
    'Bart': 59
}
d['Paul'] = 72
print d
'''

'''
d = {
    95: 'Adam',
    85: 'Lisa',
    59: 'Bart'
}
d[72] = 'Paul'
print d
'''


## 6-5 python之 遍历dict
'''
d= {
    'Adam': 95,
    'Lisa': 85,
    'Bart': 59
}
for key in d:
    print key + ':', d[key]
'''

## 6-6 python中什么是set
#set的元素没有重复，而且是无序的
'''
s = set(['Adam', 'Lisa', 'Bart', 'Paul','Lisa'])
print s
print len(s)
'''


## 6-7 python之访问set
#由于set存储的是无序集合，所以我们没法通过索引来访问。
#访问 set中的某个元素实际上就是判断一个元素是否在set中。

'''
s = set(['Adam', 'adam', 'Lisa', 'lisa', 'Bart', 'bart', 'Paul', 'paul'])
print 'adam' in s
print 'bart' in s
print 'admin' in s
print len(s)
'''

## 6-8 python之set的特点
#set的内部结构和dict很像，唯一区别是不存储value，因此，判断一个元素是否在set中速度很快。
#set存储的元素和dict的key类似，必须是不变对象，因此，任何可变对象是不能放入set中的。
#最后，set存储的元素也是没有顺序的。

'''
months = set(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
x1 = 'Feb'
x2 = 'Sun'
if x1 in months:
    print 'x1: ok'
else:
    print 'x1: error'
if x2 in months:
    print 'x2: ok'
else:
    print 'x2: error'
'''

## 6-9 python之遍历set

'''
s = set([('Adam', 95), ('Lisa', 85), ('Bart', 59)])
for x in s:
    print x[0] + ':', x[1]
'''

## 6-10 python之更新set
'''
s = set(['Adam', 'Lisa', 'Paul'])
L = ['Adam', 'Lisa', 'Bart', 'Paul','Bob']
for name in L:
    if name in s:
        s.remove(name)
    else:
        s.add(name)
print s
'''


# 第7章 函数
## 7-1 python之什么是函数
#函数就是最基本的一种代码抽象的方式。
#Python不但能非常灵活地定义函数，而且本身内置了很多有用的函数，可以直接调用。


##7-2 python之调用函数
#要调用一个函数，需要知道函数的名称和参数，比如求绝对值的函数 abs，它接收一个参数。

#计算1*1+2*2+3*3+...+10*10的和
'''
L = []
x = 1
while x <= 10:
    L.append(x * x)
    x = x + 1
print sum(L)
'''

##7-3 python之编写函数
#在Python中，定义一个函数要使用 def 语句，依次写出函数名、括号、括号中的参数和冒号:，然后，在缩进块中编写函数体，函数的返回值用 return 语句返回。

#请注意，函数体内部的语句在执行时，一旦执行到return时，函数就执行完毕，并将结果返回。因此，函数内部通过条件判断和循环可以实现非常复杂的逻辑。
#如果没有return语句，函数执行完毕后也会返回结果，只是结果为 None。
#return None可以简写为return。

#定义一个 square_of_sum 函数，它接受一个list，返回list中每个元素平方的和
'''
def square_of_sum(L):
    sum = 0
    for x in L:
        sum = sum + x * x
    return sum
print square_of_sum([1, 2, 3, 4, 5])
print square_of_sum([-5, 0, 5, 15, 25])
'''


## 7-4 python函数之返回多值
#函数可以返回多个值吗？答案是肯定的。
#Python的函数返回多值其实就是返回一个tuple

#一元二次方程的定义是：ax² + bx + c = 0
#编写一个函数，返回一元二次方程的两个解。
#Python的math包提供了sqrt()函数用于计算平方根。
#参考求根公式：x = (-b±√(b²-4ac)) / 2a
'''
import math
def quadratic_equation(a, b, c):
    t = math.sqrt(b * b - 4 * a * c)
    return (-b + t) / (2 * a),( -b - t )/ (2 * a)
print quadratic_equation(2, 3, 0)
print quadratic_equation(1, -6, 5)
'''

## 7-5 python之递归函数
#在函数内部，可以调用其他函数。如果一个函数在内部调用自身本身，这个函数就是递归函数。
#递归函数的优点是定义简单，逻辑清晰。理论上，所有的递归函数都可以写成循环的方式，但循环的逻辑不如递归清晰。
#使用递归函数需要注意防止栈溢出。在计算机中，函数调用是通过栈（stack）这种数据结构实现的，每当进入一个函数调用，栈就会加一层栈帧，每当函数返回，栈就会减一层栈帧。由于栈的大小不是无限的，所以，递归调用的次数过多，会导致栈溢出。可以试试计算 fact(10000)。



"""
汉诺塔 (http://baike.baidu.com/view/191666.htm) 的移动也可以看做是递归函数。

我们对柱子编号为a, b, c，将所有圆盘从a移到c可以描述为：

如果a只有一个圆盘，可以直接移动到c；

如果a有N个圆盘，可以看成a有1个圆盘（底盘） + (N-1)个圆盘，首先需要把 (N-1) 个圆盘移动到 b，然后，将 a的最后一个圆盘移动到c，再将b的(N-1)个圆盘移动到c。

请编写一个函数，给定输入 n, a, b, c，打印出移动的步骤：

move(n, a, b, c)

例如，输入 move(2, 'A', 'B', 'C')，打印出：

A --> B A --> C B --> C

函数 move(n, a, b, c) 的定义是将 n 个圆盘从 a 借助 b 移动到 c。

#使用递归函数计算汉诺塔

def move(n, a, b, c):
    if n ==1:
        print a, '-->', c
        return
    move(n-1, a, c, b)
    print a, '-->', c
    move(n-1, b, a, c)
move(4, 'A', 'B', 'C')

"""

## 7-6 python之定义默认参数
#定义一个 greet() 函数，它包含一个默认参数，如果没有传入，打印 'Hello, world.'，如果传入，打印 'Hello, xxx.'
'''
def greet(name='world'):
    print 'Hello, ' + name + '.'
greet()
greet('Bart')
'''

## 7-7 python之定义可变参数
#如果想让一个函数能接受任意个参数，我们就可以定义一个可变参数
#可变参数也不是很神秘，Python解释器会把传入的一组参数组装成一个tuple传递给可变参数，因此，在函数内部，直接把变量 args 看成一个 tuple 就好了。

#编写接受可变参数的 average() 函数
#可变参数的名字前面有个 * 号，我们可以传入0个、1个或多个参数给可变参数
#可变参数 args 是一个tuple，当0个参数传入时，args是一个空tuple
'''
def average(*args):
    sum = 0.0
    if len(args) == 0:
        return sum
    for x in args:
        sum = sum + x
    return sum / len(args)
print average()
print average(1, 2)
print average(1, 2, 2, 3, 4)
'''

# 第8章 切片
#介绍Python程序特有的一种“切片”操作，可以以极其简洁的方式快速对列表进行操作。

## 8-1 对list进行切片
#Python提供了切片（Slice）操作符
'''
L = ['Adam', 'Lisa', 'Bart', 'Paul']
print L[0:3]
'''


#L[0:3]表示，从索引0开始取，直到索引3为止，但不包括索引3。即索引0，1，2，正好是3个元素。

"""
如果第一个索引是0，还可以省略：
>>> L[:3]
['Adam', 'Lisa', 'Bart']

也可以从索引1开始，取出2个元素出来：
>>> L[1:3]
['Lisa', 'Bart']

只用一个 : ，表示从头到尾：
>>> L[:]
['Adam', 'Lisa', 'Bart', 'Paul']

因此，L[:]实际上复制出了一个新list。

切片操作还可以指定第三个参数：
>>> L[::2]
['Adam', 'Bart']

第三个参数表示每N个取一个，上面的 L[::2] 会每两个元素取出一个来，也就是隔一个取一个。

把list换成tuple，切片操作完全相同，只是切片的结果也变成了tuple。
"""

"""
range()函数可以创建一个数列：

>>> range(1, 101)
[1, 2, 3, ..., 100]
请利用切片，取出：

前10个数；
3的倍数；
不大于50的5的倍数。
要取出3, 6, 9可以用::3的操作，但是要确定起始索引。

L = range(1, 101)
print L[:10]
print L[2::3]
print L[4:50:5]
"""


## 8-2 倒序切片
#倒数第一个元素的索引是-1。倒序切片包含起始索引，不包含结束索引。
'''
L = range(1, 101)
print L
print L[-10:]
print L[-46::5]
'''

## 8-3 对字符串切片
#字符串 'xxx'和 Unicode字符串 u'xxx'也可以看成是一种list，每个元素就是一个字符。因此，字符串也可以用切片操作，只是操作结果仍是字符串
#字符串有个方法 upper() 可以把字符变成大写字母

'''
def firstCharUpper(s):
    return s[0].upper() + s[1:]
print firstCharUpper('hello')
print firstCharUpper('sunday')
print firstCharUpper('september')
'''

#第9章 迭代
#介绍Python程序中“迭代”的概念，以及各种迭代方式。

## 9-1 什么是迭代
#在Python中，如果给定一个list或tuple，我们可以通过for循环来遍历这个list或tuple，这种遍历我们成为迭代
"""
集合是指包含一组元素的数据结构，我们已经介绍的包括：
1. 有序集合：list，tuple，str和unicode；
2. 无序集合：set
3. 无序集合并且具有 key-value 对：dict
"""


#用for循环迭代数列 1-100 并打印出7的倍数
'''
for i in range(1, 101):
    if i % 7 == 0:
        print i
'''

## 9-2 索引迭代
#Python中，迭代永远是取出元素本身，而非元素的索引
#对于有序集合,使用 enumerate() 函数在 for 循环中拿到索引

'''
L = ['Adam', 'Lisa', 'Bart', 'Paul']
for index, name in enumerate(L):
    print index, '-', name
'''

#enumerate() 函数把['Adam', 'Lisa', 'Bart', 'Paul']变成了类似[(0, 'Adam'), (1, 'Lisa'), (2, 'Bart'), (3, 'Paul')]
'''
L = ['Adam', 'Lisa', 'Bart', 'Paul']
for t in enumerate(L):
    index = t[0]
    name = t[1]
    print index, '-', name
'''

#如果我们知道每个tuple元素都包含两个元素，for循环又可以进一步简写为

'''
L = ['Adam', 'Lisa', 'Bart', 'Paul']
for index, name in enumerate(L):
    print index, '-', name
'''

#zip()函数可以把两个 list 变成一个 list

'''
print zip([10, 20, 30], ['A', 'B', 'C'])
'''

#在迭代 ['Adam', 'Lisa', 'Bart', 'Paul'] 时，如果我们想打印出名次 - 名字（名次从1开始)

'''
L = ['Adam', 'Lisa', 'Bart', 'Paul']
for index, name in zip(range(1, len(L)+1), L):
    print index, '-', name
'''

## 9-3 迭代dict的value
#dict 对象有一个 values() 方法，这个方法把dict转换成一个包含所有value的list
#dict除了values()方法外，还有一个 itervalues() 方法，用 itervalues() 方法替代 values() 方法，迭代效果完全一样
#values() 方法实际上把一个 dict 转换成了包含 value 的list
#但是 itervalues() 方法不会转换，它会在迭代过程中依次从 dict 中取出 value，所以 itervalues() 方法比 values() 方法节省了生成 list 所需的内存
#打印 itervalues() 发现它返回一个 对象，这说明在Python中，for 循环可作用的迭代对象远不止 list，tuple，str，unicode，dict等，任何可迭代对象都可以作用于for循环，而内部如何迭代我们通常并不用关心。


#计算所有同学的平均分

'''
d = { 'Adam': 95, 'Lisa': 85, 'Bart': 59, 'Paul': 74 }
sum = 0.0
for v in d.itervalues():
    sum = sum + v
print sum / len(d)
'''


# 9-4 迭代dict的key和value
#items() 方法把dict对象转换成了包含tuple的list

'''
d = { 'Adam': 95, 'Lisa': 85, 'Bart': 59 }
print d.items()
'''

#和 values() 有一个 itervalues() 类似， items() 也有一个对应的 iteritems()

#打印出 name : score，最后再打印出平均分 average : score

'''
d = { 'Adam': 95, 'Lisa': 85, 'Bart': 59, 'Paul': 74 }
sum = 0.0
for k, v in d.iteritems():
    sum = sum + v
    print k, ':', v
print 'average', ':', sum / len(d)
'''

# 第10章 列表生成式
#介绍Python特有的列表生成式，利用列表生成式，可以通过某种规则快速创建一个列表

# 10-1 生成列表
#生成[1x1, 2x2, 3x3, ..., 10x10]


'''
L = []
for x in range(1,11):
    L.append(x*x)
print L
'''

#列表生成式可以用一行语句代替循环生成上面的list
#写列表生成式时，把要生成的元素 x * x 放到前面，后面跟 for 循环，就可以把list创建出来，十分有用，多写几次，很快就可以熟悉这种语法。

'''
L = [x * x for x in range(1, 11)]
print L
'''

#利用列表生成式生成列表 [1x2, 3x4, 5x6, 7x8, ..., 99x100]
#range(1, 100, 2) 可以生成list [1, 3, 5, 7, 9,...]

'''
L = [x * (x + 1) for x in range(1, 100, 2)]
print L
'''

## 10-2 复杂表达式
#在生成的表格中，对于没有及格的同学，请把分数标记为红色,超过80分的标记为绿色
#字符串可以通过 % 进行格式化，用指定的参数替代 %s。字符串的join()方法可以把一个 list 拼接成一个字符串


'''
d = { 'Adam': 95, 'Lisa': 85, 'Bart': 59 ,'Bob':62 }
def generate_tr(name, score):
    if score < 60:
        return '<tr><td>%s</td><td style="color:red">%s</td></tr>' % (name, score)
    elif score > 80:
         return '<tr><td>%s</td><td style="color:green">%s</td></tr>' % (name, score)
    return '<tr><td>%s</td><td>%s</td></tr>' % (name, score)
tds = [generate_tr(name, score) for name, score in d.iteritems()]
print '<table border="1">'
print '<tr><th>Name</th><th>Score</th><tr>'
print '\n'.join(tds)
print '</table>'
'''

## 10-3 条件过滤
#列表生成式的 for 循环后面还可以加上 if 判断

#计算10以内偶数的平方
'''
print [x * x for x in range(1, 11) if x % 2 == 0]
'''

#编写一个函数，它接受一个 list，然后把list中的所有字符串变成大写后返回，非字符串元素将被忽略
#isinstance(x, str) 可以判断变量 x 是否是字符串
#字符串的 upper() 方法可以返回大写的字母

'''
def toUppers(L):
    return [x.upper() for x in L if isinstance(x, str)]
print toUppers(['Hello', 'world', 101])
'''

## 10-4 多层表达式
#在列表生成式中，也可以用多层 for 循环来生成列表

#利用 3 层for循环的列表生成式，找出1000以内对称的 3 位数。例如，121 就是对称数

'''
L = []
for n1 in range(1,10):
    for n2 in range(1,10):
        for n3 in range(1,10):
            if n1==n3:
                L.append(100 * n1 + 10 * n2 + n3)
print L
'''

#列表生成式实现

'''
print [100 * n1 + 10 * n2 + n3 for n1 in range(1, 10) for n2 in range(10) for n3 in range(10) if n1==n3]
'''









