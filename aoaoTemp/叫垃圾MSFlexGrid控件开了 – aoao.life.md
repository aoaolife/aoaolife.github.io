---
title: "叫垃圾MSFlexGrid控件开了 – aoao.life"
date: 2016-12-19 08:21:44
---

VS日文系统下使用MS FlexGrid控件。工程为非UNICODE。
传日文ANSI String，显示乱码。
改传宽字符，显示乱码。
不解，查资料。在source管理器中修改字体，仍旧显示乱码。

翻箱倒柜一顿尝试设成控件UNICODE形式。改成了另外的乱码。醒悟，你传的本来就不是UNICODE，改UNICODE有屁用！！
对比source文件，发现，这该死的**FlexGrid控件单改Font属性的时候无法保存！**
于是在改Font的同时改了另外的一个属性，保存，又改回来，保存。

这个世界清净了……