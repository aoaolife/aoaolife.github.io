---
title: JS入门（4）使用Javascript实现回文检查 | aoao.life
date: 2016-05-03 19:14:49
updated: 2026-03-01 06:20:12
---

如果只是判断是否反序和正序是一样的，那其实就简单了。

但是在题目中是要求

- 忽略大小写，这要求像类似 abcCBA 这样的字符串也能够返回true。
- 忽略其他所有的标点符号，包括空格。这也要求像 never odd or even 甚至是”0\_0 (: /-\ :) 0-0”这样的字符串也应该返回true。

为了先测试，我首先写出了下面的程序

```
function palindrome(str) {
  // Good luck!
  var newArray=[];
  newArray=str.split('');
  if(newArray[0]==newArray[(newArray.length)-1])
    {
      return "true";
    }
}



palindrome("eye");
```

这个程序得到的结果自然是返回true了。毕竟eye这个字符串应该是最简单的那种了。

之后，我考虑到还是先从简单到复杂比较好，于是还是先暂时忽略掉大小写和标点符号的情况。这个时候发现，其实正确（true）的情况其实相对错误（false）来说还是太少的。所以，与其找true的情况，不如来找false的情况。使用一个for语句来达到遍历的目的，遍历的个数是(newArray.length)/2，这个我们在初高中的时候就已经学习过了。之后就是做判断了。

> 只要在取到的所有的i 中，newArray[i]的值，哪怕有一个是不等于 newArray[(newArray.length)-1-i]的值，我们都可以说，这个数组是不符合要求的，也就是正序和反序不一致的。相反，它的反面，就是所有的newArray[i]== newArray[(newArray.length)-1-i] ,这自然是可以返回true的了。

正是我刚刚这个略微拗口的思路，就有了下面的程序

```
function palindrome(str) {
  // Good luck!
  var newArray=[];
  newArray=str.split('');
  for(var i=0;i<(newArray.length)/2;i++)
    {
  if(newArray[i]!==newArray[(newArray.length)-1-i])
    {
      return "false";
    }
  }
  
   return "true";
  

}
palindrome("eyaaye")  ;  //“ ”内部内部可以随意改变以供测试
```

这个时候，这个程序已经能够实现对于一个规矩的字符串的正反序是否相同的判断了。  
下面要做到，就是加入「忽略大小写」和「标点符号」的功能了。

为了达到去掉「标点符号」的目的，思路当然还是使用正则表达式了。然后使用replace()方法来替换。

```
function palindrome(str) {
  // Good luck!
  var newArray=[];
  str=str.replace(/,|\+|\.|_|\\|-|\/|\s/g,'');
  
  
  newArray=str.split('');
  for(var i=0;i<(newArray.length)/2;i++)
    {
  if(newArray[i]!==newArray[(newArray.length)-1-i])
    {
      return "false";
    }
  }
  
   return "true";
  

}
palindrome("e  y/,e+e...y\\e")  ;  //“ ”内部内部可以随意改变以供测试
```

这个时候注意观察含有正则表达式的那一行代码：  
   
 str=str.replace(/,|+|.|\_|\|-|/|\s/g,’’);

让我们来回顾一下正则表达式，在这里|这个符号用法就是或的意思。也就是在这里，匹配是一个或的关系。replace() 方法内部含有正则表达式标准的//g ，//内部是匹配的字符。包括了逗号，句号，下划线，减号，斜杠，反斜杠等，这里要特别注意的是，由于斜杠和反斜杠本身是特殊字符，这个时候就用到了反斜杠了，在特殊字符前加反斜杠可以还原特殊字符的字面意，这样我们就可以看到|\| 这样的匹配了。

这个时候发现要求中是要输出boolean类型的true 或者是false，而我则是使用的字符串输出，因此还需要将两对引号去掉，这样才能够输出boolean量。

另外也发现，上面的正则表达式还是不能够匹配类似下面这样的字符串：

“0\_0 (: /-\ :) 0-0”

所以很显然还是要在正则表达式上做文章，将正则表达式单独拿出来看。

```
function palindrome(str) {
	  // Good luck!
	  var newArray=[];
      str=str.replace(/,|\+|\.|_|\\|-|\/|\s|:|\(|\)/g,'');
      str=str.toLowerCase();
	 return str;
      /*
      newArray=str.split('');
	  for(var i=0;i<(newArray.length)/2;i++)
	    {
	  if(newArray[i]!==newArray[(newArray.length)-1-i])
	    {
	      return false;
	    }
	  }
	  
	   return true;
	  
	*/
	}
	palindrome("0_0 (: /-\ :) 0-0")  ;  //“ ”内部内部可以随意改变以供测试
```

将回文判断的部分注释掉，便于观察，则还有括号部分和冒号部分其实还没有使用正则表达式来替换，这个时候我经过测试才意识到一左一右的括号也是属于特殊符号，所以也需要在匹配的时候在他们前面加上反斜杠。

这个时候再把/\* \*/去掉，最终可以得到：

```
function palindrome(str) {
 
  var newArray=[];
  str=str.replace(/,|\+|\.|_|\\|-|\/|\s|:|\(|\)/g,'');
  str=str.toLowerCase();
  newArray=str.split('');
  for(var i=0;i<(newArray.length)/2;i++)
    {
  if(newArray[i]!==newArray[(newArray.length)-1-i])
    {
      return false;
    }
  }
  
   return true;
}
palindrome("0_0 (: /-\ :) 0-0")  ;  //“ ”内部内部可以随意改变以供测试
```