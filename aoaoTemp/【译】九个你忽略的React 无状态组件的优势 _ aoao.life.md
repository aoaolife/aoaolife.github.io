---
title: 【译】九个你忽略的React 无状态组件的优势 | aoao.life
date: 2016-12-13 21:18:49
updated: 2026-03-01 06:20:12
---

> 本文转载自：[众成翻译](http://www.zcfy.cc/)  
> 译者：[zhangolve](http://www.zcfy.cc/@zhangolve)  
> 链接：<http://www.zcfy.cc/article/1980>  
> 原文：<https://medium.com/@housecor/react-stateless-functional-components-nine-wins-you-might-have-overlooked-997b0d933dbc#.7lv7ick6a>

React 0.14 引进了一种更简单的方式来定义组件，也就是无状态组件。这种组件使用了原生Javascript 函数，下图就是在用ES6的情况下，React 0.14 之前版本的组件写法和它之后对应的组件写法。

![](http://7ktu2f.com1.z0.glb.clouddn.com/react-stateless.png)

前者用了27行代码来实现，而后者只用了21行，这当然也没有什么了不起的。需要说明的是，由于性能方面的原因，右边代码中的`sayHi` 函数应该尽量避免这样使用。（原因见文末评论）

匆匆一览，上面左右两种代码形式似乎并没有太大区别，但是能够把**噪音**去掉就是**伟大**的胜利。（译者注：本文中所说的噪音(noise)和信号(signal)是来自于物理学中的概念。下文中其他处遇到这两个词，也是如此，不再解释。）

下面就是原因了。

### Class并无必要

诚然，我认为[围绕着ES6 的类的讨论已经太多了](https://medium.com/@housecor/in-defense-of-javascript-classes-e50bf2270a95#.92qa3ous7)。但是，我仍然认为纯函数是更加合理的，把讨厌的结构体和继承关系去掉无疑是件好事，体现了它的优势。

### 没有**this**关键字

就如上面的例子所示，无状态组件只是一个函数。因此，所有与Javascript语言中**this** 关键字有关的让人疑惑，使人讨厌的情况都会避免。没有了**this** 关键字之后，整个组件就会更加容易让人理解。只需要比较一下上例中的click 事件处理器，就能明白了。

|  |  |
| --- | --- |
| ``` 1 2 ``` | ``` onClick={this.sayHi.bind(this)}>Say Hi</a> onClick={sayHi}>Say Hi</a> ``` |

需要说明的是，对于无状态组件而言，**bind**这个关键字并非必须的。将**Class** 去掉之后，我们也无需通过绑定来将**this**关键字与上下文联系起来。 Javascript 中的 **this** 关键字给如此多的开发者造成了困惑，能够尽量不用**this** 是无状态组件的另一个优势。

### 被迫使用最好的方法

无状态组件是非常有用的[表现类组件](https://gist.github.com/chantastic/fc9e3853464dffdb1e3c)。表现类组件应该专注于UI层面而不是交互，应该避免在表现类组件中使用状态。状态应当通过更高水平的容器类组件，或者是通过FLUX/Redux 等等来管理。无状态组件不支持状态或者生命周期。\*\*这是一件好事。\*\*为什么这么说呢？因为它迫使你不再懒惰，让你不得不把容器类组件和表现类组件分离开来。

当然，你总是很愿意将状态添加到表现类组件之中，这也的确是一种很快的方法来实现一个功能。然而，无状态组件并不支持本地状态，你并不能够轻而易举地实现状态。因此，无状态组件就自动迫使当前组件保持纯函数形式。你也要被迫把状态管理放到它相应的位置：在更高水平的容器类组件中。

### 高信噪比

正如上图所示，无状态组件写起来代码量更少，这也就减少了噪音干扰。正如我在“[Writing Code for Humans 课程](https://www.pluralsight.com/courses/writing-clean-code-humans)” 中所讨论过的那样，好代码把信噪比（signal-to-noise ratio）最大化，27行代码的组件变成了21行，缩减了大约20%的代码量。如果你使用ES6 结构来处理属性(props)，那么结果是几乎所有的信号（signal）都是有用的。

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 ``` | ``` import React from ‘react’;  const HelloWorld = ({name}) => (    <div>{`Hi ${name}`}</div>   );   export default HelloWorld; ``` |

看见了吧，只用了一个函数，有一个参数，返回了一个标记(markup)。是不是很Nice ！那么，还能不能让代码量更少呢？

### 代码自动补全

如果你就像是我上面例子中那样，用ES6 拆解你的属性(props) ，那么你现在用到的所有的数据都只是作为一个简单的函数参数而已。这也就意味着，相较于基于类(class-based)的组件,你也得到了很好的自动补全代码支持。

### 很容易找出来臃肿的组件和低劣的数据结构

众所周知，如果[一个函数有很多参数，那它就是有代码异味的](http://app.pluralsight.com/courses/writing-clean-code-humans) 。当你使用ES6 架构来组织你的无状态组件时，这个参数列表已经清晰地传递了你组件的依赖关系。因此，也就很容易找到需要更改的组件。在上面的例子中，你也可以打破这个组件结构或者重新思考你正传递的数据结构。有时候，你并不需要传递一长串属性，而只需要传递一个对象。但是如果这些属性不仅仅与单独的一个对象相匹配，那么你就需要重构你的组件，把这个组件化整为零，分成若干个单独的组件。

### 便于理解

正如我们所见，当你看到一个无状态组件的时候，你就知道这其实就是一个简单的函数，它有相应的属性，可以生成HTML。即便在它的render 函数内部嵌套了很多其他的函数，它在概念上仍然是很简单的。这又是无状态组件的一个很大的优势所在。

### 便于测试

因为无状态组件只是一个纯函数，你的实现是非常直接的。给这些值对应的属性(props),我期望它返回这个标记（markup）。因此对于上面的示例 HelloWorld 组件而言，我可以把’Cory’ 这个值传递给 props.name ，这样这个组件就可以返回一个内部含有’Hi Cory’ 的 div 了。

> 由于有了React 的无状态组件，每一个组件都可以单独进行测试。无需模拟，也无需状态的操作，或者安装用于测试的特定的库。

### 表现

最后，无状态组件会在不久之后的将来提供更加优秀的性能表现。由于针对无状态组件，无需考虑状态或者生命周期，React 团队也计划在将来的版本中去掉不必要的检查和内存分配。而伴随更加优秀的性能表现而来的，是更好的语法规则，代码更加可读化，代码更加易于测试。怎么样，这么好的东西，赶紧用起来吧！

### 总结

基于以上这些原因，我们应该在可用之处尽量使用无状态组件。这也让我[热爱教授React 课程](https://www.pluralsight.com/courses/react-flux-building-applications) 有了一个新的原因。**在当今流行的框架中，React 的无状态组件是我见过的最优雅的实现可复用组件的方式，没有之一。** 是的，甚至[包括 Angular 2](https://medium.freecodecamp.com/angular-2-versus-react-there-will-be-blood-66595faafd51#.19cm9gx8c)在内，通通不在话下。

你们发现我有什么疏漏的地方？可以在下面评论框里留言哦！

注：

**来自原文下评论：**

> [Felipe Amorim](https://medium.com/@satya164/it-s-kinda-like-defining-your-functions-inside-the-render-method-535038b30ec3#.i1jjspjga) :如果在render 方法中定义你的函数的话，你不必再考虑绑定了。但是 由于无状态组件并不提供 shouldComponentUpdate 方法，当创建新的函数的时候，你也就不能阻止不必要的重新渲染了。这也就造成了性能上的问题。

> [Satyajit Sahoo](https://medium.com/@whymclovin/you-should-really-avoid-having-function-allocations-inside-statelless-components-43eb3b056818#.ucggqwnpl): 应该尽量避免在无状态组件内部使用其他函数，完全可以将这些函数放到无状态组件之外，通过传递属性值的方式来实现，这将给性能带来很大提升。