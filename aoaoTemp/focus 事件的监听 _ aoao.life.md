---
title: focus 事件的监听 | aoao.life
date: 2018-05-31 18:24:49
updated: 2026-03-01 06:20:12
---

![](http://7ktu2f.com1.z0.glb.clouddn.com/javascript.png)

---

我在上一篇 [薛定谔的导航栏](https://www.jianshu.com/p/6392732dc7ed)里面，关于代码的部分，用到了下面的语法：

`document.addEventListener('focus', this.IosFocusHandler, true);`

有同学可能会问了，为什么我们一般都默认capture:false，怎么这里监听focus事件的时候，就改成了捕获模式呢？

[MDN上面](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus)对这一块已经说的很清楚了，因为focus事件是不支持冒泡的。但是虽然不能冒泡，但是一个事件三个阶段（捕获，处理中，冒泡），还要前两个阶段呢！所以，当我们改为捕获模式的时候，就能够在捕获阶段，拿到focus事件是否触发的消息了。

顺便提一句，与focus事件很像，focusin事件支持冒泡，所以按道理来说，如果我们想要在document上面监听是否有focus的动作，其实是可以使用focusin事件的，也无需再加capture:true ,但是从caniuse.com 可以知道firefox浏览器，直到17年出的firefox52才终于支持上focusin事件。

所以，就有了这个SO的问答： [Focusin and focusout methods not working in firefox](https://stackoverflow.com/questions/24809835/focusin-and-focusout-methods-not-working-in-firefox)

如果想想在firefox浏览器下有好的表现，还是应该用

`document.addEventListener('focus', this.IosFocusHandler, true);`

focus事件加上capture:true 的写法的。

类似地，blur事件和focusout事件的区别也是冒不冒泡的区别。那么问题来了，为什么focus事件不直接支持冒泡，再去掉一个重复的focusin事件呢？

我只能试图从focus和blur的语义上来理解了。毕竟，规范这东西，都是人规定的。