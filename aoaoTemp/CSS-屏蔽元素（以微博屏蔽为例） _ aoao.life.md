---
title: CSS-屏蔽元素（以微博屏蔽为例） | aoao.life
date: 2015-06-24 10:29:49
updated: 2026-03-01 06:20:12
---

#工具

你需要PC机，firefox浏览器，stylish扩展

#举例

利用浏览器审查元素，看到你想要屏蔽的部分属于哪一个层级，然后确定要屏蔽的部分，填写类似的代码。

比如屏蔽亚洲新歌榜

```
@namespace url(http://www.w3.org/1999/xhtml);

@-moz-document domain("weibo.com") {
h4.remember-this-will-NOT-be-read {
   display: none !important;
}


WB_ad_tm2015{

display : none!important;
}
}
```

#最后

这种方法简单粗暴，事实上，一般情况下，还是推荐使用如[Yet Another Weibo Filter](https://tiansh.github.io/yawf/en.html) 这样的js脚本的，但是毕竟作者可能会更新不及时，虽然作者很卖力气，看他微博说一天曾经连更三次，但如果不及时，能够根据自己需要定制也是不错的。