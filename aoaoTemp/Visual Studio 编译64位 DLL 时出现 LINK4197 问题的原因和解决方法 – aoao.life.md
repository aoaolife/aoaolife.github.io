---
title: "Visual Studio 编译64位 DLL 时出现 LINK4197 问题的原因和解决方法 – aoao.life"
date: 2019-11-12 09:51:54
---

VS2017编译dll时，报LINK4197警告，提示是DLL的接口函数重复定义。而且比较奇怪的是x64下会报这个警告，x86下则没有。
搜索后在微软的官方网站（//support.microsoft.com/en-us/help/835326/you-receive-an-lnk4197-error-in-the-64-bit-version-of-the-visual-c-com）找到了原因。

> The Linker error number LNK4197 is generated when a function has been declared for export more than one time. A function is declared for export in one of the following ways:
>
> The function is declared by using the __declspec(dllexport) keyword in your C source file:
>
> __declspec(dllexport) int DllSample()
> {
> return 42;
> }
>
> The function is declared by using a module-definition (.DEF) file:
>
> EXPORTS
> DllSample
>
> This Linker error may occur most frequently when both the __declspec(dllexport) keyword and a .DEF file are used to define the same function name in a .DLL project.

简单的说，在DLL函数声明的时候，在函数前使用了关键字**__declspec(dllexport)**。然后在对应的def文件中，又把该函数放在EXPORT后面再次进行了声明。

所以修改的方法就是，两边只留一个。.def文件是在工程里配置的，相对不好进行差分，所以我选择删除工程下【property】-> 【linker】->【input】->【module define file】里添加的.def文件。

对于只有编译64位版本时才报警告的原因，微软网站上也有说明：

> Declaring a function for export more than one time may not produce the Linker error that is described in the “Symptoms” section of this article in 32-bit versions of the Microsoft Windows C++ Compiler and Linker. However, Microsoft recommends that you define function exports only one time in both 32-bit and 64-bit versions of the Windows C++ Compiler and Linker.

就是微软的32位编译器觉得这个问题不叫事儿。