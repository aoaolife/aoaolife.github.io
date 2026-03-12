---
title: JS入门（12）ROT13解密 | aoao.life
date: 2016-05-18 12:40:49
updated: 2026-03-01 06:20:12
---

在密码学上最简单的加密方式是[ROT13](https://en.wikipedia.org/wiki/ROT13)，这种加密方式将26个字母按照顺序进行了替换。比如A被替换成了N，B被替换成了O。我们下面要做的程序是对这样的密码进行解密。通过设计JS程序来实现解密过程。

在这里，我们假定我们的加密后的密码是一串大写的英文字母以及可能包括的空格或其他标点符号，我们要对它进行破译。

# 分析过程

考虑要完成这样的解密过程，首先要进行转换。原始的密码是字符串形式的英文字母，而字母是不容易实现+13的操作的，因此我们这个时候考虑需要先将该字符串转换成为一串代表他们的ASCII码，我们使用了String.prototype.charCodeAt() 这个方法。接着是做出判断，我们需要的是将数字类型的ASCII码进行操作，但同时要确保当操作完成之后逆向之后还必须保证原来是字母的还是字母。这样我们可以找到一个对应的公式。于是也就可以写出下面的程序：

```
function rot13(str) {

 var numArray=[]; //一个空的数组用于存放转为ASCII码的结果
 
for(var i=0;i<str.length;i++)
 {if(str.charCodeAt(i)>64&&str.charCodeAt(i)<91) //选择出是大写字母的那一部分
   {
    
   numArray[i]=str.charCodeAt(i); 将大写字母全部替换成他们对应的ASCII码
     
   }
 }
  
 
  for(var j=0;j<numArray.length;j++){
    if(typeof numArray[j]=== 'undefined'||numArray[j]===null)
      {
         numArray[j]=32;  //这是空格的ASCII码，经过优化后的程序无此条语句
        
      }

    else
	//下面是之前提到的公式，78是分界线
    if(numArray[j]<78){
      numArray[j]+=13;
    }
    else{
      numArray[j]-=13;
    }
  }
 

 var newArray=[];
  for(var l=0;l<numArray.length;l++)
    {
      
 newArray.push(String.fromCharCode(numArray[l]));  //将每一个都推入新建的数组之中。
    }
  
  return newArray.join('');  //将原来的数组又转换成字符串形式
}

// Change the inputs below to test
rot13("SERR CVMMN!");
```

# 程序改进

上面的程序还有一些问题，比如对于类似“SERR CVMMN!”的字符串，因为有一个！的存在就不能够很好地转换了，之前我的程序是认为密码中除了数字之外就只有空格了，事实显然不是这样，因此又对程序做了改动。改动的调试过程其实很长，但是有一条其实是核心的，就是要判断数组中的某个元素的类型是否是数字，我之前使用的是判断：

```
	if(typeof numArray[j]=== 'undefined'||numArray[j]===null)
```

但是这样的判断在后来判断！等的时候就变得有些困难了。后来，我选择了直接判断是不是数字类型，也就是

```
if(typeof numArray[j]==='number')
```

后来对原程序作了改进。  
   
 function rot13(str) { // LBH QVQ VG!  
   
 var numArray=[];  
   
 for(var i=0;i<str.length;i++)  
 {if(str.charCodeAt(i)>64&&str.charCodeAt(i)<91)  
 {  
   
 numArray[i]=str.charCodeAt(i);  
   
 }  
 else {  
 numArray[i]=str[i];  
 }  
 }  
   
   
 for(var j=0;j<numArray.length;j++){  
 if(typeof numArray[j]===’number’)  
 if(numArray[j]<78){  
 numArray[j]+=13;  
 }  
 else{  
 numArray[j]-=13;  
 }  
 }  
 var newArray=[];  
 for(var l=0;l<numArray.length;l++)  
 {  
 if(typeof numArray[l]===’number’){  
 newArray.push(String.fromCharCode(numArray[l]));  
 }  
 else{  
 newArray.push(numArray[l]);  
 }  
 }  
   
 return newArray.join(‘’);  
 }  
   
 // Change the inputs below to test  
 rot13(“SERR CVMMN!”);

当然上面的程序已经能够完美地实现结果了。但是代码量太大，程序执行起来效率低，三个for循环遍历有点多了。可以继续优化代码，比如将原程序中第二个for改成一个function放入第一个循环之中。总之，能够优化的方面还有很多吧，只是最先想到的还是上面的算法。

```
function rot13(str) { // LBH QVQ VG!

 var numArray=[];
 
for(var i=0;i<str.length;i++)
 {if(str.charCodeAt(i)>64&&str.charCodeAt(i)<91)
   {
    
   numArray[i]=str.charCodeAt(i);
     rot13(i);
     
   }
  else {
    numArray[i]=str[i];
    rot13(i);
  }
 }
  
 //建立一个子函数来处理数值判断
  function rot13(j){
     if(typeof numArray[j]==='number')
	  if(numArray[j]<78){
      numArray[j]+=13;
    }
    else{
      numArray[j]-=13;
    }
     }

 var newArray=[];
  for(var l=0;l<numArray.length;l++)
    {
       if(typeof numArray[l]==='number'){
 newArray.push(String.fromCharCode(numArray[l]));
       }
      else{
        newArray.push(numArray[l]);
      }
    }
  
  return newArray.join('');
}

// Change the inputs below to test
rot13("SERR CVMMN!");
```

# 总结

本题目是使用javascript实现将密码进行破解得到原始字符串,在这里我也重点回顾和学习了以下这几个知识点

- 数组和字符串之间的相互转换过程 如上所述,在这里我使用了遍历字符串str的方式通过给数组numArray中增加元素的方式来进行转换，而在上面程序的最后我使用了join()方法来将数组转换为一个字符串。
- typeof 的使用 ，在这里使用typeof无疑会使程序很高效了。如上使用typeof判断是否为number是点睛之笔。
- 上面程序使用了三次遍历，第一次遍历用来将字母转换成数字，将字符串转换为数组，第二次遍历将转换后的数字进行解密操作，第三次遍历则是将数组重新转换为字符串同时将数字转换为字母。

# 简单方法

这个方法当然并不是我自己写出来的，而是来自google的[结果](https://dzone.com/articles/rot13-javascript-function) 。但是我想对它进行分析还是有好处的，我们也不能总用傻大笨的方法吧！

```
function rot13(str) { 

return str.replace(/[a-zA-Z]/g, function(c){

	return String.fromCharCode((c <= "Z" ? 90 : 122) >= (c = c.charCodeAt(0) + 13) ? c : c - 26);

});

}
// Change the inputs below to test
rot13("SERR CVMMN!");
```

最终返回的是经过str.replace()之后的结果，这里当然也使用了正则表达式进行适配。但是这个算法的巧妙之处是replace()方法的第二个参数给出了一个function(c) ，这个参数也就是将要替换的值。

在function(c)函数之中，拆分来看String.fromCharCode()内部是一个条件选择表达式，当c<=‘Z’进行判断，如果成立则返回90（对应的是大写Z），反之不成立则返回的是122（对应的是小写z）。

之后就看不懂这神奇的代码了。以后看懂了可能会更新吧。