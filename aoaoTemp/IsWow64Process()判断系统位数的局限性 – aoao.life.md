---
title: "IsWow64Process()判断系统位数的局限性 – aoao.life"
date: 2019-11-12 09:52:32
---

背景：干一个擦屁股项目，其中一个要求是把目标从原来的32位改成64位。

程序启动的时候要调用另一个工具，该工具有32位和64位的版本。所以我们的代码中有个判断当前系统是32位还是64位的函数。
这个函数完全是照搬的标准答案：

```
BOOL IsWow64()
{
typedef BOOL (WINAPI *LPFN_ISWOW64PROCESS) (HANDLE, PBOOL);
LPFN_ISWOW64PROCESS fnIsWow64Process;
BOOL bIsWow64 = FALSE;
fnIsWow64Process = (LPFN_ISWOW64PROCESS)GetProcAddress( GetModuleHandle("kernel32"),"IsWow64Process");
if (NULL != fnIsWow64Process)
{
fnIsWow64Process(GetCurrentProcess(),&bIsWow64);
}
return bIsWow64;
}
```

然而，改成64位编译之后，这段微软推荐的代码给我返FALSE。
仔细看了CSDN上的解答，才发现这个函数的使用是有前提的：在**Win32**下。
可能人家的意思是，如果你本身已经是Wow64了，还去判断系统干嘛，不是64位你自己都起不来啊！

找到原因就好解决了。在外面另封一层编译宏开关【WIN_64Bit】，把宏定义到VS的PreProcess设定中就行了，代码中判断如果是64位编译器，直接返回TRUE即可。

```
#ifndef WIN_64Bit
BOOL IsWow64()
{
typedef BOOL (WINAPI *LPFN_ISWOW64PROCESS) (HANDLE, PBOOL);
LPFN_ISWOW64PROCESS fnIsWow64Process;
BOOL bIsWow64 = FALSE;
fnIsWow64Process = (LPFN_ISWOW64PROCESS)GetProcAddress( GetModuleHandle("kernel32"),"IsWow64Process");
if (NULL != fnIsWow64Process)
{
fnIsWow64Process(GetCurrentProcess(),&bIsWow64);
}
return bIsWow64;
}
#else
BOOL IsWow64()
{
return TRUE;
}
#endif
```

也怪不到以前同事，只满足当时需求嘛。