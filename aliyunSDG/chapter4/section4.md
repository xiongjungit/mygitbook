数据库管理人员可以参考本文档进行 MySQL 数据库系统的安全配置加固，提高数据库的安全性，确保数据库服务稳定、安全、可靠地运行。

#漏洞发现

您可以使用安骑士企业版自动检测您的服务器上是否存在 MySQL 漏洞问题，或者您也可以自己排查您服务器上的 MySQL 服务是否存在安全问题。

#安全加固

##1. 帐号安全

###禁止 Mysql 以管理员帐号权限运行

以普通帐户安全运行 mysqld，禁止以管理员帐号权限运行 MySQL 服务。在 /etc/my.cnf 配置文件中进行以下设置。

```
[mysql.server]
user=mysql
```

###避免不同用户间共享帐号

参考以下步骤。

a. 创建用户。

```
mysql> mysql> insert into
mysql.user(Host,User,Password,ssl_cipher,x509_issuer,x509_sub 
ject) values("localhost","pppadmin",password("passwd"),'','','');
```

执行以上命令可以创建一个 phplamp 用户。

b. 使用该用户登录 MySQL 服务。

```
mysql>exit; 
@>mysql -u phplamp -p 
@>输入密码 
mysql>登录成功
```

###删除无关帐号

DROP USER 语句可用于删除一个或多个 MySQL 账户。使用 DROP USER 命令时，必须确保当前账号拥有 MySQL 数据库的全局 CREATE USER 权限或 DELETE 权限。账户名称的用户和主机部分分别与用户表记录的 User 和 Host 列值相对应。

执行DROP USER user;语句，您可以取消一个账户和其权限，并删除来自所有授权表的帐户权限记录。

##2. 口令

检查账户默认密码和弱密码。口令长度需要至少八位，并包括数字、小写字母、大写字母和特殊符号四类中的至少两种类型，且五次以内不得设置相同的口令。密码应至少每 90 天进行一次更换。

您可以通过执行以下命令修改密码。

```
mysql> update user set password=password('test!p3') where user='root';
mysql> flush privileges;
```

##3. 授权

在数据库权限配置能力范围内，根据用户的业务需要，配置其所需的最小权限。

查看数据库授权情况。

```
mysql> use mysql;
mysql> select * from user;
mysql>select * from db;
mysql>select * from host;
mysql>select * from tables_priv;
mysql>select * from columns_priv;
```

通过 revoke 命令回收不必要的或危险的授权。

```
mysql> help revoke
Name: 'REVOKE'
Description:
Syntax:
REVOKE
priv_type [(column_list)]
   [, priv_type [(column_list)]] ...
 ON [object_type]
     {
         *
       | *.*
       | db_name.*
       | db_name.tbl_name
       | tbl_name
       | db_name.routine_name
     }
 FROM user [, user] ...
```

##4. 开启日志审计功能

数据库应配置日志功能，便于记录运行状况和操作行为。

MySQL服务有以下几种日志类型：

- 错误日志： -log-err
- 查询日志： -log （可选）
- 慢查询日志： -log-slow-queries （可选）
- 更新日志： -log-update
- 二进制日志： -log-bin

找到 MySQL 的安装目录，在 my.ini 配置文件中增加上述所需的日志类型参数，保存配置文件后，重启 MySQL 服务即可启用日志功能。例如，

```
#Enter a name for the binary log. Otherwise a default name will be used. 
#log-bin= 
#Enter a name for the query log file. Otherwise a default name will be used. 
#log= 
#Enter a name for the error log file. Otherwise a default name will be used. 
log-error= 
#Enter a name for the update log file. Otherwise a default name will be used. 
#log-update=
```

该参数中启用错误日志。如果您需要启用其他的日志，只需把对应参数前面的 “#” 删除即可。

日志查询操作说明

```
执行show variables like 'log_%';命令可查看所有的 log。
执行show variables like 'log_bin';命令可查看具体的 log。
```

##5. 安装最新补丁

确保系统安装了最新的安全补丁。

注意： 在保证业务及网络安全的前提下，并经过兼容性测试后，安装更新补丁。

##6. 如果不需要，应禁止远程访问

禁止网络连接，防止猜解密码攻击、溢出攻击、和嗅探攻击。

注意： 仅限于应用和数据库在同一台主机的情况。

如果数据库不需要远程访问，可以禁止远程 TCP/IP 连接，通过在 MySQL 服务器的启动参数中添加--skip-networking参数使 MySQL 服务不监听任何 TCP/IP 连接，增加安全性。

您可以使用 安全组 进行内外网访问控制，建议不要将数据库高危服务对互联网开放。

##7. 设置可信 IP 访问控制

通过数据库所在操作系统的防火墙限制，实现只有信任的 IP 才能通过监听器访问数据库。

```
mysql> GRANT ALL PRIVILEGES ON db.*
·-> -> TO 用户名@'IP子网/掩码';
```

##8. 连接数设置

根据您的机器性能和业务需求，设置最大、最小连接数。

在 MySQL 配置文件（my.conf 或 my.ini）的 [mysqld] 配置段中添加max_connections = 1000，保存配置文件，重启 MySQL 服务后即可生效。