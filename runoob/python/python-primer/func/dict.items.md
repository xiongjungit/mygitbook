#Python 字典(Dictionary) items()方法

#描述
Python 字典(Dictionary) items() 函数以列表返回可遍历的(键, 值) 元组数组。

#语法
items()方法语法：

```
dict.items()
```

#参数
NA。

#返回值
返回可遍历的(键, 值) 元组数组。

#实例
以下实例展示了 items()函数的使用方法：

```
#!/usr/bin/python

dict = {'Name': 'Zara', 'Age': 7}

print "Value : %s" %  dict.items()
```

以上实例输出结果为：

```
Value : [('Age', 7), ('Name', 'Zara')]
```