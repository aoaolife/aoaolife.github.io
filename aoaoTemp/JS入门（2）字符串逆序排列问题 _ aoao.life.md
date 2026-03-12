---
title: JS入门（2）字符串逆序排列问题 | aoao.life
date: 2016-05-03 19:12:49
updated: 2026-03-01 06:20:12
---

原始题目是：给出一个字符串比如说“hello”，要求将这个字符串处理成“olleh”。

思路其实很清晰了，在JS中有split()可以将字符串切分成一个array。这个时候再对这个array进行处理，把这个array进行逆序，使用reverse()方法。

我的第一步是先要切分字符串“hello”，由于我之前学习的时候是切分一句话式的字符串，比如“hello world”，这个时候可以使用

```
string.split(' ')
```

注意括号里引号内有一个空格的位置，就是说以空格作为切分区间。但是在这里没有空格，后来发现，没有空格就不要空格了。所以写成了下面这样：

```
function reverseString(str) {
  var newArray=str.split('');
  return newArray;
}

reverseString("hello");
```

得到了切分好的序列。

后面的过程就很清晰了，使用reverse()方法进行序列反转。

```
function reverseString(str) {
  var newArray=str.split('');
  return newArray.reverse();
}

reverseString("hello");
```

然后再使用join()方法

```
function reverseString(str) {
  var newArray=str.split('');
  return newArray.reverse().join('');
}
	
reverseString("hello");
```

注意这里的join()方法中的`‘’`还是不能够去掉，否则还是无法得到一个字符串。