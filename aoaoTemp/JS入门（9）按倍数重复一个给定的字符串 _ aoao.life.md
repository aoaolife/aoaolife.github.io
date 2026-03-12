---
title: JS入门（9）按倍数重复一个给定的字符串 | aoao.life
date: 2016-05-07 15:45:49
updated: 2026-03-01 06:20:12
---

按倍数重复一个给定的字符串

要求是一个function里面有两个参数，第一个参数str表示的是这个字符串，第二个参数num 表示的是这个字符串的重复次数。当num为负数或0的时候，则输出一个空的字符串。

分析，

```
function repeatStringNumTimes(str, num) {
  // repeat after me
  newArray=[str];   //将字符串放置到数组当中
  for(var i=1;i<num+1;i++)
    {
      str1=newArray.join(str); //这样的写法是不对的： str=str.join(); 只有arr.join()
                                //这里还要注意的是，经过join方法之后，应该是一个字符串
    }
  
}
repeatStringNumTimes("abc", 3);
```

我最初是写出了上面的程序，想要使用join()方法，但是事实上join方法的作用是将数组中的多个元素合并成一个字符串，因此并不能够满足我的要求。这时候想到了使用concat方法，它的作用是可以合并几个数组成为一个新的数组的。

```
function repeatStringNumTimes(str, num) {
  // repeat after me
  var Array=[];
  var newArray=[str];   //将字符串放置到数组当中
  for(var i=1;i<num+1;i++)
    {
      Array=Array.concat(newArray);                    
    }
   return Array.join("");
  
}

repeatStringNumTimes("abc", 3);
```

上面的程序还是用到了到了最后还是用到了join()方法，要把原来存放到数组中的元素以字符串的形式合并起来。另外要注意的是，在原题目中有要求的num不为正整数的情况，我在程序中并没有写道num不为正整数的，这是因为当num不为正整数时，由于不能够返还一个Array.join(“”)的字符串，因此自然而然地返回了一个空的字符串，完美地符合了题目中的要求。

总结，在此题中，熟练了对于array.join()方法和array.concat()方法的应用。