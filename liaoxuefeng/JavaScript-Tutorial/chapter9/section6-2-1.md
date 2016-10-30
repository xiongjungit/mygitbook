#9-6-2-1 使用Sequelize


##访问MySQL

当我们安装好MySQL后，Node.js程序如何访问MySQL数据库呢？

访问MySQL数据库只有一种方法，就是通过网络发送SQL命令，然后，MySQL服务器执行后返回结果。

我们可以在命令行窗口输入mysql -u root -p，然后输入root口令后，就连接到了MySQL服务器。因为没有指定--host参数，所以我们连接到的是localhost，也就是本机的MySQL服务器。

在命令行窗口下，我们可以输入命令，操作MySQL服务器：

	mysql> show databases;
	+--------------------+
	| Database           |
	+--------------------+
	| information_schema |
	| mysql              |
	| performance_schema |
	| test               |
	+--------------------+
	4 rows in set (0.05 sec)
输入exit退出MySQL命令行模式。

对于Node.js程序，访问MySQL也是通过网络发送SQL命令给MySQL服务器。这个访问MySQL服务器的软件包通常称为MySQL驱动程序。不同的编程语言需要实现自己的驱动，MySQL官方提供了Java、.Net、Python、Node.js、C++和C的驱动程序，官方的Node.js驱动目前仅支持5.7以上版本，而我们上面使用的命令行程序实际上用的就是C驱动。

目前使用最广泛的MySQL Node.js驱动程序是开源的mysql，可以直接使用npm安装。

##ORM

如果直接使用mysql包提供的接口，我们编写的代码就比较底层，例如，查询代码：

	connection.query('SELECT * FROM users WHERE id = ?', ['123'], function(err, rows) {
	    if (err) {
	        // error
	    } else {
	        for (let row in rows) {
	            processRow(row);
	        }
	    }
	});
考虑到数据库表是一个二维表，包含多行多列，例如一个pets的表：

	mysql> select * from pets;
	+----+--------+------------+
	| id | name   | birth      |
	+----+--------+------------+
	|  1 | Gaffey | 2007-07-07 |
	|  2 | Odie   | 2008-08-08 |
	+----+--------+------------+
	2 rows in set (0.00 sec)
每一行可以用一个JavaScript对象表示，例如第一行：

	{
	    "id": 1,
	    "name": "Gaffey",
	    "birth": "2007-07-07"
	}
这就是传说中的ORM技术：Object-Relational Mapping，把关系数据库的表结构映射到对象上。是不是很简单？

但是由谁来做这个转换呢？所以ORM框架应运而生。

我们选择Node的ORM框架Sequelize来操作数据库。这样，我们读写的都是JavaScript对象，Sequelize帮我们把对象变成数据库中的行。

用Sequelize查询pets表，代码像这样：
	
	Pet.findAll()
	   .then(function (pets) {
	       for (let pet in pets) {
	           console.log(`${pet.id}: ${pet.name}`);
	       }
	   }).catch(function (err) {
	       // error
	   });
因为Sequelize返回的对象是Promise，所以我们可以用then()和catch()分别异步响应成功和失败。

但是用then()和catch()仍然比较麻烦。有没有更简单的方法呢？

可以用ES7的await来调用任何一个Promise对象，这样我们写出来的代码就变成了：

	var pets = await Pet.findAll();
真的就是这么简单！

await只有一个限制，就是必须在async函数中调用。上面的代码直接运行还差一点，我们可以改成：

	(async () => {
	    var pets = await Pet.findAll();
	})();
考虑到koa的处理函数都是async函数，所以我们实际上将来在koa的async函数中直接写await访问数据库就可以了！

这也是为什么我们选择Sequelize的原因：只要API返回Promise，就可以用await调用，写代码就非常简单！

##实战

在使用Sequlize操作数据库之前，我们先在MySQL中创建一个表来测试。我们可以在test数据库中创建一个pets表。test数据库是MySQL安装后自动创建的用于测试的数据库。在MySQL命令行执行下列命令：

	grant all privileges on test.* to 'www'@'%' identified by 'www';
	
	use test;
	
	create table pets (
	    id varchar(50) not null,
	    name varchar(100) not null,
	    gender bool not null,
	    birth varchar(10) not null,
	    createdAt bigint not null,
	    updatedAt bigint not null,
	    version bigint not null,
	    primary key (id)
	) engine=innodb;
第一条grant命令是创建MySQL的用户名和口令，均为www，并赋予操作test数据库的所有权限。

第二条use命令把当前数据库切换为test。

第三条命令创建了pets表。

然后，我们根据前面的工程结构创建hello-sequelize工程，结构如下：

	hello-sequelize/
	|
	+- .vscode/
	|  |
	|  +- launch.json <-- VSCode 配置文件
	|
	+- init.txt <-- 初始化SQL命令
	|
	+- config.js <-- MySQL配置文件
	|
	+- app.js <-- 使用koa的js
	|
	+- start.js <-- 启动入口js
	|
	+- package.json <-- 项目描述文件
	|
	+- node_modules/ <-- npm安装的所有依赖包
