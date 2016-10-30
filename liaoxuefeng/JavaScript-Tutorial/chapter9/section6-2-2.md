#9-6-2-2 建立Model


直接使用Sequelize虽然可以，但是存在一些问题。

团队开发时，有人喜欢自己加timestamp：

	var Pet = sequelize.define('pet', {
	    id: {
	        type: Sequelize.STRING(50),
	        primaryKey: true
	    },
	    name: Sequelize.STRING(100),
	    createdAt: Sequelize.BIGINT,
	    updatedAt: Sequelize.BIGINT
	}, {
	        timestamps: false
	    });
有人又喜欢自增主键，并且自定义表名：
	
	var Pet = sequelize.define('pet', {
	    id: {
	        type: Sequelize.INTEGER,
	        autoIncrement: true,
	        primaryKey: true
	    },
	    name: Sequelize.STRING(100)
	}, {
	        tableName: 't_pet'
	    });
一个大型Web App通常都有几十个映射表，一个映射表就是一个Model。如果按照各自喜好，那业务代码就不好写。Model不统一，很多代码也无法复用。

所以我们需要一个统一的模型，强迫所有Model都遵守同一个规范，这样不但实现简单，而且容易统一风格。

##Model

我们首先要定义的就是Model存放的文件夹必须在models内，并且以Model名字命名，例如：Pet.js，User.js等等。

其次，每个Model必须遵守一套规范：

1. 统一主键，名称必须是id，类型必须是STRING(50)；
2. 主键可以自己指定，也可以由框架自动生成（如果为null或undefined）；
3. 所有字段默认为NOT NULL，除非显式指定；
4. 统一timestamp机制，每个Model必须有createdAt、updatedAt和version，分别记录创建时间、修改时间和版本号。其中，createdAt和updatedAt以BIGINT存储时间戳，最大的好处是无需处理时区，排序方便。version每次修改时自增。

所以，我们不要直接使用Sequelize的API，而是通过db.js间接地定义Model。例如，User.js应该定义如下：

	const db = require('../db');
	
	module.exports = db.defineModel('users', {
	    email: {
	        type: db.STRING(100),
	        unique: true
	    },
	    passwd: db.STRING(100),
	    name: db.STRING(100),
	    gender: db.BOOLEAN
	});
这样，User就具有email、passwd、name和gender这4个业务字段。id、createdAt、updatedAt和version应该自动加上，而不是每个Model都去重复定义。

所以，db.js的作用就是统一Model的定义：

	const Sequelize = require('sequelize');
	
	console.log('init sequelize...');
	
	var sequelize = new Sequelize('dbname', 'username', 'password', {
	    host: 'localhost',
	    dialect: 'mysql',
	    pool: {
	        max: 5,
	        min: 0,
	        idle: 10000
	    }
	});
	
	const ID_TYPE = Sequelize.STRING(50);
	
	function defineModel(name, attributes) {
	    var attrs = {};
	    for (let key in attributes) {
	        let value = attributes[key];
	        if (typeof value === 'object' && value['type']) {
	            value.allowNull = value.allowNull || false;
	            attrs[key] = value;
	        } else {
	            attrs[key] = {
	                type: value,
	                allowNull: false
	            };
	        }
	    }
	    attrs.id = {
	        type: ID_TYPE,
	        primaryKey: true
	    };
	    attrs.createdAt = {
	        type: Sequelize.BIGINT,
	        allowNull: false
	    };
	    attrs.updatedAt = {
	        type: Sequelize.BIGINT,
	        allowNull: false
	    };
	    attrs.version = {
	        type: Sequelize.BIGINT,
	        allowNull: false
	    };
	    return sequelize.define(name, attrs, {
	        tableName: name,
	        timestamps: false,
	        hooks: {
	            beforeValidate: function (obj) {
	                let now = Date.now();
	                if (obj.isNewRecord) {
	                    if (!obj.id) {
	                        obj.id = generateId();
	                    }
	                    obj.createdAt = now;
	                    obj.updatedAt = now;
	                    obj.version = 0;
	                } else {
	                    obj.updatedAt = Date.now();
	                    obj.version++;
	                }
	            }
	        }
	    });
	}
我们定义的defineModel就是为了强制实现上述规则。

Sequelize在创建、修改Entity时会调用我们指定的函数，这些函数通过hooks在定义Model时设定。我们在beforeValidate这个事件中根据是否是isNewRecord设置主键（如果主键为null或undefined）、设置时间戳和版本号。

这么一来，Model定义的时候就可以大大简化。

##数据库配置

接下来，我们把简单的config.js拆成3个配置文件：

- config-default.js：存储默认的配置；
- config-override.js：存储特定的配置；
- config-test.js：存储用于测试的配置。

