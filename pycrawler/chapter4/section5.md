# Python爬虫进阶五之多线程的用法

## 前言

我们之前写的爬虫都是单个线程的？这怎么够？一旦一个地方卡到不动了，那不就永远等待下去了？为此我们可以使用多线程或者多进程来处理。

首先声明一点！

多线程和多进程是不一样的！一个是 thread 库，一个是 multiprocessing 库。而多线程 thread 在 Python 里面被称作鸡肋的存在！而没错！本节介绍的是就是这个库 thread。

不建议你用这个，不过还是介绍下了，如果想看可以看看下面，不想浪费时间直接看[multiprocessing 多进程](http://cuiqingcai.com/3335.html)

## 鸡肋点

### 名言：

> 
“Python下多线程是鸡肋，推荐使用多进程！”
那当然有同学会问了，为啥？

### 背景

1、GIL是什么？

GIL的全称是Global Interpreter Lock(全局解释器锁)，来源是python设计之初的考虑，为了数据安全所做的决定。

2、每个CPU在同一时间只能执行一个线程（在单核CPU下的多线程其实都只是并发，不是并行，并发和并行从宏观上来讲都是同时处理多路请求的概念。但并发和并行又有区别，并行是指两个或者多个事件在同一时刻发生；而并发是指两个或多个事件在同一时间间隔内发生。）

在Python多线程下，每个线程的执行方式：

- 获取GIL
- 执行代码直到sleep或者是python虚拟机将其挂起。
- 释放GIL

可见，某个线程想要执行，必须先拿到GIL，我们可以把GIL看作是“通行证”，并且在一个python进程中，GIL只有一个。拿不到通行证的线程，就不允许进入CPU执行。

在Python2.x里，GIL的释放逻辑是当前线程遇见IO操作或者ticks计数达到100（ticks可以看作是Python自身的一个计数器，专门做用于GIL，每次释放后归零，这个计数可以通过 sys.setcheckinterval 来调整），进行释放。

而每次释放GIL锁，线程进行锁竞争、切换线程，会消耗资源。并且由于GIL锁存在，python里一个进程永远只能同时执行一个线程(拿到GIL的线程才能执行)，这就是为什么在多核CPU上，python的多线程效率并不高。

那么是不是python的多线程就完全没用了呢？

在这里我们进行分类讨论：

1、CPU密集型代码(各种循环处理、计数等等)，在这种情况下，由于计算工作多，ticks计数很快就会达到阈值，然后触发GIL的释放与再竞争（多个线程来回切换当然是需要消耗资源的），所以python下的多线程对CPU密集型代码并不友好。

2、IO密集型代码(文件处理、网络爬虫等)，多线程能够有效提升效率(单线程下有IO操作会进行IO等待，造成不必要的时间浪费，而开启多线程能在线程A等待时，自动切换到线程B，可以不浪费CPU的资源，从而能提升程序执行效率)。所以python的多线程对IO密集型代码比较友好。

而在python3.x中，GIL不使用ticks计数，改为使用计时器（执行时间达到阈值后，当前线程释放GIL），这样对CPU密集型程序更加友好，但依然没有解决GIL导致的同一时间只能执行一个线程的问题，所以效率依然不尽如人意。

### 多核性能

多核多线程比单核多线程更差，原因是单核下多线程，每次释放GIL，唤醒的那个线程都能获取到GIL锁，所以能够无缝执行，但多核下，CPU0释放GIL后，其他CPU上的线程都会进行竞争，但GIL可能会马上又被CPU0拿到，导致其他几个CPU上被唤醒后的线程会醒着等待到切换时间后又进入待调度状态，这样会造成线程颠簸(thrashing)，导致效率更低

### 多进程为什么不会这样？

每个进程有各自独立的GIL，互不干扰，这样就可以真正意义上的并行执行，所以在python中，多进程的执行效率优于多线程(仅仅针对多核CPU而言)。

所以在这里说结论：多核下，想做并行提升效率，比较通用的方法是使用多进程，能够有效提高执行效率。

所以，如果不想浪费时间，可以直接看多进程。

直接利用函数创建多线程

Python中使用线程有两种方式：函数或者用类来包装线程对象。

函数式：调用thread模块中的start_new_thread()函数来产生新线程。语法如下：

```
<span class="s1">thread</span><span class="s2">.</span><span class="s1">start_new_thread </span><span class="s2">(</span> <span class="s3">function</span><span class="s2">,</span><span class="s1"> args</span><span class="s2">[,</span><span class="s1"> kwargs</span><span class="s2">]</span> <span class="s2">)</span>
```

参数说明:

- function – 线程函数。
- args – 传递给线程函数的参数,他必须是个tuple类型。
- kwargs – 可选参数。

先用一个实例感受一下：

```
# -*- coding: UTF-8 -*-

import thread
import time


# 为线程定义一个函数
def print_time(threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print "%s: %s" % (threadName, time.ctime(time.time()))


# 创建两个线程
try:
    thread.start_new_thread(print_time, ("Thread-1", 2,))
    thread.start_new_thread(print_time, ("Thread-2", 4,))
except:
    print "Error: unable to start thread"


while 1:
   pass

print "Main Finished"
```


运行结果如下：

```
Thread-1: Thu Nov  3 16:43:01 2016
Thread-2: Thu Nov  3 16:43:03 2016
Thread-1: Thu Nov  3 16:43:03 2016
Thread-1: Thu Nov  3 16:43:05 2016
Thread-2: Thu Nov  3 16:43:07 2016
Thread-1: Thu Nov  3 16:43:07 2016
Thread-1: Thu Nov  3 16:43:09 2016
Thread-2: Thu Nov  3 16:43:11 2016
Thread-2: Thu Nov  3 16:43:15 2016
Thread-2: Thu Nov  3 16:43:19 2016
```

可以发现，两个线程都在执行，睡眠2秒和4秒后打印输出一段话。

注意到，在主线程写了

```
while 1:
   pass
```

这是让主线程一直在等待

如果去掉上面两行，那就直接输出

```
Main Finished
```

程序执行结束。

## 使用Threading模块创建线程

使用Threading模块创建线程，直接从threading.Thread继承，然后重写init方法和run方法：

```
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time

import thread

exitFlag = 0

class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            thread.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1

# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# 开启线程
thread1.start()
thread2.start()

print "Exiting Main Thread"
```


运行结果：

```
Starting Thread-1Starting Thread-2
 
Exiting Main Thread
Thread-1: Thu Nov  3 18:42:19 2016
Thread-2: Thu Nov  3 18:42:20 2016
Thread-1: Thu Nov  3 18:42:20 2016
Thread-1: Thu Nov  3 18:42:21 2016
Thread-2: Thu Nov  3 18:42:22 2016
Thread-1: Thu Nov  3 18:42:22 2016
Thread-1: Thu Nov  3 18:42:23 2016
Exiting Thread-1
Thread-2: Thu Nov  3 18:42:24 2016
Thread-2: Thu Nov  3 18:42:26 2016
Thread-2: Thu Nov  3 18:42:28 2016
Exiting Thread-2
```


有没有发现什么奇怪的地方？打印的输出格式好奇怪。比如第一行之后应该是一个回车的，结果第二个进程就打印出来了。

那是因为什么？因为这几个线程没有设置同步。

## 线程同步

如果多个线程共同对某个数据修改，则可能出现不可预料的结果，为了保证数据的正确性，需要对多个线程进行同步。

使用Thread对象的Lock和Rlock可以实现简单的线程同步，这两个对象都有acquire方法和release方法，对于那些需要每次只允许一个线程操作的数据，可以将其操作放到acquire和release方法之间。如下：

多线程的优势在于可以同时运行多个任务（至少感觉起来是这样）。但是当线程需要共享数据时，可能存在数据不同步的问题。

考虑这样一种情况：一个列表里所有元素都是0，线程”set”从后向前把所有元素改成1，而线程”print”负责从前往后读取列表并打印。

那么，可能线程”set”开始改的时候，线程”print”便来打印列表了，输出就成了一半0一半1，这就是数据的不同步。为了避免这种情况，引入了锁的概念。

锁有两种状态——锁定和未锁定。每当一个线程比如”set”要访问共享数据时，必须先获得锁定；如果已经有别的线程比如”print”获得锁定了，那么就让线程”set”暂停，也就是同步阻塞；等到线程”print”访问完毕，释放锁以后，再让线程”set”继续。

经过这样的处理，打印列表时要么全部输出0，要么全部输出1，不会再出现一半0一半1的尴尬场面。

看下面的例子：

```
# -*- coding: UTF-8 -*-

import threading
import time

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
       # 获得锁，成功获得锁定后返回True
       # 可选的timeout参数不填时将一直阻塞直到获得锁定
       # 否则超时后将返回False
        threadLock.acquire()
        print_time(self.name, self.counter, 3)
        # 释放锁
        threadLock.release()

def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1

threadLock = threading.Lock()
threads = []

# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# 开启新线程
thread1.start()
thread2.start()

# 添加线程到线程列表
threads.append(thread1)
threads.append(thread2)

# 等待所有线程完成
for t in threads:
    t.join()

print "Exiting Main Thread"
```


在上面的代码中运用了线程锁还有join等待。

运行结果如下：

```
Starting Thread-1
Starting Thread-2
Thread-1: Thu Nov  3 18:56:49 2016
Thread-1: Thu Nov  3 18:56:50 2016
Thread-1: Thu Nov  3 18:56:51 2016
Thread-2: Thu Nov  3 18:56:53 2016
Thread-2: Thu Nov  3 18:56:55 2016
Thread-2: Thu Nov  3 18:56:57 2016
Exiting Main Thread
```

这样一来，你可以发现就不会出现刚才的输出混乱的结果了。

## 线程优先级队列

Python的Queue模块中提供了同步的、线程安全的队列类，包括FIFO（先入先出)队列Queue，LIFO（后入先出）队列LifoQueue，和优先级队列PriorityQueue。这些队列都实现了锁原语，能够在多线程中直接使用。可以使用队列来实现线程间的同步。

