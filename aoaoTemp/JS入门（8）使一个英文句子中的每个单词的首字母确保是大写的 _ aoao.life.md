---
title: JS入门（8）使一个英文句子中的每个单词的首字母确保是大写的 | aoao.life
date: 2016-05-07 15:44:49
updated: 2026-03-01 06:20:12
---

题目要求：使一个英文句子中的每个单词的首字母确保是大写的

题目中给定的原程序是：

```
function titleCase(str) {
  return str;
}

titleCase("I'm a little tea pot");
```

思路是先将这个句子形式的字符串切分成以单词为单位的数组，然后再对每个数组中的元素进行处理。

```
function titleCase(str) {
  var arr=str.split(" ");
  for(var i=0;i<arr.length;i++)
    
    {
      str1=arr[i];  
      str1=arr[i].toLowerCase();     //先将整个单词的每个字母都统一成小写
     
      str1=str1.replace(/(\w)/,        //使用正则表达式来替换每个单词的首字母
                        function(m){      //正则表达式中的/\w/表示的替换的第一个字母咯。
        return m.toUpperCase();           //替换的第二部分使用一个function意在返回一个大写字母，这个是我现在想 
      });                                  //不到的，看了别人的代码
      arr[i]=str1;
      
    }
  
    /*for end* 到for循环结束的时候其实arr这个数组中的每个元素，也就是每个单词已经是首字母大写了/
  var new=arr.join(" ");      //通过使用join方法将原来的数组合并成一个新的字符串
							//这里还是要注意join()方法内的引号中有一个空格
  return new;                       //最后就是返回这个字符串的值了。
}

titleCase("I'm a little tea pot");
```