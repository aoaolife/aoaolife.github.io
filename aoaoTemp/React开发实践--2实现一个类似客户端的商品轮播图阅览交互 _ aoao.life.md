---
title: React开发实践--2实现一个类似客户端的商品轮播图阅览交互 | aoao.life
date: 2018-05-27 18:24:49
updated: 2026-03-01 06:20:12
---

![](http://7ktu2f.com1.z0.glb.clouddn.com/react.png)

---

# 写在前面

这篇仍然并不会也不打算去介绍或者科普`React`框架的基本知识点，但是会在行文中有很多涉及。

# 怎样实现的思路

一个电商APP, 要想让他的web HTML5 体验更接近客户端本身还是有很大的挑战的。怎样做出一些更符合客户端用户操作习惯的交互来，是前端开发中很重要的一个点。

我想要做的是一个类似客户端的商品轮播图阅览交互，总体来说，他的主要逻辑是：

1. 在商品详情页显示商品轮播图
2. 点击任意一张商品轮播图，能够全局浏览商品轮播图
3. 通过左划右滑手势可是在全屏状态下阅览商品轮播图
4. **点击返回键，退出全屏，回到商品详情页**

有赖于`react-photoswipe`　这个库的支持，它已经将前三项做得很好了。我希望做的其实是第四项。细化需求，它不仅仅要求能够回到商品详情页，还希望能够最大限度地优化性能，最好的体验就是像客户端那样。

这里，我采取的措施是，将我集成了`react-photoswipe`　这个库的组件放到</ProductDetail />　组件之中。

|  |  |
| --- | --- |
| ``` 1 ``` | ``` <ProductCarousel images={product.images} alt = {product.name} /> ``` |

接下来，我的想法是这样的：

> 当用户在商品详情页点击任意一张商品轮播图时，页面上全屏显示那张商品轮播图，同时，当前的路由发生改变,由`/products/:productId` 到`/products/:productId/showpic`，这样，当用户点击返回的时候，就能够实现从当前路由`/products/:productId/showpic`返回到了`/products/:productId`

但是，这个时候，我遇到了很多与`React-router`有关的坑，其实与其说是坑，倒不如说是知识上的不足。当我把这些知识补足之后，再来看，其实并不难了。

## React-router

### 第一个问题: exact

很明显，第一个问题是关于`React-router` 在`app.js` 中的配置的。前面介绍了我的总体思路，这个思路的一个关键点是**当路由发生改变的时候，`</ProductDetail />`组件不应该unmount 或者重新didmount**， 这样才能够让这种轮播图阅览交互更像是客户端的体验。

这时候，用到的第一个知识点是`React-router`的exact 配置。这本身并不是什么难点，我在这里只是想说明它的这一妙用。

由于我们大部分的`React-router`的匹配都采用了exact的匹配，在这个时候，我把原来对商品详情页的exact匹配去掉了，使得能够实现前述我的思路。

### 第二个问题: `</ProductDetail />`组件的生命周期

前面说了，我们在这个项目中，为了优化前端性能，使用了动态加载，来进行`split coding`。这个时候，我发现，如果使用了动态加载，我的`</ProductDetail />`组件每次进入轮播图全屏页面时，都会因为进入到了下一个生命周期，而不能进入轮播图全屏页。

这个问题出在哪里呢？原来这个问题是由于`React-router`以及它所关联的`React`生命周期造成的。

我以前有个误区，不知道各位读者是否也会存在这样的误区。就是React简单地认为它是单向数据流，除非父组件传递給子组件能够改变父组件本身的属性，否则，子组件的更新，不会引起父组件的更新甚至进入下一个生命周期。

但是，当然没有那么简单。

还是以我上面的问题为例，为什么会出现那样的问题呢？原因是：当一开始进入轮播图详情页面时，在我的`<ProductCarousel />`这个子组件发生了变化，他引起了路由的变化。由于我的路由管理由`React-router`完成，实际上顶部的`<Switch>`也相应地发生了更新，甚至可以这么说， `<Switch>`组件也必须发生更新，只有这样，他才有存在的意义。而紧接着，由于我们对动态引入的错误使用，造成了`</ProductDetail />`组件被迫重新装载，而他的重新装载又直接造成了他进入下一个生命周期。

关于我们是怎样错误使用动态引入的，以后会详细来解释。

这里，还是针对我刚刚提到的误区来谈一谈。所以，还是说回来，这当然不能算是坑，这是对知识理解的不深刻。

看到这个问题之后，我最初想到的是: **如果路由改变了，而加载的组件（import）并没有改变，就不更新这个组件的状态**

但是，马上就发现了问题，还是这个例子：路由从`/products/:productId` 到`/products/:productId/showpic`发生了改变，这个时候我们没有改变`</ProductDetail />`组件的状态，则他的属性（location,props）较之前并没有发生改变。这本身就不是正常的，也就会从根本上造成虽然一个问题解决了，但是总还有新的问题产生。为什么呢？因为你没有按照规律办事啊！

`React-router`的思想是什么呢？其中一个思想就是组件上的React-router赋予的属性（location,history )是与实际相一致的。但是刚才，我试图通过调用 `componentWillReceiveProps`方法，来实现阻止组件更新的目的。

