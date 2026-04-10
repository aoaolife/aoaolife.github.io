---
title: 薛定谔的导航栏 | aoao.life
date: 2018-05-30 18:24:49
updated: 2026-03-01 06:20:12
---

![](http://7ktu2f.com1.z0.glb.clouddn.com/javascript.png)

---

# 需求

自从在本单位工作之后，大部分时候做的都是移动开发。因此，也就不可避免地会遇到很多移动开发的坑。这些坑来源于真实的业务场景，因此，简单总结一下。

第一个坑是关于导航栏的，我们知道市面上的大部分国产APP，它的iOS版本和Android版本，在UI设计上几乎都没有区别，我们做的APP也是如此。因此，也是会在APP的底部有一个导航栏。

这个时候，有意思的事情就出现了。如果是H5页面的话，通常情况下，这个底部导航栏都是通过fixed定位来实现的。而由于移动终端虚拟键盘的作用，Android和iOS对此的反应又并不相同，因此，就出现了这个坑。

我看了很多APP，比如美团，微信，孩子王等APP，当光标聚集到输入框上面的时候，往往会有一个动画，然后将这个搜索页全屏处理。且不论这些APP是否是内嵌H5的，但这样的交互，如果在H5上面也如是一样，就能避免上面提到的由于fixed定位产生的坑。

# 这个坑的详细表现

在iOS上面的表现：

> 软键盘唤起后，页面的 fixed 元素将失效（即无法浮动，也可以理解为变成了 absolute 定位），所以当页面超过一屏且滚动时，失效的 fixed 元素就会跟随滚动了。（ 来自[Web移动端Fixed布局的解决方案](http://efe.baidu.com/blog/mobile-fixed-layout/) ）

而在Android上面的表现是:

软键盘唤起后，页面的 fixed 元素并没有失效，但是视窗的高度将重新被计算。(原来的视窗高度-虚拟键盘的高度)

所以，如果我们仍然要把底部导航栏和元素放在一个页面上，就需要着手进行改造。不然，就非常影响用户体验。

## 解决方案

[Web移动端Fixed布局的解决方案](http://efe.baidu.com/blog/mobile-fixed-layout/) 提到的当然是一种解决方案，但是，我试着总是不能符合我的要求。

这就说会到我这篇文的题目《薛定谔的导航栏》，我的想法是这样的：如果弹出了虚拟键盘，则将导航栏的样式设置为 `display:none`，反之，如果隐藏了虚拟键盘，则将导航栏的样式设置为`display:block; position:fixed`。所以，一个小白，如果看到了弹出虚拟键盘的页面，你问他，现在到底页面上存在不存在导航栏呢？

假如他回答存在，你把这个虚拟键盘隐藏掉，结果当然是有的。可是当时有没有呢？并没有吧。

加入他回答不存在，你把这个虚拟键盘隐藏点，结果却是有的，很明显又和实际看到的不一样了。

# 知识点

所以接下来和核心问题，就是如何在iOS上和Android上去检测虚拟键盘的弹出和隐藏了。

下面进入直接贴代码说明问题环节，这里要说明一下，由于我使用了React框架，因此，实际上，我下面写的代码都是JSX文件的一部分

## iOS

```
addIosKeyboardHandler = () => {  // IOS上，弹出输入框后，同样隐藏底部导航。
    document.addEventListener('focus', this.IosFocusHandler, true);
    document.addEventListener('focusout', this.focusoutHandler, true);
}

removeKeyboardHandler = () => {
    document.removeEventListener('focus', this.IosFocusHandler, true);
    document.removeEventListener('focusout', this.focusoutHandler, true);
}

IosFocusHandler = () => {
    if (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA') {
        window.scrollTo(0, 0);
        const footer = document.getElementById('footer');
        footer.classList.remove('fixed');
        footer.classList.add('hidden');
        window.setTimeout(() => {
            document.activeElement.scrollIntoViewIfNeeded();
        }, 100);
    }
}
focusoutHandler =() => {
    window.scrollTo(0, 0);
    const footer = document.getElementById('footer');
    footer.classList.add('fixed');
    footer.classList.remove('hidden');
}
```

这里有几个点需要注意：

- focus事件需要通过捕获(capture: true)的形式才能触发，在document上面的监听
- focusout要比blur事件在描述虚拟键盘隐藏这件事情上更加准确，blur事件不会冒泡
- 当弹出输入法准备敲击时，先将页面滚动到顶部

## Android

Android 上和IOS上又有一些不同，主要的不同点在于：当弹出虚拟键盘后，通过点击返回键，隐藏掉虚拟键盘，这个时候，如果我们对此不做任何处理的话，那么光标还是会在输入框里面，换句话说，此时对于输入框俩说，并没有发生blur事件，因为很显然，光标还在输入框里面。

因此还是根据Android上的表现来做判断，既然弹出虚拟键盘会让视窗的高度变小，而收起虚拟键盘又会让视窗的高度变大，那么我们就从这里着手。

```
addAndroidKeyboardHandler = () => {
    this.maxHeight = document.documentElement.clientHeight;
    window.addEventListener('resize', this.AndroidKeyboardHandler.bind(this, this.maxHeight));
    document.addEventListener('focusout', this.focusoutHandler, true);
}

removeAndroidKeyboardHandler = () => {
    window.removeEventListener('resize', this.AndroidKeyboardHandler.bind(this, this.maxHeight));
    document.removeEventListener('focusout', this.focusoutHandler, true);
}

AndroidKeyboardHandler = maxHeight => { // 解决 Android 弹出输入框时，底部导航一同浮起的问题。隐藏底部导航
    const presentHeight = window.innerHeight;
    const footer = document.getElementById('footer');
    if (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA') {
        if (presentHeight < maxHeight) { // 隐藏底部导航
            footer.classList.remove('fixed');
            footer.classList.add('hidden');
            window.setTimeout(() => {
                document.activeElement.scrollIntoViewIfNeeded();
            }, 100);
        } else {
            document.activeElement.blur();
            footer.classList.add('fixed');
            footer.classList.remove('hidden');
        }
    }
}
```

## 小提示

这个时候只需要把我上面代码中的addIosKeyboardHandler 方法在`componentDidMount`的时候，进行触发即可。

当然，这里可能要补充一个小知识点，由于`componentDidMount`的时候，通过`React`渲染的dom已经处于loaded的状态，因此无需再像以往通过`window.onload`或者jq的`$(document).ready`去添加事件处理程序。

## 下面的问题

这样的方法可以解决大部分的问题。但是还是会有一些历史遗留代码与此方案相处地并不融洽。

比如在购物车页面，会有一个输入框，可以改变选定商品的数量。购物车的结算button是fixed的定位，当时考虑到在他下面还有导航栏，因此，提前计算好了导航栏的高度。于是这个部分的样式大概是这样的：

```
  display: fixed;
  bottom: 1.4rem;
```

恩，我们使用了rem布局。结果就会造成由于我前面的处理，只会在出现虚拟键盘的时候将footer（底部导航栏）隐藏掉，并不会对结算button进行处理，因此，如果看Android上的表现，这个时候，这个button所在的部分就会和键盘之间有1.4rem的间距。而诡异的是，结算button部分还是处于fixed的状态，而这，并非我所期待的。

这就是另外一个问题了。

所以，还是说回来。这也是为什么之前看到其他一些人有一些友情提示：**在做移动开发的时候，不要将input元素和其他fixed的元素放在一起**。而像我这种更要命，我直接在页面底部放了两个fixed的元素。

我目前的措施是针对这种情况，单独处理。毕竟，这也只是特例。