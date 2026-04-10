---
title: "comments_template()隐藏的秘密 – aoao.life"
date: 2022-03-02 23:24:00
---

目前的模板是[自己拼凑](https://pewae.com/2010/02/change-a-theme.html )出来的，意外发现不能正常显示pinback的内容。
google之后找到解决的办法（http://wordpress.org/support/topic/352439）
，在调用$comments_by_type之前先调用一下

```
<?php $comments_by_type = &#038;separate_comments($comments); ?>
```

，对评论进行分类。
可是，跟在WP官方论坛上提出疑问的哥们一样，我也奇怪为什么别人不用分类，到我这里就必须分。
搜索了一下separate_comments的出处，我找到了答案。
原来问题出在

```
comments-template.php中comments_template( $file = '/comments.php', $separate_comments = false )
```

的第二个参数上。
代码里明明白白写着，这个参数就是管是否对评论进行分类的。
而我的主题，single抄自default模板，调用的是默认参数。

```
<?php comments_template(); ?>
```

而带分类的模板，调用comments的时候，用的是

```
<?php comments_template('', true); ?>
```

所以……
怪不得传说3.0的时候要换default了。