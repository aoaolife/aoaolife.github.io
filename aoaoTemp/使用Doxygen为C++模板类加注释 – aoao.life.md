---
title: "使用Doxygen为C++模板类加注释 – aoao.life"
date: 2018-04-08 16:40:46
---

土鳖客户死板的编码规范又一次不适用了。因为Doxygen会把模板识别符号尖括号“<>”认成html标记，从而导致生成文档异常。
搜索半天找到解决方案。其实只要在注释里避免中括号就好了。
而且Doxygen其实自带了一个关键字tparam，使用就好了。
下面是例子：

```
/**
* @brief Defines a class for stuff.
* @tparam T Type to work with.
* @tparam NDim Number of dimensions.
*/
template <class T, int NDim>
class myClass {

public:
.
.
};
```