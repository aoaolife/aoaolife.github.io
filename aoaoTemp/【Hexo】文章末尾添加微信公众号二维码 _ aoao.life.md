---
title: 【Hexo】文章末尾添加微信公众号二维码 | aoao.life
date: 2016-04-22 12:10:49
updated: 2026-03-01 06:20:12
---

其实已经很久没有折腾的主题样式了，因为过去的好长时间都在**瞎忙**。最近这几天，因为闲下来了，便觉得那糟糕的博客主题实在有必要折腾一下了。  
好吧，先来回忆一下过去的读者打开我的博客首页，看到的是什么鬼。。。

![](http://7ktu2f.com1.z0.glb.clouddn.com/blogscreen1.jpg)  
![](http://7ktu2f.com1.z0.glb.clouddn.com/blogscreen1.jpg)

简直不能忍受啊，其实原本的博客主题是直接拿来的人家的开源模板，但是都怪自己，改动中出现了一些问题。  
主要的问题大概是：

- 博客图床问题
- 博客文章中出现#xxxx 这样丑陋的东东
- 博客的多说评论一直不能正常开启
- 博客首页不是显示摘要，而是显示全文  
  于是换回了一个原始版的[yilia](https://github.com/litten/hexo-theme-yilia) 主题。又进行了简单的配置，对前面提到的三个问题，重点注意了一番。这个时候，也终于能够让我暂时看得过去了。



---

# 文章末尾添加微信公众号二维码

这个其实并不复杂，简单的使用搜索引擎，找到一篇类似的[Hexo文章末尾添加版权或自定义文本](http://starsky.gitcafe.io/2015/11/15/Hexo%E6%96%87%E7%AB%A0%E6%9C%AB%E5%B0%BE%E6%B7%BB%E5%8A%A0%E7%89%88%E6%9D%83%E6%88%96%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%87%E6%9C%AC/) 。事实上，原理都是类似的，我们如果可以在文章末尾添加「版权信息」，自然也能够在文章的末尾添加一个图片。

原文中给出了三种方法，我选择了其中第二种方法，并对其加以修改，下面来说说具体操作：

在你的主题文件夹中找到nav.ejs  
nav.ejs相关代码改为：

个人微信公众号

  
 ![](http://7ktu2f.com1.z0.glb.clouddn.com/wechatopen.jpg) //“”里面的是我的二维码图片地址，你可以替换成你自己的。

而article.styl相关代码改为

```
.article-end-text-wrap
  margin: 5px 0
.article-end-text
  font-family: "微软雅黑"
  font-size: 20px
  line-height: 1.6em
  text-align:center
  padding: 1em 2em
  
  background: color-widget-background
  box-shadow: 1px 2px 3px color-border
  //border: 1px solid color-widget-border
  border-radius: 3px
```

---

**其实你们应该明白，如果能够添加图片，那公众号二维码，个人微信二维码，支付宝付款，微信付款二维码统统不在话下了。**