Queue模块中的常用方法:

- Queue.qsize() 返回队列的大小
- Queue.empty() 如果队列为空，返回True,反之False
- Queue.full() 如果队列满了，返回True,反之False
- Queue.full 与 maxsize 大小对应
- Queue.get([block[, timeout]])获取队列，timeout等待时间
- Queue.get_nowait() 相当Queue.get(False)
- Queue.put(item) 写入队列，timeout等待时间
- Queue.put_nowait(item) 相当Queue.put(item, False)
- Queue.task_done() 在完成一项工作之后，Queue.task_done()函数向任务已经完成的队列发送一个信号
- Queue.join() 实际上意味着等到队列为空，再执行别的操作

用一个实例感受一下：

```
# -*- coding: UTF-8 -*-

import Queue
import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print "Starting " + self.name
        process_data(self.name, self.q)
        print "Exiting " + self.name

def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print "%s processing %s" % (threadName, data)
        else:
            queueLock.release()
        time.sleep(1)

threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = Queue.Queue(10)
threads = []
threadID = 1

# 创建新线程
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
print "Exiting Main Thread"
```


运行结果：

```
Starting Thread-1
Starting Thread-2
Starting Thread-3
Thread-3 processing One
Thread-1 processing Two
Thread-2 processing Three
Thread-3 processing Four
Thread-2 processing Five
Exiting Thread-2
Exiting Thread-3
Exiting Thread-1
Exiting Main Thread
```

上面的例子用了FIFO队列。当然你也可以换成其他类型的队列。

## 参考文章

1. http://bbs.51cto.com/thread-1349105-1.html
2. http://www.runoob.com/python/python-multithreading.html