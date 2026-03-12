---
title: JS入门（6）判断是否一个字符串target是另外一个字符串str的结尾 | aoao.life
date: 2016-05-07 15:41:49
updated: 2026-03-01 06:20:12
---

判断是否一个字符串target是另外一个字符串str的结尾

其实还是要用到遍历，我最初的考虑是在str里找出所有可能的字符串情况出来，题目中提示了可以使用substr()方法来实习，我之前并没有用过substr()方法，后来明白了它的使用方法。substr()方法就是用来找子字符串的方法，它有两个参数，第一个参数规定字符串的起始位置，正数代表的是从0开始数的正序，负数代表的是逆序。

于是写下了下面这样的程序。

```
function confirmEnding(str, target) {
  // "Never give up and good luck will find you."
  // -- Falcor
  for(var i=0;i<str.length;i++)
    {
      for(var j=1;j<str.length+2-i;j++)    //经过计算得出的公式
      { var substr=str.substr(i,j);            
      if (substr==target)
        {
          return true;     //只要有一个是匹配的，就立即返回true这个布尔量，程序不再执行
        }
      
      }
      
    }
    return false;     //当for循环全部执行结束，仍然找不到匹配时，返回false
}

confirmEnding("Connor", "n");
```

但是这样的程序只能够做到判断这样target是否在字符串str中，并不能够判断target是否是str字符串的结尾，还好，已经离目标很近了。

这个时候当然是用倒序来检查序列应该是更加合适一点了。

后来我写出了下面的程序，事实上，它比上面的程序要简单得多，因为只用到了一个for循环。但是这个时候还是有问题，~~当str只是一个单词的时候，没有问题，一旦它是一个句子，也就是单词与单词之间出现空格的时候，就会出现错误。~~

```
function confirmEnding(str, target) {
  // "Never give up and good luck will find you."
  // -- Falcor
for(var i=1;i<str.length+1;i++)
     {
var substr=str.substr(-1,i);      
   if(target==substr){
     return true;
   }   
     }
      
    
  return false;
}

confirmEnding("He has to give me a new name", "name");
```

上面的程序之所以有错误，是因为还是没有理解substr方法，当substr方法中第一个参数是负数的时候，例如上面程序中的-1，指的是从倒序最后一个数开始正序来数，我上面的程序是认为可以逆序来数的，所以自然是错误的。

所以，还是我自己把问题想复杂了。只需要确保无论从哪一个数字开始数，都能够到str字符串的最后一个字符结尾就OK了。因此可以通过计算字符串的长度和找到字符串最后一位与字符串长度之间的关系来确定。

```
function confirmEnding(str, target) {
  // "Never give up and good luck will find you."
  // -- Falcor
for(i=0;i<str.length+1;i++)
  {
    var substr=str.substr(i,(str.length+1-i));   //这一条语句很关键了，实际上大概就是初中数学的知识了。
    if(target==substr)
      {
        return true;
      }
  }
    
  return false;
}

confirmEnding("name", "ame");
```