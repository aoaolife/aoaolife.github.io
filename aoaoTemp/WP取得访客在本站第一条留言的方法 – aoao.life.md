---
title: "WP取得访客在本站第一条留言的方法 – aoao.life"
date: 2020-08-21 13:51:34
---

之前

```
万戈
```

曾经提出要手动查找留言者在本站的最早留言的内容。作为一个Coder，我觉得他的方案虽然很有人情味，但是太不智能了。所以今天就简单写了个SQL文，包成了一个函数。可以直接放在functions.php里，然后在有comments循环的地方直接调用。效果见本站（很烂而且本人认为这个功能很蛋疼，所以演示在两周后关闭。）

```
<?php if (function_exists( 'get_first_comment' )){ get_first_comment (get_comment_author_email() ); } ?>
```

随便转载，随便自由发挥，反正不注明出处我也看不到。只是给不会写SQL的同学们打个样子而已。
因为功能实在太简单了，所以就懒得写说明了，有技术问题直接回复交流好了。

P.S:启用了中文工具箱的同学可以把函数放在中文工具箱里，然后把注释去掉，可以解决中文内容最后的半字符乱码问题。
函数具体代码：

```
function get_first_comment ($author_email = '')
{
global $wpdb;
$result = "<p>";
$got = false;
$author_email = "'".$author_email."'" ;
$q = "SELECT C.comment_ID, C.comment_author, P.post_title, P.guid , C.comment_date, C.comment_content FROM wp_comments C, zuosuo_posts P WHERE (C.comment_post_ID = P.ID) AND (P.post_status = 'publish') AND (C.comment_approved = '1') AND (C.comment_author != 'blogmaster') AND (C.comment_author != '') AND (C.comment_author_email = $author_email) ORDER BY C.comment_date ASC LIMIT 1" ;
$comments = $wpdb->get_results($q);
foreach ($comments as $comment) {
$got = true;
$content = substr($comment->comment_content,0,20);
//$content = utf8_trim($content).'...';
$comment_date = mysql2date('j.M.Y', $comment->comment_date);
$comment_author = '<b>'.$comment->comment_author.</b>;
$comment_url = $comment->guid.'#comment-'.$comment->comment_ID;
$result = $result.$comment_author.'最早于'.$comment_date.'在本站说过：<a href="'.$comment_url.'" rel="comment" title = "'.$content.'">'.$content.'</a>';
}
if ($got)
{
$result = $result.'</p>';
echo $result ;
}
}
```