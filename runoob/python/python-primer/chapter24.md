#Python File(文件) 方法
file 对象使用 open 函数来创建，下表列出了 file 对象常用的函数：

|序号	|方法|描述
|-|-|-
|1	|[file.close()](./file/close.md)|关闭文件。关闭后文件不能再进行读写操作。
|2	|[file.flush()](./file/flush.md)|刷新文件内部缓冲，直接把内部缓冲区的数据立刻写入文件, 而不是被动的等待输出缓冲区写入。
|3	|[file.fileno()](./file/fileno.md)|返回一个整型的文件描述符(file descriptor FD 整型), 可以用在如os模块的read方法等一些底层操作上。
|4	|[file.isatty()](./file/isatty.md)|如果文件连接到一个终端设备返回 True，否则返回 False。
|5	|[file.next()](./file/next.md)|返回文件下一行。
|6	|[file.read([size])](./file/read.md)|从文件读取指定的字节数，如果未给定或为负则读取所有。
|7	|[file.readline([size])](./file/readline.md)|读取整行，包括 "\n" 字符。
|8	|[file.readlines([sizehint])](./file/readlines.md)|读取所有行并返回列表，若给定sizeint>0，返回总和大约为sizeint字节的行, 实际读取值可能比sizhint较大, 因为需要填充缓冲区。
|9	|[file.seek(offset[, whence])](./file/seek.md)|设置文件当前位置
|10	|[file.tell()](./file/tell.md)|返回文件当前位置。
|11	|[file.truncate([size])](./file/truncate.md)|截取文件，截取的字节通过size指定，默认为当前文件位置。
|12	|[file.write(str)](./file/write.md)|将字符串写入文件，没有返回值。
|13	|[file.writelines(sequence)](./file/writelines.md)|向文件写入一个序列字符串列表，如果需要换行则要自己加入每行的换行符。