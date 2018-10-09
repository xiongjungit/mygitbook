##Rancher Compose
Rancher Compose是一个多主机版本的Docker Compose。它运行于Rancher UI里属于一个环境多个主机的应用里。Rancher Compose启动的容器会被部署在满足调度规则的同一环境中的任意主机里。如果没有设置调度规则，那么这些服务容器会被调度至最少容器运行的主机上运行。这些被Rancher Compose启动的容器的运行效果是和在UI上启动的效果是一致的.

Rancher Compose工具的工作方式是跟Docker Compose的工作方式是相似的，并且兼容版本V1和V2的 docker-compose.yml 文件。为了启用Rancher的特性，你需要额外一份rancher-compose.yml文件，这份文件扩展并覆盖了docker-compose.yml文件。例如，服务缩放和健康检查这些功能就会在rancher-compose.yml中体现。

在阅读这份Rancher Compose文档之前，我们希望你已经懂得 Docker Compose 了。如果你还不认识 Docker Compose，请先阅读 Docker Compose文档。

###安装
Rancher Compose的可执行文件下载链接可以在UI的右下角中找到，我们为你提供了Windows, Mac 以及 Linux 版本供你使用。

另外，你也可以到Rancher Compose的发布页找到可执行二进制文件的下载链接。

###为 RANCHER COMPOSE 设置 RANCHER SERVER
为了让Rancher Compose可以在Rancher实例中启动服务，你需要设置一些环境变量或者在Rancher Compose命令中送一些参数。必要的环境变量分别是 RANCHER_URL, RANCHER_ACCESS_KEY, 以及 RANCHER_SECRET_KEY。 access key和secret key是一个环境API Keys, 可以在API -> 高级选项菜单中创建得到。

> 注意：
默认情况下，在API菜单下创建的是账号API Keys, 所以你需要在高级选项中创建环境API Keys.

```
# Set the url that Rancher is on
$ export RANCHER_URL=http://server_ip:8080/
# Set the access key, i.e. username
$ export RANCHER_ACCESS_KEY=<username_of_environment_api_key>
# Set the secret key, i.e. password
$ export RANCHER_SECRET_KEY=<password_of_environment_api_key>
```

如果你不想设置环境变量，那么你需要在Rancher Compose 命令中手动送入这些变量：

```
$ rancher-compose --url http://server_ip:8080 --access-key <username_of_environment_api_key> --secret-key <password_of_environment_api_key> up
```

现在你可以使用Rancher Compose 配合docker-compose.yml文件来启动服务了。这些服务会在环境API keys对应的环境中启动服务的。

就像Docker Compose，你可以在命令后面加上服务名称来选择启动全部或者仅启动指定某些docker-compose.yml中服务

```
$ rancher-compose up servicename1 servicename2
$ rancher-compose stop servicename2
```

###调试 RANCHER COMPOSE
你可以设置环境变量RANCHER_CLIENT_DEBUG的值为true来让Rancher Compose输出所有被执行的CLI命令。

```
# Print verbose messages for all CLI calls
$ export RANCHER_CLIENT_DEBUG=true
```

如果你不需要所有的 CLI 命令信息，你可以在命令后上--debug来指定输出哪些可视化CLI命令。

```
$ rancher-compose --debug up -d
```

###删除服务或容器
在缺省情况下，Rancher Compose不会删除任何服务或者容器。这意味着如果你在一行命令里执行两次 up 命令，那么第二个 up 命令不会起任何作用。这是因为第一个 up 命令会创建出所有东西后让他们自己运行。即使你没有在 up 中使用 -d 参数，Rancher Compose 也不会删除你任何服务。为了删除服务，你只能使用 rm 命令。

###构建
构建docker镜像可以有两种方法。第一种方法是通过给build命令一个git或者http URL参数来利用远程资源构建，另一种方法则是让 build 利用本地目录，那么会上传构建上下文到 S3 并在需要时在各个节点执行

为了可以基于S3来创建，你需要设置 AWS 认证。我们提供了一个说明怎样利用在Rancher Compose 里使用S3详细例子供你参考


