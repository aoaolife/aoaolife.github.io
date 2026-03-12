---
title: 用github结合hexo建立个人博客的几点注意及参考资料 | aoao.life
date: 2014-05-25 08:30:16
updated: 2026-03-01 06:20:12
---

首先谈一下为什么要写这样一篇文字，可以说，当初自己从想要建立这样一个博客到最后博客建成，一路上确实是遇到了很多问题的，而这些问题，我相信，对于大多数小白可能也会遇到。同时，鉴于是刚刚开的博客，所以新鲜的味道还没有散去，故而自然要写一个练练手。当然，我觉得互联网上的分享其实也类似于学术分享，所谓站在巨人的肩膀上，我在建站之出参考了很多的资料，然而没有一个的资料是十分全面的，所以也想借此机会来重新梳理一下。

\*\*我的题目也已经说了，本文是对已有资料的补充。所以，自然也不会再多说废话在一些别的教程上已经说的很清楚的地方。\*\*我建站时参考的主要教程是来自[如何搭建一个独立博客——简明Github Pages与Hexo教程](http://cnfeat.com/2014/05/10/2014-05-11-how-to-build-a-blog/) ，所以我之后的所说的也都是对此篇教程的补充。

# 1购买域名

---

购买域名中存在的问题在登录[goadaddy](www.godaddy.com/)时是用firefox浏览器登录之后出现了国家和货币那两个项目的混乱，你开始选的是US，等到下一步继续进行的时候就变成了越南了，货币也随之变成了越南盾，这是我的现象，不知道其他人有没有，所以还是推荐使用chrome浏览器吧，如果是英语不太好的话，还可以自动翻译。  
![我所说的货币和国家混乱](http://ww4.sinaimg.cn/large/63a3d9b7gw1egq96ajyzbj20ev03rdg0.jpg)  
20151118更新，如今再读下面这一段，废话。  
~~用github和hexo结合在一起建站真的很经济，对于只是想单纯的玩博客的而不是搞复杂的网站的人绰绰有余。我购买了一年的域名花了50多软妹，想一想，50多块在当今社会真的不是钱啦！~~~

#2安装软件

这个不多说，应该说教程上很详细。

# 配置和使用Github

这一点要注意的是，当使用git的时候我所出现的几个问题。

- 1在输入密码状态是，你打在键盘上的密码是不显示出来的，对，是连\*\*\*\*\*\*\*\*\*\*这样的都不会显示的，所以你只管放心地去输入你的github账号的正确的密码就好了。
- 安装完成之后使用命令`hexo g` `hexo s` 之后去浏览器输入<http://localhost:4000进行查看，如果是一个很不错的网页，有图片，有第一篇hello> world的博文的话，则可以进行更新主题的继续操作，如果出现了如![这样的图片](http://ww1.sinaimg.cn/large/63a3d9b7gw1egq9s7gyl3j20oh066wf5.jpg)出现在浏览器的窗口上，则需要进行如下操作。

  ```
   $ npm install hexo-renderer-ejs --save
   $ npm install hexo-renderer-stylus --save
   $ npm install hexo-renderer-marked --save
  ```

而且是就在当前的博客目录下，因为你的博客目录下缺少渲染网页的工具，所以上面的操作是下载这些工具的。这一个点我找了好久都没有找到，还专门问了一个写教程的博主，然而他也不太了解，最后是通过Google看的hexo的开发者的[issue](https://github.com/tommy351/hexo/releases/tag/2.6.0) 解决的， 所以也请你们一定要注意啦！  
#本地空间的上传  
这一点我觉得那个教程做的不太好，他在域名绑定之后就说博客已经搭建完成了，但是在我们这些小白看来要搭建完至少应当是将本地仓库传到远程（remote）之后才能说得上是搭建完成。这里就不吐槽了。上传其实很简单**只需要对根目录下的config.yml进行简单的配置就可以了**可以参考<http://zipperary.com/2013/05/28/hexo-guide-2/> ，所以我觉得正确的搭建顺序是**先能把本地的仓库上传到远程之后才是域名的绑定和所谓的进阶**

PS ~~我还是很喜欢jacman这个主题的，相比于<http://zipperary.com/2013/05/28/hexo-guide-2/> 教程中的light主题而言，他更加的简单，当然这也要看个人了。~~20150118更新：我现在在用的这个主题：[kael](https://github.com/yuche/hexo-theme-kael)其实更加简洁朴实尤其适合那些非技术类的博客，具体可以参考我的[hexo博客主题更换为kael](http://hktkdy.com/2015/01/01/201501/0101/) 这篇文章。  
#进阶方面  
其实人家已经给你配置好了，当你下载了他的主题之后，再进行简单的copy和改变，比如一些很个性化的东西就需要你自己的设置，比如网页页面上的邮箱，微博，豆瓣，github的地址等，人家是根据自己的需要设置的，所以你要替换成你自己的。这些即使看不懂那些网络语言也可以很轻松地替换。

- 图床  
  ~~我用的是“围脖是个好图床”通过搜索可以很方便地找到。不过是个浏览器扩展（插件），但是也真的很方便，将图片拖动到他的大空白区域，然后就可以生成一个网络地址，将此地址复制到博客中即可。ps前提是你需要首先在浏览器上登录你的微博账号啦！~~  
  20150118更新：实际上没用几天那个围脖是个好图床，由于chrome升级之后不能安装非官方的xpi，而同时我又发现其实七牛的云存储真的很给力，于是果断的更换成了七牛，毕竟他的两大优点速度快以及可以将原来的文件都可见很吸引我。当然，每月10G的流量对我来说绰绰有余。

---

- 其他须知  
  1使用git时可能出现的其他问题  
  提示出现  
  `Github “Updates were rejected because the remote contains work that you do not have”`  
  这个时候只需要执行

  git remote add origin //your github url

  ```
    //pull those changes
    
    git pull origin master
    
    //now, push your work to your new repo
    
    git push origin master
  ```

2应当比较熟练的使用下面的命令

```
 `hexo g`   `hexo s`  
 `hexo d`    `int init` 
 `git pull`  `git push` 
 `git pull` `origin master`
 `git push`  `origin master`
```

3博客的生成从上传到远程仓库到最后生成网页可能需要十分钟左右，所以请耐心等候，用那谁的话说“可以泡一杯咖啡”。

4博客的写作  
20150118更新：  
经过了半年多的使用，发现markdown确实是个好东西，与此同时也发现了另外一个比较好的markdown书写工具，简书。这个网站不仅能够在线用markdown写文章，还能够发表文章，我往往是在上面写好之后顺便就发表了，同时投稿到几个专题里，收获的阅读数往往会比[http://hktkdycom](http://hktkdycom/) 这个博客要高。我的简书地址：[http://www.jianshu.com/users/1c26e9e36267/latest\_articles](https://www.jianshu.com/users/1c26e9e36267/latest_articles) 欢迎关注  
将在这里写好的博客粘贴到posts生成的博客md文件里面，再运行  
`hexo g hexos`

就可以在本地查看你的博客的效果啦（建议将http:lacalhost：4000存为一个浏览器书签以便随时查看）

~~可以用Cmd markdown <https://www.zybuluo.com/mdeditor/note/14372> ，我现在就在用这个，因为也是第一次用，也不是很熟练，所以你会看到我的博客排版确实有点问题。。。。~~ 现在排版好多了，好不好！

5摘要的设置  
Q: 老子原来使用<–! more –>分割的摘要怎么在首页中就剩下140个字了？  
A: 骚年，慧眼啊！是这样的：为了提高打开首页的速度故首页不加载文章图片，只加载文章摘要。因此我强烈建议大家在写文章的时候自己总结description并将其放在开头的front-matter中。如果没有会截取<–! more –>内容前的140个字，如果你连这个都懒得写，没关系，依旧为你截取文章内容的前140个字作为摘要。  
以上问题来自（[http://yangjian.me/pacman/hello/introducing-pacman-theme/）](http://yangjian.me/pacman/hello/introducing-pacman-theme/%EF%BC%89) 我看了也是很受用的。

6hexo版本回退问题

20150118更新：  
由于我看了一篇[博客](http://blog.yuanbin.me/posts/2014/05/multi-deployment-with-hexo.html) 讲可以将博客同时部署到github和gitcafe，所以就打算试一试，在设置了相关的：

```
 deploy:
    type: git
    message: [message]
    repo:
    github: <repository url>,[branch]
    gitcafe: <repository url>,[branch]
```

但是仍然未能达到理想的效果，提示出错hexo g之后没有问题，但是hexo s的时候不能上传，而且可以肯定就是这里出了问题。于是想到了升级hexo，觉得是现在的版本不支持deploy到两个远程。谁知道升级之后问题更大了，hexo  
g都显示错误，最后懒得折腾，觉得没必要这样同时放到两个远程。倒不如换个思路退回原版本，这样倒也方便。  
方法是：

> 打开命令行，输入npm install -g hexo@版本号就可以回退到没有出现问题的版本上来。  
> 这个命令适用于所有Node.js模块

建站之后我发现的其他有关的问题，可以参考我的这一篇博文.<http://hktkdy.com/2014/05/24/0524>  
最后感谢给我帮助的前人博主们，感谢hexo的发明人tommy351。  
[cnfeat](http://cnfeat.com/)  
[Zippera](http://zipperary.com/)  
[tommy351](https://github.com/tommy351)  
[yangjian](http://yangjian.me/pacman/)

---

转载请注明原博地址：[用github结合hexo建立个人博客的几点注意及参考资料](http://hktkdy.com/2014/05/25/201405/0525/)