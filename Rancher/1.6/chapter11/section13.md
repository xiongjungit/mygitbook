##密文 - 实验性的
Rancher支持创建密文并在容器中使用该密文（在容器中使用该密文需要部署应用商店里的Rancher Secrets服务）。Rancher通过对接加密后台来保障密文的安全。加密后台可以使用本地的AES密钥或者使用Vault Transit

###加密后台设置
默认情况下，Rancher Server会使用本地的AES256密钥来对密文进行加密。加密的密文存储在MySQL数据库里。

####使用VAULT TRANSIT
如果不想使用本地密钥加密，你可以通过配置Vault Transit来进行密文加密。

#####在RANCHER中配置VAULT TRANSIT
在安装Rancher Server之前，需要进行如下Vault Transit相关的配置。

1. 在要运行Rancher Server的主机上安装Vault transit后台。
2. 通过Vault命令行或者API，创建一个叫rancher的加密密钥。
3. 通过Vault命令行或者API，创建一个Vault访问口令，这个访问口令可以通过rancher加密密钥进行加密和解密。
 - 这个访问口令必须具有一个给Rancher Server使用的安全策略，来限制Rancher Server的访问权限。下面列表中的<KEY>就是之前创建的rancher加密密钥
	
	```
	path "transit/random/*" {
	  capabilities = ["create", "update"]
	}
	
	path "transit/hmac/*" {
	  capabilities = ["create", "update"]
	}
	
	path "transit/encrypt/rancher" {
	  capabilities = ["create", "update"]
	}
	
	path "transit/decrypt/rancher" {
	  capabilities = ["create", "update"]
	}
	
	path "transit/verify/rancher/*" {
	  capabilities = ["create", "update", "read"]
	}
	
	path "transit/keys/*" {
	  capabilities = ["deny"]
	}
	
	path "sys/*" {
	  capabilities = ["deny"]
	}
	```
4. 启动Rancher Server，并加入相关环境变量来连接Vault。
```
$ docker run -d --restart=unless-stopped -p 8080:8080 \
   -e VAULT_ADDR=https://<VAULT_SERVER> -e VAULT_TOKEN=<TOKEN_FOR_VAULT_ACCCESS> rancher/server
```
> 注意：
请检查运行的Rancher Server版本是否是你想要的。

5. 在Rancher服务启动成功之后，你需要修改Rancher中的service-backend设置。在系统管理 -> 系统设置 -> 高级设置中，找到secrets.backend。它的默认值是localkey，你可以把它修改为vault。

> 注意：
目前Rancher不支持对不同加密后台之间进行切换。

###创建密文
你可以在每个Rancher环境里创建密文。这也意味着，密文名称在环境中是唯一的。同一个环境下的任何容器都可以通过配置来共享密文。例如，一个数据库的密码db_password可以被用在数据库容器里，也可以被用在Wordpress容器里。一旦这个密文被创建了，这个密文的密文值就不能被修改了。如果你需要修改一个现有的密文，唯一的方法就是删除这个密文，然后再创建一个新密文。新密文被创建后，使用这个密文的服务需要重新部署。这样容器才能使用新的密文值。

####通过RANCHER命令行创建密文
在命令行当中有两种方法来创建密文。一种是在标准输入中（stdin）输入密文值，另一种是给命令行传递含有密文的文件名称。

#####通过标准输入（STDIN）创建密文
```
$ rancher secrets create name-of-secret - <<< secret-value
```

#####通过传递密文所在的文件名称来创建密文

```
$ echo secret-value > file-with-secret
$ rancher secrets create name-of-secret file-with-secret
```

###通过UI创建密文
点击基础架构 -> 密文。点击添加密文。输入名称和密文值然后点击保存。

###删除密文
> 备注：
目前Rancher命令行不支持删除密文。

你可以在UI里把密文从Rancher中删除，但是这并不会在已使用该密文的容器中删除该密文文件。如果一台主机上运行着使用该密文的容器，Rancher也不会在该主机上删除该密文文件。

###在RANCHER中启用密文
为了在容器中使用密文，你要先部署Rancher Secrets服务。你可以把这个服务加到环境模版中，在添加该服务之后部署的新环境里都会含有Rancher Secrets服务。你也可以直接通过应用商店部署该服务。如果你想在现有的环境中部署Rancher Secrets服务，你可以通过应用商店 -> 官方认证，然后搜索Rancher Secrets找到Rancher Secrets服务。如果不部署Rancher Secrets服务的话，你仅仅可以创建密文，但是不能在你的容器里使用这些密文。

###向服务／容器中添加密文
当密文被添加到容器中时，密文会被写到一个tmpfs卷中。你可以在容器里和主机上访问这个卷。

