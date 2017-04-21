#Python List pop()方法


#描述
pop() 函数用于移除列表中的一个元素（默认最后一个元素），并且返回该元素的值。

#语法
pop()方法语法：

```
list.pop(obj=list[-1])
```

#参数
- obj -- 可选参数，要移除列表元素的对象。

#返回值
该方法返回从列表中移除的元素对象。

#实例
以下实例展示了 pop()函数的使用方法：

```
#!/usr/bin/python

aList = [123, 'xyz', 'zara', 'abc'];

print "A List : ", aList.pop();
print "B List : ", aList.pop(2);
```

以上实例输出结果如下：

```
A List :  abc
B List :  zara
```