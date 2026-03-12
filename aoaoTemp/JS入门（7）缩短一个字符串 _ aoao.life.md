---
title: JS入门（7）缩短一个字符串 | aoao.life
date: 2016-05-07 15:42:49
updated: 2026-03-01 06:20:12
---

题目要求：缩短一个字符串

给定一个字符串str和一个数字num，num表示需要的字符串数目，如果str的长度大于num的话，并且num是大于3的，这个时候就将从指定的位置进行截断 ，并且在截断的位置后面加上…（三个英文半角句号，也就是省略号Ellipsis） 如果num是不大于3的话，那么

我们先从最简单的情况考虑，如果num是不大于3的情况，那么我们可以写出下面的程序：

```
function truncateString(str, num) {
  if(num<=3)
    {
     str2 =str.slice(0,num) ;  //这个时候的str2为全局变量，如果使用var str为局部变量不符合要求
    }
  return str2;
}

truncateString("A-tisket a-tasket A green and yellow basket", 2);
```

我开始的思路是将截取之后的第二部分用英文省略号来替换，也就是使用string.replace()这个方法，后来发现这样的替换并不简单，反倒是可以直接在生成的第一个字符串后面加上省略号，其实实现起来会更加简单。

```
function truncateString(str, num) {
  if(num<=3)
    {
     str2 =str.slice(0,num) ;  //这个时候的str2为全局变量，如果使用var str为局部变量不符合要求
       str2=str2.concat('...'); 
}
  else{
    str2=str.slice(0,num-3);
    str2=str2.concat('...');
    
  }
  return str2;
}

truncateString("A-tisket a-tasket A green and yellow basket",11);
```

上面的程序已经能够实现了当str>num的情况下的应用了。接下来我们看一下str<=num时的情况。当str小于等于num时，这个时候超出了要截取的范围了，因此应当是输出原str字符串。所以就应该有下面的程序。

```
function truncateString(str, num) {
  if(str.length>num)
    {
  if(num<=3)
    {
     str2 =str.slice(0,num) ;//这个时候的str2为全局变量，如果使用var str为局部变量不符合要求
     str2=str2.concat("...");
    }
  else{
    str2=str.slice(0,num-3);
    str2=str2.concat('...');
    
  }
  return str2;
    }
  
  else{
    return str;
  }
}

truncateString("A-tisket a-tasket A green and yellow basket",11);
```