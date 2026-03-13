---
title: 转Typecho - aoao.life
date: 2026-03-02 00:00:00
updated: 2026-03-02 00:00:00
---

当您看到这篇文章时，表示我已经成功将博客从Wordpress转到Typecho。

自从用了几年的单栏简洁主题因为Wordpress升级无法使用后，陆续更换了3次主题都无法让我满意，最终决定走出舒适区投身Typecho阵营。

没错，只是因为这个主题决心把博客从wordpress转到Typecho。

**开发插件**

一下决心换程序，立马开始动手，安装还算顺利，在将数据从wordpress迁移过来时，却费了不少功夫。

官方提供的wordpress to typecho转换插件太拉垮，转换几次都不成功，数据库一转就被搞崩。本来准备放弃了，突然想到为何不试着用AI自己写个转换插件。

心动不如行动，没有流行的openclaw，将就用腾讯元宝基于DeepSeek试了试，没想到AI大模型强大如斯，很快就生成了一个wordpress转typecho插件，且第一次上传后就能启动。之后的转换过程中当然还有各种小问题，生成代码3分钟，bug调试却花了大半天，主要还是第一次用生疏没经验，调试过程中越用越熟练效率就快很多，最终靠着Ai大模型完成一个完善版的“wordpress To typecho插件”。

[![](https://www.leolin86.com/usr/uploads/2026/03/1181732261.png)](https://www.leolin86.com/usr/uploads/2026/03/1181732261.png)

人生的开发的第一个博客插件，居然是靠Ai完成的，默默为程序员们捏了把汗。

折腾完脑海里又冒出一个念头，为了一个主题费这么大劲把wordpress转Typecho，是不是也可以用AI试着修复之前出bug的wordpress主题，尴尬了～～～

**oneblog主题**  
这里特别鸣谢oneblog主题的开发者彼岸临窗，正如他所说，这是精心打磨的精品主题～越看越喜欢，值得我为它转到typecho，感谢作者的无私分享。

**其他**  
1、部分页面还在完善，友情链接后续会补上。

**分享插件下载**

[WordPressToTypecho](/usr/uploads/WordPressToTypecho.zip)

说明：  
1、本插件本人只在wordpress6.9.1转Typecho 1.3.0使用，其他版本的转换没有验证，如果试用记得先备份好数据。  
2、担心数据量大带崩服务器和数据库，文章每次插入20篇，评论每次200个，均需手动点导入直到日志显示剩余为0。  
3、因需要ID映射，需按顺序先导入用户、分析、文章、评论，顺序不能乱。  
4、使用过程中有问题可以上传插件文件和日志，通过千问、元宝、豆包等大模型自行修正。

本文著作权归作者 [ aoao.life ] 享有，未经作者书面授权，禁止转载，封面图片来源于 [ 互联网 ] ，本文仅供个人学习、研究和欣赏使用。如有异议，请联系博主及时处理。

[Wordpress](https://www.leolin86.com/tag/wordpress/)[Typecho](https://www.leolin86.com/tag/typecho/)[插件开发](https://www.leolin86.com/tag/%E6%8F%92%E4%BB%B6%E5%BC%80%E5%8F%91/)