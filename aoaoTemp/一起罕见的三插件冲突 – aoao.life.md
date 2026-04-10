---
title: "一起罕见的三插件冲突 – aoao.life"
date: 2022-12-02 22:08:31
---

把这次调查问题的思路整理一下，看看对各位WP玩家能否有所帮助。

从搬家以来，WP Code Highlight就一直存在显示问题。上插件官网报个问题吧，给设置评论审核了，也没个回应。
癣疥之疾，一直没当回事。直到上午不宜乐乎兄弟再次指摘，才又抽空找了一下原因。

1、定位调查方向
本地模拟环境下，单独只运行一个插件，没问题。在服务器上换主题，仍旧出现问题。
所以把目标锁定在插件冲突上。

2、确定原因
分别保存下能正常显示和不能正常显示的时候，两组pagesource。通过对比发现，WP Code Highlight用于分行的span标签被意外干掉了。
比较工具：WinMergeU。

3.查找元凶
推论是，这是某个对the_content的内容进行动作的插件干得好事！
在所有插件中搜索“the_content”。发现仅有四个插件对the_content进行了过滤。
逐个Disable/Enable插件，试图锁定问题插件。这时发现了一个奇怪的现象：NextGEN Gallery和BJ Lazy Load不能同时共存，但单独运行其中一个都不会导致问题发生。

4.解决问题
这时，问题反而清晰了。NGG Gallery对BJ Lazy Load的某个特殊处理，导致了WP Code Highlight添加的tag无效。
再次在NGG Gallery中搜索the_content，发现罪魁祸首在module.third_party_compat.php的第364行：

```
function bjlazyload_filter($content)
{
return trim(preg_replace("/\s\s+/", " ", $content));
}
```

看到了吧：这个函数起作用的话，就会把尖括号中间的span给干掉！
最简单的改法就是把

```
return trim(preg_replace("/\s\s+/", " ", $content));
```

改成

```
return $content;
```

但是这样改似乎并不太好。最理想的状态是干掉那个filter，就是干掉这一句所产生的后果。

```
add_action('wp',   array(&amp;$this, 'bjlazyload'), PHP_INT_MAX);
```

NGG又做得太绝了一点，把这句添加的时机放在了最后。而本人学艺不精，并不清楚“wp”后面的动作是什么。所以没想到在function.php中阻止它的好办法。
所以只好把这一行注掉。
大功告成。

最后再总结一下结论给通过关键字搜索来的朋友：
**WP Code Highlight只显示一行的一个原因是：**
**WP Code Highlight与NextGEN Gallery，BJ Lazy Load有冲突。**

解决方法是：
注掉\nextgen-gallery\products\photocrati_nextgen\modules\third_party_compat\module.third_party_compat.php第81行

```
add_action('wp',   array(&amp;$this, 'bjlazyload'), PHP_INT_MAX);
```