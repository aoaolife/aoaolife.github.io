---
title: "std::thread()使用lambda表达式调用函数导致的离奇bug – aoao.life"
date: 2025-01-13 10:44:40
---

最近项目升级开发环境，从visual stdio 2017升级到visual stdio 2022，出现奇怪的现象：同样的代码，2017编译出来风平浪静，2022编译出来一运行就是段错误。

我们的函数大概长这样：

```
class a {
public:
void DoThings(std::string str1, std::string str2, int idx){...};
void Do0(){...};
void OnInit() {
std::string str1 = "FileName.txt";
std::string str2 = "X:\\Dest\\Path\";
int i = 0;
std::thread thd = std::thread([&]{DoThings(str1, str2, i);});
thd.detach();
};
};
```

从debug表现来看，是调用线程函数的时候，传入了典型的野指针。但是啊，三个参数，两个是std::string，另外一个是int啊！string有问题可以理解，可int怎么还能错呢？
把参数改成传入前new，调用后delete，自然是解决了。但心里各种不爽，new一个int，脸往哪搁啊！
好在问题定位的范围比较小，只是起线程调用函数这一小块地方。

2017只支持到C++ 11，而2022是C++ 14，看来问题出在这里了。
去找lambda的[说明](https://pewae.com/gaan/aHR0cHM6Ly9lbi5jcHByZWZlcmVuY2UuY29tL3cvY3BwL2xhbmd1YWdlL2xhbWJkYQ==):

> For the entities that are captured by reference (with the capture-default [&] or when using the character &, e.g. [&a, &b, &c]), it is unspecified if additional data members are declared in the closure type, but any such additional members must satisfy.

人家说了，你用lambda进行引用捕获的时候，必须保证捕获的成员是安全的。
看到这里差不多明白了，是[&]的锅。[&]的意思是所有参数按照引用的方式捕获。而你的三个变量都是临时变量，传个毛线的引用啊！
如果不安全会怎么样？这玩意儿叫“未定义的行为”，爱咋样咋样。也就是说，我们的写法触发了这种未定义的右值引用行为，人家可以给你实装成保留地址，也可以转换成另外的指针进行实装。故而2017和2022都没错，错的是写代码的人。
继续写个例子验证一下:

```
#include "stdafx.h"
#include <iostream>
#include <thread>
#include <mutex>
using namespace std;

std::mutex g_mtx;

class CTester {
public:
CTester() {
};

virtual ~CTester() {
};
void Run() {
for (int i = 100, j = 1, n = 0; n < 3; i += 100, j += 1, n++) {
std::thread thd = std::thread([&#038;] { Show(i, j, "std::thread([&#038;] { Show(i, j); }): "); });
thd.detach();
thd = std::thread([&#038;, i, j] { Show(i, j, "std::thread([&#038;, i, j] { Show(i, j); }): "); });
thd.detach();
thd = std::thread([&#038;, j] { Show(i, j, "std::thread([&#038;, j] { Show(i, j); }): "); });
thd.detach();
thd = std::thread([=] { Show(i, j, "std::thread([=] { Show(i, j); }): "); });
thd.detach();
}
}
void Show(int x, int y, const char* pri) {
std::lock_guard< std::mutex>lock(g_mtx);
char szOut[128] = { 0 };
sprintf(szOut, "pri = %s x=%d y=%d\n", pri, x, y);
std::cout << szOut;
}
};

int main()
{
std::cout << "Test Start" << '\n';
CTester t;
t.Run();
_sleep(500);
std::cout << "Test End" << '\n';
int c = getchar();
return 0;
}
```

2017的运行结果:
`Test Start
pri = std::thread([&] { Show(i, j); }): x=100 y=1
pri = std::thread([&, i, j] { Show(i, j); }): x=100 y=1
pri = std::thread([&, j] { Show(i, j); }): x=100 y=1
pri = std::thread([=] { Show(i, j); }): x=100 y=1
pri = std::thread([&] { Show(i, j); }): x=200 y=2
pri = std::thread([&, i, j] { Show(i, j); }): x=200 y=2
pri = std::thread([&, j] { Show(i, j); }): x=200 y=2
pri = std::thread([=] { Show(i, j); }): x=200 y=2
pri = std::thread([&] { Show(i, j); }): x=300 y=3
pri = std::thread([&, i, j] { Show(i, j); }): x=300 y=3
pri = std::thread([&, j] { Show(i, j); }): x=300 y=3
pri = std::thread([=] { Show(i, j); }): x=300 y=3
Test End`
2022的运行结果:
`Test Start
pri = std::thread([&] { Show(i, j); }): x=7599872 y=1992189472
pri = std::thread([=] { Show(i, j); }): x=100 y=1
pri = std::thread([&] { Show(i, j); }): x=7599872 y=1992189472
pri = std::thread([&, i, j] { Show(i, j); }): x=100 y=1
pri = std::thread([&, j] { Show(i, j); }): x=7599872 y=1
pri = std::thread([&, i, j] { Show(i, j); }): x=200 y=2
pri = std::thread([&, j] { Show(i, j); }): x=7599872 y=2
pri = std::thread([=] { Show(i, j); }): x=200 y=2
pri = std::thread([&] { Show(i, j); }): x=7599872 y=1992189472
pri = std::thread([&, j] { Show(i, j); }): x=7599872 y=3
pri = std::thread([&, i, j] { Show(i, j); }): x=300 y=3
pri = std::thread([=] { Show(i, j); }): x=300 y=3
Test End`
很明显，只要敢给2022（C++ 14）传引用，它就敢给你乱引……

这部分代码是从厂商的例子里抄的。人家写的是

```
std::thread([&]{Do0();});
```

只是隐式地捕获一个this！当然写[&]就行了。
友军抄的时候根本不知道方括号是干什么的，只改了后面，才造成了这样的后果。

那么怎么解决呢？写[=]或者[&, str1, str2, i]吗？并不是。
lambda叫啥？“匿名函数”啊！你都要调用真正的函数了，就别整匿名函数那一套了。
正确的std::thread调用类函数的时候应该长这样：

```
std::thread thrd = std::thread(&a::DoThings, this, str1, str2, i);
thrd.detach();
```

我是真心的不喜欢lambda。