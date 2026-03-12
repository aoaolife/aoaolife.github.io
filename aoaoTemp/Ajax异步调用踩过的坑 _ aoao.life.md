---
title: Ajax异步调用踩过的坑 | aoao.life
date: 2016-12-23 15:18:49
updated: 2026-03-01 06:20:12
---

![](http://7ktu2f.com1.z0.glb.clouddn.com/qianduan3.jpg)

---

# 写在前面

这些天在看朴灵的[《node.js 深入浅出》](https://book.douban.com/subject/25768396/) 这本书，也对Javascript中的异步调用了有了更深入的一些理解。想起来我最早遇到的有关JS中的异步问题，应该就是在学习Ajax 的时候，当时对Ajax的概念甚至还不清楚，只是晓得Ajax能够用来接收后台API传过来的数据，后来也踩了几个坑，便有了想要梳理一番的想法，遂有此文吧。内容基础，倘若有不对之处，欢迎讨论。

# Ajax的写法问题

曾经在网上看到有人发过帖子，去面试的时候面试官要求手写原生JS的Ajax格式，于是帖子下面纷纷在喷那位面试官。在这里，我说的Ajax 指是调用jQuery 库之后的Ajax写法了。

首先，我说一下我自己最常用的一种[Ajax写法](https://www.sitepoint.com/use-jquerys-ajax-function/)

```
    $.ajax({
       url: 'http://api.joind.in/v2.1/talks/10889',
       data: {
          format: 'json'
       },
       type: 'GET',
       async:true,
       error: function() {
          $('#info').html('<p>An error has occurred</p>');
       },
       dataType: 'jsonp',
       success: function(data) {
          var $title = $('<h1>').text(data.talks[0].talk_title);
          var $description = $('<p>').text(data.talks[0].talk_description);
          $('#info')
             .append($title)
             .append($description);
       },
       
    });
```

# 同步和异步

我曾经有一段时间弄不明白Ajax的同步和异步，就像是这个[问题中](http://stackoverflow.com/questions/14220321/how-do-i-return-the-response-from-an-asynchronous-call) 给出的写法那样写。

```
function foo() {
    var result;
    $.ajax({
        url: '...',
        type：'GET',
        success: function(response) {
            result = response;
            // return response; // <- I tried that one as well
        }
    });
    return result;
}
var result = foo(); // It always ends up being `undefined`.
//use result continue
```

当发现不能实现自己想要的效果的时候，我通过网络搜索，也为了图省事，找到了这样一种写法。

```
    function foo() {
    var result;
    $.ajax({
        url: '...',
        async:false,
        type:'GET',
        success: function(response) {
            result = response;
            // return response; // <- I tried that one as well
        }
    });
    return result;
}
var result = foo(); // have the result value,not undefined
//use result continue
```

上面的写法，相比于前面result为undefined 的情况，显然从结果上看是成功了，两种写法区别，只在于在$.ajax()函数内部添加了一个async:false 的条件，也就是将同步属性设置为了错，即此时调用Ajax之后实际上是走的同步流程。如果直接使用这样的写法，使用Chrome浏览器的话，打开浏览器的控制台后，调用Ajax的时候，控制台上会输出警告信息，不建议使用这种同步方法。然而，我当时以解决问题为目的，解决完这个问题很长一段时间，我也就没有再深入研究这个问题。

# 可以这样用

后来看了一些关于JS异步方面的博客和书籍，觉得既然JS的优势是他的异步，那么就应该充分发挥它的这种优势。然后在实际的项目中也发现，如果调用后台服务，数据量很大的话，使用同步机制的话，会造成页面的假卡死，而如果使用异步调用的话，我们可以在接收数据期间添加一些过渡动画来进行过渡，防止假死。在正式的项目中，当然也要避免使用async:false的情况了。

然后就有了下面的Ajax写法

```
    function foo() {
    var result;
    $.ajax({
        url: '...',
        type:'GET',
        success: function(response) {
            result = response;
            
           //use result continue
           console.log(result);
           alert(result)
        }
    });
   
}
```

上面的Ajax 写法，乍一看，好像并没有什么不同。但是事实上，将Async:false去掉了，也就是使用了默认的异步方法。另外，也是最重要的，将需要使用 `result` 的流程放到了success响应函数内部，即可以等到success响应之后立刻执行。仍然是异步处理的。

# 再进一步

我们可以把success 的响应函数单独提出来，下面的代码可以在[我的codepen](https://codepen.io/zhangolve/pen/XNQGGo) 找到，并无问题(jQuery 的ajax我倒是真的能纯手写了)。

```
let test =function(response){
  console.log(response)
}
$.ajax({
  url:'https://api.github.com/users',
  type:'GET',
  datatype:'JSON',
  success:test
})
```

# 封装

后来我又遇到了另外的一个问题，由于我最近的项目中使用了node.js+React+antd+webpack ，在项目中有一些函数需要在很多组件中频繁使用，因此我想到了可以对这些函数进行封装，这样不仅能够让每个组件中的代码量少很多，而且逻辑上也更加清晰了，还方便维护，很好。最初，我考虑到的是能不能使用React的一些特性来实现可复用函数，后来发现这种思路并不正确。实际上，node已经提供了引入导出的功能，我们完全可以将我们需要复用的文件写到一个模块里，然后只需要在合适的组件中引入模块即可。关于npm 的引入导出，可以看这篇[文章](http://web.jobbole.com/87536/) 。

这个时候，就又用到了前面提到的调用github API例子中的方法了,下面以代码示例(我目前使用ES6 编写程序，示例也是ES6语法)。

```
let student=(name,age,func)=>{
let url = 'www.example.com/v1';
 $.ajax({
   type: 'POST',
   url:url,
   dataType: 'json',
   data: {
     'age':age, // 年龄
     'name': name, //姓名
   },
   async:true,
   success:func
 });
   }
export default student
```

这个时候当我们需要在我们的组件中使用上面的函数时，只需要在文件中引入student，并且传入相应的参数。

# 最后

正如我本文提到的那个示例，stackoverflow上那个关于这个这个话题的[问题](http://stackoverflow.com/questions/14220321/how-do-i-return-the-response-from-an-asynchronous-call)和相关回答给了我很大启发。有些so上面的大神也提出了使用ES6 的promise语法来实现，在这里我就不做讨论了。