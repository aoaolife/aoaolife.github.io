---
title: 【LEETCODE-300】最长增加子序列问题 | aoao.life
date: 2016-07-05 16:40:49
updated: 2026-03-01 06:20:12
---

问题描述：

> Given an unsorted array of integers, find the length of longest increasing subsequence.

> For example,  
> Given [10, 9, 2, 5, 3, 7, 101, 18],  
> The longest increasing subsequence is [2, 3, 7, 101], therefore the length is 4. Note that there may be more than one LIS combination, it is only necessary for you to return the length.

> Your algorithm should run in O(n2) complexity.

> Follow up: Could you improve it to O(n log n) time complexity?

给定一个不规则的整数数组，找出最长的增加的子序列  
比如给定数组为[10, 9, 2, 5, 3, 7, 101, 18]，最长增加子序列为 [2, 3, 7, 101，因此这个长度是4.这里所说的子序列，要求是值是一直在增加的。这时候可能会有多种方案，但是我们需要的只是这个子序列的长度值。

算法的复杂度in O(n2)。

分析：遍历

来看一下使用Java实现的代码：

```
public class Solution {  
    public int lengthOfLIS(int[] nums) {  
        //[10, 2, 5, 3, 7],  
        if(nums==null || nums.length<1) return 0;  
          
        int [] d = new int[nums.length];  //动态规划中的数组，默认的长度是nums这个原数组的长度。
        d[0] = 1;        
        int max = 1;  
        for(int i=1; i<nums.length; i++) {  
            d[i] = 1;    
            for(int j=0; j<i; j++) {  
                if(nums[i] > nums[j]) {  
                    d[i] = Math.max(d[i], d[j]+1);  
                }  
            }  
            max = Math.max(max, d[i]);  
        }  
        return max;  
    }  
}
```

看网络上对这道题的分析，说是一道动态规划的问题。

> An easy dynamic programming problem.

> Given array arr, we can define another array dp, dp[i] means the length of longest increasing subsequence when the last item is arr[i]. How to get dp[i]? We can get it by enumerating from index=0 to index=i-1(for instance j), and check the value of arr[j] and arr[i], if arr[i] > arr[j], then dp[i]=max(dp[i],dp[j]+1).

> The algorithm above runs in O(n2) complexity, how to improve it to O(n log n) time complexity? Use binary search, see the code in detail. My runtime beats 100.00% of javascript submissions.

我最初写的js代码：

```
/**
 * @param {number[]} nums
 * @return {number}
 */
var lengthOfLIS = function(nums) {
    var j=1;
    var length=0;
    var newArray=[0,0];
    for(var m=2;m<nums.length;m++)  //这是一个外嵌套
    {
    for(var i=m;i<nums.length;i++)
    {
        if(nums[i]<nums[i+j])
        {
            newArray[i]=nums[i];
            newArray[i+j]=nums[i+j];
            
        }
        
        else{
            j++;
            i--;
            
        }
        
    }
     for(var k= 0 ;k<newArray.length;k++)
 {
             if(newArray[k] === "" || typeof(newArray[k]) === "undefined")
             {
                      newArray.splice(k,1);
                      k= k-1;
                  
             }
              
 }
     
     if(length<newArray.length)
     {
         length=newArray.length;
         return newArray;
     }
    }
    

};
```

在学习「动态规划」的过程中，也了解到[什么是动态规划？动态规划的意义是什么?](https://www.zhihu.com/question/23995189/answer/35324479)

原来的英文解释稀里糊涂，在这个知乎回答中看到了对问题的重新解释：

- 给定一个数列，长度为N，
- 设F\_{k}为：以数列中第k项结尾的最长递增子序列的长度.
- 求F\_{1}..F\_{N} 中的最大值.

显然，这个新问题与原问题等价。  
而对于F\_{k}来讲，F\_{1} .. F\_{k-1}都是F\_{k}的子问题：因为以第k项结尾的最长递增子序列（下称LIS），包含着以第1..k-1中某项结尾的LIS。

这里解释一下，比如原序列为[1,3,2,5,7,4],这里如果取k=5的话，这个时候N=6，代入进来看。给定的序列长度为6，F\_{k}即为F\_{5}=4,这个子序列就是[1,3,5,7]，注意这个时候以第5项结尾（也就是以7结尾）的最长子序列是一个范围更大的序列，他也一定包含着小序列。当取k=4的时候，这个时候最长子序列为[1,3,5]，而这个[1,3,5]是属于[1,3,5,7]这个序列的。

这个时候问题就可以转化了（数学上说的状态转移方程）：

以第k项结尾的LIS的长度是：保证第i项比第k项小的情况下，以第i项结尾的LIS长度加一的最大值，取遍i的所有值（i小于k）。  
这个时候，就需要用到递归了。

经过这样的理解之后，我自己又看了前面提到的Java版本的程序，写出了下面的程序：

```
/**
 * @param {number[]} nums
 * @return {number}
 */
var lengthOfLIS = function(nums) {
    
    if(nums===null||nums.length<1)
    {
        return 0;
    }
    
    
    
    var dp=[];
    dp[0]=1;
    
    for(var i=1;i<nums.length;i++)
    {
        dp[i]=1;
        for(var j=0;j<i;j++)
        {
        if(nums[j]<nums[i])
        {   
            
            dp[i]=Math.max(dp[j]+1,dp[i]);  //比较
        }
        }
    }
    var max=1;
    for(var k=0;k<dp.length;k++)
    {
        if(max<dp[k])
        {
            max=dp[k];
        }
    }
    return max;
};
```

上面的程序，总体设计思路是与前面的Java版本相同的，也是状态转移方程的思路。