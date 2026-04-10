---
title: "关于CLOCK_MONOTONIC与CLOCK_REALTIME在VxWorks下的理解 – aoao.life"
date: 2020-05-12 19:29:32
---

今天，组里小孩用POSIX的clock_gettime()函数的时候问了个问题：
“第一个参数，CLOCK_MONOTONIC和CLOCK_REALTIME究竟有什么区别啊？”
这问题其实有些老生常谈了。

“
CLOCK_MONOTONIC从系统上电后从某个时间点开始计数，从那以后只加不减。
CLOCK_REALTIME可以被人为（向前）修改。
”

“可是，REALTIME不是‘实时’的意思吗？”
“MONOTONIC的意思是单一的，而REALTIME则可以理解为‘实时改变’的。去看帮助文档，发现对REALTIME的解释的时候有很多老外给解释成wall-time，也就是所谓的‘墙上时间’。墙上时间从表上来，表盘的时间可以是格林尼治时间，也可以是东八区时间，更可以是东八区时间快15分钟。只要每次取时钟的时候用同一标准，那么计算出的差值仍旧是准确的。”

“
举个例子，最常用的信号量“等一秒”是这样写的：

```
#include <time.h>
#include <semaphore.h>

int main (int argc, char* argv[]) {
sem_t* pSem = NULL;
struct timespec ts = {0};
pSem = sem_open("\SemTest", O_CREAT | O_EXCL, 0, 1);
(void)clock_gettime(CLOCK_REALTIME, &ts);
ts.tv_sec += 1;
(void)sem_timedwait(pSem, &ts);
return 0;
}
```

”

这里用clock_gettime()取了一个时间，使用的是CLOCK_REALTIME。这么做是由sem_timedwait()这个函数决定的。在手册里明确说sem_的系列函数内部使用的必须是CLOCK_REALTIME才行。

“那么，CLOCK_REALTIME的值与CLOCK_MONOTONIC取的值不相同吗？尤其是在从来没调用过clock_settime()的前提下？”
“并不相同。你不调不等于系统不调。系统初始化CLOCK_MONOTONIC的时机非常早。但是在初始化clockLib的时候，CLOCK_REALTIME也被默认设置了。这就造成了，传不同参数的时候取得的两个时间完全不同。”

“又及，VxWorks还支持一个CLOCK_THREAD_CPUTIME_ID的参数。使用这个参的时候要传pthread_getcpuclockid()的输出参。这种用法显然是给多核准备的。
CLOCK_PROCESS_CPUTIME_ID并不被VxWork所支持，原因大抵也跟上面一样。”

“clock_settime()当然是不能设CLOCK_MONOTONIC的。”