- 在使用该密文的容器中：这个卷被挂载在/run/secrets/.
- 在运行使用该密文的容器所在的主机上：这个卷被挂载在/var/lib/rancher/volumes/rancher-secrets/.

####通过RANCHER命令行添加密文到服务中
> 注意：
密文是在compose文件版本3中被引入的。由于Rancher不支持compose文件版本，所以我们在版本2中加入了密文功能。

你可以在docker-compose.yml里，通过配置服务的secrets值来指定一个或者多个密文。密文文件的名称与在Rancher中加入的密文名称相同。在默认情况下，将使用用户ID0和组ID0创建该密文文件，文件权限为0444。在secrets里将external设置为true确保Rancher知道该密文已经被创建成功了。

#####基础示例DOCKER-COMPOSE.YML
```
version: '2'
services:
  web:
    image: sdelements/lets-chat
    stdin_open: true
    secrets:
    - name-of-secret
    labels:
      io.rancher.container.pull_image: always
secrets:
  name-of-secret:
    external: true
```

如果你想要修改密文的默认配置，你可以用target来修改文件名，uid和gid来设置用户ID和组ID，mode来修改文件权限。

######修改密文文件配置示例DOCKER-COMPOSE.YML

```
version: '2'
services:
  web:
    image: sdelements/lets-chat
    stdin_open: true
    secrets:
    - source: name-of-secret
      target: different-target-filename
      uid: "1"
      gid: "1"
      mode: 0400
    labels:
      io.rancher.container.pull_image: always
secrets:
  name-of-secret:
    external: true
```

Racnher可以在创建应用的时候创建密文。你可以通过指定file参数，使Rancher在创建应用并启动服务之前创建密文。该密文值来自你指定的文件内容。

######指定多个密文并且在启动服务前创建密文的示例DOCKER-COMPOSE.YML

```
version: '2'
services:
  web:
    image: sdelements/lets-chat
    stdin_open: true
    secrets:
    - name-of-secret
    - another-name-of-secret
    labels:
      io.rancher.container.pull_image: always
secrets:
  name-of-secret:
    external: true
  another-name-of-secret:
    file: ./another-secret
```

####通过RANCHER UI添加密文到服务中
你可以在创建服务/容器页面的密文页里，向服务/容器中添加密文。

1. 点击添加密文
2. 下拉列表中会列出，已经加入到Rancher中的全部可用密文。你可以选择一个你想要使用的密文。
3. （可选操作） 默认情况下，挂载到容器内的密文文件的名称为密文名。你可以在映射名称栏，给容器中的密文文件设置一个不同的文件名。
4. （可选操作） 如果你想要修改默认的文件所有者和文件权限。你可以点击自定义文件所有者及权限链接来更新配置。你可以修改用户ID，组ID和文件权限。用户ID的默认值为0，组ID的默认值为0，文件权限的默认值为0444。
5. 点击 创建.

###DOCKER HUB镜像
Docker在很多自己的官方镜像中都支持通过文件来传递密文。你可以添加以_FILE结尾的环境变量名并且以/run/secrets/NAME>为值的环境变量，来达到这一效果。当在容器启动时，文件中的密文值将会被赋给去掉_FILE的环境变量里。

例如，当你部署一个MySQL容器的时候，你可以配置如下环境变量。

```
-e MYSQL_ROOT_PASSWORD_FILE=/run/secrets/db_password
```

MYSQL_ROOT_PASSWORD环境变量的值，就是你所指定这个文件的内容。这个文件就是我们在Rancher中添加的密文。这样你就可以很方便的从环境变量中获取在Rancher中配置的密文，而不用自己去读取密文文件。但并不是所有镜像都支持这个功能。

###已知的安全隐患

####被入侵的RANCHER SERVER容器
存储在Rancher中的密文和存储在CI系统（如Travis CI和Drone）中的密文安全程度是一样。由于加密密钥直接存储在Rancher Server容器中，所以如果Rancher Server容器被入侵，全部的密文都能被黑客获取到。Rancher将在以后的版本中努力降低这种情况的安全隐患。

> 注意：
如果你使用Vault进行加密，你需要创建一个策略来限制Rancher Server所用的token的访问权限。

####被入侵的主机
如果一台主机被入侵了，这台主机上所运行的容器中使用到的全部密文，都可以被读取。 但是黑客获取不到其他主机上的额外密文。

####容器访问
如果一个用户可以exec进入到容器中，该用户可以通过容器中挂载的卷查看到密文值。可以通过如下方式访问容器：

- UI点击”执行命令行”
- Rancher命令行工具
- Docker原生命令