例如，默认的config-default.js可以配置如下：

	var config = {
	    dialect: 'mysql',
	    database: 'nodejs',
	    username: 'www',
	    password: 'www',
	    host: 'localhost',
	    port: 3306
	};

module.exports = config;
而config-override.js可应用实际配置：

	var config = {
	    database: 'production',
	    username: 'www',
	    password: 'secret-password',
	    host: '192.168.1.199'
	};

	module.exports = config;
config-test.js可应用测试环境的配置：

	var config = {
	    database: 'test'
	};
	
	module.exports = config;
读取配置的时候，我们用config.js实现不同环境读取不同的配置文件：

	const defaultConfig = './config-default.js';
	// 可设定为绝对路径，如 /opt/product/config-override.js
	const overrideConfig = './config-override.js';
	const testConfig = './config-test.js';
	
	const fs = require('fs');
	
	var config = null;
	
	if (process.env.NODE_ENV === 'test') {
	    console.log(`Load ${testConfig}...`);
	    config = require(testConfig);
	} else {
	    console.log(`Load ${defaultConfig}...`);
	    config = require(defaultConfig);
	    try {
	        if (fs.statSync(overrideConfig).isFile()) {
	            console.log(`Load ${overrideConfig}...`);
	            config = Object.assign(config, require(overrideConfig));
	        }
	    } catch (err) {
	        console.log(`Cannot load ${overrideConfig}.`);
	    }
	}
	
	module.exports = config;
具体的规则是：

1. 先读取config-default.js；
2. 如果不是测试环境，就读取config-override.js，如果文件不存在，就忽略。
3. 如果是测试环境，就读取config-test.js。

这样做的好处是，开发环境下，团队统一使用默认的配置，并且无需config-override.js。部署到服务器时，由运维团队配置好config-override.js，以覆盖config-override.js的默认设置。测试环境下，本地和CI服务器统一使用config-test.js，测试数据库可以反复清空，不会影响开发。

配置文件表面上写起来很容易，但是，既要保证开发效率，又要避免服务器配置文件泄漏，还要能方便地执行测试，就需要一开始搭建出好的结构，才能提升工程能力。

##使用Model

要使用Model，就需要引入对应的Model文件，例如：User.js。一旦Model多了起来，如何引用也是一件麻烦事。

自动化永远比手工做效率高，而且更可靠。我们写一个model.js，自动扫描并导入所有Model：

	const fs = require('fs');
	const db = require('./db');
	
	let files = fs.readdirSync(__dirname + '/models');
	
	let js_files = files.filter((f)=>{
	    return f.endsWith('.js');
	}, files);
	
	module.exports = {};
	
	for (let f of js_files) {
	    console.log(`import model from file ${f}...`);
	    let name = f.substring(0, f.length - 3);
	    module.exports[name] = require(__dirname + '/models/' + f);
	}
	
	module.exports.sync = () => {
	    db.sync();
	};
这样，需要用的时候，写起来就像这样：

	const model = require('./model');
	
	let
	    Pet = model.Pet,
	    User = model.User;
	
	var pet = await Pet.create({ ... });
##工程结构

最终，我们创建的工程model-sequelize结构如下：

	model-sequelize/
	|
	+- .vscode/
	|  |
	|  +- launch.json <-- VSCode 配置文件
	|
	+- models/ <-- 存放所有Model
	|  |
	|  +- Pet.js <-- Pet
	|  |
	|  +- User.js <-- User
	|
	+- config.js <-- 配置文件入口
	|
	+- config-default.js <-- 默认配置文件
	|
	+- config-test.js <-- 测试配置文件
	|
	+- db.js <-- 如何定义Model
	|
	+- model.js <-- 如何导入Model
	|
	+- init-db.js <-- 初始化数据库
	|
	+- app.js <-- 业务代码
	|
	+- start.js <-- 启动入口js
	|
	+- package.json <-- 项目描述文件
	|
	+- node_modules/ <-- npm安装的所有依赖包
注意到我们其实不需要创建表的SQL，因为Sequelize提供了一个sync()方法，可以自动创建数据库。这个功能在开发和生产环境中没有什么用，但是在测试环境中非常有用。测试时，我们可以用sync()方法自动创建出表结构，而不是自己维护SQL脚本。这样，可以随时修改Model的定义，并立刻运行测试。开发环境下，首次使用sync()也可以自动创建出表结构，避免了手动运行SQL的问题。

init-db.js的代码非常简单：

	require('babel-core/register')({
	    presets: ['stage-3']
	});
	
	const model = require('./model.js');
	model.sync();
	
	console.log('init db ok.');
	process.exit(0);
它最大的好处是避免了手动维护一个SQL脚本。

##参考源码

[model-sequelize](https://github.com/michaelliao/learn-javascript/tree/master/samples/node/web/db/model-sequelize)