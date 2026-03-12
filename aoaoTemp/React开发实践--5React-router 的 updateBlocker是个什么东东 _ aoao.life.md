---
title: React开发实践--5React-router 的 updateBlocker是个什么东东 | aoao.life
date: 2018-05-31 09:24:49
updated: 2026-03-01 06:20:12
---

![](http://7ktu2f.com1.z0.glb.clouddn.com/react.png)

---

昨天在阅读[react-router](https://reacttraining.com/react-router/web/guides/dealing-with-update-blocking)的官方文档的时候，发现了以前没有注意到的一个东东。`<UpdateBlocker>`

当时由于在试图解决一个问题: 路由切换的时候，某一个公用组件又重新didmount,即进入下一个生命周期，因而也没有好好地阅读文档，误以为这个`<UpdateBlocker>`的作用是能够阻止组件进入下一个生命周期。

后来几经测试，也没有得到满意的结果。后来仔细阅读文档，才发现与我之前的理解有很大差别。

`React-router`文档里面提到的这个`<UpdateBlocker>`，实际上是只是告诉你**结合React能够实现怎样的功能** 。

我们知道有些时候，我们并不想让组件发生更新，或者根据实际情况有选择地进行更新。这样也能够最大限度地保证WEB APP的性能。而这个`<UpdateBlocker>`的作用正在于此。

这时候，其实还是要说回到`React` 的官方文档，从[reactpurecomponent](https://reactjs.org/docs/react-api.html#reactpurecomponent)这一章节可以看出来，

> `React.PureComponent` is similar to [`React.Component`](https://reactjs.org/docs/react-api.html#reactcomponent). The difference between them is that [`React.Component`](https://reactjs.org/docs/react-api.html#reactcomponent) doesn’t implement [`shouldComponentUpdate()`](https://reactjs.org/docs/react-component.html#shouldcomponentupdate), but `React.PureComponent` implements it with a shallow prop and state comparison.

就是说`React.PureComponent`内部已经实现了 [`shouldComponentUpdate()`](https://reactjs.org/docs/react-component.html#shouldcomponentupdate)方法，我们可以拿来就用。而不用像使用 [`React.Component`](https://reactjs.org/docs/react-api.html#reactcomponent)那样，如果为了实现一个同样的**判断组件是否需更新**的功能，手动写这样一个方法。

P.S 渣英语理解错了，还以为`React.PureComponent`