---
title: React开发实践--3对象引用的误区 | aoao.life
date: 2018-05-28 18:24:49
updated: 2026-03-01 06:20:12
---

![](http://7ktu2f.com1.z0.glb.clouddn.com/react.png)

---

一个电商应用，有他的一个基本的结构。为了简化我们的代码，我们每一个页面组件外面都会再套上一层`<BaseLayout/>` ,通过配置`<BaseLayout/>`，我们可以控制每一个页面是否需要使用公共页头(header),公共的底部导航(footer)。这当然也是一些很基础的功能了，在此不再赘述。

基于上面的需要，我们最初写了下面的代码

```
        const RouteWithLayout = ({loader = null, exportName = null, hideFooter = true, hideReturnTop = false, ...rest}) => {
                const loadableOpts = {
                    loader,
                    loading: LoadingComponent
                };

                if (exportName) {
                    loadableOpts.render = (loaded, props) => { // eslint-disable-line  react/display-name
                        const Component = loaded[exportName];
                        return <Component {...props} />;
                    };
                }
                const LoadableComponent = Loadable(loadableOpts);
                return (
                    <Route {...rest} render={matchProps => (
                        <BaseLayout hideFooter={hideFooter} hideReturnTop={hideReturnTop} {...matchProps}>
                            <LoadableComponent {...matchProps} />
                        </BaseLayout>
                        )}
                    />
                );
        };
```

看了前面 part-1的同学可能知道，我们在项目中引入了`React-loadable`这个第三方库，上面的代码也是基于它的实现。乍一看，他似乎没有问题。接下来，我们只需要写这样的配置就ok了。

```
        <RouteWithLayout exact path="/shopping-cart" hideFooter={false} hideReturnTop={true} loader={() => import('./ShoppingCart')} />
```

但是，在2-实现一个类似客户端的商品轮播图阅览交互 里面，我也已经提到过，我在此处遇到了一个坑。这个坑，也正是与上面我展示的代码有关。

再来简单回顾一下，当路由从/products/:productId 到/products/:productId/showpic，事实上，动态引入的组件还是那个`ProductDetail`组件。按照我们的期待，如果前后两次引入的是同一个组件，这个组件需要update，而不是重新mount。但是就如同我在《React开发实践–2》里面介绍的那样，当路由发生改变的时候，`</ProductDetail />`竟然进入了下一个生命周期。

究其原因，由于路由发生了改变，如果`RouteWithLayout`没有写其他的生命周期方法的话，那它必然会得到更新。那么我们来看看`RouteWithLayout`组件更新之后的影响。这时候我们发现`LoadableComponent`这个变量的引用实际上发生了变化。因此造成当render `<LoadableComponent {...matchProps} />`时，需要到下一个生命周期重新render。

可是对象引用发生了变化这种事情，我们应该怎么理解呢？说起来，这其实考察的还是JavaScript的基础。让我们暂时忘掉React这个框架，只提JavaScript。来看看下面这几行代码

```
let arr = []
for(let i=0;i<2;i++) {
    const foo={a:1};
    arr.push(foo)
}

console.log(arr[0]===arr[1]);  //false
```

大概学过半年JavaScript的同学，也都能明白这里为什么arr[0]和arr[1]并不相等了。这里还是谈谈我对这件事情的理解：

对于for循环内部的每次执行，都是一个`block`，每一个 `block`之间都相互独立。所以，我们也可以将上面的代码进行拆解。

```
let arr = []
 {
    const foo={a:1};
    arr.push(foo)
}
 {
    const foo={a:1};
    arr.push(foo)
}

console.log(arr[0]===arr[1]);  //false
```

这个时候，就更好理解了。对于每一个块里面的`i`变量来说，他只在当前块内有效，当前块执行完毕之后，他就会被`垃圾回收`，销毁掉了。因此当我们比较的时候，arr[0]和arr[1]之间就不相等了。

有同学可能会问了，你用的是ES6 的语法。ES5是这样的吗？of course！

```
var arr = []
for(var i=0;i<2;i++) {
    var foo={a:1};
    arr.push(foo)
}

console.log(arr[0]===arr[1]);  //false
console.log(i);
```

关于我的这个示例，ES5 和 ES6的结果并没有区别。如果硬要说有什么区别的话，那就是`i`这个变量是否在块级(block)之外继续有效。那相对于我本次讨论，实际上是另外一个话题了。

既然说到了这里，我们再想一想。怎么样才能让arr[0]与arr[1]相等呢？在**JavaScript，只能是在比较的两者为同一引用的情况下，才能实现严格相等**。所以按照这个思路，我们可以对上面的代码进行个改写。

```
const foo={a:1};
let arr = []
for(let i=0;i<2;i++) {
    arr.push(foo)
}

console.log(arr[0]===arr[1]);  //true
```

没错，就是把foo的生命提到for循环之外。这样的话，每次推入到arr这个数组中的值的引用就一定是相同的了。

这时候，让我们重新回到刚才遇到问题的React代码。`RouteWithLayout`当前是一个无状态组件，只要它的父组件发生了更新，它也会相应地发生更新。然后执行相应的代码。这其实就类似于我们上面提到的for循环结构。**每一次`RouteWithLayout`执行的时候，都像是for循环在执行其中一个block**，不难理解，每一次LoadableComponent的引用发生了变化。

所以，还是上面的思路，我们把`LoadableComponent`的声明放到`render()`方法之外，怎么做到呢？改写无状态组件为有状态组件。将这个对象声明以状态的方式存在于组件当中。这样就可以实现我们想要的效果，即如果动态加载的是同一个组件，则组件只会发生更新，而不会进入下一个生命周期。相应的代码在《React开发实践–2》中已经提到过了，再粘贴一遍。

```
        `
        import React from 'react';
        import ReactDOM from 'react-dom';
        import PropTypes from 'prop-types';
        import {BrowserRouter, Route, Switch, Redirect} from 'react-router-dom';
        import BaseLayout from './BaseLayout';
        import Loading from 'react-loading';
        import Loadable from 'react-loadable';


        const LoadingComponent = props => {
        // something 
        };


        class RouteWithLayout extends React.Component {
            state = {
                loader: () => {},
                exportName: null,
                LoadableComponent: null
            }

            static getDerivedStateFromProps(nextProps, prevState) {
            
                if (nextProps.loader.toString() === prevState.loader.toString() && nextProps.exportName === prevState.exportName) return null;
                const { loader, exportName } = nextProps;
                const loadableOpts = {
                    loader,
                    loading: LoadingComponent
                };

                if (exportName) {
                    loadableOpts.render = (loaded, props) => {
                        const Component = loaded[exportName];
                        return <Component {...props} />;
                    };
                }
                return {
                    loader,
                    exportName,
                    LoadableComponent: Loadable(loadableOpts)
                };
            }

            render() {
                const { hideFooter, hideReturnTop, ...rest} = this.props;
                return (
                    <Route {...rest} render={matchProps => (
                        <BaseLayout hideFooter={hideFooter} hideReturnTop={hideReturnTop} {...matchProps}>
                            <this.state.LoadableComponent {...matchProps} />
                        </BaseLayout>
                        )}
                    />
                );
            }
        }`
```