---
title: nodejs event loop | aoao.life
date: 2019-06-12 11:19:07
updated: 2026-03-01 06:20:12
---

1.线程的问题

2.各个方法优先级的问题

需要知道宏任务，微任务的概念。  
process.nextTick()

3.对event loop的理解

事件循环机制可以让程序来执行非阻塞的io操作。虽然js语言本身是单线程的，把一些任务转移给操作系统内核来完成。

因为大多数现代操作系统内核是多线程的，因此他们能够控制多个操作在后台执行。当这些操作中有一个操作完成之后，这个内核就会告诉nodejs，这个操作已经完成，这个时候，callback函数就会被添加到队列中，等待执行。

┌───────────────────────────┐  
┌─>│ timers │  
│ └─────────────┬─────────────┘  
│ ┌─────────────┴─────────────┐  
│ │ pending callbacks │  
│ └─────────────┬─────────────┘  
│ ┌─────────────┴─────────────┐  
│ │ idle, prepare │  
│ └─────────────┬─────────────┘ ┌───────────────┐  
│ ┌─────────────┴─────────────┐ │ incoming: │  
│ │ poll │<─────┤ connections, │  
│ └─────────────┬─────────────┘ │ data, etc. │  
│ ┌─────────────┴─────────────┐ └───────────────┘  
│ │ check │  
│ └─────────────┬─────────────┘  
│ ┌─────────────┴─────────────┐  
└──┤ close callbacks │  
 └───────────────────────────┘

从上面的流程图可以看出，timer的顺序是要高于poll的

## 各个阶段

各个阶段：

timer=>pending callback=>

pending callbacks:

poll： callbacks池，一些callback放到这个队列中，等待执行，setTimeout的时间最少是设定的时间，因为还有从队列中取出来执行的时间。

check: setImediate 的callback在这里执行

close callback：一些关闭callback在这里执行

## 理解io操作

我们编写的程序除了自身会定义一些数据信息外，经常还会引用外界的数据，或是将自身的数据发送到外界。比如，我们编写的程序想读取一个文本文件，又或者我们想将程序中的某些数据写入到一个文件中。这时我们就要使用输入与输出。

读取文件，我们可以使用读取文件的方法。比如fs.readFile(‘/path/to/file’, callback);

# 堆内存 栈内存

## 堆

二叉树来进行维护

堆是一种数据结构，是利用完全二叉树维护的一组数据，堆分为两种，一种为最大堆，一种为最小堆

堆内存 栈内存  
<https://juejin.im/entry/589c29a9b123db16a3c18adf>

与其他语言不通，JS的引用数据类型，比如数组Array，它们值的大小是不固定的。引用数据类型的值是保存在堆内存中的对象。JavaScript不允许直接访问堆内存中的位置，因此我们不能直接操作对象的堆内存空间。在操作对象时，实际上是在操作对象的引用而不是实际的对象。因此，引用类型的值都是按引用访问的。这里的引用，我们可以粗浅地理解为保存在栈内存中的一个地址，该地址与堆内存的实际值相关联。

### 二叉树

在计算机科学中，二叉树是每个结点最多有两个子树的树结构。通常子树被称作“左子树”（left subtree）和“右子树”（right subtree）。二叉树常被用于实现二叉查找树和二叉堆。  
一棵深度为k，且有2^k-1个节点的二叉树，称为满二叉树。这种树的特点是每一层上的节点数都是最大节点数。而在一棵二叉树中，除最后一层外，若其余层都是满的，并且最后一层或者是满的，或者是在右边缺少连续若干节点，则此二叉树为完全二叉树。具有n个节点的完全二叉树的深度为floor(log2n)+1。深度为k的完全二叉树，至少有2k-1个叶子节点，至多有2k-1个节

## setTimeout

解释：setTimeout/setInterval 的第二个参数取值范围是：[1, 2^31 - 1]，如果超过这个范围则会初始化为 1，即 setTimeout(fn, 0) === setTimeout(fn, 1)。

setTimeout 的第二个参数只是说的，callback什么时候放到事件循环的队列中去。

为什么timeout的时间不准

setTimeout 的第二个参数只是说的，callback什么时候放到事件循环的队列中去。

To reduce the load (and associated battery usage) from background tabs, timeouts are throttled to firing no more often than once per second (1000 ms) in inactive tabs.

如果是非活跃标签页，那么它每1000ms会去检查一下callback执行。这个时候也是会出现时间不准的情况。

dom.min\_background\_timeout\_value

For Firefox in particular, you can change the dom.min\_background\_timeout\_value preference in about:config to a number of your liking in the profile that you use to run the tests. I wouldn’t suggest doing that in your default browsing profile, though: the reason for the high clamp is that it cuts down on web sites in background tabs chewing up CPU updating silly tickers and the like.

Node uses libuv which a cross-platform abstraction layer for lower level system things like file-system

In Node, if you specify setTimeout(callback, 1) then it will be executed one millisecond later (assuming the system doesn’t delay it due to be overwhelmed). In browsers, the minimum time will be 4 milliseconds as specified by the HTML5 spec:

<https://stackoverflow.com/questions/7221504/does-node-js-enforce-a-minimum-delay-for-settimeout>

宏任务，微任务

先执行同步任务，再执行微任务，最后执行宏任务。  
宏任务有 setTimeout, setInerval, setImmerdate等，优先级不能确定

微任务 process.nextTick , promise, 按照优先级排列

当然是为了和浏览器更加趋同。  
了解浏览器的eventloop可能就知道，浏览器的宏任务队列执行了一个，就会执行微任务。  
简单的说，可以把浏览器的宏任务和node10的timers比较，就是node10只有全部执行了timers阶段队列的全部任务才执行微任务队列，而浏览器只要执行了一个宏任务就会执行微任务队列。  
现在node11在timer阶段的setTimeout,setInterval…和在check阶段的immediate都在node11里面都修改为一旦执行一个阶段里的一个任务就立刻执行微任务队列。  
最后  
所以在生产环境建议还是不要特意的去利用node和浏览器不同的一些特性。即使是node和浏览器相同的特性，但规范没确定的一些特性，也建议小心使用。否则一次小小的node升级可能就会造成一次线上事故，而不只是啪啪打脸这么简单了。

作者：zy445566  
链接：<https://juejin.im/post/5c3e8d90f265da614274218a>  
来源：掘金  
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

异步意味着任务不会阻塞，比如，如果我要下载一个比较忙的网络资源，我的程序不需要一直等待下载完成，它可以在等待下载时继续做其他事情。这与并行执行多个操作不同。 其实还是应用上了多线程，对于js语言而言，等于js的主线程上，再等待响应，去做了其他的事情。而系统的其他线程，则再处理相应。这是从系统层面来看这个问题，比如读取某个文件的操作，其实也是有两个线程，一个线程是js主线程，另一个线程是系统上读取文件的线程。

# 参考资料

<https://juejin.im/post/5c3d8956e51d4511dc72c200>

<https://zhuanlan.zhihu.com/p/34182184>

<https://jakearchibald.com/2015/tasks-microtasks-queues-and-schedules/>  
<https://juejin.im/post/5c3d8956e51d4511dc72c200>