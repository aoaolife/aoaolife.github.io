---
title: "如何将DokuWiki中indexmenu插件和tagcloud插件中显示的英文内容变为大写 – aoao.life"
date: 2020-06-22 12:34:44
---

[DokuWiki](https://pewae.com/gaan/aHR0cHM6Ly93d3cuZG9rdXdpa2kub3JnL2Rva3V3aWtp)的保存规则，是把所有的字母统一改成小写。这样做便于管理，无可厚非。
[indexmenu](https://pewae.com/gaan/aHR0cHM6Ly93d3cuZG9rdXdpa2kub3JnL3BsdWdpbjppbmRleG1lbnU=)插件和[cloud](https://pewae.com/gaan/aHR0cHM6Ly93d3cuZG9rdXdpa2kub3JnL3BsdWdpbjpjbG91ZA==)插件是DokuWiki的两个常用插件，它们调用了DokuWiki的默认函数以生成链接，所以当然也是显示成全小写。
但在显示一些特定内容，尤其是大量使用英文缩写作为专有名词的时候，看起来就特别扭。
能搜到修改保存链接的方案。但是我觉得全存小写挺好的，我只想修改读出来的内容。

经过几个小时的研究，终于被我找到了把他们改成大写的方法。
而且还找到不止一种。

## 1.不改代码，通过修改css实现小写变大写

编辑【dokuwiki目录】/conf/userstyle.css，追加下列样式：

```
.dokuwiki div.cloud a {
text-transform: uppercase;
}
#dokuwiki__aside a {
text-transform: uppercase;
}
```

这种方法其实除了表里不一以外没什么缺点。可是我非要找到生成链接的位置不可。

## 2.1 将侧边栏标题中的小写变大写

编辑【dokuwiki目录】/lib/plugins/indexmenu/syntax/indexmenu.php
查找函数【_html_list_index】，824行附近：

```
$ret .= $item['title'];
```

替换成：

```
//$ret .= $item['title'];
$ret .= mb_strtoupper($item['title'], 'UTF-8');
```

## 2.2 将侧边栏内链接中的小写变大写

编辑【dokuwiki目录】/lib/plugins/indexmenu/syntax/indexmenu.php
查找函数【_html_list_index】，829行附近：

```
$ret .= html_wikilink(':'.$item['id']);
```

替换成：

```
//$ret .= html_wikilink(':'.$item['id']);
$match = array();
preg_match('/<a (.*)>(.*)<\/a>/', html_wikilink(':'.$item['id']), $match);
$ret .= str_replace($match[2], mb_strtoupper($match[2], 'UTF-8'), html_wikilink(':'.$item['id']));
```

用了三行代码。如果专业的话应该能用一个preg_regx函数搞定，奈何咱搞正则实在是心虚啊！

## 2.3 将tagcloud中的小写变大写

编辑【dokuwiki目录】/lib/plugins/cloud/syntax.php
查找函数【render】，146行附近：

```
if ($flags ['showCount'] === true) {
$name .= '('.$size.')';
}
```

在其下方追加：

```
$name = mb_strtoupper($name, 'UTF-8');
```

搞定！