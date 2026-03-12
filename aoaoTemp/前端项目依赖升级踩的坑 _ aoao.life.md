---
title: 前端项目依赖升级踩的坑 | aoao.life
date: 2022-01-14 14:41:16
updated: 2026-03-01 06:20:12
---

## 背景

前几天对工作项目的前端依赖包做了升级，简单说一说这个过程。

首先说一说背景，我来这家公司两年半的时间。单就我此次升级的这个项目而言，有几次大的转变。

第一次，是将这个项目从一个父项目中拆出来，形成了一个微前端项目。这一次拆分，奠定了这个项目的基础。我也给这个新拆分出来的项目，提交的第一个PR。

第二次，是引入typescript的支持，这个时间点，大概是一年半以前，这个工作由我来做的。2020年的时候，我在另外一个项目里，引入了typescript的支持，随后也将这个配置同步到了这个项目当中。

第三次，是引入了私有库。在此之前，我们只能使用public npm package，但是到了这个时候，我们已经可以引入私有库，使用私有库的共享库，这个背景则是为了写自动化case。

经过上面三次大的升级，这个前端依赖包，到了这个时间节点有了一些问题。

- babel相关的配置比较老，历次升级都没有动过。还是刚刚拆分时的版本
- eslint相关的配置比较老，历次升级都没有动过。还是刚刚拆分时的版本
- eslint没有对typescript的支持，eslint基本处于荒废状态了。
- 一些老的业务依赖，也没有得到升级，可能会有些漏洞

所以，此次升级我也主要针对这样一些方面展开

## 业务依赖

- yup

业务依赖对这个叫做`yup`的包进行了升级，然而很快发现了一个问题。由于这个项目，还需要对IE11进行支持，但是我当时升级到了v0.32,结果经过测试，发现在IE浏览器上打不开页面，后来查到了一些线索：

<https://github.com/jquense/yup/issues/1175>

原来v0.32已经不再支持IE11了，因此只好降级到了支持IE11的最高版本。

## babel 升级

我们之前用的babel配置大概还是v7.5，后来我们就升级到了v7.15.在这个过程中，也发现了另外一个问题。

babel的preset-env会随着版本的升级，而将很多的proposal plugin包含在其中。例如，我们可以从v7.15.6这个版本的源码中看到，都有那些plugin被包含其中，

<https://github.com/babel/babel/blob/v7.15.6/packages/babel-compat-data/scripts/data/plugin-features.js>

官方文档上有一段说明，可以帮助我们理解这件事情：

> Note: @babel/preset-env won’t include any JavaScript syntax proposals less than Stage 3 because at that stage in the TC39 process, it wouldn’t be implemented by any browsers anyway. Those would need to be included manually. The shippedProposals option will include Stage 3 proposals that some browsers have already implemented.

简而言之，就是随着时间的推移，越来越多的proposal，也就是提议被纳入ES的标准当中，因而，babel的预置环境设置中，就已经有了这些内容。至于为啥有这样一个过程，我之前也写过：

