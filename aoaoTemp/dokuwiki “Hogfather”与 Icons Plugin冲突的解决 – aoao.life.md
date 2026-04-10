---
title: "dokuwiki “Hogfather”与 Icons Plugin冲突的解决 – aoao.life"
date: 2021-10-16 23:58:29
---

dokuwiki在2020年7月份升级了一个大版本，”Hogfather”。这个版本的更新与我一直使用的icons插件产生了冲突。具体的现象便是，在编辑画面，点击icon按钮后，弹出的窗口中只能显示tab页标题，里面的图标一个也显示不了。
去年8、9月份还能摸鱼上网的时候，隔三差五就去插件官网查看解决方案，然而这个插件的作者就像死掉了一样，完全不给回馈。
用这种小众应用的小众插件，遇到这种问题几乎是在所难免的。
一直到上个月服务器搬迁，忽然又想起了这个问题。竟然有热心网友给解决了。
说穿了一文不值，Hogfather版增加了一个叫做【defer_js】的新功能，导致了冲突。在设置页面给禁止掉就可以了。
[via](https://pewae.com/gaan/aHR0cHM6Ly9naXRodWIuY29tL2dpdGVybGl6emkvZG9rdXdpa2ktcGx1Z2luLWljb25zL2lzc3Vlcy8yOQ==)