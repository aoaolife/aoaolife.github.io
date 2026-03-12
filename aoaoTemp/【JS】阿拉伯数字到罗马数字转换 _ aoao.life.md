---
title: 【JS】阿拉伯数字到罗马数字转换 | aoao.life
date: 2016-07-13 14:42:49
updated: 2026-03-01 06:20:12
---

要求是给定一个阿拉伯数字（范围从1-9999），将这个阿拉伯数字转化成罗马数字。

# 分析

这道题目本身并不复杂，我最初想过一些比较复杂的方法，后来觉得可能想起来比较简单的方法虽然代码较多，但还是能够实现。因此只写出了下面的代码。这里要注意的一点是，与C语言不同，Javascript中的运算操作，两个整数相除，在C语言中会自动取整，而在Javascript中，则是会取小数，例如5/2，在C语言中的结果是2，而在JS中则是2.5。我也正是在这一步中，出现了一些Bug，因此调试了一会儿。

# 代码实现

```
function convertToRoman(num) {
 var arr0 =['I','II','III','IV','V','VI','VII','VIII','IX'];
  var arr1=['X','XX','XXX','XL','L','LX','LXX','LXXX','XC'];
  var arr2=['C','CC','CCC','CD','D','DC','DCC','DCCC','CM'];
  var arr3=['M','MM','MMM','MV','V','VM','VMM','VMMM','MX'];
 var luoqian,luobai,luoshi,luoge;
  var luo=[];
  
  
  var ge=num%10;
  var shi=parseInt(num/10);
  var bai=parseInt(num/100);
  var qian=parseInt(num/1000);
  
  if(qian>0){
	
	luoqian=arr3[qian-1];
	luobai=arr2[bai%10-1];
	luoshi=arr1[shi%10-1];
	luoge=arr0[ge-1];
	
  }
  else if(bai>0){
	luobai=arr2[bai-1];
	luoshi=arr1[shi%10-1];
	luoge=arr0[ge-1];
	
  }
  
  
  else if(shi>0){
	
	luoshi=arr1[shi-1];
	luoge=arr0[ge-1];
	console.log(luoshi);
  }
  
  else{
	luoge=arr0[ge-1];
	
  }
  
  
  
  luo.push(luoqian,luobai,luoshi,luoge);
  for(var i=0,len=luo.length;i<len;i++)
	{
	  if(luo[i]===''||luo[i]===undefined)
		{
		  luo.splice(i,1);
		  len--;
		  i--;
		}
	  
	}

  var luonumber=luo.join('');
  return luonumber;
  
  
}

convertToRoman(1990);
```