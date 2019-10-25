# 生成文件



使用 Hexo 生成静态文件快速而且简单。

```
$ hexo generate
```

### 监视文件变动

Hexo 能够监视文件变动并立即重新生成静态文件，在生成时会比对文件的 SHA1 checksum，只有变动的文件才会写入。

```
$ hexo generate --watch
```

### 完成后部署

您可执行下列的其中一个命令，让 Hexo 在生成完毕后自动部署网站，两个命令的作用是相同的。

```
$ hexo generate --deploy
$ hexo deploy --generate
```

> 简写
>
> 上面两个命令可以简写为
> 
> $ hexo g -d
> 
> $ hexo d -g