> 我记得刚开始使用babel的时候，的确有时候会用上一些stage-2,stage-3 的特性，那时候还为了了解这些所谓的stage去看了ECMASCRIPT 新版本发布的[流程](https://github.com/tc39/proposals)，觉得也很有意思。但是虽然有意思，配置起来却的确繁琐，有时候，你的确需要为了配置这样一个`Babel`看好多相关文档，这无疑算是一个痛点了。现在好了，就如同文档里面所提到的：在没有任何配置选项的情况下，babel-preset-env与 babel-preset-latest行为相同

随着我们升级Babel，我们的preset-env也得到了升级。因此原本需要额外安装的plugin，也已经放在了标准当中。

正是基于以上的原因，随着升级babel的配置，我也将一些插件从package中删除了，也从babel config里面删除了。这样的改变之后，无疑配置更加简洁了。

关于babel的更多内容，我自己早在2018年，就写过一些理解，可以看[这里](https://hktkdy.com/2018/08/09/201808/babel-and-polifill/)

另外一个与babel有关的改动，是对[quickbaseoss/babel-plugin-styled-components-css-namespace](https://www.npmjs.com/package/@quickbaseoss/babel-plugin-styled-components-css-namespace) 这个包进行了升级，当时我们之所以要使用这个包，是因为想要提高styled-components样式的权重，根据[styled-components官方文档](https://styled-components.com/docs/advanced)的说法，我们引入了这个包。后来发现当升级其他babel配置后，这个包如果不升级将无法编译，所以我们从原来一个rc版本升级到了v1.0.0的版本

## eslint相关升级

引入eslint并不是我来完成的，但是使用eslint却是我主张推动的。大概在一两年以前，我为了测试a11y，想要通过eslint来辅助代码坚持。也正是在那个时候，我在这个项目里做了一件事情，也就是经过`npm run lint`之后，error清零。但是后来有很长时间，没有再管lint相关的事情，造成又有了error数量，而且前面也已经提到typescript代码之前是没有经过lint的，这也是需要解决的问题。

本次升级，我将eslint的版本升到了v7.32.这应该是v7版本的最后版本。

这里的重点是eslintrc的配置，我们之前使用的是babel/parser，但是当我想要去用eslint检查ts或者tsx文件时，兼容性并不是很好。具体的问题，大概如这个问题所说：<https://stackoverflow.com/questions/62535621/typescript-casting-with-babel-eslint-parsing/68981466#68981466>

所以我的解决办法，也正式将parser替换掉

> parser”: “@babel/eslint-parser”,

不过当我替换了parser之后，又要去配置parserOption这个时候，又发现一个问题。有些文件不能够被resolve。

我也去看了ts的官方文档，看了他们怎样去寻找文件路径

![](https://storage.googleapis.com/13823zxw.appspot.com/AQADkrExG9WX8FZ-.jpg)

我最后发现，原因大概是像这个issue所说: <https://github.com/microsoft/TypeScript/issues/26859>

![](https://user-images.githubusercontent.com/11130898/93716163-e807b080-fb8d-11ea-8c08-b23d9e577daf.png)

我不得不为了匹配common/index.tsx而写一条独立的path。

这个问题，算是升级eslint的过程中的一个大问题了。

其他的小问题还包括：

- tsconfig 中target应该为es2019,理由是我们的jenkins环境是node12，而target如果太高，会让测试代码无法运行
- `eslint '*/**/*.{js,ts,tsx}'` 这样的glob语法无法在windows shell下运行，但可以在wsl下运行，与node版本关系不大([ref](https://stackoverflow.com/questions/27594550/glob-wildcards-in-windows-npm/30114333)),一个兼容的写法可以是`eslint --ext .js,.jsx,.tsx,.ts .`

### tsconfig 重点字段理解

- target

target这个字段，指编译出来的目标js标准。前面已经提到，我在这个项目中，有两处用到了tsconfig，一个是eslint，它其实并不做编译，因而并不关心target，另外一处则是测试case，这些测试case最后需要编译成js语法来跑在node环境下，因此也就出现了上面说的一个坑，即node12下，target最大只能是es2019.

- moduleResolution

指定typescript使用怎样的方式去找模块，一般我们按照node的方式去找就是可以的。所以这个字段的值是”node”就可以。

- allowJs

是否允许在代码库中有JavaScript的存在，对于老的项目来说，我们也只能选true，当然如果是新项目，或许我们可以更改这个选项。

- paths

这个字段可以定义一些alias。这样的话，在我们的代码中，我们就无需去写长长的引用路径了，直接写我们定义好的path就可以了。不过怎样写path，就又说回到我前面遇到的那个坑了。

这里多说两句，之前我们实际上是有三处定义alias的地方，分别是

- webpack config alias
- eslint import/resolve alias
- tsconfig paths

前面我们将eslint的parser改为了typescript及parser option改为了typescript config之后，我们已经不需要再用eslint 去做import resolve alias了，因为eslint这块的检查，都交由typescript去控制了

所以，什么时候，我们能够将现在这两处alias改成一处呢，大概就是啥时候我们将babel-loader改为typescript-loader的时候，但是需要改吗，也未必。

## babel与ts的关系

需要说的另外一点是，随着Babel的升级， 需要理清楚这层关系。我们仍然是把babel-loader用做我们的webpack中js的解析器，我们只是在eslint里，把解析器换成了typescript。

目前看来，有可能出现的一种场景是，代码能够在webpack里正常执行，但是由于eslint的原因，在vscode里可能会报一些error提示。这应该是由于，babel有的语法，typescript并没有，因而就会有这样的问题了。我们会尽量取他俩的交集来书写代码，不过也希望有一天，我们只需要保留一个。

## 总结

经过了这样的过程，上面的升级基本上就完成了。通过升级，通过lint，也暴露了一些问题。比如我们的代码中还在使用`componentwillreceiveprops` 这样的语法，又比如我们的代码没有做到持久化组件，造成了一些问题。这些问题，通过[no-unstable-nested-components](https://github.com/yannickcr/eslint-plugin-react/blob/master/docs/rules/no-unstable-nested-components.md) 这条规则暴露了出来。所以，之后我们还会做一个工作，就是去把这些有问题的代码加以修改。