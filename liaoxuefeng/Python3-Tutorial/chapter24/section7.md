#24-7 Day 7 - 编写MVC

阅读: 13363
现在，ORM框架、Web框架和配置都已就绪，我们可以开始编写一个最简单的MVC，把它们全部启动起来。

通过Web框架的@get和ORM框架的Model支持，可以很容易地编写一个处理首页URL的函数：

	@get('/')
	def index(request):
	    users = yield from User.findAll()
	    return {
	        '__template__': 'test.html',
	        'users': users
	    }
`'__template__'`指定的模板文件是test.html，其他参数是传递给模板的数据，所以我们在模板的根目录templates下创建test.html：

	<!DOCTYPE html>
	<html>
	<head>
	    <meta charset="utf-8" />
	    <title>Test users - Awesome Python Webapp</title>
	</head>
	<body>
	    <h1>All users</h1>
	    {% for u in users %}
	    <p>{{ u.name }} / {{ u.email }}</p>
	    {% endfor %}
	</body>
	</html>
接下来，如果一切顺利，可以用命令行启动Web服务器：

	$ python3 app.py
然后，在浏览器中访问http://localhost:9000/。

如果数据库的users表什么内容也没有，你就无法在浏览器中看到循环输出的内容。可以自己在MySQL的命令行里给users表添加几条记录，然后再访问：

![awesomepy-all-users](../image/chapter24/24-7-1.jpg)

##参考源码

[day-07](https://github.com/michaelliao/awesome-python3-webapp/tree/day-07)