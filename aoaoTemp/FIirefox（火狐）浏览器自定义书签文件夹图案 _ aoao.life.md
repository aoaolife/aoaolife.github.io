---
title: FIirefox（火狐）浏览器自定义书签文件夹图案 | aoao.life
date: 2014-06-04 17:30:16
updated: 2026-03-01 06:20:12
---

## 经常逛火狐吧，也看到很多吧友们晒出来自己的火狐界面，不得不说有些真的很惊艳。于是也学着他们装了UC 脚本等等，最近的迫切需求是希望能够把书签栏简化，想要让书签只显示图标，于是Google到了一个stylish样式，（名叫Bookmarks toolbar - favicons or label only，用的话直接搜索即可），这个时候确实可以让书签只显示图标了，但是原来的书签文件夹却显示出来了一个干秃秃的文件夹图标，而且我自己又不止有一个书签文件夹，这样显示的话根本分不清哪个文件夹是哪个了，与之前想要达到的简洁的目的背道而驰了。 对了，听明白没，就是这个效果。

所以这样肯定不行的，而之前也确实看过别人能够把书签文件夹的图标个性化。所以经过了Google之后并没有找到答案就又去问吧友了，这时候得到的答案是一个css样式模板。用它可以完美解决此问题，鉴于此处可能有和我一样的小白，说的详细一点。  
这样的代码是：

> /*针对指定的书签文件夹*/
>
> .bookmark-item[container=”true”][label=”文件夹名称”] { list-style-image:  
> url(“图标地址或base64码”) !important;  
> -moz-image-region: rect(0px 16px 16px 0px) !important; }  
> /*针对未指定书签文件夹*/  
> .bookmark-item[container=”true”] { list-style-image:  
> url(“图标地址或base64码”) !important;  
> -moz-image-region: rect(0px 16px 16px 0px) !important; } /*针对未指定的书签图标*/  
> /*针对未指定的书签图标*/  
> .bookmark-item:not([container=”true”]) { list-style-image:  
> url(“图标地址或base64码”) !important;  
> -moz-image-region: rect(0px 16px 16px 0px) !important; }

这里解释一下，文件夹名称里面就是填写你的书签文件夹的名称，比如我有个文件夹名字叫“娱乐”，那么我就可以在“”里面打进去娱乐两个字，而图标的base64码，这是一种编码形式，迅雷的ed2k文件就是用的这种编码形式，你要把你的本地图片上传到网上，然后转码。  
废话不多说，直接上过程：

1. 上网找自己喜欢的图标，最好是正方形的logo。
2. 将找到的图标用美图秀秀之类的软件统一裁剪成16\*16的图标格式大小
3. 将在本地做好的图标上传到<http://webcodertools.com/imagetobase64converter> 这个网站上来然后按upload，将你得到的双引号里面的部分复制下来，填入代码模板里的图标地址或base64中，这个url的标准格式是data:image/png;base64,iVBO省略无数英语字母。
4. 如此类推，做好一个又一个的书签文件夹图标。你需要的仅仅是复制> /*针对指定的书签文件夹*/
   > .bookmark-item[container=”true”][label=”文件夹名称”] { list-style-image:  
   > url(“图标地址或base64码”) !important;  
   > -moz-image-region: rect(0px 16px 16px 0px) !important; }

这行代码，有一个书签文件夹就有一个这样的模板代码。以此类推。而对于没有说明的其他书签文件夹用到了第二个注释里面的内容，也是同理，重复前三步。  
这个时候就需要自己建stylish样式了，  
![enter image description here](http://ww4.sinaimg.cn/large/63a3d9b7gw1eh26k0paq5j20d606qgm7.jpg)  
点击你的样式管理的S图标，按照上面的操作建立一个新的样式。也就是空白样式。将你刚才弄好的代码粘贴到主要空白区域里面去，名字可以随便起，能让人看到知道做什么的就可以。然后点击预览，如果成功的话，会直接在你的书签文件夹上看到效果，如果失败会提示错误原因，可再进行排查。  
我的效果如下：  
![enter image description here](http://ww3.sinaimg.cn/large/63a3d9b7gw1eh26njevxnj208c00owec.jpg)  
第一个是用的百度云的图标，意思是一些资源类的网站，第二个用的推特的图标，用意是社交类的网站，第三个是百度图标，用意是几个常逛的百度贴吧。如此不再介绍，可根据自己的喜好，自由定制，真的很不错。

注意：1如果你在找完图标的base64代码之后将代码保存到txt文本文件中可能会出错，也是编码的问题，建议用notepad+的utf-8编码，没问题。如果还不成功，看看你的base64吗复制粘贴有没有问题，人家的模板模型肯定是没有问题滴。  
参考资料：[怎样自定义火狐书签文件夹图标](http://tieba.baidu.com/f?ct=335675392&tn=baiduPostBrowser&sc=51600669817&z=3082647113#51600669817)

如果不懂得可以在下面给我留言评论，也可以到百度firefox吧去提问，吧友们都很热情的。