结果造成什么问题了呢？

一开始，我点击轮播图，路由切换，打开轮播图，没有问题。可是当我点击返回键的时候，由于我前面的判断：**如果路由改变了，而加载的组件（import）并没有改变，就不更新这个组件的状态**，导致没有退回到商品详情浏览页。这当然是不正常的了。

我们应该顺应`React-router`的设计思想，最后采取的办法是：**如果路由改变了，而加载的组件（import）并没有改变，这个装载的组件不变，但他的属性(location,history)要相应地发生改变，他必须仍然在原有的生命周期中**

可能听起来，还是有点抽象，还是直接上代码：

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 ``` | ``` import React from 'react'; import ReactDOM from 'react-dom'; import PropTypes from 'prop-types'; import {BrowserRouter, Route, Switch, Redirect} from 'react-router-dom'; import BaseLayout from './BaseLayout'; import Loading from 'react-loading'; import Loadable from 'react-loadable';   const LoadingComponent = props => { // something  };   class RouteWithLayout extends React.Component {     state = {         loader: () => {},         exportName: null,         LoadableComponent: null     }      static getDerivedStateFromProps(nextProps, prevState) {                 if (nextProps.loader.toString() === prevState.loader.toString() && nextProps.exportName === prevState.exportName) return null;         const { loader, exportName } = nextProps;         const loadableOpts = {             loader,             loading: LoadingComponent         };          if (exportName) {             loadableOpts.render = (loaded, props) => {                 const Component = loaded[exportName];                 return <Component {...props} />;             };         }         return {             loader,             exportName,             LoadableComponent: Loadable(loadableOpts)         };     }      render() {         const { hideFooter, hideReturnTop, ...rest} = this.props;         return (             <Route {...rest} render={matchProps => (                 <BaseLayout hideFooter={hideFooter} hideReturnTop={hideReturnTop} {...matchProps}>                     <this.state.LoadableComponent {...matchProps} />                 </BaseLayout>                 )}             />         );     } } ``` |

### 第三个问题: 匹配不匹配

我们知道，在客户端的图片阅览里，实际上，是不能直接通过访问地址的方式，来全屏浏览商品轮播图的，这是一个更深层次的交互设计，因此我在`</ProductDetail />`组件的`componentDidMount` 方法中写下了这样的代码

|  |  |
| --- | --- |
| ``` 1 2 3 ``` | ``` if (!this.props.match.isExact) {     this.props.history.replace(this.props.match.url); } ``` |

如此依赖，当初次载入`</ProductDetail />`组件时，一律显示商品详情页面。

## 最后

最终的实现效果，前面提到的指标都已经完成了。也能够比较完美地使用动态加载来加载组件了。