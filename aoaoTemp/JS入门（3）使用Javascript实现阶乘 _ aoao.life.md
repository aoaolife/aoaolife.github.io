---
title: JS入门（3）使用Javascript实现阶乘 | aoao.life
date: 2016-05-03 19:13:49
updated: 2026-03-01 06:20:12
---

使用Javascript实现阶乘

思路是，由于阶乘的定义就是

N!=N×(N-1)×（N-2）—–2×1

因此将原来给定的数字N按照定义组成一个数组，也就是将从1开始，这个时候使用一个for循环配合array.push() 方法就可以达到上面所要的目的。

我最初为了测试是这样写的：  
   
 function factorialize(num) {  
   
 Factorials= 1;  
 var arr=[];  
 for(var i=1;i<(num+1);i++)  
 {  
 total=arr.push(i);  
 }  
   
 return total  
 }  
 factorialize(5);

结果是输出了一个数字 5.

事实是我的返回值是 total ，而total 在这里表示的就是数组中元素的个数。如果查看array.push()的使用方法就会发现，array.push之后，array也相应的发生了改变，因此在这里返回arr就可以了。

因此，改变之后，再将数组中的元素进行一次遍历，进行累乘。

```
function factorialize(num) {
  
  Factorials= 1;
  var arr=[];
  for(var i=1;i<(num+1);i++)
    {
      arr.push(i);
    }
  for(var j=0;j<arr.length;j++)
    {
      Factorials*=arr[j];
      
    }
  return Factorials;
}


factorialize(5);
```