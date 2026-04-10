---
title: "wordpress新page template的创建 – aoao.life"
date: 2022-04-23 22:29:47
---

这两天,关于单机版9601的研究陷入僵局.转投到换模板的研究当中.其实换模板就P大点事.但是插件装得多了,就难免会有顾头不顾腚的事情发生.所以先利用xampplite单机修改模板,插件和css先.wordpress的cache别的功能没有,在线改css制造出来的麻烦可不是一般二般的强.
同时也动了增加新plugin的花花心思.想用某插件的时候需要一个page template,却左右都找不到写page的时候template的选项.对比现有的blog更是百思不得其解,没看清楚差别在哪里.只是隐约记得跟不同的模板有关系.
百度跟股沟这两个烂货,什么有价值的信息都找不到.只好直接查看wordpress的源代码.发现原理模板选择的选项需要模板数大于0才会出现(隐藏boss?)
用google,全英文关键字,终于找到了正主的模板创建说明简单看了一下,原来如彼啊!!翻译一下吧,免得以后再遇到同样问题的哥们晕倒.
**BTW:俺的blog好像被baidu打入黑名单了,搜不到任何东西.已经三个多月没有来自百度搜索的访问量了**
下边是俺翻译的原文:

> **创建你自己的页模板(Page Templates)**
> 用来定义页模板的文件放在主题(Theme)目录下.为了创建一个新的用于页的模板,你必须新创建一个文件.如果我们把我们的第一个页模板叫做”snarfer.php”的话,那么在snarfer.php的顶部,粘贴上这段:

```
<?php
/*
Template Name: Snarfer
*/
?>
```

> 上面的代码定义了一个”snarfer.php”文件作为叫做”Snarfer”的模板.自然地,”Snarfer”可以被其他的任何名字所替代.这个名字在你使用主题编辑器(Theme Editor)的时候,会作为一个链接出现.
> 这个文件几乎可以以任何词汇或字母作为名字,以php作为扩展名即可.(参照保留的主题文件名称(reserved Theme filenames),查看哪些名字不可以作为文件名.这些名字作为wordpress的保留名字出现.).
> 想在上面的五行代码之后加些什么,由你自己决定.你写在后面的代码将决定”Snarfer”这个页模板将显示些什么.为了实现这个目的,你可以查看模板标签(Template Tags)看看有哪些供Wordpress模板使用的函数.更方便的做法是,拷贝现有的模板(比如page.php或者index.php)到snarfer.php,再把上边的五行代码考到文件的顶部.这样,你可以只改动少量的html和php内容,而不必一切从头开始.下班有一个例子当你把创建好一个页模板并把它放在主题目录下之后,在你创建或者编译一个页的时候,就可以选用这个模板了.
>
> **一个页模板的例子**
> 这个例子在上部显示页的内容,下边按月显示历史记录.它是为wordpress默认主题(aka Kubrick)设计的,但是稍做修改后在大多数主题下都可以使用.

```
<?php
/*
*/
?>

<?php get_header(); ?>

<div id="content" class="widecolumn">

<?php if (have_posts()) : while (have_posts()) : the_post();?>
<div class="post">
<h2 id="post-<?php the_ID(); ?>"><?php the_title();?></h2>
<div class="entrytext">
<?php the_content('<p class="serif">Read the rest of this page &raquo;</p>'); ?>
</div>
</div>
<?php endwhile; endif; ?>
<?php edit_post_link('Edit this entry.', '<p>', '</p>'); ?>

</div>
<div id="main">

<?php include (TEMPLATEPATH . '/searchform.php'); ?>

<h2>Archives by Month:</h2>
<ul>
<?php wp_get_archives('type=monthly'); ?>
</ul>

<h2>Archives by Subject:</h2>
<ul>
<?php wp_list_cats(); ?>
</ul>

</div>
<?php get_footer(); ?>
```