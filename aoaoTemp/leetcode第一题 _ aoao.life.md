---
title: leetcode第一题 | aoao.life
date: 2016-05-18 12:38:49
updated: 2026-03-01 06:20:12
---

LeetCode 第一题

题目要求：

Given an array of integers, return indices of the two numbers such that they add up to a specific target.

You may assume that each input would have exactly one solution.

Example:

Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,  
return [0, 1].

UPDATE (2016/2/13):  
The return format had been changed to zero-based indices. Please read the above updated description carefully.

Subscribe to see which companies asked this question

简单地翻译一下就是给定一个数组nums和一个目标target，要求能够将数组中两个元素相加能够与target相等，这个时候就输出两个元素的index。

使用Javascript语言，我写出了下面的程序。总体来说，这道题目确实比较简单，就是二重循环遍历而已，只要要求内层遍历的数字j总比外层遍历的数字i大，这个先决条件成立就可以了。当找到符合要求的两个数字i和j之后呢，只需要将这两个数字放入到一个新的数组之中输出就ok了。

```
/**
 * @param {number[]} nums
 * @param {number} target
 * @return {number[]}
 */
var twoSum = function(nums, target) {
    for(var i=0;i<nums.length;i++){
        for(var j=i+1 ;j<nums.length;j++)
        {
            if(nums[i]+nums[j]==target){
                var newArray=[i,j];
                return newArray;
            
            }
        }
    }
    
};
```