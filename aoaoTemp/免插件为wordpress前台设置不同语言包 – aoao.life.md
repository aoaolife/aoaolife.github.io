---
title: "免插件为wordpress前台设置不同语言包 – aoao.life"
date: 2023-12-12 15:46:16
---

一直以来，都比较排斥使用中文版的WP，因为觉得后台部分翻译得不好。所以导致前台的界面也一直是英文的。
今天搜了一下让前台和后台设置不同语言的方案，发现给出的都是下载一个叫admin-locale的插件。
下载这个插件之后，发现其只有寥寥几行。这种简单的东西如果还允许作为插件存在，就太面上无光了。
把里面的内容去芜存菁（因为我不用区别后台和插件是否有语言包）以后，就剩下简单粗暴的干货了。如下。

```
add_filter( 'locale', 'my_locale', 99 );
function my_locale( $locale )
{
if ( is_admin() )
{
return $locale ; /*或者指定某种语言*/
}
return 'zh_CN' ; /*或者指定某种语言*/
}
```

当然这样还不算完。因为有主题上的很多文字部分使用的不是主题语言包，而是系统语言包。所以，还要把zh_CN.po和zh_CN.mo拷贝到/wp-content/languages/下(因为我不喜欢中文的其他处理,所以只拷贝这两个文件。)

或者如果主题的语言包写得好的话，也可以采用另外一种温柔一点的方式：

```
add_filter( 'theme_locale', 'my_theme_locale', 999 );
function my_theme_locale( $locale, $domain )
{
return 'zh_CN' ;
}
```

搞定收工！