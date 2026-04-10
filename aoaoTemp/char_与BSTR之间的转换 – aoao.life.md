---
title: "char*与BSTR之间的转换 – aoao.life"
date: 2022-07-31 13:17:07
---

现在项目涉及到com与外界的接口。设计时“为了显得更正规”所有的原来的字符串接口都改成了BSTR。
首先，需要把传入的BSTR转换成char*，起先用的方法是

```
TCHAR* zsFilePath= NULL;
zsFilePath = (TCHAR*)malloc(sizeof(TCHAR) * wcslen(strName));
WideCharToMultiByte(CP_ACP,
0,
strName,
wcslen(strName),
szFilePath,
wcslen(strName),
NULL,
NULL);
...
free(szFilePath);
```

其中，strName是传进来的BSTR值，CP_ACP是字符转换格式，第一个wcslen(strName)是字符的个数，第二个是缓冲区大小。因为TCHAR大小是1，所以就不乘了。
但是这样做是有问题的，因为传进来的时候，BSTR中存的是文件路径名，其中的反斜线“\”是加了转义字符的，就是说这个路径实际上比真正路径要长。但是转换成char*后，多出了字符数差个不可显示字符，在调用windows取文件版本的API之前，还需要再次处理。而且不能在szFilePath上直接处理，因为这样的话它就不能释放了。

后来找到的真正简单的方法是利用_bstr_t建一个中间变量，然后直接给char*赋值。

```
DWORD dwVerHnd;
_bstr_t bstrTName = strName;
TCHAR* szFilePath = bstrTName;
```

真正的麻烦其实出在返回的时候，函数原型里的第二个参数是一个这样的struct

```
typedef struct
{
BSTR strTitle;
BSTR strProvider;
BSTR strDate;
BSTR strVersion;
BSTR strCopyRight;
BSTR strSigner;
} SDriverInformation;
```

单独给一个BSTR赋值也是可以的，但是整体结构传出去之后就指针产生了混乱。最终的解决方案是采用了最后一种方法，

```
CComBSTR bstrCopyRight(DLL_Info);
pVersion->strCopyRight = bstrCopyRight.m_str;
```