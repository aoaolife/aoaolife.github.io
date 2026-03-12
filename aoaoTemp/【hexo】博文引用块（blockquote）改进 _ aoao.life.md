---
title: 【hexo】博文引用块（blockquote）改进 | aoao.life
date: 2015-05-15 07:31:49
updated: 2026-03-01 06:20:12
---

#缘由

刚刚在上网随便闲逛的时候，看到了这样一篇[写球迷感受的博文](http://drunkevil.com/2015/04/09/the-beautiful-spurs/#comments) ，内容其实并不算新鲜，只是它的网页设计吸引了我，准确地说是它的「引用部分」吸引了我，于是便在博文下面评论留言，询问博主那是怎样实现的，与此同时，我也自己查相关资料，由于之前我是看过html,js,css相关的书籍的，所以如今已经大概能够猜到是对于css的设置，不过看网页源代码发现，这种css应该不是内嵌样式表，从网页上不能直接得到。

但是我由此产生了一个想法（事实上以前也有过类似想法，尤其是看到一些很惊艳的设计的时候），自己对我的blog的blockquote部分进行改进，因为之前的实在是很丑。（不是重点，不再截图了），但是毕竟之前只是随便看了看书，并没有实践过，所以又从头开始。

#过程  
由于之前对样式表（css）是有一些认识的，实际上并没有多难。自己本身又是用的firefox浏览器，安装了stylish，就更加得心应手了。先是在网上随便找了几个css的代码贴在了stylish的新样式里面，然后看了看效果，如下图所示：

![图一](http://hktkdy.qiniudn.com/firstquote.jpg)

这个效果和我未更改前是差不多的，只是增加了一个大大的「,」，这不能让我满意，后来又找到了另外一个相关css的代码，大概看懂了意思，几经修改，就达到了现在的效果：

![图二](http://hktkdy.qiniudn.com/aroundquote.jpg)

代码如下；

```
blockquote {
font-family: Microsoft YaHei;
font-size: 16px;
font-style: italic;
width: 500px;
margin: 0.25em 0;
padding: 0.25em 40px;
line-height: 1.45;
position: relative;
color: #383838;
border:3px dashed #c1c1c1;
background:#fff;
}
```

于是乎，由于我使用的是hexo的keal主题，于是在hexo\themes\kael\source\css 这个目录下，找到screen.css ，用notepad++打开，对其中的blockquote部分进行编辑（通过加注释的方法，将原有的blockquote部分在代码中去掉），加入上面所列的代码。

经过简单的修改之后，显示效果，就如上图二所示。

#后来

由于我先把此文发在简书，其实我也很讨厌简书的那个blockquote块，于是顺手，把那个stylish脚本又为简书稍加修改，感觉也稍微好看点，当然，事实上，差不多。  
![添加stylish脚本前](http://hktkdy.qiniudn.com/jianshuquote2.jpg)  
![添加stylish脚本后](http://hktkdy.qiniudn.com/jianshuquote.jpg)

#体会

现在这个效果肯定还不是最好的，哪天真的可以考虑自己独立写一个css来实现自己心目中想要的效果。

————————————–分割线——————————  
如果您喜欢本文，可以点下面的喜欢按钮，也可以关注[本人简书](https://www.jianshu.com/users/1c26e9e36267/latest_articles)  
或简书专题：[我们在自己的世界里独自狂欢](https://www.jianshu.com/collection/7b424559990a)

也可以阅读我的独立博客，了解更多内容。

[![](http://hktkdy.qiniudn.com/slogan.jpg)](http://hktkdy.com/)