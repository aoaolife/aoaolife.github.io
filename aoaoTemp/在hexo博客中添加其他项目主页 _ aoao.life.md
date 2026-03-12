---
title: 在hexo博客中添加其他项目主页 | aoao.life
date: 2014-09-07 08:50:16
updated: 2026-03-01 06:20:12
---

我看到有同样搭建在github上的这个博客<http://hukai.me/> ，在这个博客里面有一个<http://hukai.me/android-training-course-in-chinese/index.html> 网页，而根据我的了解<http://hukai.me/android-training-course-in-chinese/index.html> 这个网页的生成也是通过gh-pages，项目pages，于是我试着fork了一个2048的项目到自己的github上，打开 <http://zhangolve.github.io/2048> .之后跳转到我的博客上（http:hktkdy.com ）出现404页面，但是在那个项目的 options中显示这个项目主页已经published  
![](https://camo.githubusercontent.com/0fcb1cfd60cd6a7c84ed9c29acdfc47facafc987/687474703a2f2f686b746b64792e71696e6975646e2e636f6d2f69737375656865786f2e706e67)  
这个问题是本人在[hexo issue820](https://github.com/hexojs/hexo/issues/820#issuecomment-54732767)中提到的。

# 解决方法：

经过了与热心网友的几轮讨论之后，最终得到的解决方法是：

> 可以把那个库放在themes/themes-name/source目录下。hexo g之后，会出现在博客的主目录下

当然**还要在themes目录下的config文件中加上该项目的url指向**  
例如本人的clone的2048项目就有如下的设置：  
![](http://hktkdy.qiniudn.com/config.png)

然后将本地库运行hexo s之后无误后将之提交到远程，最后就能够看到形如本人博客<http://hktkdy.com/2048/> 这样的效果。

**需要注意的是，文件夹的名称要与你config文件中配置的路由名称相同，比如我的2048项目名称为2048，那么就是上图中的配置**

# 更新

这个问题最早出现在14年，距离现在已经2年多了，关于这个问题，[hexo issue820](https://github.com/hexojs/hexo/issues/820#issuecomment-54732767) 又有了一些讨论，我想其实用二级域名的方式也还不错，只是一直没有改过去，而如果是用我现在的这个方法的话，在我个人的理解中，如果你写了一个项目，这个项目有一个文件夹，这个项目有一个索引网页index.html ,那么解决方法就是如上面所示。

如果你只是写了一个测试网页test.html 文件，这个时候其实更方便的做法是将这个生成后的网页放到hexo 目录public文件夹之下，就如同404.html 那样。另一个方法是自己构造出一个项目来，比如生成一个名为test的文件夹，然后将你原来的test.html文件更名为index.html ，执行

`hexo g && hexo s`

访问 <http://localhost:4000/test/>

也能够达到同样的效果。亲测可行

![](http://7ktu2f.com1.z0.glb.clouddn.com/QQ%E6%88%AA%E5%9B%BE20170205171207.png)

总之，原理就在那里。

# 最后

本人其他关于博客方面的博文参见：  
<http://hktkdy.com/tags/%E5%8D%9A%E5%AE%A2/>

感谢github网友：[xuanwo](https://github.com/Xuanwo)