##指令与参数
Rancher Compose 工具的工作方式是跟 Docker Compose 的工作方式是相似的，并且支持版本V1的 docker-compose.yml 文件。为了启用 Rancher 的特性，你需要额外一份rancher-compose.yml文件，这份文件扩展并覆盖了docker-compose.yml文件。例如，服务缩放和健康检查这些特性就会在rancher-compose.yml中体现。

###RANCHER-COMPOSE 命令
Rancher Compose 支持所有 Docker Compose 支持的命令。

|Name    |Description
|:-|:-|
|create  |创建所有服务但不启动
|up  |启动所有服务
|start   |启动服务
|logs    |输出服务日志
|restart |重启服务
|stop, down  |停止服务
|scale   |缩放服务
|rm  |删除服务
|pull    |拉取所有服务的镜像
|upgrade |服务之间进行滚动升级
|help, h |输出命令列表或者指定命令的帮助列表

###RANCHER COMPOSE 选项
无论何时你使用 Rancher Compose 命令，这些不同的选项你都可以使用

|Name    |Description
|:-|:-|
|--verbose, --debug|-|
|--file, -f [–file option –file option]  |指定一个compose 文件 (默认: docker-compose.yml) [$COMPOSE_FILE]
|--project-name, -p  |指定一个项目名称 (默认: directory name)
|--url   |执行 Rancher API接口 URL [$RANCHER_URL]
|--access-key    |指定 Rancher API access key [$RANCHER_ACCESS_KEY]
|--secret-key    |指定 Rancher API secret key [$RANCHER_SECRET_KEY]
|--rancher-file, -r  |指定一个 Rancher Compose 文件 (默认: rancher-compose.yml)
|--env-file, -e  |指定一个环境变量配置文件
|--help, -h  |输出帮助文本
|--version, -v   |输出 Rancher Compose 版本

####例子
准备开始后，你需要创建一个 docker-compose.yml 文件和一个可选的 rancher-compose.yml 文件，如果没有 rancher-compose.yml 文件，那么所有服务默认只分配1个容器

#####样例文件 DOCKER-COMPOSE.YML

```
version: '2'
services:
  web:
    image: nginx
  db:
    image: mysql
    environment:
      MYSQL_ROOT_PASSWORD: test
```

#####样例文件 RANCHER-COMPOSE.YML

```
# Reference the service that you want to extend
version: '2'
services:
  web:
    scale: 2
  db:
    scale: 1
```

当你的这些文件创建好后，你就可以启动这些服务到 Rancher 服务了

```
# Creating and starting services without environment variables and selecting a stack
# If the stack does not exist in Rancher, it will be created in Rancher
$ rancher-compose --url URL_of_Rancher --access-key <username_of_environment_api_key> --secret-key <password_of_environment_api_key> -p stack1 up

# Creating and starting services with environment variables already set
$ rancher-compose -p stack1 up

# To change the scale of an existing service
$ rancher-compose -p stack1 scale web=3

# To launch a specific service in the docker-compose.yml
$ rancher-compose -p stack1 up web
```

> 注意：
如果你没有传入 -p <STACK_NAME>，应用名就是你执行Rancher Compose命令所在的文件夹名称。

####使用 --ENV-FILE 选项
当你运行 Rancher Compose 命令时，可以使用--env-file 选项传入一个环境变量配置文件。

#####样例 SECRETS 文件

```
MYSQL_ROOT_PASSWORD=test
```

#####样例文件 DOCKER-COMPOSE.YML

```
version: '2'
services:
  db:
    image: mysql
    environment:
    # Just like Docker Compose, if there is only a key, Rancher Compose will resolve to
    # the values on the machine or the file passed in using --env-file
      MYSQL_ROOT_PASSWORD:
```

你可以启动服务时传入 secrets 文件

```
$ rancher-compose --env-file secrets up -d
```

