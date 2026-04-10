---
title: "解决Firefox 【Image Block】插件被停用后不能显示图片的问题 – aoao.life"
date: 2017-11-15 16:01:23
---

今天FF自动升级成了57.0版本，又一批之前的插件被停用了。其中包括一个用来阻止图片显示的Image Block插件。
不巧的是，FF升级之前，这个插件恰好处在阻止图片显示的状态。于是尴尬了：所有的图片都不能显示，开关也没了。

试图清空所有的扩展配置，无效。

最终还是在FF本身的设置上找到了解决办法。说穿了一文不值。
*浏览器地址栏键入about:config回车
查找
permissions.default.image
把2（禁止所有）改成1（显示所有）
OK！*

P.S：找到一个替代插件，叫“Block Image|Video”，使用30分钟感觉还可以。

Resolve the no picture problem causing by the invalid extension “Image Block” after firefox updated.

A terrible thing happens after firefox updated to version 57.0.
I was using an extension “Image Block” to block all pictures during working time. After the updating, the “block/show” button is disappeared because the extension is not valid any more. But there are still no pictures displaying under the browser.

I find an easy way to resolve it.
1. Type about:config and tap on the enter key afterwards.
2. Search for the preference permissions.default.image
3. Change the value to 1.(1 = display all, 2 = block all, 3 = block third-party images only)