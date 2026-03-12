---
title: React开发实践--1从动态加载聊起 | aoao.life
date: 2018-05-18 18:24:49
updated: 2026-03-01 06:20:12
---

![](http://7ktu2f.com1.z0.glb.clouddn.com/react.png)

---

# 写在前面

最近，在实际项目中，遇到了一个坑。正好，借由这个坑，来多聊一聊前端的东西。

# 需求

## 背景知识

- 我们的技术栈是React + React-Router+webpack4 的结构
- 我们的应用是电商网站，所有页面会有一些公共的部分。因此，我们需要在实际用到的组件外面，再包裹一层组件，我们叫做

### 知识点１　动态加载

在 webpack 2或 webpack 3的时代，我们自己写了一个动态加载的实现。  
这里的核心，大概就是下面这一行代码了。

|  |  |
| --- | --- |
| ``` 1 ``` | ``` loader={() => System.import('./ProductDetail').then(c =>  c.default)} ``` |

[Module 的加载实现](http://es6.ruanyifeng.com/#docs/module-loader)

<https://github.com/systemjs/systemjs>

包括我们当时，还自己实现了一个组件。嗯，他其实也是一个高阶组件。

到后来，我们引入了[React-loadable](https://github.com/jamiebuilds/react-loadable) 这个组件，同时由于能够使用`babel-plugin-syntax-dynamic-import`这个babel 插件，我们直接在引入组件方式上发生了改变。原来，我们的引入方式是`System.import`，现在我们则可以将import去掉，直接用来自未来的JavaScript语法规则来实现我们的需求了。

后来，阅读源代码我发现，我们自己实现的那个动态加载的高阶组件（），基础逻辑是相同的。

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 ``` | ``` return class LoadableComponent extends React.Component {     constructor(props) {       super(props);       init();     }   render() {       if (this.state.loading || this.state.error) {         return React.createElement(opts.loading, {           isLoading: this.state.loading,           pastDelay: this.state.pastDelay,           timedOut: this.state.timedOut,           error: this.state.error,           retry: this.retry         });       } else if (this.state.loaded) {         return opts.render(this.state.loaded, this.props);       } else {         return null;       } } } ``` |

在这里，只截取了部分代码。

我在这里，就不展示我们以前的组件实现了。我们只实现了React-loadable最基础的功能，事实上它还能够有以下几点优势：

- 当加载组件的过程中，给出过渡效果
- 当加载失败、加载错误后，给出一个类似404的页面，不致于白屏
- 能够进行retry 等行为

正是因为它有这些好处，并且有很多人的实践，我们才用到了它。

但是，无论是在引入React-loadable 之前还是之后，都有一个坑，我试图搞定它，却一直没有搞定，直到最近，才终于把这个坑填上。

下回《2-实现一个类似客户端的商品轮播图阅览交互》