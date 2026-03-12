---
title: JS入门（11）判断一个数组中，第二个元素中的所有字母是否全部在第一个元素之中。 | aoao.life
date: 2016-05-18 12:33:49
updated: 2026-03-01 06:20:12
---

判断一个数组中，第二个元素中的所有字母是否全部在第一个元素之中。如果成立的话，则返会true，反之，如果错误的话，则返回false。  
这里的要求是对字母的大小写不作区分，也不区分字母的顺序。

比如一个数组是[“hello”, “Hello”]，那么将应该返回一个true。而如果数组是 [“hello”, “hey”] ，那么就需要返回一个false了。

对于这样的问题，首先是要将大小写统一掉，在这里我将数组中两个元素（也就是两个字符串）全部统一成小写。

接下来，仍然是使用for循环进行遍历了。但是这里有一个关键的点是，如何通过遍历来得到true或者false的结果呢？

这里我采用了给定一个初始值num=0，我们是要用数组中第二个元素中的字母与第一个元素中的元素进行匹配，因此可以有下面的逻辑：

> 有一个字母匹配成功一次，我就使num+1，这样只有判断num是否与数组中第二个元素的长度相等就可以判断是否已经全部匹配了

基于上面的分析，就有了下面的程序：

```
function mutation(arr) {
  
   arr[0]=arr[0].toLowerCase();
   arr[1]=arr[1].toLowerCase();
   var num=0;
   for(var i=0;i<arr[1].length;i++)
     {
       for(var j=0;j<arr[0].length;j++)
         {
           if(arr[1][i]==arr[0][j])    
             {
             num+=1;
               break; //这个break语句必不可少，如果没有这一句，就容易

				 //出现num计数增多的情况，是因为没有立即跳出
		}
         }
       
     }
  //return num;  这一句最初是在为调试程序加上的，因为最初没有加上前面的break语句，导致num偏大。
 
    if(num==arr[1].length)
      {
        return true;
      }
  else{
    return false;
  }
 
}	
mutation(["hello", "hello"]);
```