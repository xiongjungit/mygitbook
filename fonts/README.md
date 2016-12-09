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
