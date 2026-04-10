---
title: 在webpack项目中配置postcss，实现autoprefix | aoao.life
date: 2018-09-01 09:24:49
updated: 2026-03-01 06:20:12
---

##１希望能够让开发者写代码更轻松

以往没有引入postcss autoprefixer之前，我们为了css相关特性能够在各个浏览器上的兼容，引入了scss，利用它的mixins来实现prefix。但是每一个mixin　都有一个自己的语法。

比如以往，如果我们我们想要写一条

```
div {
    display: flex;
    align-items: center;
    justify-content: center;
}
```

为了各个相对早期浏览器的prefix，我们需要mixin，然后这样写

```
import 'common/flexbox';

div {
    @include flexbox;
    @flex(1);
    @justify-content(center);
}
```

然后按照这样的约定，来加上需要的prefix。

这当然是一个方法，但是对于开发者来讲，实际上增加了一些学习成本，而且相当于将标准放到了一边，去使用另外一套标准。

我们之前的mixin，由于已经有好几年的历史。当时为了兼容市面上那些还有很大市场份额的浏览器，prefix写的很全。比如下面这个mixin　flexbox到代码:

```
@mixin flexbox {
    display: -webkit-box;
    display: -webkit-flex;
    display: -moz-flex;
    display: -ms-flexbox;
    display: flex;
}
```

为了写这篇博客，我又确认了一下，那个mixin flexbox的开源库来自于2013年，距离现在已经五年了,五年的时间，淘汰了很多过时的浏览器，五年前可能需要兼容到ie8，现在移动端开发甚至完全可以无需理睬IE的存在，所以这样的一套prefix就显得有些过时了。那位说了，我更新我的mixin不就好了，比如在2018年做移动端开发，也许我只需要将上面的代码改写成:

```
@mixin flexbox {
    display: -webkit-flex;
    display: flex;
}
```

但是我们也许需要想地更远一些，也许再过两年，我们甚至不需要对-webkit-的支持了。那时候，难道我们又要改一遍这个mixin吗？

postcss解决了这样一个痛点，可以直接书写标准的css（现在是css3，但是过几年也可能就是css4了），我们有了这样的工具，再指定一个浏览器兼容表，就能够实现自动prefix，而这相比于sass/scss　mixin的方式，维护起来更加简单，应该是一个很好的实践。

## ２对用户更友好

这当然也是显而易见的，以前我们可能为了兼容更多浏览器，而写更多的prefix，可是随着时间的推移，很多prefix完全并不需要。我们通过postcss来处理，简单明了，缩小了生成的css文件的体积，最后反映到用户那里，会快上一丢丢！

# 步骤

1 安装postcss-loader ,postcss-preset-env

```
yarn add -D postcss-loader  postcss-preset-env
```

安装postcss-preset-env，无需再安装autoprefixer，由于postcss-preset-env已经内置了相关功能。

２　添加.browserlistrc　文件到项目根目录

> 1% in CN  
> android >= 4.4  
> ios >= 8  
> not ie <= 11

这个需要根据项目的世纪情况来自由选择，我是考虑我们的项目是移动端项目，且确实有用户在用Android４.4　或者ios８，但是再很难看到低于这些版本之下的系统了。

３配置postcss.config.js

```
module.exports = {
  loader: 'postcss-loader',  
  plugins: {
      'postcss-preset-env': {},
    }
}
```

4　配置webpack.config.js

```
{
test: /\.scss$/,
use:[ 
    MiniCssExtractPlugin.loader,
    {
        loader: 'css-loader',
            options: {
                root: 'static',
                minimize: true,
                importLoaders: 1
            }
    },
    'postcss-loader',
    'sass-loader',
]
},
{
test: /\.css$/,
use: [
    MiniCssExtractPlugin.loader,
    {
        loader: 'css-loader',
            options: {
                root: 'static',
                minimize: true,
                importLoaders: 1
            }
    },
    'postcss-loader'
]
}
```

由于我们的项目中使用了scss，因此需要sass-loader。这里需要注意各个loader的顺序，一开始我的顺序是MiniCssExtractPlugin.loader,css-loader，sass-loader，　postcss-loader，结果发现并没有能够autoprefix，原因是如果想让postcss-loader认识并且处理，需要先用sass-loader进行处理，转化成postcss-loader可以认识的代码。

另外需要注意的是，我们这里还在使用css-loader v0.28，目前已经有了v1.0，版本改动很大，以至于我们暂时不能升级。