gitbook 网站生成的 pdf 中文字体非常难看，字体大小不一。

解决办法是手工指定中文字体，指定 pdf 文字大小。

book.json 例子：

```
{
  "gitbook": "2.x.x",
  "title": "Go语言圣经",
  "description": "<The Go Programming Language>中文版",
  "language": "zh",
  "structure": {
    "readme": "preface.md"
  },
  "pluginsConfig": {
    "fontSettings": {
      "theme": "white",
      "family": "msyh",
      "size": 2
    },
    "plugins": [
      "yahei",
      "katex",
      "-search"
    ]
  },
  "pdf": {
    "pageNumbers": true,
    "fontSize": 18,
    "paperSize": "a4",
    "margin": {
      "right": 30,
      "left": 30,
      "top": 30,
      "bottom": 50
    }
  }
}
```

例子使用的 微软雅黑 字体，默认linux下没有这个字体，需要手工将字体拷贝到 /usr/share/fonts/truetype 目录。

#gitbook其他设置

当我们在gitbook.com上建好书籍后，我们可以为书籍进行封面，主题，配置域名等设置。

**封面**：在gitbook在线编辑器设置按钮下添加封面或者直接书籍仓库的根目录下放置一个cover.jpg即可

**主题**：在gitbook.com书籍页面的setting页面有landing page选项用于设置主题

**配置域名**：gitbook.com上书籍setting页面选择domains，设置homepage和content的域名。在书籍目录编译后的_book下添加一个CNAME文件，添加好域名即可！ 

**书籍左边sidebar**：在book.json的sidebar key 下设置，见上方配置代码

**发布到github pages**：链接：发布到 GitHub Pages

**本地转换为pdf等格式**：