在传入一个文件并一个环境变量只含一个key，Rancher Compose 将从这个文件或者从运行 Rancher Compose 命令的机器中的系统环境变量中提取这个值。当在文件和系统环境变量中同时存在同一个变量时，Rancher Compose 使用文件中的值。

###命令选项

####UP命令
|Name    |Description
|:-|:-|
|--pull, -p  |升级前先在各个已有这个镜像的主机拉取最新镜像
|-d  |不要阻塞或输出日志
|--upgrade, -u, --recreate   |当服务改变时升级
|--force-upgrade, --force-recreate   |强制升级服务，不管服务是否改变
|--confirm-upgrade, -c   |确认升级成功并删除老容器
|--rollback, -r  |回滚到上一个已部署的版本
|--batch-size "2"    |每次升级多少个容器
|--interval "1000"   |升级间隔

当你运行 Rancher Compose 的 up 命令时，在所有任务完成后进程会继续运行。如果你希望任务完成后进程退出，那么你需要传入 -d 选项，防止阻塞和输出日志。

```
# If you do not use the -d flag, Rancher Compose will continue to run until you Ctrl+C to quit
$ rancher-compose up

# Use the -d flag for rancher-compose to exit after running
$ rancher-compose up -d
```

阅读更多关于 利用Rancher Compose升级服务.

####START命令
|Name    |Description
|:-|:-|
|-d  |防止阻塞或输出日志

如果你希望任务完成后进程退出，那么你需要传入 -d 选项，防止阻塞和输出日志。

#####LOGS命令
|Name    |Description
|:-|:-|
|--follow    |持续输出日志

#####RESTART命令
|Name    |Description
|:-|:-|
|--batch-size "1"    |每次重启多少个容器
|--interval "0"  |重启间隔


缺省情况下，Rancher Compose 会顺序地逐个重启服务。你可以设置批量大小和重启间隔。

#####STOP 与 SCALE
|Name    |Description
|:-|:-|
|--timeout, -t "10"  |指定停止超时秒数


```
# To change the scale of an existing service
$ rancher-compose -p stack1 scale service1=3
```

#####RM 命令
|Name    |Description
|:-|:-|
|--force, -f |允许删除所有服务
|-v  |同时移除关联的容易


当移除服务时，Rancher Compose 仅移除在 docker-compose.yml 文件中出现的服务。如果有其他的服务在Rancher 的 stack 里，他们不会被移除，因为 Rancher Compose 不知道他们的存在。

所以 stack 不会被移除，因为 Rancher Compose 不知道stack 里是否还有其他容器。

缺省情况下，附加到容器的卷不会被移除。你可以通过 docker volume ls 查看所有的卷。

#####PULL 命令
|Name    |Description
|:-|:-|
|--cached, -c    |只更新存在该镜像缓存的主机，不要拉取新的


```
# Pulls new images for all services located in the docker-compose.yml file on ALL hosts in the environment
$ rancher-compose pull

# Pulls new images for all services located in docker-compose.yml file on hosts that already have the image
$ rancher-compose pull --cached
```

> 注意：
不同于 docker-compose pull, 你不可以指定拉取哪些服务的镜像，Rancher Compose 会拉取所有在 docker-compose.yml 里的服务镜像。

#####UPGRADE 命令
你可以使用 Rancher Compose 升级在 Rancher 里的服务。请阅读更多关于在何时和怎样更新你的服务.

###删除服务／容器
默认情况下，Rancher Compose 不会删除任何东西。 这意味着如果你在一行里有两个 up 命令，第二个 up 是不会做任何事情的。这是因为第一个 up 会创建所有东西并保持运行。甚至你没有传 -d 给 up，Rancher Compose 也不会删除你的服务。要删除服务，你只能使用 rm 。

##环境插值
在使用 Rancher Compose 时，docker-compose.yml 和 rancher-compose.yml 文件中可以使用运行 Rancher Compose 的机器中的环境变量。
这个特性只在 Rancher Compose 命令中有效，在 Rancher UI 中是没有这个特性的。

