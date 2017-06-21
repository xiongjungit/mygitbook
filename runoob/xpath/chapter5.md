# XPath 运算符
XPath 表达式可返回节点集、字符串、逻辑值以及数字。

## XPath 运算符
下面列出了可用在 XPath 表达式中的运算符：

|运算符|描述|实例|返回值|
|:--|:--|:--|:--|
|｜|计算两个节点集|//book ｜ //cd|返回所有拥有 book 和 cd 元素的节点集|
|+|加法|6 + 4|10|
|-|减法|42890|2|
|*|乘法|6 * 4|24|
|div|除法|8 div 4|2|
|=|等于|price=9.80|如果 price 是 9.80，则返回 true。<br>如果 price 是 9.90，则返回 false。|
|!=|不等于|price!=9.80|如果 price 是 9.90，则返回 true。<br>如果 price 是 9.80，则返回 false。|
|<|小于|price<9.80|如果 price 是 9.00，则返回 true。<br>如果 price 是 9.90，则返回 false。|
|<=|小于或等于|price<=9.80|如果 price 是 9.00，则返回 true。<br>如果 price 是 9.90，则返回 false。|
|>|大于|price>9.80|如果 price 是 9.90，则返回 true。<br>如果 price 是 9.80，则返回 false。|
|>=|大于或等于|price>=9.80|如果 price 是 9.90，则返回 true。<br>如果 price 是 9.70，则返回 false。|
|or|或|price=9.80 or price=9.70|如果 price 是 9.80，则返回 true。<br>如果 price 是 9.50，则返回 false。|
|and|与|price>9.00 and price<9.90|如果 price 是 9.80，则返回 true。<br>如果 price 是 8.50，则返回 false。|
|mod|计算除法的余数|5 mod 2|1|
