---
title: FreeCodeCamp JS算法题部分【2】 | aoao.life
date: 2016-08-27 16:38:49
updated: 2026-03-01 06:20:12
---

第一部分见：<http://hktkdy.com/2016/08/03/201608/free-code-camp-some-test/>

# Inventory Update

## 题目要求：

对库存的管理,两个二维数组，二维数组的形式是内层数组表示的是某个商品的数量值。外层数组表示的是所有的这些商品。第一个数组表示的是当前库存，第二个数组表示的是新加入的商品。

又遇到了这种都不等于才做处理的事情。

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 ``` | ``` function updateInventory(arr1, arr2) {     // All inventory must be accounted for or you're fired!   function getAdd(arr1,arr2)   {   var finalInv=[];      for(var i=0;i<arr1.length;i++)     for(var j=0;j<arr2.length;j++)     {       if(arr1[i][1]==arr2[j][1])         {           finalInv.push([arr1[i][0]+arr2[j][0],arr1[i][1]]);         }     }     return finalInv;   }    var finalInv=getAdd(arr1,arr2);     function get(arr1,arr2)   {   var count=0;   for(var j=0;j<arr2.length;j++)     {       for(var i=0;i<arr1.length;i++)         {           if(arr2[j][1]!=arr1[i][1])             {               count++;//对于所有的都不等于才执行。             }               }       if(count==arr1.length)         {           arr1.push(arr2[j]);                   }       count=0;            }          return arr1;   }   get(finalInv,arr1);   finalInv= get(finalInv,arr2);      finalInv.sort(function (a, b) {        if (a[1] > b[1]) {            return 1;        }        if (a[1] < b[1]) {            return -1;        }        return 0;    });      return finalInv;   	}   	// Example inventory lists var curInv = [     [21, "Bowling Ball"],     [2, "Dirty Sock"],     [1, "Hair Pin"],     [5, "Microphone"] ];  var newInv = [     [2, "Hair Pin"],     [3, "Half-Eaten Apple"],     [67, "Bowling Ball"],     [7, "Toothpaste"] ];  updateInventory(curInv, newInv); ``` |

上面是我的代码，我的思路是先将能够合并的库存找出来，然后进行叠加处理。然后再把不能合并的挑选出来，推入到堆栈当中。  
下面再看一下[网友版](https://github.com/FreeCodeCamp/FreeCodeCamp/wiki/Algorithm-Inventory-Update)的：

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 ``` | ```  function updateInventory(arr1, arr2) {      // Variable for location of product     var index;      // A helper method to return the index of a specified product (undefined if not found)     var getProductIndex = function (name) {         for (var i = 0; i < this.length; i++) {             if (this[i][1] === name) {  //这里的this是什么呢?下面有注释arr1是this。                 return i;             }         }         return undefined;     }      // For each item of the new Inventory     for (var i = 0; i < arr2.length; i++) {          // Invoke our helper function using arr1 as this         index = getProductIndex.call(arr1, arr2[i][1]); //这里使用call方法无疑很巧妙了。          // If the item doesn't exist           //call中第一个参数作为this         if (index === undefined) {             // Push the entire item             arr1.push(arr2[i]);         } else {             // Add the new quantity of the current item             arr1[index][0] += arr2[i][0];         }      }      // Sort alphabetically, by the product name of each item     arr1.sort(function (a, b) {         if (a[1] > b[1]) {             return 1;         }         if (a[1] < b[1]) {             return -1;         }         return 0;     });      return arr1; }  // test here // Example inventory lists var curInv = [     [21, "Bowling Ball"],     [2, "Dirty Sock"],     [1, "Hair Pin"],     [5, "Microphone"] ];  var newInv = [     [2, "Hair Pin"],     [3, "Half-Eaten Apple"],     [67, "Bowling Ball"],     [7, "Toothpaste"] ];  updateInventory(curInv, newInv); ``` |

这个算法的思路是这样的，默认将第一个数组，也就是当前库存放入到堆栈当中，然后对第二个数组也就是添加的库存进行处理，如果发现已经有这样的产品，则进行叠加计算再推入堆栈，否则就直接把该新加入的商品推入堆栈之中。将全部处理完毕之后，再按照商品的数目进行排序。

# No repeats please

## 题目要求：

给定一个字符串，然后找到这个字符串的所有可能的排列情况。比如字符串为’aab’,那么这个时候，就会有6种排列，分别为 (aab, aab, aba, aba, baa, baa)，但是只有aba和aba这两种是没有相邻字母相同的。这个时候就返回一个2.

## 分析

排列组合的问题。  
我们知道如果忽略掉正反颠倒的情况以及忽略掉相邻字母相同排列的情况，那么这个时候就像上面所说’aab’这个字符串是有6种排列情况的，这个规律就是n的阶乘，其中n是这个字符串的长度。

```
function permAlone(str) {
  var len=str.length;
  var num=1;
  for(var i=1;i<len+1;i++)
    {
      num*=i;
    }
  return num;
}

permAlone('abcdefa');
```

上面的方法，就是用来计算这种阶乘的。  
如果有一个重复值，重复了i次，是n！-(n-1)!\*i，就是把重复值看成一个整体来考虑，更多的情况更加复杂了。

而后，我看到了[这篇文章](http://www.knanthony.com/blog/free-code-camp-no-repeats-please/) ,当然也是英文的，讲述了他的思考过程。

他最初的想法跟我一样，也是先把总的次数找出来，再把重复的次数去除掉，最后剩下的，就是最终的结果。但是当遇到了重复值不止一个，重复次数不止一次的情况时，这个方法就不好用了。

然后是Heap’s algorithm算法，根据百度百科的介绍，他的算法描述是：

> Heap’s algorithm递归的产生n个不同物品的全排列。具体来说，首先因为有n个物品，我们用1至n将这些物品编号。我们执行下列步骤：

> (1) 我们设置一个变量i，初始化i为0。

> (2) i等于n则算法产生所有全排列，退出。i不等于n，执行第(3)步。

> (3) 我们用该算法产生了前n-1个物品的全排列 (共(n-1)!个)。我们将第n个物品作为最后一个元素放入到这些排列中。这样，我们就得到了所有n个不同物品的全排列中，第n个物品在排列的最后一位的排列。接下来，如果n是奇数，则我们将排列里的第一个元素与最后一个元素互换。如果n是偶数，我们将排列的第i个元素与最后一个元素互换。

> (4) i加1。回第(2)步。

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 ``` | ``` function perms(data) { if (!(data instanceof Array)) {     throw new TypeError("input data must be an Array"); }  data = data.slice();  // make a copy var permutations = [],     stack = [];  function doPerm() {     if (data.length == 0) {         permutations.push(stack.slice());     }     for (var i = 0; i < data.length; i++) {         var x = data.splice(i, 1);         stack.push(x);         doPerm();         stack.pop();         data.splice(i, 0, x);     } }  doPerm(); return permutations; }  var input = "abcd".split('');  var result = perms(input);  for (var i = 0; i < result.length; i++) { result[i] = result[i].join(''); }  console.log(result); ``` |

# Friendly Date Ranges

## 题目要求

- 使用月份的名称而不是数字代表，日期使用缩写而不是数字
- 如果日期的范围小于一年，那么不展示结尾年份
- 如果日期范围是从当年（2016年）开始，并且在一年内（指的是365天这样的概念，而不是2016年这样的概念）结束，那么年份将不会被显示出来
- 如果日期的范围是在同年同月里（不是指在三十天内），那么将不显示结尾年份和月份。
- 还要注意的是在原来的格式中是年月日的格式，但是在转换之后，就成了月日年的格式(满足上面的条件，年甚至可以省略掉)

  比如makeFriendlyDates([“2016-07-01”, “2016-07-04”]) should return [“July 1st”,”4th”]

  在上面例子中，它满足上面提到这全部要求。

## 尝试

题目并不复杂，但是需要构造的方法较多。我在这个过程中构造了

​

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 ``` | ``` function parse(arr)   {     for(var i=0;i<arr.length;i++)       {       arr[i]=parseInt(arr[i]);       }    } ``` |

用于将原来的字符串型量转化为整型量。

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 ``` | ``` function formatDay(day)   {     switch(day)       {       case 1:day=date[0];break;       case 2:day=date[1];break;       case 3:day=date[2];break;       case 21:day=date[3];break;       case 22:day=date[4];break;       case 23:day=date[5];break;       case 31:day=date[6];break;         default:day=day+'th';       }   return day;    } ``` |

用于转化日期格式

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 ``` | ``` function formatMonth(mon)   {                     for(var i=1;i<13;i++)           {             if(mon==i)               {               mon=month[i-1];               }           }              return mon;    } ``` |

用于转化月份格式

我造了很多的轮子，最后为了实现它，写的代码超过了两百行，代码太多，就不往上贴了，放到了gists上面，感兴趣的可以戳[这里](https://gist.github.com/zhangolve/f2940e24512adff4056150442f1b2143), 就这样实际上还复用(reuse)了很多方法，但是最后看一些参考的[答案](https://github.com/Rafase282/My-FreeCodeCamp-Code/wiki/Bonfire-Friendly-Date-Ranges) , 使用了getUTCDate() 以及getUTCFullYear()这个方法，这样做就能够确保「当年」是随着时间而改变的，而不是像我程序中的，只能是2016年，过了2016年，这个「当年」就过时了。另外，还使用getMonth,getTime等方法，这也在告诉我，掌握哪些已经成熟的轮子有多么重要。

# Map the Debris

## 题目要求

轨道周期问题。

[天文学](https://zh.wikipedia.org/wiki/%E5%A4%A9%E6%96%87%E5%AD%A6)中绕中心天体在圆形或者椭圆轨道上运转的小天体轨道周期为：

其中：![](https://wikimedia.org/api/rest_v1/media/math/render/svg/f454d3ecae15ea7887c1f3f40b0b80b0d6f711af)

![](https://wikimedia.org/api/rest_v1/media/math/render/svg/183d080fad6c5e9292cd08bc28897f334189b75f)

![a](https://wikimedia.org/api/rest_v1/media/math/render/svg/ffd2487510aa438433a2579450ab2b3d557e5edc)，是轨道[半长轴](https://zh.wikipedia.org/wiki/%E5%8D%8A%E9%95%B7%E8%BB%B8)长度, ![G](https://wikimedia.org/api/rest_v1/media/math/render/svg/f5f3c8921a3b352de45446a6789b104458c9f90b)，是[引力常数](https://zh.wikipedia.org/wiki/%E5%BC%95%E5%8A%9B%E5%B8%B8%E6%95%B8), ![M](https://wikimedia.org/api/rest_v1/media/math/render/svg/f82cade9898ced02fdd08712e5f0c0151758a0dd)，是中心天体质量

*T*小时, *R*天体半径 若太阳为中心天体，我们简单的设![](https://wikimedia.org/api/rest_v1/media/math/render/svg/8073f9e9d38f6eaa5ff50e677b526ed022ce38a4)

*T*单位年, *a*表示距离[天文单位](https://zh.wikipedia.org/wiki/%E5%A4%A9%E6%96%87%E5%8D%95%E4%BD%8D)。等同于[开普勒第三定律](https://zh.wikipedia.org/wiki/%E5%BC%80%E6%99%AE%E5%8B%92%E8%A1%8C%E6%98%9F%E8%BF%90%E5%8A%A8%E5%AE%9A%E5%BE%8B)

其实就是要实现上面的轨道周期公式。

## 过程

在使用中，用到了js 中的一些math方法，比如Math.pow(),另外由于公式中有圆周率常数pi，因此还用到了Math.PI。

由于有：

> The values should be rounded to the nearest whole number. The body being orbited is Earth.

要求是取得最接近的整数，则应该是四舍五入的。

则应当使用Math.round() 方法。最后写出了下面的程序：

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 ``` | ```  function orbitalPeriod(arr) {   var GM = 398600.4418;   var earthRadius = 6367.4447;   var orPstack=[];   var result=[];   function orP(avg)   {   var a3=Math.pow(avg+earthRadius,3);   //return a3;   return Math.round(2*Math.PI*Math.pow(a3/GM,0.5));   }   for(var i=0;i<arr.length;i++)     {       orPstack.push(orP(arr[i].avgAlt));     }      for(var j=0;j<arr.length;j++)     {    result.push({name:arr[j].name,orbitalPeriod:orPstack[j]});     }   return result; }  orbitalPeriod([{name : "sputnik", avgAlt : 35873.5553}]); ``` |

最后想说一句，学个编程还不能够把高中物理给忘记啊。

总结下来，这个题目还是考察的是对象和基本的JS数学操作方法。

# Pairwise

## 题目要求：

给定一个数组，找出这个数组中的元素对，它们的和与第二个参数arg相等，这个时候返回这个元素对的地址和（indices）

如果有多个元素对的可能，这个时候返回地址和加起来最小的元素对的地址和，另外需要注意的一点是每一个元素一旦被使用了也就不能够被再次使用了。

举例来说

> `pairwise([7, 9, 11, 13, 15], 20)` returns `6`. The pairs that sum to 20 are `[7, 13]` and `[9, 11]`

## 过程

题目本身并不复杂，我写下了下面的程序用于测试。

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 ``` | ```  function pairwise(arr, arg) {   var middle=0;   var stack=[];   for(var i=0;i<arr.length;i++)     {              for(var j=i+1;j<arr.length;j++)         {           if(arr[i]+arr[j]==arg)             {               stack.push(i,j);               arr.splice(j,1);               break;             }         }          }   return stack;    }  pairwise([0,0,0,0,1,1], 1); ``` |

这个时候出现了问题，这时候得到的结果是：

`[0,4,1,4]`

很显然，由于我在程序中使用了arr.splice(j,1)，导致在数组arr中，原来本来应该位于index=5的最后一个1现在却处在了index=4的位置。

这个时候我只把arr.splice(j,1)改成了arr[j]=’a’，事实上arr[j]可以是任意的非数字类型量，我的目的就是让这个arr[j]不再被使用。

有了上面的判断之后，我就写出了下面的程序：

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 ``` | ```  function pairwise(arr, arg) {   var middle=0;   var stack=[];   for(var i=0;i<arr.length;i++)     {              for(var j=i+1;j<arr.length;j++)         {           if(arr[i]+arr[j]==arg)             {               stack.push(i,j);               arr[j]='a';               break;             }         }          }      if(stack.length===0)     { return 0;     }   else{   var sum=stack.reduce(function(a,b)               {     return a+b;   });   return sum;   } }  pairwise([], 100); ``` |