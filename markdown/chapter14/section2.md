#14-2 缩进式多行代码

缩进 4 个空格或是 1 个制表符

一个代码区块会一直持续到没有缩进的那一行（或是文件结尾）。

##代码：

	    #include <stdio.h>
	    int main(void)
	    {
	        printf("Hello world\n");
	    }

##显示效果：

```
#include <stdio.h>
int main(void)
{
    printf("Hello world\n");
}
```