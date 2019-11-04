{% raw %}

# 标签插件（Tag Plugins）



标签插件和 Front-matter 中的标签不同，它们是用于在文章中快速插入特定内容的插件。

## 引用块

在文章中插入引言，可包含作者、来源和标题。

**别号：** quote

```
{% blockquote [author[, source]] [link] [source_link_title] %}
content
{% endblockquote %}
```

### 样例

**没有提供参数，则只输出普通的 blockquote**

```
{% blockquote %}
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque hendrerit lacus ut purus iaculis feugiat. Sed nec tempor elit, quis aliquam neque. Curabitur sed diam eget dolor fermentum semper at eu lorem.
{% endblockquote %}
```

> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque hendrerit lacus ut purus iaculis feugiat. Sed nec tempor elit, quis aliquam neque. Curabitur sed diam eget dolor fermentum semper at eu lorem.

**引用书上的句子**

```
{% blockquote David Levithan, Wide Awake %}
Do not just seek happiness for yourself. Seek happiness for all. Through kindness. Through mercy.
{% endblockquote %}
```

> Do not just seek happiness for yourself. Seek happiness for all. Through kindness. Through mercy.
>
> **David Levithan**Wide Awake

**引用 Twitter**

```
{% blockquote @DevDocs https://twitter.com/devdocs/status/356095192085962752 %}
NEW: DevDocs now comes with syntax highlighting. http://devdocs.io
{% endblockquote %}
```

> NEW: DevDocs now comes with syntax highlighting. [http://devdocs.io](http://devdocs.io/)
>
> **@DevDocs**[twitter.com/devdocs/status/356095192085962752](https://twitter.com/devdocs/status/356095192085962752)

**引用网络上的文章**

```
{% blockquote Seth Godin http://sethgodin.typepad.com/seths_blog/2009/07/welcome-to-island-marketing.html Welcome to Island Marketing %}
Every interaction is both precious and an opportunity to delight.
{% endblockquote %}
```

> Every interaction is both precious and an opportunity to delight.
>
> **Seth Godin**[Welcome to Island Marketing](http://sethgodin.typepad.com/seths_blog/2009/07/welcome-to-island-marketing.html)

## 代码块

在文章中插入代码。

**别名：** code

```
{% codeblock [title] [lang:language] [url] [link text] %}
code snippet
{% endcodeblock %}
```

### 样例

**普通的代码块**

```
{% codeblock %}
alert('Hello World!');
{% endcodeblock %}
```

```
alert('Hello World!');
```

**指定语言**

```
{% codeblock lang:objc %}
[rectangle setX: 10 y: 10 width: 20 height: 20];
{% endcodeblock %}
```

```
[rectangle setX: 10 y: 10 width: 20 height: 20];
```

**附加说明**

```
{% codeblock Array.map %}
array.map(callback[, thisArg])
{% endcodeblock %}
```

```
Array.map
array.map(callback[, thisArg])
```

**附加说明和网址**

```
{% codeblock _.compact http://underscorejs.org/#compact Underscore.js %}
_.compact([0, 1, false, 2, '', 3]);
=> [1, 2, 3]
{% endcodeblock %}
```

```
_.compact
_.compact([0, 1, false, 2, '', 3]);
=> [1, 2, 3]
```

[Underscore.js](http://underscorejs.org/#compact)

## 反引号代码块

另一种形式的代码块，不同的是它使用三个反引号来包裹。

\``` [language] [title] [url] [link text] code snippet ```

## Pull Quote

在文章中插入 Pull quote。

```
{% pullquote [class] %}
content
{% endpullquote %}
```

## jsFiddle

在文章中嵌入 jsFiddle。

```
{% jsfiddle shorttag [tabs] [skin] [width] [height] %}
```

## Gist

在文章中嵌入 Gist。

```
{% gist gist_id [filename] %}
```

## iframe

在文章中插入 iframe。

```
{% iframe url [width] [height] %}
```

## Image

在文章中插入指定大小的图片。

```
{% img [class names] /path/to/image [width] [height] "title text 'alt text'" %}
```

## Link

在文章中插入链接，并自动给外部链接添加 `target="_blank"` 属性。

```
{% link text url [external] [title] %}
```

## Include Code

插入 `source/downloads/code` 文件夹内的代码文件。`source/downloads/code` 不是固定的，取决于你在配置文件中 `code_dir` 的配置。

```
{% include_code [title] [lang:language] [from:line] [to:line] path/to/file %}
```

### 样例

**嵌入 test.js 文件全文**

```
{% include_code lang:javascript test.js %}
```

**只嵌入第 3 行**

```
{% include_code lang:javascript from:3 to:3 test.js %}
```

**嵌入第 5 行至第 8 行**

```
{% include_code lang:javascript from:5 to:8 test.js %}
```

**嵌入第 5 行至文件结束**

```
{% include_code lang:javascript from:5 test.js %}
```

**嵌入第 1 行至第 8 行**

```
{% include_code lang:javascript to:8 test.js %}
```

## Youtube

在文章中插入 Youtube 视频。

```
{% youtube video_id %}
```

## Vimeo

在文章中插入 Vimeo 视频。

```
{% vimeo video_id %}
```

## 引用文章

引用其他文章的链接。

```
{% post_path slug %}
{% post_link slug [title] [escape] %}
```

在使用此标签时可以忽略文章文件所在的路径或者文章的永久链接信息、如语言、日期。

例如，在文章中使用 `{% post_link how-to-bake-a-cake %}` 时，只需有一个名为 `how-to-bake-a-cake.md` 的文章文件即可。即使这个文件位于站点文件夹的 `source/posts/2015-02-my-family-holiday`目录下、或者文章的永久链接是 `2018/en/how-to-bake-a-cake`，都没有影响。

默认链接文字是文章的标题，你也可以自定义要显示的文本。此时不应该使用 Markdown 语法 `[]()`。

**链接使用文章的标题**

```
{% post_link hexo-3-8-released %}
```

[Hexo 3.8.0 Released](https://hexo.io/news/2018/10/19/hexo-3-8-released/)

**链接使用自定义文字**

```
{% post_link hexo-3-8-released '通往文章的链接' %}
```

[通往文章的链接](https://hexo.io/news/2018/10/19/hexo-3-8-released/)

## 引用资源

引用文章的资源。

```
{% asset_path slug %}
{% asset_img slug [title] %}
{% asset_link slug [title] [escape] %}
```

## Raw

如果您想在文章中插入 Swig 标签，可以尝试使用 Raw 标签，以免发生解析异常。

```
{% raw %}
content
{% endraw %}
```

## 文章摘要和截断

在文章中使用 ``，那么 `` 之前的文字将会被视为摘要。首页中将只出现这部分文字，同时这部分文字也会出现在正文之中。

例如：

```
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.<!-- more -->Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
```

首页中将只会出现

```
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
```

正文中则会出现

```
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
```

注意，摘要可能会被 Front Matter 中的 `excerpt` 覆盖。

{% endraw %}