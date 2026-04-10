---
title: FreeCodeCamp JS算法题部分【1】 | aoao.life
date: 2016-08-03 13:42:49
updated: 2026-03-01 06:20:12
---

这是我自己在 Freecode.camp 上做的几道算法题目，基本上是边做边写，写的过程是为了厘清楚解题的思路，加深对原有题目的印象，后来就想着干脆发到博客上。但因为是边做边写的，有些时候思路清晰的，往往就一笔带过了，而没有思路的，却着了很多的笔墨。另外，也由于是边做边写，原文的排版并不是非常友好，此稿也是我经过了很多改正之后的结果，想着这也就是作为自己的笔记日后来看，若是能够帮上其他朋友，也是非常高兴的。

~~全文共记述了15道算法题的答案，大多有解题的思路和过程，全文较长，然而此文中痛点在于没有目录，皆因我是用的Markdown编辑，这也是Markdown的一大短板，在本地的Typora是能够看到目录的(只需要添加一条[TOC])，但这个hexo 主题并不具有此功能，以后有时间，再做更改。（说以后有时间，估计就没有以后了。笑cry）~~

然而，刚刚写完上面的那段话，立刻就反应过来：可不就是主题的问题。于是搜索了一番，果然是有针对yilia主题添加目录的配置和方法：<https://github.com/iblogc/hexo-theme-yilia/tree/add-toc>

# Sorted Union

来自：<https://www.freecodecamp.com/challenges/sorted-union>

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 ``` | ``` function uniteUnique(arr) {   return arr; }  uniteUnique([1, 3, 2], [5, 2, 1, 4], [2, 1]); ``` |

最初的代码是这样的，那么现在所要解决的第一个问题是，明明在uniteUnique 这个function中有三个参数array的，但是在这里只能够调用一个。

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 ``` | ``` function uniteUnique(arr,arr2,arr3) {   return arr.concat(arr2); }  uniteUnique([1, 3, 2], [5, 2, 1, 4], [2, 1]); ``` |

这就解决了第一个问题，就是参数。但是事实上，我们并不知道究竟有几个参数，比如给定的还可以是类似于[1, 2, 3], [5, 2, 1, 4], [2, 1], [6, 7, 8]，这时候就是有4个参数了，所以说，这个问题，还是没有根本解决，但是在这里打算先实现[1, 3, 2], [5, 2, 1, 4], [2, 1]这个的特例。

这里的思路是遍历，将重复的元素去除掉，将新的数组与原数组结合。

