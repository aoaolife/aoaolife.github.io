---
title: "【翻译】让MFC的窗口程序支持输出到stdout – aoao.life"
date: 2025-05-20 16:35:05
---

今日接到一个需求：要求我们的一个MFC窗口程序同时兼容命令行模式，也就是用命令行启动并传一个以上参数时，以命令行方式运行，并在命令行上打印运行结果。
visual studio的工程向导创建工程时就对命令行输出进行了规划：如果选择Console程序，工程的编译选项将会出现“/SUBSYSTEM:CONSOLE”，这样工程编译运行之后，stdin，stdout和stderr都指向窗口。但如果选择的是Windows工程，那么编译选项会变成“/SUBSYSTEM:WINDOWS”，就无法向窗口输出了。
解决方法是重定向输出

```
void EnablePrintfAtMFC()
{
if (AttachConsole(ATTACH_PARENT_PROCESS))
{
FILE* pCout;
freopen_s(&pCout, "CONOUT$", "w", stdout);
std::cout.clear();
std::wcout.clear();
}
}
```

这样，只要在输出到窗口前调用上面的EnablePrintfAtMFC();就能将字符串输出到窗口了。
注意两行clear不能省略，我第一次找到这个方法就是因为没clear而造成不能正常显示。

```
EnablePrintfAtMFC();
printf("Hello world!\n");
std::cout << "It works!" << endl;
```

但是，在我们的日文命令行下想输出日文还要注意一个转码的问题。
再封装一次就好。

```
void MyPrint(CString strOutput)
{
int nSjislen = WideCharToMultiByte(932, 0, strOutput.GetBuffer(0), -1, nullptr, 0, nullptr, nullptr);
if (nSjislen >0)
{
CStringA strPrintA;
char* pstr = strPrintA.GetBuffer(nSjislen);
WideCharToMultiByte(932, 0, strOutput.GetBuffer(0), -1, pstr, nSjislen, nullptr, nullptr);
printf(pstr);
strPrintA.ReleaseBuffer();
}
strOutput.ReleaseBuffer();
}
```

中文比日文稍微麻烦一点，有几种码，懒得查了，找到或者用GetConsoleCP()取一下，替换掉932就行。

[via](https://pewae.com/gaan/aHR0cHM6Ly9zdGFja292ZXJmbG93LmNvbS9xdWVzdGlvbnMvNTA5NDUwMi9ob3ctZG8taS13cml0ZS10by1zdGRvdXQtZnJvbS1hbi1tZmMtcHJvZ3JhbQ==)