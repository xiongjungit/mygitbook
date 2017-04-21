#Python File readlines() 方法


#概述
readlines() 方法用于读取所有行(直到结束符 EOF)并返回列表，若给定sizeint>0，返回总和大约为sizeint字节的行, 实际读取值可能比sizhint较大, 因为需要填充缓冲区。
如果碰到结束符 EOF 则返回空字符串。

#语法
readlines() 方法语法如下：

```
fileObject.readlines( sizehint );
```

#参数
- sizehint -- 从文件中读取的字节数。

#返回值
返回列表，包含所有的行。

#实例
以下实例演示了 readline() 方法的使用：
文件 runoob.txt 的内容如下：

```
1:www.runoob.com
2:www.runoob.com
3:www.runoob.com
4:www.runoob.com
5:www.runoob.com
```

循环读取文件的内容：

```
#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 打开文件
fo = open("runoob.txt", "rw+")
print "文件名为: ", fo.name

line = fo.readlines()
print "读取的数据为: %s" % (line)

line = fo.readlines(2)
print "读取的数据为: %s" % (line)


# 关闭文件
fo.close()
```

以上实例输出结果为：

```
文件名为:  runoob.txt
读取的数据为: ['1:www.runoob.com\n', '2:www.runoob.com\n', '3:www.runoob.com\n', '4:www.runoob.com\n', '5:www.runoob.com\n']
读取的数据为: []
```