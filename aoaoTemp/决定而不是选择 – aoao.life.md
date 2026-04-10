---
title: "决定而不是选择 – aoao.life"
date: 2016-12-17 07:52:30
---

WP4.2这个大版本，没什么激动人心的功能不说，反而惹了一身骚。
关于emoji，[9sep.org的解决方案](https://pewae.com/gaan/aHR0cDovL3d3dy45c2VwLm9yZy9yZW1vdmUtZW1vamktaW4td29yZHByZXNz)很到位，有需要的照着做就好了。

但这并不能化解我对这个新机能的怨念，随打算上官网骂上那么一骂。
登上以后，发现有歪果仁朋友已经捷足先登了。via (https://wordpress.org/support/topic/get-rid-of-emoji)

一楼：请你们把4.2的emoji新机能做成可选项呗。请提供一个在setting里关掉它的方法。

> Please make the new emoji additions added in 4.2 optional. we don’t want this on our site and would appreciate a way to turn them off in settings somehow.

二楼：顶楼上。内核里有这玩意儿怪怪的。

> Agree with you. Strange decision to put this into the core…

三楼：用WP这么多年我头一次装完新版本回滚了！这只是个小亮点，为嘛要替换掉以前的表情？把我现在的表情转一半丢一半的，让留言者自己加表情的功能也不好用了。建议从内核里挪到某个插件里。

> For the first time in several years I had to roll back a new version of WordPress to the old one. The Reason Is Emoji. What was the need to implement this for all users by default? That’s a pretty specific function! I want the old smilies!
>
> Give the opportunity to choose to use emoticons or Emoji. After updating all my emoticons partially replaced by Emoji, partially instead of black squares that looks terrible!
>
> Previously, I have added all the smilies under the comment form that commentators would put them in the form of a comment, now it will not start! Still the file names in the path to the images are broken, replacing the file name in Emoji and a link causes a 404 error. Do something, it looks bad.
>
> I suggest to remove Emoji from the core of WordPress and add them as a plugin, for example in a Jetpack.

四楼（技术团队）：如果想禁用emoji，用这个插件，如果想恢复旧表情，用这个插件。

> If you just want to disable the new emoji code, this will do it:
>
> > [Disable Emojis (GDPR friendly)](https://pewae.com/gaan/aHR0cHM6Ly93b3JkcHJlc3Mub3JnL3BsdWdpbnMvZGlzYWJsZS1lbW9qaXMv)
>
> If you want to disable the emojis and also revert all the smilies to the original ones, this will do it:
> https://wordpress.org/plugins/classic-smilies/

五楼=楼主：我不想通过插件屏蔽emoji。

> We dont want to have to install a plugin just to remove emojis!

六楼=四楼：你不能移除对emoji的支持。任何对内核的修改都应该通过插件。插件系统是WP的脊梁，它支持了整个WP系统的运行。要么用emoji，要么通过插件解决你遇到的问题。想BB在自己的blog上随便，这里是技术论坛，我们只提供解决方案，不是听你瞎嚷嚷的。

> Then you won’t be able to remove the emoji support.
>
> Any changes you wish to make to the core system can be done through plugins. Plugins are the way that the system is altered. If you don’t want to use a plugin, then nothing actually gets changed. Even core changes happen through feature plugins.
>
> Plugins are the backbone of the WordPress system. Most of the internal functionality in the core code is done through a plugin system. The plugin system is fundamental to how WordPress works.
>
> So live with the emoji’s, or use a plugin to solve the problem you’re having. That’s how it is.
>
> If you just want to rant, then do that on your own blog. These are support forums. We’re here to provide solutions, not to listen to you complain.

七楼=三楼：我就是不想通过插件屏蔽WP的内核功能。请提供可配置方案。而且无用的js和css会影响SEO。如果我想用某个功能，我可以用不同的社交网站来记日记。但WP是最好的blog引擎，不应该强制用户使用emoji或者其它什么第三方应用。

> Yes! We don’t want to install plugins to deactivate the functions of the WordPress core! Users should always be a choice, please make it to were you can choose to use the standard emoticons or emoji! It’s a matter of taste and the appearance of the site.
>
> And the fact that inserts emoji me unnecessary scripts and styles in the header – is clearly of no use to the blog and contrary to all the Google guidelines for optimization and acceleration of the work site. Emoji needs to be an option and not a forced imposition. The desire for functionality of social networks does not Bode well, if I wanted something would keep his diary in a social network, but WordPress is the best blogging engine, and it should not impose its users using emoji or other third-party services.

八楼=四楼：@三楼：这是你的观点，但它违背了WP开发的原则“决定而不是选择”。在未来也不大可能变成一个可选项。所以，你可以通过插件使用你想要的表情，或者保留emoji。插件就是WP为你提供的选择。如果它不够好，那就对不起了。但它不会为你提供一个checkbox，WP不是那么运行的。

> @webliberty: That is a view, certainly, but it’s one that contrary to the philosophical principles guiding WordPress development.
> “Decisions, not options.”
> It is highly unlikely that this will be made into an optional thing in the future. Therefore, you can either use a plugin to enable the type of emoticons you want, or you can not do that. You do have a choice. Plugins are the way that WordPress offers choices. Sorry if that’s not good enough for you, but they’re not going to put in a checkbox type of thing. That’s just not how WordPress works.

九楼：@三楼：顶。@四楼：我非常同意你说的“插件就是WP为你提供的选择”。所以emoji本身才应该成为一个插件啊！至少，应该是一个admin选项。不是已经有不少admin选项了吗？

> @webliberty: I totally agree
> @Samuel Wood: “Plugins are the way that WordPress offers choices” I think that what you said sums things up perfectly. This Emoji thing should have been made as an optional plugin that users have the choice to install or not. At the very least, it should be an option to enable or disable via the admin. There are many core features built into WordPress that can be enabled or not used via a choice in the admin…this should be one of them…its only common sense.

十楼=三楼：我只装了5个插件。我觉得插件应该是用来实现功能而不是屏蔽某个功能的。当我升级到4.2，我所有的表情变成了可怕的小黑方块，难道要我手动去改几百个帖子吗？WP有很多选择的机会，为什么不给emoji和表情一个机会？再说如果浏览器搞了一遍Unicode，我从s.w.org又搞了一遍下来，这是弄啥咧？而且把72*72的图片缩小了，凭啥固定成11em啊？现在留言框上的表情都成死链了，我怎么让访客留表情？为啥不提供列出所有emoji的方法？移动设备访问的是方便了，PC的咋整？

> I have now just installed 5 plugins and not very desirable whenever the innovation is to install a new plugin to disable something. The plugin you want to use to add new features, not to disable them.
> When I upgraded to WP 4.2 all my emoticons in the records turned into a terrible emoji and some were black squares. Do I have several hundred records manually edit to remove them from the pages?
> Because in WP there are many things where you can select. Why not give the option to choose between emoticons and emoji? After all code in the kernel file functions.php not much has changed.
> I read somewhere that emoji is not symbols and Unicode characters, however, if you inspect element in the browser all the Unicode character I also loaded the picture from the website s.w.org. If this is the same picture, then what’s the point? And the original picture size 72×72 px and they are scaled to a smaller size. Why to force the size of the emoji 1em is equal?
> Here is a look at the screenshot, I wasn deduced smiles at the comment form using the code: https://www.dropbox.com/s/9gfg8c29d0tzo4c/smilies.png?dl=0
> Now I can’t do that because the link to the picture in the form of breaks and a file called smiley face turns into a strange symbol, so the link doesn’t work. How will users be able to insert a smiley in a comment? Now how to implement it? Why not make a standard function to list all available emoji form?
> For users with mobile devices that may be convenient, but how to paste on a PC? Why do commentators have to open obscure third sites and copy the codes from there?

十一楼往后开始讨论”咋整”……

几点体会：
1.wordpress官方是铁了心要支持emoji了。后续版本代码可能会优化，但想移出内核不太可能。
2.从开发者的角度讲，”Decisions, not options.”这句话非常赞！我都已经给出方案了，爱用不用。
3.emoji这种东西确实算第三方，应该给出可配置项，就像gravatar一样，连不上起码可以关闭啊。
4.对于插件的理解，看来我跟官方是一致的（不愧是从1.5就在用的老用户）。是“对功能作出的修改”，而不是“对功能的扩展”。对内核有任何的不满意都应该通过插件来实现。其实好多的所谓“免插件如何如何”不过是把代码从插件里拿到了主题里，并未超出广义上插件系统的范畴。
5.360提升在WPer族群中刷存在感的机会又来了！
6.虽然赞同开发者，但我还是去骂了。耽误我那么长时间，不骂怎么行。

emoji这么不受国人待见，难道是因为先天不足，名字来源于日语（颜文字）？

最后,测个表情 😉