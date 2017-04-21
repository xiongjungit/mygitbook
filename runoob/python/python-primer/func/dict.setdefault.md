#Python 字典(Dictionary) setdefault()方法

#描述
Python 字典(Dictionary) setdefault() 函数和get()方法类似, 如果键不已经存在于字典中，将会添加键并将值设为默认值。

#语法
setdefault()方法语法：

```
dict.setdefault(key, default=None)
```

#参数
- key -- 查找的键值。
- default -- 键不存在时，设置的默认键值。

#返回值
该方法没有任何返回值。

#实例
以下实例展示了 setdefault()函数的使用方法：

```
#!/usr/bin/python

dict = {'Name': 'Zara', 'Age': 7}

print "Value : %s" %  dict.setdefault('Age', None)
print "Value : %s" %  dict.setdefault('Sex', None)
```

以上实例输出结果为：


```
Value : 7
Value : None
```