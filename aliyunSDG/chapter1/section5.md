为了确保 OpenSSL 的安全，建议用户升级 OpenSSL 版本到官方最新版本。本文介绍了具体的升级方法。

#升级 OpenSSL
打开 shell 运行命令行。

#使用源更新 OpenSSL
对于Linux/CentOS 服务器，以 root 权限运行以下命令：
```
sudo yum update openssl
```

对于 Ubuntu Server/Debain 服务器，以 root 权限运行以下命令：

```
sudo apt-get update
sudo apt-get upgrade
```

#使用编译安装更新 OpenSSL

下载最新版本 OpenSSL（以 openssl-1.1.0e 为例）。

注意：以下编译升级操作存在风险，建议由专业技术人员来操作。

以 root 权限运行以下命令：

```
wget https://www.openssl.org/source/openssl-1.1.0e.tar.gz 
tar zxvf openssl-1.1.0e.tar.gz
cd openssl-1.1.0e
./config shared zlib
make
make install
# 替换旧版 OpenSSL
mv /usr/bin/openssl /usr/bin/openssl.old
mv /usr/include/openssl /usr/include/openssl.old
ln -s /usr/local/bin/openssl /usr/bin/openssl
ln -s /usr/local/include/openssl/ /usr/include/openssl
```

#检查 OpenSSL 版本
以 root 权限运行 openssl version -a 命令，系统会返回 OpenSSL 版本信息，如下所示。

```
OpenSSL 1.1.0e  16 Feb 2017
built on: reproducible build, date unspecified
platform: linux-x86_64
compiler: gcc -DZLIB -DDSO_DLFCN -DHAVE_DLFCN_H -DNDEBUG -DOPENSSL_THREADS -DOPENSSL_NO_STATIC_ENGINE -DOPENSSL_PIC -DOPENSSL_IA32_SSE2 -DOPENSSL_BN_ASM_MONT -DOPENSSL_BN_ASM_MONT5 -DOPENSSL_BN_ASM_GF2m -DSHA1_ASM -DSHA256_ASM -DSHA512_ASM -DRC4_ASM -DMD5_ASM -DAES_ASM -DVPAES_ASM -DBSAES_ASM -DGHASH_ASM -DECP_NISTZ256_ASM -DPADLOCK_ASM -DPOLY1305_ASM -DOPENSSLDIR="\"/usr/local/ssl\"" -DENGINESDIR="\"/usr/local/lib/engines-1.1\""  -Wa,--noexecstack
OPENSSLDIR: "/usr/local/ssl"
ENGINESDIR: "/usr/local/lib/engines-1.1"
```

了解更多：[OpenSSL 官方漏洞信息公告](https://www.openssl.org/news/vulnerabilities.html?spm=5176.7752154.2.3.OgbOGo)。