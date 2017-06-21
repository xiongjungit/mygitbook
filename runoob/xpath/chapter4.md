# XPath 轴（Axes）

## XML 实例文档
我们将在下面的例子中使用此 XML 文档：

```
<?xml version="1.0" encoding="UTF-8"?>
 
<bookstore>
 
<book>
  <title lang="en">Harry Potter</title>
  <price>29.99</price>
</book>
 
<book>
  <title lang="en">Learning XML</title>
  <price>39.95</price>
</book>
 
</bookstore>
```

## XPath 轴（Axes）
轴可定义相对于当前节点的节点集。

|轴名称	|结果
|-|-|
|ancestor	|选取当前节点的所有先辈（父、祖父等）。
|ancestor-or-self	|选取当前节点的所有先辈（父、祖父等）以及当前节点本身。
|attribute	|选取当前节点的所有属性。
|child	|选取当前节点的所有子元素。
|descendant	|选取当前节点的所有后代元素（子、孙等）。
|descendant-or-self	|选取当前节点的所有后代元素（子、孙等）以及当前节点本身。
|following	|选取文档中当前节点的结束标签之后的所有节点。
|following-sibling	|选取当前节点之后的所有兄弟节点
|namespace	|选取当前节点的所有命名空间节点。
|parent	|选取当前节点的父节点。
|preceding	|选取文档中当前节点的开始标签之前的所有节点。
|preceding-sibling	|选取当前节点之前的所有同级节点。
|self	|选取当前节点。