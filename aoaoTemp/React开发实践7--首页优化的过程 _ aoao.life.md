---
title: React开发实践7--首页优化的过程 | aoao.life
date: 2018-08-07 09:24:49
updated: 2026-03-01 06:20:12
---

需要说明一点是，关于比较常规的React性能优化，可以看这篇文章：  
[React 16 加载性能优化指南](https://mp.weixin.qq.com/s?__biz=MzIzNjcwNzA2Mw==&mid=2247485902&idx=1&sn=952e0db3bc0f36b7cd4db71b17914daa&chksm=e8d28456dfa50d407e52c935cb7518cf76f1179a8bcbbac760f1685f88fd8d809ca84f5d9c3f&mpshare=1&scene=1&srcid=0720NL5okWr9xzIeEpbQmWyZ#rd)，我要聊到是一些非常规，与实际开发密切相关的坑，但也正是因为这是我个人遇到的个案，或者并不构成普遍意义。

我前面一篇[《React开发实践5–详细说说滚动记忆》](https://www.jianshu.com/p/db42bb62f69a) 其实跟React关系不大，只是因为做React的项目遇到了问题，也就顺手写下来了。最早遇到这个问题，的确第一反映是React这个库的锅，但是稍稍理性的想一想也知道，React的本质也是JS啊，于是很快就将注意力转移了。

说回头来，上一篇文章说到的那个业务需求，在React-router的官方文档里专门有一节在讲，也就是[Scroll Restoration](https://reacttraining.com/web/guides/scroll-restoration)。这里也说到了我在上一篇结尾列出来的那个文档：[scrollRestoration](https://majido.github.io/scroll-restoration-proposal/history-based-api.html#usage)

如此说来，我现在资料颇多了。有了前面的铺垫，我想我也就不用再废话了。

# CMS 这个坑

首先我引入了一个库`react-router-scroll-4`，眼尖的朋友看出来了为什么还要带个`4`呢，这是因为原本的库是`react-router-scroll`,因为这个库不支持react-router v4，因此有开发者又fork出来一个能够支持react-router v4的分支，我用的也就是这一个了。我看过他的源码，核心思想其实就像上面提到的react-router官方文档所介绍的一样，通过session-storage 来处理。

之后，我开始对商品列表页和APP首页进行改造。商品列表页改造地非常简单，无非是对组件进行一次包裹。但是APP首页的改造却遇到了麻烦。同样是对该组件进行包裹，结果现象却是无法实现滚动记忆。这让我好生无奈。这又是为什么呢？我首先想到了是不是这个`react-router-scroll-4`支持不够好，毕竟这是一个连github项目库都没有的npm包，顺着这个思路，我去看了这个库的源码，又通过打印log的方式去debug，发现了问题所在：原来这个库对 `dangerouslySetInnerHTML`这种注入HTML的方式没有进行处理，这里面的关键点在于生命周期，此处我并不想多讲，但最终导致无法实现滚动记忆。而我们之所以要在项目中使用 `dangerouslySetInnerHTML`,也是因为项目中有用到CMS的模块，历史遗留问题，一时无法解决。

但是你知道的，虽然我后来通过修改这个第三方库`react-router-scroll-4`，最终实现了首页的滚动记忆，但是前面我也提到了由于使用了CMS系统，造成首页的几乎所有点击都是普通的a标签href的跳转，即这样的交互将原本的React app的优势：独立的路由体系打散了。事实证明，在性能上也造成很大问题。

为了更好地说明问题，举个例子。如果是在同一个路由体系下，从首页/切换到 /abc，这个过程，只会去加载abc路由所需要的资源。但是如果脱离了这个路由体系，而是通过普通的a标签href跳转，进入/abc的时候，相当于又重新进入一遍app，这个时候原本一些bundle的资源又会被重新加载一边，虽然这些资源可能被浏览器缓存了起来，但是缓存好了和根本不需要又是两回事，对不对。

所以，如果能够尽量在进入一个React app之后，尽量不再脱离这个app，也就是一直React-router的方式进行跳转，用我前面文章提到过的说法，就是假跳转，其实是能够有很好的优势的。

原来有一个CMS，我会调用一个接口，返回一个HTML页面内容。如果能够将HTML转成REACT组件，这样是不是更好呢？我后来找到了`html-react-parser`这个库，其实还有另外一个库，不过另外一个库有一些问题，比如图片的url上面如果有大写字母会转成小写字母，造成图片加载失败。

这个库很好地解决了我的问题。接下来，我做了如下改动，一切都水到渠成。

- 在第一次进入首页的时候，将首页内容(cms html)放置到React state中进行储存，在下次回到首页时，无须重复调用获取首页内容接口，即可快速获取首页内容，达到尽快地相应
- 将原本html上面的a标签上的click事件进行劫持，根据情况，将原来的a跳转改为react-router 的history.push()，使之不脱离这个app。由于这里没有脱离app，则当接下来用户点击返回回到首页时，还是会按照react-router的方式去返回，则次过程也不会脱离app了。

这里有个小tips,如果我们获取e.target.href的话，我们会发现即便是我们原本写的a标签是这样的

[one product](/product/1)

最后得到的 e.target.href也会自动添加上网址。可是我们知道history.push()只认相对路径，因此e.target.href并不能满足我们的需求，而通过获取a标签上的href属性，也就是getAttribute(‘href’),能够保留a标签上的href属性值，而这个值，正是我们所需要的。

# 结论：

React应用还是应该干净一些，避免使用 `dangerouslySetInnerHTML`，使用它会有很多tricky的事情发生，比如在componentDidMount的时候，dom上某个元素还处在undefind的状态，原因很可能是因为这个元素是由 `dangerouslySetInnerHTML`产生的，而他往dom里面添加节点是在componentDidMount之后。

我还是不很确定，通过history api完成跳转的，滚动记忆的情况。

react-router的假跳转，其核心当然还是利用了history api