---
title: "股沟股沟，欲挂还休 – aoao.life"
date: 2020-08-21 13:51:42
---

五一期间没上网，有一位新朋友尚磊同学来访。他的置顶贴里推荐了google官方出的adsense的wp插件。
作为一个插件党，遇到这样的东东自然要动手试试。虽然我一直感觉google adsense刷得又慢又慢的，但毕竟有两年多没挂过了，一旦好使了呢？再说土木坛子同学不久前[曾信誓旦旦地说过](https://pewae.com/gaan/aHR0cHM6Ly90dW11dGFuemkuY29tL2FyY2hpdmVzLzEzMTUw)adsense在他那边是好使的，他曾经VPN回国内刷过。

那就试试呗。挂上之后简单刷两下，果然跟我想象的一样，不开代理不出来。但坛子同学也没必要骗人啊，他只是承认了google fonts可能刷得慢，却没说过整只广告都出不来的情况。索性上他那里刷广告玩。
坛子那儿的广告果然是可以出来的！但头几次还是会有部分内容没有加载。通过插件查看，加载失败的域名是google-analytics.com。几个页面之后，这个域名也不会出来作祟了。显然，google的广告头几次是通过google-analytics.com记IP的，几次之后，不再统计我的IP，也就顺畅了。（P.S：把插件关了之后才发现坛子那边的gravatar竟然没处理过，难道没人跟他提过这事儿吗？？）

那么推荐google官方插件的尚磊同学那里呢？嘿嘿，果然是挂掉的。现象跟我这里一样，加载失败的域名是googlesyndication.com和google-analytics.com。几次之后仅剩googlesyndication.com无法访问，广告也无法刷新。

再回到坛子那里，他那儿能连上的的广告究竟是来自哪里呢？googleadservices.com
真相终于大白了。google闲得没事注册了400多个域名。googleadservices.com这个域名未被GFW认证，所以来自这里的广告可以正常显示；而googlesyndication.com这个域名被认证了，所以就啥都刷不出来。至于google根据什么规则用哪个域名往外放广告，就不得而知了。

至于google-analytics.com为啥我这里连不上而好多小伙伴都反应能用，就只能理解成辽宁联通自己加料了。