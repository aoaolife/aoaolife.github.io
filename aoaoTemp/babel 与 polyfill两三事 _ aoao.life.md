---
title: babel 与 polyfill两三事 | aoao.life
date: 2018-08-09 09:24:49
updated: 2026-03-01 06:20:12
---

熟悉前端开发的朋友，应该对 `Babel`这个项目并不陌生，早在两年多以前，阮一峰大大就已经写过文章[《Babel 入门教程》](http://www.ruanyifeng.com/blog/2016/01/babel.html) 对他进行了介绍，那个时候，其实`Babel`应该已经算得上是网红开源前端库了。这两年，`Babel`其实也一直在发展，我这里想说的是我看到的`Babel`的成长

# babel-preset-env

首先是`babel-preset-env`，详细的介绍文档在这里：<https://www.babeljs.cn/docs/plugins/preset-env/>

我也并不会去介绍怎么去用这个，只是想谈谈自己的体会。我记得刚开始使用babel的时候，的确有时候会用上一些stage-2,stage-3 的特性，那时候还为了了解这些所谓的stage去看了ECMASCRIPT 新版本发布的[流程](https://github.com/tc39/proposals)，觉得也很有意思。但是虽然有意思，但是配置起来却的确繁琐，有时候，你的确需要为了配置这样一个`Babel`看好多相关文档，这无疑算是一个痛点了。现在好了，就如同文档里面所提到的：

> 在没有任何配置选项的情况下，babel-preset-env 与 babel-preset-latest（或者babel-preset-es2015，babel-preset-es2016和babel-preset-es2017一起）的行为完全相同。

# babel-polyfill

## 为什么你这么大

我们都知道，`Babel`为了存心让我们配置起来更困难，故意将他的功能分拆成了两部分，其一是语法上的转化，这个默认情况下他自会帮我们处理。而另外一部分，就是新API的polyfill，需要我们引入`babel-polyfill`来完成。当然，我前面说，`Babel`是存心折腾开发者的确是开玩笑的，毕竟并不是所有的时候我们都需要polyfill的。这有点像是React项目也有两个核心包,`React`和`ReactDOM`类似。

```
    import React from 'react';  
    import ReactDOM from 'react-dom';
```

babel-polyfill是好东西，能够将新API作用在老的浏览器上，但是我们要注意不要滥用。比如我们随便在百度上搜索一篇文章，讲解如何使用 [babel-polyfill的引用和使用](https://www.cnblogs.com/princesong/p/6728250.html),往往都会看到有这样的描述：

```
module.exports = {entry: ["babel-polyfill", "./app/js"]};
```

这样做，从功能实现上来看当然是没有错的。但是，如果我们原来的入口是

```
module.exports = {entry: ["./app/js"]};
```

那么很容易就能够发现由于入口处增加了`babel-polyfill`，导致webpack在处理之后，最终的到的入口核心js文件比原来增加了有100kb左右。对于这个问题，也已经有[issue](https://github.com/babel/babel-loader/issues/163),不过很奇怪这位网友把issue提到了babel-loader这个项目下。

然后针对这个问题，有老外网友介绍到了`transform-runtime`等。但是经过我的测试，这也并不是一个很好的实践。

## 动态识别

为了polyfill 这件事情，其实是有两种思路可循的。第一个思路是根据浏览器缺失哪些特性来补全哪些特性，这个思路的代表是 [polyfill-service](https://polyfill.io/v2/docs/),这个[项目](https://github.com/Financial-Times/polyfill-service) 。它能够根据浏览器的UA来判断当前浏览器缺失哪些特性，进而进行补强。但是经过我的调研，这个项目在天朝可能还存在水土不服的问题，一个很明显的事实是将安卓微信内置的QQ浏览器X5交给这个库来处理，它会认为当前的浏览器是safari，原因大概是因为UA上有safari这个字段。考虑到我们天朝还有类似微信这样很怪异的UA，我认为并不适合在当前这个时间来对此进行实践。(在这里多说两句，polyfill-service这个库和另外一个知名项目fastclick同属于英国金融时报，而最近我发现fastclick在现代浏览器上也有一些tricky的地方，在他们的issue区有能够找到一些吐槽，然而，这个库已经两年多没有人维护了)

把polyfill-service仍在一边，我们接下来说另一个思路。能不能根据我使用了多少新API，来决定我引入多少polyfill的内容呢？比如我只在我的项目中使用了ES6的`set`，没有使用其他新API。那么我引入polyfill的时候，能不能只引入set的polyfill呢？答案当然是可以的，这就是babel-7的新特性，没错，由于当前稳定版是babel-6，因此这个特性还处在测试阶段。但是根据我自己的测试，表现很多。

不过有趣的是，虽然还只是Beta版，Babel却将之写入了正式版的文档当中，结果当时我为了测试这个新特性，都已经测试到怀疑人生了。文档戳[这里](https://babeljs.io/docs/en/babel-preset-env/#usebuiltins),感兴趣的同学可以去看看。总之，实际上只是对babel增加一项配置。

```
      "useBuiltIns": "usage"
```

不过由于涉及到升级`Babel`，当时我在测试的时候，还是有些不顺的。但是一旦迁移成功，应用上`useBuiltIns`的这项配置，的确能够让polyfill的体积大幅度减小。

# browserlist

前面的动态polyfill，的确可以让webpack生成的js文件体积更小，但是能不能再小一些呢？毕竟我们前端开发的目的就是极致的用户体验，当然可以。这个时候browserlist能够帮到我们。

关于这个话题，网路上相关的文章非常多，我就不再多谈了。

感兴趣的同学，可以看看`ant-design`项目中使用的browserlist。

<https://github.com/ant-design/antd-tools/blob/master/lib/getBabelCommonConfig.js>