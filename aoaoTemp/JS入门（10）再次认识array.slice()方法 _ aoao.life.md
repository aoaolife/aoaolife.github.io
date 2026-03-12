---
title: JS入门（10）再次认识array.slice()方法 | aoao.life
date: 2016-05-07 15:47:49
updated: 2026-03-01 06:20:12
---

再次认识array.slice()方法

题目的要求是要将原来的字符串数组进行切分，给定两个参数，第一个参数为字符串数组atr，第二个参数是需要切分的长度size，要求是按照需要切分的长度切分，这样得到一个二维数组。

分析，考虑是可以先建立一个空的数组tdarr，然后通过遍历原数组str将每一个新的切好的数组放到tdarr中，这样数组里面套数组，也就是二维数组了。

在实际的应用中，使用到了array.slice() 方法，该方法以前用过，但是并不熟练，大概需要注意一下几点

- 通过应用array.slice()方法，最后得出来的还是一个数组，原数组array不发生改变。
- array.slice() 方法内部两个参数，start和end，第一个参数表示的是起始的位置，第二个参数表示的是结束的位置。我就混淆了，认为第二个参数指的是需要的元素数目。经过测试，显然是不对的了。比如如果一个数组中有4个元素，如[1,2,3,4]，那么array.slice(2,2)表示的并不是[3，4]，而是[3].
- 当array.slice()方法内部参数为负数时，表示的是逆序，不再详述。

当然，有关array.slice()方法的更多内容还是参考：[Array.prototype.concat()](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array/concat)

最后我写出的程序是这样的，这里要注意的是，在for循环中的循环条件(arr.length)/size ，这并不要求参数size和arr.length需要是正倍数的关系。例如当size=4而arr.length=6的时候，(arr.length)/size=1.5，这一点要特别注意，因为在Javascript中两个整数相除（这里指是6/4的形式写法或6.0/4.0的形式写法）是可以出现浮点数的，而不一定必须是整数，这一点和C或者Java有很大不同。

```
function chunkArrayInGroups(arr, size) {
  // Break it up.
  var tdarr=[];  //构建起一个空的二维数组
  
  for(var i=0;i<(arr.length)/size;i++)
 { 
  tdarr[i]= arr.slice(i*size,size*(i+1));  //
 }
  return tdarr;
  

}


chunkArrayInGroups(["a", "b", "c", "d"], 2);
```

参考资料：[算数操作符](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/Arithmetic_Operators)