然后，添加如下依赖包：

	"babel-core": "6.13.2",
	"babel-polyfill": "6.13.0",
	"babel-preset-es2015-node6": "0.3.0",
	"babel-preset-stage-3": "6.5.0",
	"sequelize": "3.24.1",
	"mysql": "2.11.1"
注意mysql是驱动，我们不直接使用，但是sequelize会用。

用npm install安装。

config.js实际上是一个简单的配置文件：

	var config = {
	    database: 'test', // 使用哪个数据库
	    username: 'www', // 用户名
	    password: 'www', // 口令
	    host: 'localhost', // 主机名
	    port: 3306 // 端口号，MySQL默认3306
	};

module.exports = config;
下面，我们就可以在app.js中操作数据库了。使用Sequelize操作MySQL需要先做两件准备工作：

第一步，创建一个sequelize对象实例：

	const Sequelize = require('sequelize');
	const config = require('./config');
	
	var sequelize = new Sequelize(config.database, config.username, config.password, {
	    host: config.host,
	    dialect: 'mysql',
	    pool: {
	        max: 5,
	        min: 0,
	        idle: 30000
	    }
	});
第二步，定义模型Pet，告诉Sequelize如何映射数据库表：

	var Pet = sequelize.define('pet', {
	    id: {
	        type: Sequelize.STRING(50),
	        primaryKey: true
	    },
	    name: Sequelize.STRING(100),
	    gender: Sequelize.BOOLEAN,
	    birth: Sequelize.STRING(10),
	    createdAt: Sequelize.BIGINT,
	    updatedAt: Sequelize.BIGINT,
	    version: Sequelize.BIGINT
	}, {
	        timestamps: false
	    });
用sequelize.define()定义Model时，传入名称pet，默认的表名就是pets。第二个参数指定列名和数据类型，如果是主键，需要更详细地指定。第三个参数是额外的配置，我们传入{ timestamps: false }是为了关闭Sequelize的自动添加timestamp的功能。所有的ORM框架都有一种很不好的风气，总是自作聪明地加上所谓“自动化”的功能，但是会让人感到完全摸不着头脑。

接下来，我们就可以往数据库中塞一些数据了。我们可以用Promise的方式写：

	var now = Date.now();
	
	Pet.create({
	    id: 'g-' + now,
	    name: 'Gaffey',
	    gender: false,
	    birth: '2007-07-07',
	    createdAt: now,
	    updatedAt: now,
	    version: 0
	}).then(function (p) {
	    console.log('created.' + JSON.stringify(p));
	}).catch(function (err) {
	    console.log('failed: ' + err);
	});
也可以用await写：

	(async () => {
	    var dog = await Pet.create({
	        id: 'd-' + now,
	        name: 'Odie',
	        gender: false,
	        birth: '2008-08-08',
	        createdAt: now,
	        updatedAt: now,
	        version: 0
	    });
	    console.log('created: ' + JSON.stringify(dog));
	})();
显然await代码更胜一筹。

查询数据时，用await写法如下：

	(async () => {
	    var pets = await Pet.findAll({
	        where: {
	            name: 'Gaffey'
	        }
	    });
	    console.log(`find ${pets.length} pets:`);
	    for (let p of pets) {
	        console.log(JSON.stringify(p));
	    }
	})();
如果要更新数据，可以对查询到的实例调用save()方法：

	(async () => {
	    var p = await queryFromSomewhere();
	    p.gender = true;
	    p.updatedAt = Date.now();
	    p.version ++;
	    await p.save();
	})();
如果要删除数据，可以对查询到的实例调用destroy()方法：

	(async () => {
	    var p = await queryFromSomewhere();
	    await p.destroy();
	})();
运行代码，可以看到Sequelize打印出的每一个SQL语句，便于我们查看：

	Executing (default): INSERT INTO `pets` (`id`,`name`,`gender`,`birth`,`createdAt`,`updatedAt`,`version`) VALUES ('g-1471961204219','Gaffey',false,'2007-07-07',1471961204219,1471961204219,0);
##Model

我们把通过sequelize.define()返回的Pet称为Model，它表示一个数据模型。

我们把通过Pet.findAll()返回的一个或一组对象称为Model实例，每个实例都可以直接通过JSON.stringify序列化为JSON字符串。但是它们和普通JSON对象相比，多了一些由Sequelize添加的方法，比如save()和destroy()。调用这些方法我们可以执行更新或者删除操作。

所以，使用Sequelize操作数据库的一般步骤就是：

首先，通过某个Model对象的findAll()方法获取实例；

如果要更新实例，先对实例属性赋新值，再调用save()方法；

如果要删除实例，直接调用destroy()方法。

注意findAll()方法可以接收where、order这些参数，这和将要生成的SQL语句是对应的。

##文档

Sequelize的API可以参考[官方文档](http://docs.sequelizejs.com/)。

##参考源码

[hello-sequelize](https://github.com/michaelliao/learn-javascript/tree/master/samples/node/web/db/hello-sequelize)