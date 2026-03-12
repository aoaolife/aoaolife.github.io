---
title: JS入门（5）找出一个英文句子字符串中最长的单词并返回单词的长度值 | aoao.life
date: 2016-05-07 15:37:49
updated: 2026-03-01 06:20:12
---

找出一个英文句子字符串中最长的单词并返回单词的长度值

思路是先将这个英文句子使用split() 切分成各个单词，然后通过遍历得到每个单词的长度，通过比较每个单词的长度来得到最长的单词并返回该单词长度值。

最初给定的程序是下面这样的：  
   
 function findLongestWord(str) {  
 return str.length;  
 }  
   
 findLongestWord(“The quick brown fox jumped over the lazy dog”);

然后按照之前的思路来写程序，得到了下面的程序：

```
function findLongestWord(str) {
  var arr= str.split(" ");  //句子切分
  var max=0;    //因为只是要返回一个数字，因此给定一个变量max，
  for(var i=0;i<arr.length;i++)    //通过遍历来找到这个数组中所有的字符串
    {
       var num=arr[i].length;      //使用.length 方法来找到每个字符串的长度
      if(max<num){                   //将每个字符串长度与原始给定值max做比较，确保max始终是一个最大值
        max=num;
      }      
    }
  return max;
}

findLongestWord("The quick brown fox jumped over the lazy dog");
```