###怎么使用
在 docker-compose.yml 和 rancher-compose.yml 文件中，你可以引用你机器中的环境变量。如果没有该环境变量，它的值会被替换为空字符串，请注意的是 Rancher Compose 不会自动去除 : 两侧的空字符来适配相近的镜像。例如 `<imagename>`: 是一个非法的镜像名称，不能部署出容器。它需要用户自己来保证环境变量在该机器上是存在并有效的。

####例子
在我们运行 Rancher Compose 的机器上有一个这样的环境变量，IMAGE_TAG=14.04 。

```
# Image tag is set as environment variable
$ env | grep IMAGE
IMAGE_TAG=14.04
# Run Rancher Compose
$ rancher-compose up
```

####样例文件 docker-compose.yml

```
version: '2'
services:
  ubuntu:
    tty: true
    image: ubuntu:$IMAGE_TAG
    stdin_open: true
```

在 Rancher 里，一个 ubuntu 服务会使用镜像 ubuntu:14.04 部署。

###环境插值格式
Rancher Compose 支持和 Docker Compose 一样的格式。

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

##利用 AWS S3 构建
构建 docker 镜像可以有两种方法。第一种方法是通过给 build 命令一个 git 或者 http URL参数来利用远程资源构建，另一种方法则是让 build 利用本地目录，那么会上传构建上下文到 S3 并在需要时在各个节点执行

###前置条件
- Docker
- Rancher Compose
- AWS 账户
- Rancher Server 和1台主机

在我们这个例子里，我们会在docker-compose.yml里定义我们的应用，并且把这个文件放在composetest下。这个compose文件会定义个web服务，它会打开5000端口并映射到主机上，还会链接redis服务，这样可以让在web中运行的服务可以通过redis这个主机名来访问redis容器

```
version: '2'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    links:
      - redis

  redis:
    image: redis
```

我们还会添加一个 rancher-compose.yml 到同一个 composetest 目录下来使用 Rancher的缩放能力。缺省情况下，如果没有rancher-compose.yml文件或者服务在rancher-compose.yml中没有定义，那么容器数量默认为1个。

```
version: '2'
services:
  web:
    scale: 3
```

当提供给 Rancher Compose 的这些文件准备好后，下一步就是实现这个程序并按照步骤来构建它。

使用docker-compose文档中的例子，我们会创建一个名为app.py的文件。这个应用会访问一个名为redis的主机，这个主机会运行 redis KV 存储服务。它会递增redis 中的键为 hits 的键值，然后取回这个值。

```
from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    redis.incr('hits')
    return 'Hello World! I have been seen %s times.' % redis.get('hits')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
```

这个应用会依赖两个库，所以我们同时会创建一个名为 requirements.txt 的文件。

```
flask
redis
```

现在我们会在Dockerfile文件中定义应用的构建步骤。在Dockerfile文件里的指令会定义出要怎么构建出这个应用容器。

```
FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD python app.py
```

因为你已经运行着Rancher Server了，所以你只需要配置好你 AWS 认证信息，然后用你的 Rancher Server URL 和API key来运行 Rancher Compose 。

```
# Set up your AWS credentials
$ aws configure
AWS Access Key ID []: AWS_ACCESS_KEY
AWS Secret Access Key []: AWS_SECRET_KEY
Default region name []: NOT_NEEDED_FOR_S3
Default output format [None]:
# Run rancher-compose in your composetest directory where all the files are created
$ rancher-compose --url URL_of_Rancher --access-key username_of_API_key --secret-key password_of_API_key up
```

根据上面的指令，这个 web 容器会在一台 Rancher Server 管理的主机上运行起来。rancher-compose 会先上传当前目录到 S3，而你可以到 S3的 UI 上检索到这个目录。当镜像上传成功后，它会下载这个些文件到主机上构建起一个容器。

###问题解答
如果你在利用S3构建时出现了一些问题，你可以先在本机测试一下是否可以构建并运行。在你运行rancher-compose的同一目录下，使用下面的命令来校验是否在 docker 中可以正常工作。

```
# Test building locally to see if works
$ docker build -t test .
# Test running the newly built image
$ docker run test
```