这里首先牵扯到一个问题：[如何判断一个值不等于另外一个数组中的任何一个值](http://stackoverflow.com/questions/12116326/javascript-simple-way-to-check-if-variable-is-equal-to-two-or-more-values)。

可以用类似如下代码实现：

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 ``` | ``` if ([5,6,7,8].indexOf(x) > -1)   	{  	} ``` |

如果x在[5,6,7,8]这个数组之中，则符合要求。这是判断一个值等于另外一个数组中的某一个值。

后来觉得还是直接使用splice()方法将重复的元素删除掉比较好一些。

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 ``` | ``` function uniteUnique(arr,arr2,arr3) {   for(var i=0;i<arr2.length;i++)     {       for(var j=0;j<arr.length;j++){         if(arr2[i]==arr[j]){   //要求是对于所有的都不等于          var removed =arr2.splice(i,1);           return removed;                   }          }      // return arr.concat(arr2)       }}     uniteUnique([1, 3, 2], [5, 2, 1, 4], [2, 1]); ``` |

仍然是个失败的尝试。这个返回的是2.这说明能找出来重复值了。

这里要注意，没有arr[-1]这样的用法。

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 ``` | ``` function uniteUnique(arr,arr2,arr3) {  return arr[-1];    }  uniteUnique([1, 3, 2], [5, 2, 1, 4], [2, 1]); ``` |

没有返回值。

> 网络上的解法：  
> Problem Explanation:
>
> The program has to return a new array of unique values from two original arrays in the order they show up. So there is not sorting required, and no duplicates.  
> 没有排序要求
>
> Hint: 1
>
> Since you have no idea how many parameters were passed, it would be best to loop through the arguments before looping through the arrays.  
> 由于不知道有多少个参数，所以可以在遍历数组之前遍历所有的参数  
> Hint: 2
>
> I used loops, you can use something else like map, reduce or others if you want.  
> 使用循环遍历  
> Hint: 3
>
> You will have to check if the current value is already on the array to be returned for every value.  
> 检查

代码：

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 ``` | ``` function unite(arr1, arr2, arr3) {   // Creates an empty array to store our final result.   var finalArray = [];    // Loop through the arguments object to truly made the program work with two or more arrays   // instead of 3.   for (var i = 0; i < arguments.length; i++) {     var arrayArguments = arguments[i];      // Loops through the array at hand     for (var j = 0; j < arrayArguments.length; j++) {       var indexValue = arrayArguments[j];        // Checks if the value is already on the final array.       if (finalArray.indexOf(indexValue) < 0) {         finalArray.push(indexValue);       }     }   }    return finalArray; } ``` |

这个解决方案的思路是先将所有参数找出来，所有的参数就是所有的数组，我们不管究竟哪一个元素是哪一个数组里的，只判断这个元素是否在新的数组之中，如果不在的话，就push到数组里。

|  |  |
| --- | --- |
| ``` 1 ``` | ``` finalArray.indexOf(indexValue) < 0 ``` |

当然是很巧妙的啊。

我自己的解法是这样的：

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 ``` | ``` function uniteUnique(arr,arr2,arr3) { var finalArr=[];   for(var i=0;i<arguments.length;i++)     {       for(var j=0;j<arguments[i].length;j++)         {       if(finalArr.indexOf(arguments[i][j])<0)         {           finalArr.push(arguments[i][j]);                    }                  }            }       return finalArr;  } uniteUnique([1, 3, 2], [5, 2, 1, 4], [2, 1]); ``` |

# Convert HTML Entities

很显然又用的了正则表达式。

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 ``` | ``` &：&amp; '：&apos; <:&lt;  >:&gt; >":&quot;. 空格:&nbsp; ``` |

首先搞清楚什么是HTML实体

我们可以看出来，在HTML中<>是标记符，让他们显示他们原本的意思，因此就有了html实体。

```
<p>
2&lt;4&#60;6
</p>
```

他就相当于是

2<4<6

使用这种entities的好处就是方便记忆，方便检查。比较完整的[charref](https://dev.w3.org/html5/html-author/charref)

# [Spinal Tap Case](https://www.freecodecamp.com/challenges/spinal-tap-case#)

这个题目提示可以使用正则表达式，但是我还是没有用。题目的要求就是将原来无论怎样格式的句子改写成中间用-连接。

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 ``` | ``` function spinalCase(str) {   var newArr=str.split('');   for(var i=0;i<newArr.length;i++)     {       if(newArr[i]===' '||newArr[i]==='_'){         newArr[i]='-';         //将空格和下划线替换成减号。                  }              if(newArr[i].charCodeAt(0)>64&&newArr[i].charCodeAt(0)<91&&i!==0)       {              newArr[i]='-'+newArr[i];       }             newArr[i]=newArr[i].toLowerCase();            }      str=newArr.join('');   var finalArr=str.split('');     for(var j=0;j<finalArr.length;j++)     {       if(finalArr[j]==='-'&&finalArr[j+1]==='-')         {           finalArr[j+1]='';                    }  }          var newstr=finalArr.join('');   return newstr;    }  spinalCase('This Is Spinal Tap'); ``` |

# [Sum All Odd Fibonacci Numbers](https://www.freecodecamp.com/challenges/sum-all-odd-fibonacci-numbers)

这个题目的要求是找出所有奇数的费内巴切数的和。

思路是首先要找到费内巴切数列，这就是一个很简单的一个问题了。

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 ``` | ``` function sumFibs(num) {   var Fib=[1,1];   var sum=0;   for(var i=0;i<100;i++)     {   Fib[i+2]=Fib[i]+Fib[i+1];     } //找出一个费内巴切数列，实际上这已经是一个很大的数列了。   var end=0; //将截至的数字定为end   for(var j=0;j<100;j++)     {       if(Fib[j+1]>num)       {          end=j;         break;       }     } //找到截至的那个数字   for(var k=0;k<end+1;k++)     {       if(Fib[k]%2==1)         {           sum+=Fib[k];         }            } //通过取余的操作来判断出奇数   return sum; }  sumFibs(4); ``` |

# [Sum All Primes](https://www.freecodecamp.com/challenges/sum-all-primes)

题目要求：所有质数相加

我们先来看一个程序，[找出来一个数是否为质数](http://stackoverflow.com/questions/11966520/how-to-find-prime-numbers-between-0-100)

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 ``` | ``` function isPrime(num) { if(num < 2) return false; for (var i = 2; i < num; i++) {     if(num%i==0)         return false; } return true; } ``` |

这是一个可以用来判断是否为质数的方法，我们可以利用它。

​

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 ``` | ``` function sumPrimes(num) { var sum=0; var array=[]; var end; function isprime(addNum){ for(var i=2;i<addNum;i++)  {  if(addNum%i===0){ return false;  }          }     return true;   }      for(var j=2;j<1000;j++)     {       if(isprime(j))         {           array.push(j);         }             }              for(var k=0;k<array.length;k++)     {       if(array[k]>num)       {         end=k-1;         break;       }     }      for(var h=0;h<end+1;h++)     {       sum+=array[h];       	    }       	    	  return sum; }  sumPrimes(10);	 ``` |

​

# [Smallest Common Multiple](https://www.freecodecamp.com/challenges/smallest-common-multiple)

题目要求：最小公倍数问题，要求是甚至这个最小公倍数能够被这个范围内的数字整除。也就是说，同时也是这个范围内数字的公倍数。

​

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 ``` | ```    function smallestCommons(arr) {    var newArr=[];     var sum=1;      // it is a prime num?    function isprime(addNum){ 	  for(var i=2;i<addNum;i++) 	    { 	      if(addNum%i===0){ 	        return false; 	         	      } 	     	    } 	    return true; 	  }      //have common div      function havecom(first,second)   {         var common=1;     for(var i=2;i<second;i++)       {         if(isprime(i))           {         if(first%i===0&&second%i===0)           {             common*=i;             }           }        }     return common;       }      function sort(a,b)   {     var mid;   if (a>b)     {        newArr[0]=b;        newArr[1]=a;            }     else{       newArr[0]=a;       newArr[1]=b;     }       }        sort(arr[0],arr[1]);   var min=newArr[0];   var max=newArr[1];      for(var j=min;j<max+1;j++)     {       if(havecom(sum,j)==1)         {           sum=sum*j;                    }       else{         sum=sum*j/havecom(sum,j);                }          }      /*   for(var j=min;j<max;j++)     for(var k=j+1;k<max;k++)       {         if(havecom(j,k)!==1)           {             sum=sum/havecom(j,k);                        }                }       */   return sum;    } smallestCommons([1,8]); ``` |

​

我最初的程序是这样的，它的主要问题是计算两个数的最大公约数的方法havecom() 其实是错误的。

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 ``` | ```   function smallestCommons(arr) {   var newArr=[];   var sum=1;  // it is a prime num? //   function isprime(addNum){  for(var i=2;i<addNum;i++)    {      if(addNum%i===0){        return false;              }        }    return true;  }  //have common div  function havecom(first,second) {       for(var i=second;i<8000000;i++)     {     if(i%first===0&&i%second===0)         {           return i;             }     }   }  function sort(a,b) {   var mid; if (a>b)   {      newArr[0]=b;      newArr[1]=a;        }   else{     newArr[0]=a;     newArr[1]=b;   }     }      sort(arr[0],arr[1]); var min=newArr[0]; var max=newArr[1];  for(var j=min;j<max+1;j++)   {     sum=havecom(j,sum);        }           return sum;    }   }   smallestCommons([18,22]); ``` |

这个求两个数的最小公倍数的方法，实际上要求的时间很大，因为在

|  |  |
| --- | --- |
| ``` 1 ``` | ``` for(var i=second;i<8000000;i++) ``` |

这一步之中，使用到的并不是一个特别好的方法.i每增加1，相应的计算机就执行一次运算。也正因此，计算机运算很大，添加了//noprotect 这个loop保护解除。

# [Finders Keepers](https://www.freecodecamp.com/challenges/finders-keepers)

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 ``` | ``` function findElement(arr, func) {   for(var i=0;i<arr.length;i++)     {       if(func(arr[i]))         {           return arr[i];           }            } }  findElement([1, 2, 3, 4], function(num){ return num % 2 === 0; }); ``` |

# [Drop it](https://www.freecodecamp.com/challenges/drop-it#)

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 ``` | ``` function dropElements(arr, func) {   // Drop them elements.   var end;   for(var i=0;i<arr.length;i++)     {       if(func(arr[i])){         end=i;         break;       }            }   if(typeof end==='number')     {   return arr.slice(end);     }   else{     return [];        } }  dropElements([1, 2, 3, 4], function(n) {return n > 5;}); ``` |

仍然比较简单，只需要记住

|  |  |
| --- | --- |
| ``` 1 ``` | ``` if(typeof end==='number') ``` |

其中需要将number用引号引起来，并且要求是小写而不是Number这样的首字母大写。

# [Steamroller](https://www.freecodecamp.com/challenges/steamroller#)

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 ``` | ``` function steamrollArray(arr) {   var newArr=[];   // I'm a steamroller, baby   var digout=function dig(a)   {     if(!Array.isArray(a))       {         newArr.push(a);       }     else {       for(var b in a)         {           digout(a[b]);         }          }       };         for(var i in arr)     {       digout(arr[i]);          }   return newArr; }  steamrollArray([1, [2], [3, [[4]]]]); ``` |

这里面用到了递归，只要找到的是数组类型的值，就继续往里挖，直到找到所有的非数组类型的值。

# [Binary Agents](https://www.freecodecamp.com/challenges/binary-agents)

关于[二进制到十进制的转换](http://stackoverflow.com/questions/10258828/how-to-convert-binary-string-to-decimal)

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 ``` | ``` function binaryAgent(str) {   var arr=str.split(' ');   var newArr=[];   var secArr=[];   for(var i in arr)     {   newArr.push(parseInt(arr[i], 2));     }      //return String.fromCharCode(newArr[0]);   for(var j in newArr)     {      secArr.push(String.fromCharCode(newArr[j]));     }   return secArr.join(''); }  binaryAgent("01000001 01110010 01100101 01101110 00100111 01110100 00100000 01100010 01101111 01101110 01100110 01101001 01110010 01100101 01110011 00100000 01100110 01110101 01101110 00100001 00111111"); ``` |

针对这个测试的结果是：Aren’t bonfires fun!?

熟练地使用join()方法和push()方法等。  
熟练地使用for in这样的表达，而不再使用

|  |  |
| --- | --- |
| ``` 1 ``` | ``` for(var i=0 ;i<arr.length;i++） ``` |

# [Everything Be True](https://www.freecodecamp.com/challenges/everything-be-true)

题目要求：第二个参数作为属性，判断这个属性是否对于collection中每一个对象都存在，如果都存在，则返回true，否则是返回false。在实际写代码的过程中，发现判断false相对来说更加简单。

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 ``` | ``` function truthCheck(collection, pre) {   // Is everyone being true?   for(var i in collection)     {        if(!collection[i][pre])          {            return false;                      }            return true;    }  truthCheck([{"user": "Tinky-Winky", "sex": "male"}, {"user": "Dipsy", "sex": "male"}, {"user": "Laa-Laa", "sex": "female"}, {"user": "Po", "sex": "female"}], "sex"); ``` |

也是个比较简单的问题了。还是对JSON的复习。

# [Arguments Optional](https://www.freecodecamp.com/challenges/arguments-optional)

​

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 ``` | ``` function addTogether() {   var sum=0;      if(arguments.length==2&&typeof arguments[0]=='number'&&typeof arguments[1]=='number')     {            sum=arguments[0]+arguments[1];       return sum;     }      else if(arguments.length==1&&typeof arguments=='number')     {              var c=arguments;       return function(arg2)       {       if(args!=='')         {           sum=c+arg2;           return sum;         }       };     }      else{     return undefined;        } ``` |



|  |  |
| --- | --- |
| ``` 1 2 ``` | ``` } addTogether(2)(3); ``` |

没有解决，网络上的解法：

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 ``` | ``` function add() {   // Function to check if a number is actually a number   // and return undefined otherwise.   var checkNum = function(num) {     if (typeof num !== 'number') {       return undefined;     } else       return num;   };    // Check if we have two parameters, check if they are numbers   // handle the case where one is not   // returns the addition.   if (arguments.length > 1) {     var a = checkNum(arguments[0]);     var b = checkNum(arguments[1]);     if (a === undefined || b === undefined) {       return undefined;     } else {       return a + b;     }   } else {     // If only one parameter was found, returns a new function that expects two     // Store first argument before entering the new function scope     var c = arguments[0];      // Check the number again, must be outside the function to about returning an object     // instead of undefined.     if (checkNum(c)) {       // Return function that expect a second argument.       return function(arg2) {         // Check for non-numbers         if (c === undefined || checkNum(arg2) === undefined) {           return undefined;         } else {           // if numbers then add them.           return c + arg2;         }       };     }   } } ``` |

多少还是有些不能理解的地方，等以后再看吧。

# 正则表达式

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 ``` | ``` function telephoneCheck(str) {   // Good luck!   var re= /5/g;   //var re = /apples/gi;  newStr= str.replace(re,'6');   return newStr;    } telephoneCheck("555-555-5555"); ``` |

这里要注意使用replace()方法的时候，要注意的是要replace()方法不改变原字符串，需要新建一个新的字符串，在这里是字符串newStr

如果一个字符串str=[22448848]，针对typeof str[0]，我想当然地以为是number类型，但其实是string。

# [Validate US Telephone Numbers](https://www.freecodecamp.com/challenges/validate-us-telephone-numbers)

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 ``` | ``` function telephoneCheck(str) {   // Good luck!   var re= /-|\s|\(|\)/g;   var kuohao=/\(|\)/g;      var left,right;   var newStr;   //var re = /apples/gi; //var  newStr= str.replace(re,'');  // return newStr;   for(var i=0;i<str.length;i++)     {      if(str[i]=='(')        {         left=i;        }          }   for(var j=0;j<str.length;j++)     {      if(str[j]==')')        {         right=j;        }          }      if(typeof left!=='number'&&typeof right!=='number'||left<right)     {        newStr=str.replace(re,'');         if(typeof parseInt(newStr)!=='number')           {             return false;             }              if(newStr[0]==1)         {           if(newStr.length==11)             {               return true;             }           else{             return false;           }                    }       else{            if(newStr.length==10)              {                return true;              }         else{           return false;         }             }                }                else{     return false;        }   }   telephoneCheck("(6505552368)"); ``` |

知识点parseInt()方法，正则表达式等。

这里要注意的是：parseInt(“40 years”) 的结果是40。只要有数字，就能够解析。

还有一点需要注意的是：  
typeof parseInt(hello) 就是number类型的。parseInt(hello) 的结果是null。  
判断一个字符串是否全部为数字

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 ``` | ``` for(var i=0;i<str.length;i++) {  if( !parseInt(str[i])) {  return false; } } return true; ``` |

最后写出了下面的程序：  
​   
​

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 ``` | ``` function telephoneCheck(str) {   // Good luck!   var re= /-|\s|\(|\)/g;   var place=/\s|-/g;   //如果字符串中第一位是-则直接返回false   if(str[0]=='-')     {       return false;     }       str=str.replace(place,'');       //首字母是否为1   //首字母为1       if(str[0]=='1')      {        //出现一对括号的情况        if(str[1]=='('&&str[5]==')')          {                        str=str.replace(re,'');                        if(str.length==11)              {                return true;                              }            else{              return false;                          }             }        //没有括号的情况        else {          for(var i=0;i<str.length;i++)          {            if( !parseInt(str[i]))              return false;                      }                  }                        str=str.replace(re,'');                   if(str.length==11)           {             return true;           }        else{          return false;        }        //没有括号情况结束      }      //首字母不为0      else{     //有一对括号的情况      if(str[0]=='('&&str[4]==')')        {                     str=str.replace(re,'');                     if(str.length==10)           {             return true;           }          else{            return false;          }                     }    //没有一对括号的情况     else{        for(var j=0;j<str.length;j++)          {            if( !parseInt(str[j]))              return false;                      }       str=str.replace(re,'');       if(str.length==10)         {           return true;         }         else{           return false;         }     }       }         }         telephoneCheck("(555)555-5555"); ``` |

缺点是使用了大量的if else，十分不便于阅读。应该是可以进行简化的。

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 ``` | ``` function telephoneCheck(str) {   // Good luck!   var re= /-|\s|\(|\)/g;   var place=/\s|-/g;   //如果字符串中第一位是-则直接返回false      //构建一个比较的方法    function compare(a,b)   {   if(a==b)     {      return true;                      }    else{    return false;       }       }       if(str[0]=='-')     {       return false;     }       str=str.replace(place,'');        }        //没有括号的情况        else {          for(var i=0;i<str.length;i++)          {            if( !parseInt(str[i]))              return false;                      }                  }                        str=str.replace(re,'');                   return compare(str.length,11);        //没有括号情况结束      }      //首字母不为0      else{     //有一对括号的情况      if(str[0]=='('&&str[4]==')')        {                     str=str.replace(re,'');                    return compare(str.length,10);                     }    //没有一对括号的情况     else{        for(var j=0;j<str.length;j++)          {            if( !parseInt(str[j]))              return false;                      }       str=str.replace(re,'');       return compare(str.length,10);     }     }    } telephoneCheck("(555)555-5555"); ``` |

将比较是否相等的功能提出来做一个方法，这样就让代码相对之前更加简洁了。

层次优先级是首先判断首字母，其次判断是否有一对括号放在合适的位置，最后是判断经过筛选之后的字符串的长度。

美国的电话号码，国码为1，三位的区码，以及7位的普通码，其中，国码可以省略掉。

# [Symmetric Difference](https://www.freecodecamp.com/challenges/symmetric-difference)

创建一个方法，它有两个及以上的数组作为参数，返回一个数组，这个数组中有非公有的元素。

比如A = {1, 2, 3}，B = {2, 3, 4}，这个时候组成的C就是{1,2,3,4},以此类推，可以有多个参数。

移除一个数组中的重复元素

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 ``` | ``` var names = ["Alex","Tony","James","Suzane", "Marie", "Laurence", "Alex", "Suzane", "Marie", "Marie", "James", "Tony", "Alex"]; var uniqueNames = [];      for(var i in names){         if(uniqueNames.indexOf(names[i]) === -1){             uniqueNames.push(names[i]);         }     } ``` |

仿照着上面的程序，就可以构造一个二维数组，将原来每个数组中的重复元素去除掉

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 ``` | ``` var newArr=[];//define a new array    //find out the length of arguments    for(var i=0;i<arguments.length;i++)   {     newArr[i]=[];//this is important ,you must make the newArr[i]==empty firstly,or there would be console newArr[i] is undefined.   //delete the duplicate elements   for(var j=0;j<arguments[i].length;j++)     {       // delete and push to a new array  if(newArr[i].indexOf(arguments[i][j])===-1)    {      newArr[i].push(arguments[i][j]);         }          } //delete end } ``` |

然后是构造了这样的这样的一个方法，来得到两个数组中的非同项：

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 ``` | ```  function twoArg(arr1,arr2) { var finalArr=[];//the final array var middle=[];//the middle array var dub=[];//the dub array finalArr=arr1.concat(arr2); for(var k=0;k<finalArr.length;k++)  {  if(middle.indexOf(finalArr[k])===-1)   middle.push(finalArr[k]);   else{   dub.push(finalArr[k]);      }       }    for(var m=0;m<dub.length;m++)      {     for(var n=0;n<middle.length;n++) {  if(middle[n]==dub[m])          {            middle.splice(n,1);          } } } return middle; } ``` |

变量名命名不是太好。

然后定义一个全局的变量，final。这样就可以写：

|  |  |
| --- | --- |
| ``` 1 ``` | ``` final=twoArg(newArr[0],newArr[1]); ``` |



|  |  |
| --- | --- |
| ``` 1 ``` | ``` for(var m=2;m<newArr.length;m++) ``` |



|  |  |
| --- | --- |
| ``` 1 2 3 4 ``` | ``` {       final=twoArg(final,newArr[m]);       }         return final; ``` |

这样就可以将这三部分组合在一起。此题目可以加深对函数式编程的理解。

​

# [Exact Change](https://www.freecodecamp.com/challenges/exact-change)

题目要求：设计一个找零钱的系统

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 ``` | ``` function checkCashRegister(price, cash, cid) {   var change;   // Here is your change, ma'am.   change=cash-price;   return change; }  checkCashRegister(19.50, 20.00, [["PENNY", 1.01], ["NICKEL", 2.05], ["DIME", 3.10], ["QUARTER", 4.25], ["ONE", 90.00], ["FIVE", 55.00], ["TEN", 20.00], ["TWENTY", 60.00], ["ONE HUNDRED", 100.00]]); ``` |

最初给定的程序是这样的，其中第一个参数是商品价格price，第二个参数是顾客实际付款金额，第三个参数是一个数组，也就是收银台目前剩余的零钱数目。

这个程序的要求是能够判断是否有零钱找，找的零钱各自是多少（美元为单位，所以不光有1分，5分这样的零钱，还有25美分等）。

如果执行：

|  |  |
| --- | --- |
| ``` 1 2 3 4 ``` | ``` checkCashRegister(19.50, 20.00, [["PENNY", 1.01], ["NICKEL",  2.05], ["DIME", 3.10], ["QUARTER", 4.25], ["ONE", 90.00], ["FIVE",  55.00], ["TEN", 20.00], ["TWE NTY", 60.00], ["ONE HUNDRED", 100.00]]) ``` |

则结果应当是：

`[[“QUARTER”, 0.50]]，注意这是个二维数组。

这个时候我想先找出来在抽屉里面总共有多少钱，想要将总数相加，但是这个时候要注意cid是一个二维数组，而不是一个JSON，因此应该相加的是cid[0][1]+cid[1][1]…..

但是这个时候遇到一个问题：

return 1.01+2.05; 返回的3.05999996 这样一个值。

而 return 1.01+2.0; 返回的则就是3.01

搜索发现：<http://www.lezhu99.com/2202.html> 和<https://gist.github.com/binjoo/3926896>

得出的结果是这是Javascript语言的BUG。

下面的[方法](https://gist.github.com/binjoo/3926896)可以解决这个Bug

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 ``` | ```  function accAdd(arg1, arg2) {      var r1, r2, m, c;      try {          r1 = arg1.toString().split(".")[1].length;      }      catch (e) {          r1 = 0;      }      try {          r2 = arg2.toString().split(".")[1].length;      }      catch (e) {          r2 = 0;      }      c = Math.abs(r1 - r2);      m = Math.pow(10, Math.max(r1, r2));      if (c > 0) {          var cm = Math.pow(10, c);          if (r1 > r2) {              arg1 = Number(arg1.toString().replace(".", ""));              arg2 = Number(arg2.toString().replace(".", "")) * cm;          } else {              arg1 = Number(arg1.toString().replace(".", "")) * cm;              arg2 = Number(arg2.toString().replace(".", ""));          }      } else {          arg1 = Number(arg1.toString().replace(".", ""));          arg2 = Number(arg2.toString().replace(".", ""));      }      return (arg1 + arg2) / m; } ``` |

这时候注意下面这种情况；

checkCashRegister(19.50, 20.00, [[“PENNY”, 0.01], [“NICKEL”, 0], [“DIME”, 0], [“QUARTER”, 0], [“ONE”, 1.00], [“FIVE”, 0], [“TEN”, 0], [“TWENTY”, 0], [“ONE HUNDRED”, 0]]);

在抽屉里面是有1.01元的，而应找是0.5元，虽然抽屉里的钱足够找，但是却不能够找钱，因为凑不出来这0,5元。

看网上说找零钱问题也属于动态规划，也算是一个比较经典的算法问题了，所以打算先研究研究。

但是这道题目又与动态规划不是太一样，因为给定的约束条件中，每个面值的钱币并不是足够的，因此改变策略。

最后的完整实现过程如下：

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)

[Show hidden characters]({{ revealButtonHref }})








|  |  |
| --- | --- |
|  | // Create an object which hold the denominations and their values 建立一个json来将原来的英文表述转化为数字表述，方便以后的比较 |
|  | var denom = [ |
|  | { name: 'ONE HUNDRED', val: 100.00}, |
|  | { name: 'TWENTY', val: 20.00}, |
|  | { name: 'TEN', val: 10.00}, |
|  | { name: 'FIVE', val: 5.00}, |
|  | { name: 'ONE', val: 1.00}, |
|  | { name: 'QUARTER', val: 0.25}, |
|  | { name: 'DIME', val: 0.10}, |
|  | { name: 'NICKEL', val: 0.05}, |
|  | { name: 'PENNY', val: 0.01} |
|  | ]; |
|  |  |
|  |  |
|  | function checkCashRegister(price, cash, cid) { |
|  | var change = cash - price;//找零数额等于给的现金数目减去商品价格 |
|  |  |
|  | // Transform CID array into drawer object reduce方法是累加器，用于累加，这里就是计算抽屉里的总金额数 |
|  | //arr.reduce(callback,[initialValue]) 第二个参数是累加器的初始值，在这里初始值是total：0 |
|  | var register = cid.reduce(function(acc, curr) { |
|  | acc.total += curr[1]; |
|  | acc[curr[0]] = curr[1]; |
|  | return acc; |
|  | }, {total: 0}); |
|  |  |
|  | // Handle exact change 抽屉里的金额与需找零相等 |
|  | if (register.total === change) { |
|  | return 'Closed'; |
|  | } |
|  |  |
|  | // Handle obvious insufficent funds 抽屉里的金额不足 |
|  | if (register.total < change) { |
|  | return 'Insufficient Funds'; |
|  | } |
|  |  |
|  | // Loop through the denomination array 遍历开头创建的数组， |
|  | var change\_arr = denom.reduce(function(acc, curr) { |
|  | var value = 0; |
|  | // While there is still money of this type in the drawer |
|  | // And while the denomination is larger than the change reminaing有这种类型的钱，并且这种类型的钱比需找要少。 |
|  | //比如需找30，20元面值的钱有1张，这就够了。 |
|  | //这里的 curr.name |
|  | while (register[curr.name] > 0 && change >= curr.val) { //这就是上面提到的30元比20元多的情况 |
|  | change -= curr.val; //重新设定需找数额，这时候就是还差10元了，因为已经有1张20元 |
|  | register[curr.name] -= curr.val; //拿总金额数来减 |
|  | value += curr.val; |
|  |  |
|  | // Round change to the nearest hundreth deals with precision errors |
|  | change = Math.round(change \* 100) / 100; |
|  | } |
|  | // Add this denomination to the output only if any was used. |
|  | if (value > 0) { |
|  | acc.push([ curr.name, value ]); |
|  | } |
|  | return acc; // Return the current Change Array |
|  | }, []); // Initial value of empty array for reduce |
|  |  |
|  | // If there are no elements in change\_arr or we have leftover change, return |
|  | // the string "Insufficient Funds" |
|  | if (change\_arr.length < 1 || change > 0) { |
|  | return "Insufficient Funds"; |
|  | } |
|  |  |
|  | // Here is your change, ma'am. |
|  | return change\_arr; |
|  | } |
|  |  |
|  | // test here |
|  | checkCashRegister(19.50, 20.00, [["PENNY", 1.01], ["NICKEL", 2.05], ["DIME", 3.10], ["QUARTER", 4.25], ["ONE", 90.00], ["FIVE", 55.00], ["TEN", 20.00], ["TWENTY", 60.00], ["ONE HUNDRED", 100.00]]); |

[view raw](https://gist.github.com/zhangolve/40a244aee8198a4e949bdfecc3b77d47/raw/8513d9ec5045b035791d7e9babb04e4a50b4f826/Exact-change.js)
[Exact-change.js](https://gist.github.com/zhangolve/40a244aee8198a4e949bdfecc3b77d47#file-exact-change-js)
hosted with ❤ by [GitHub](https://github.com)

​