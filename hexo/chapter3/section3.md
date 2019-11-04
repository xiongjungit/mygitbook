{% raw %}
# 部署

Hexo 提供了快速方便的一键部署功能，让您只需一条命令就能将网站部署到服务器上。

```
$ hexo deploy
```

在开始之前，您必须先在 `_config.yml` 中修改参数，一个正确的部署配置中至少要有 `type` 参数，例如：

```
deploy:
  type: git
```

您可同时使用多个 deployer，Hexo 会依照顺序执行每个 deployer。

```
deploy:
- type: git
  repo:
- type: heroku
  repo:
```

> 缩进
>
> YAML依靠缩进来确定元素间的从属关系。因此，请确保每个deployer的缩进长度相同，并且使用空格缩进。

## Git

安装 [hexo-deployer-git](https://github.com/hexojs/hexo-deployer-git)。

```
$ npm install hexo-deployer-git --save
```

修改配置。


```
deploy:
  type: git
  repo: <repository url> #https://bitbucket.org/JohnSmith/johnsmith.bitbucket.io
  branch: [branch] #published
  message: [message]
```


| 参数      | 描述|
| :-------- | :--------------------------------|
| `repo`    | 库（Repository）地址|
| `branch`  | 分支名称。如果不指定，则默认值为 master|
| `message` | 自定义提交信息 (默认为 `Site updated: {{ now('YYYY-MM-DD HH:mm:ss') }}`) |



生成站点文件并推送至远程库。执行 `hexo clean && hexo deploy` 命令（如果您并未全局安装 Hexo Cli，则需要执行 `./node_modules/.bin/hexo clean && ./node_modules/.bin/hexo deploy`）

登入 Github/BitBucket/Gitlab，请在库设置（Repository Settings）中将默认分支设置为`_config.yml`配置中的分支名称。稍等片刻，您的站点就会显示在您的Github Pages中。

### 这一切是如何发生的？

当执行 `hexo deploy` 时，Hexo 会将 `public` 目录中的文件和目录推送至 `_config.yml` 中指定的远端仓库和分支中，并且**完全覆盖**该分支下的已有内容。

> For 使用 Git 管理站点目录的用户
>
> 由于 Hexo 的部署默认使用分支 `master`，所以如果你同时正在使用 Git 管理你的站点目录，你应当注意你的部署分支应当不同于写作分支。
> 一个好的实践是将站点目录和 Pages 分别存放在两个不同的 Git 仓库中，可以有效避免相互覆盖。
> Hexo 在部署你的站点生成的文件时并不会更新你的站点目录。因此你应该手动提交并推送你的写作分支。



此外，如果您的 Github Pages 需要使用 CNAME 文件**自定义域名**，请将 CNAME 文件置于 `source` 目录下，只有这样 `hexo deploy` 才能将 CNAME 文件一并推送至部署分支。

## Heroku

安装 [hexo-deployer-heroku](https://github.com/hexojs/hexo-deployer-heroku)。

```
$ npm install hexo-deployer-heroku --save
```

修改配置。

```
deploy:
  type: openshift
  repo: <repository url>
  message: [message]
```

| 参数      | 描述                                                         |
| :-------- | :----------------------------------------------------------- |
| `repo`    | Heroku 库（Repository）地址                                  |
| `message` | 自定提交信息 (默认为 `Site updated: {{ now('YYYY-MM-DD HH:mm:ss') }}`) |

## Netlify

[Netlify](https://www.netlify.com/) 是一个提供网络托管的综合平台。它集持续集成（CI）CDN 自定义域名 HTTPS 持续部署（CD）等诸多功能于一身。您可以通过以下两种方式将Hexo站点部署到Netlify。

首先，也是最通用的方式，就是使用Netlify提供的网页端用户界面。前往[新建一个网站页面](https://app.netlify.com/start)，选择需要关联的 Github/BitBucket/Gitlab 库，然后遵循网站提示。



另一种方式是使用Netlify提供的命令行客户端工具 [Node based CLI](https://www.netlify.com/docs/cli/) 管理和部署您的站点。

此外，您还可以在项目的README中增加一个 [部署至Netlify按钮](https://www.netlify.com/docs/deploy-button/)，这样其他用户在fork或clone了您的项目之后可以方便快捷地一键部署。

## Rsync

安装 [hexo-deployer-rsync](https://github.com/hexojs/hexo-deployer-rsync)。

```
$ npm install hexo-deployer-rsync --save
```

修改配置。

```
deploy:
  type: ftpsync
  host: <host>
  user: <user>
  pass: <password>
  remote: [remote]
  port: [port]
  ignore: [ignore]
  connections: [connections]
  verbose: [true|false]
```

| 参数            | 描述                   | 默认值 |
| :-------------- | :--------------------- | :----- |
| `host`          | 远程主机的地址         |        |
| `user`          | 使用者名称             |        |
| `root`          | 远程主机的根目录       |        |
| `port`          | 端口                   | 22     |
| `delete`        | 删除远程主机上的旧文件 | true   |
| `verbose`       | 显示调试信息           | true   |
| `ignore_errors` | 忽略错误               | false  |

> rsync部署模块的工作方式
>
> 需要注意的是，要求您提供的实际上是一个能通过SSH登陆远程主机的Linux用户。Hexo会自动处理关于rsync使用的一切操作。因此，您需要在远程主机上为您的Hexo站点建立一个用户，并允许其通过SSH登陆。不过，这里的`port`，的确是指rsync监听的端口，请确保防火墙打开了该端口。

## OpenShift

安装 [hexo-deployer-openshift](https://github.com/hexojs/hexo-deployer-openshift)。

```
$ npm install hexo-deployer-openshift --save
```

修改配置。

```
deploy:
  type: openshift
  repo: <repository url>
  message: [message]
```

| 参数      | 描述                                                         |
| :-------- | :----------------------------------------------------------- |
| `repo`    | OpenShift 库（Repository）地址                               |
| `message` | 自定提交信息 |

## FTPSync

安装 [hexo-deployer-ftpsync](https://github.com/hexojs/hexo-deployer-ftpsync)。

```
$ npm install hexo-deployer-ftpsync --save
```

修改配置。

```
deploy:
  type: ftpsync
  host: <host>
  user: <user>
  pass: <password>
  remote: [remote]
  port: [port]
  ignore: [ignore]
  connections: [connections]
  verbose: [true|false]
```

| 参数          | 描述             | 默认值 |
| :------------ | :--------------- | :----- |
| `host`        | 远程主机的地址   |        |
| `user`        | 使用者名称       |        |
| `pass`        | 密码             |        |
| `remote`      | 远程主机的根目录 | `/`    |
| `port`        | 端口             | 21     |
| `ignore`      | 忽略的文件或目录 |        |
| `connections` | 使用的连接数     | 1      |
| `verbose`     | 显示调试信息     | false  |

> FTP部署可能出现的问题
>
> 您可能需要预先通过其他方式将所有文件上传到远程主机中。否则初次使用ftpsync插件就可能出现报错。另外，由于FTP协议的特征，它每传送一个文件就需要一次握手，相对速度较慢。

## SFTP

安装 [hexo-deployer-sftp](https://github.com/lucascaro/hexo-deployer-sftp)。

```
$ npm install hexo-deployer-sftp --save
```

修改配置。

```
deploy:
  type: sftp
  host: <host>
  user: <user>
  pass: <password>
  remotePath: [remote path]
  port: [port]
  privateKey: [path/to/privateKey]
  passphrase: [passphrase]
  agent: [path/to/agent/socket]
```

| 参数         | 描述                        | 默认值           |
| :----------- | :-------------------------- | :--------------- |
| `host`       | 远程主机的地址              |                  |
| `user`       | 使用者名称                  |                  |
| `pass`       | 密码                        |                  |
| `remotePath` | 远程主机的根目录            | `/`              |
| `port`       | 端口                        | 22               |
| `privateKey` | ssh私钥的目录地址           |                  |
| `passphrase` | （可省略）ssh私钥的密码短语 |                  |
| `agent`      | ssh套接字的目录地址         | `$SSH_AUTH_SOCK` |

## 其他方法

Hexo 生成的所有文件都放在 `public` 文件夹中，您可以将它们复制到您喜欢的地方。
{% endraw %}