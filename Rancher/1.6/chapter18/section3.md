##变量替换
使用rancher up时，可以在docker-compose.yml和rancher-compose.yml文件中使用运行rancher命令的机器中的环境变量。 这仅仅在rancher命令中支持，在Rancher UI中不支持。

###如何使用
通过使用docker-compose.yml和rancher-compose.yml文件，你可以引用机器上的环境变量。 如果机器上没有环境变量，它将用空白字符串替换。 Rancher将会提示一个警告，指出哪些环境变量没有设置。 如果使用环境变量作为镜像标签时，请注意，rancher不会从镜像中自动删除：来获取latest镜像。 因为镜像名，比如<镜像名>：是一个无效的镜像名，所以不会部署成功。用户需要确定机器中所有的环境变量的有效性。

例子

在我们运行rancher的机器上，我们有一个环境变量IMAGE_TAG = 14.04。

```
# Image tag is set as environment variable
$ env | grep IMAGE
IMAGE_TAG=14.04
# Run rancher
$ rancher up
```

例子： docker-compose.yml

```
version: '2'
services:
  ubuntu:
    tty: true
    image: ubuntu:$IMAGE_TAG
    stdin_open: true
```

在Rancher中，一个ubuntu服务将使用ubuntu:14.04镜像来部署。

####变量替换格式
Rancher支持与’docker-compose’相同的格式。

```
version: '2'
services:
  web:
    # unbracketed name
    image: "$IMAGE"

    # bracketed name
    command: "${COMMAND}"

    # array element
    ports:
    - "${HOST_PORT}:8000"

    # dictionary item value
    labels:
      mylabel: "${LABEL_VALUE}"

    # unset value - this will expand to "host-"
    hostname: "host-${UNSET_VALUE}"

    # escaped interpolation - this will expand to "${ESCAPED}"
    command: "$${ESCAPED}"
```

####模板
在docker-compose.yml里面，Rancher能够支持使用Go模板系统，这样我们可以在docker-compose.yml里面使用逻辑条件语句。

模板可以与Rancher CLI一起使用，也可以与应用商店组合使用，这样可以让你配置你的应用商店模板，也可以让你根据答案来改变你的模板文件。

> 注意：
目前我们只支持对string的比较。

例子

如果你希望能够生成一个在内部暴露端口或者在外部暴露端口的服务，那么你可以设置逻辑条件来实现这样的功能。 在这个例子中，如果public变量设置为ture，那么ports下面的8000端口将对外开放。 否则，这些端口将在expose下开放。在我们的示例中，默认值为true。

docker-compose.yml

```
version: '2'
services:
  web:
    image: nginx
    \{\{- if eq .Values.PUBLIC "true" \}\}
    ports:
    - 8000
    \{\{- else \}\}
    expose:
    - 8000
    \{\{- end \}\}
```

rancher-compose.yml

```
version: '2'
catalog:
  name: Nginx Application
  version: v0.0.1
  questions:
  - variable: PUBLIC
    label: Publish Ports?
    required: true
    default: true
    type: boolean
```

config.yml

```
name: "Nginx Application"
version: v0.0.1
```

####应用栈名称替换
从Rancher v1.6.6开始，我们支持在docker-compose.yml文件中替换 \{\{ .Stack.Name \}\} 。这样可以在compose文件中使用应用栈名称。

Docker Compose文件可以用于创建新的应用栈，可以通过Rancher命令行或UI来创建。 如下面中的例子，你可以创建一个基于应用栈名称的标签。

示例 DOCKER-COMPOSE.YML

```
version: '2'
services:
  web:
    image:  nginx
    labels:
      stack-name: \{\{ .Stack.Name \}\}
```

如果你通过Rancher命令行来创建应用，例如rancher up -s myawesomestack -f docker-compose.yml，那么这个应用将会创建一个带有标签stack-name=myawesomestack的服务。

> 注意：
替换只是发生在应用栈创建时，之后对应用名称的修改无法触发替换。

####双括号使用
随着Rancher引入了模板系统，双括号 (\{\{ or \}\}) 将被视为模板的一部分。如果你不想将这些字符转换为模板，你可以在包含字符的compose文件的顶部添加上＃notemplating。

```
# notemplating

version: '2'
services:
  web:
    image: nginx
    labels:
      key: "\{\{`\{\{ value \}\}`\}\}"
```