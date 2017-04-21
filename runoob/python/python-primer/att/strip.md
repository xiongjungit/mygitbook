#Python strip()方法


#描述
Python strip() 方法用于移除字符串头尾指定的字符（默认为空格）。

#语法
strip()方法语法：

```
str.strip([chars]);
```

#参数
- chars -- 移除字符串头尾指定的字符。

#返回值
返回移除字符串头尾指定的字符生成的新字符串。

#实例
以下实例展示了strip()函数的使用方法：


```
#!/usr/bin/python

str = "0000000this is string example....wow!!!0000000";
print str.strip( '0' );
```

以上实例输出结果如下：

```
this is string example....wow!!!
```