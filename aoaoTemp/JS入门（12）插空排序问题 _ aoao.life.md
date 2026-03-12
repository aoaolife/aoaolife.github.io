---
title: JS入门（12）插空排序问题 | aoao.life
date: 2016-05-18 12:35:49
updated: 2026-03-01 06:20:12
---

要求是给定一个顺序不规则的数组和一个数字，设计一套算法来确定当这个数字添加到这个数组之中后，这个数字在数组中的位置。

这里的排序算法显然是不对的了。只能够排相邻的两个数的大小。

```
function getIndexToIns(arr, num) {
  // Find my place in this sorted array.
  var max=0;
  for(var i=0;i<arr.length;i++)
    {
      if(arr[i]>max)
        {
          max=arr[i];
        }
      else{
        arr[i-1]=arr[i];
        arr[i]= max;
        
      }
    }
  return arr;
 /*
  for(var j=0;j<arr.length;j++)
    {
      if(num<=arr[j])
        {
         return j;
        }
      
        
    }
    */
}

getIndexToIns([5, 3, 20, 3], 5);
```

后来我的程序是下面这样的，没有自己造轮子，而是使用了现成的array.sort()方法来进行排序。

```
function getIndexToIns(arr, num) {
  // Find my place in this sorted array.
  
  arr.sort(function(a,b){
    return a-b;
  }
  );
 
  for(var j=0;j<arr.length;j++)
    {
      if(num<=arr[j])
        {
         return j;
        }
     
            
        
    }
    return j;
   
}

getIndexToIns([2, 5, 10], 15);
```