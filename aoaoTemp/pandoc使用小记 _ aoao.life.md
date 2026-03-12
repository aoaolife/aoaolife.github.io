---
title: pandoc使用小记 | aoao.life
date: 2015-01-21 14:59:16
updated: 2026-03-01 06:20:12
---

#pandoc是什么

pandoc是一个开源的格式转换工具，可以实现一些常见格式的转化。github地址在：<https://github.com/jgm/pandoc>  
#为什么要用pandoc  
简单来说，因为我自己一直以来有一种「成集」情结，也就是把自己这些年来在网上写的博客文字全部汇总到一起，然后自己做一个电子书。之前我在高中毕业之后做过一个利用word转pdf，来制作了一个高中三年博客的pdf电子书。我希望在我大学结束之后能够将这七年来的文字全部汇集到一起，因为最近一直在用markdown很自然的就想到了用markdown能否转换成epub格式的电子书。后来网上搜索了一下，结果被我找到了这个号称瑞士军刀的pandoc。  
值得一说的是网上一些搜索引擎排名比较靠前的使用方法的教程帖子，对他的下载地址都没有进行更新，而实际上这个工具已经从google转移到了github，下载地址在此，请戳：<https://github.com/jgm/pandoc/releases>

#安装使用  
安装默认安装即可，使用我遇到点问题，我开始以为要安装那个Haskell平台才能够使用，后来又看了相关的资料，发现实际上只需要在命令行操作即可。我的做法就是打开cmd，然后通过cd指令到达安装目录，将所需要转化的md文件来放到这个目录下面，执行

> pandoc -s -o book.epub book.md

![](http://hktkdy.qiniudn.com/pandoctest.png)  
这个时候就开始生成epub格式的电子书了，当然由于我这个md文件本身的问题，云端的图片被删除了(也可能被墙了)，所以不能找到文件也是理所应当，但是实际测试得到的epub文件还是符合要求的。  
#结语  
实际上，这个pandoc的用处不止于此，还能够用它来制作幻灯片，转化成docx的格式，转化成pdf，不过实际上对我来说目前都还没有类似的需求。有时间倒是可以再研究一番。而事实上，即使这个md to epub也是最近用不到的，完全是好奇这个东西的神奇，看看它是在吹牛还是在果真是瑞士军刀。事实证明，其实除了没有个GUI，总体也还不错。  
p.s 网上这篇<http://www.yangzhiping.com/tech/pandoc.html> 搜索引擎非常靠前的对于此工具的使用讲解，对我这等小白来说实在是晦涩难懂，不推荐作为参考资料。

参考：<http://blog.michiru.me/something-about-epub.html>

#DIY  
为了让这篇博客更有说服力，用pandoc这个工具自制了两个epub文件。  
我的2014年20篇较好博文： <http://pan.baidu.com/s/1eQGPh2U>  
美剧基础词汇（来自百度贴吧用户的word文档转制而成） <http://pan.baidu.com/s/1gdre9hD>

更新：类似下面的命令可以给电子书添加封面

```
pandoc -o my-ebook.epub title.txt my-ebook.md --epub-cover-image=cover.jpg --epub-metadata=metadata.xml --toc --toc-depth=2 --epub-stylesheet=stylesheet.css
```