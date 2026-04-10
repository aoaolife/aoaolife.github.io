---
title: "我使用的历史上的今天代码 – aoao.life"
date: 2021-08-12 18:26:33
---

侵权勿怪。
话说这东东实在是忘记了从哪个插件的代码里扒出来的，自己改良了一番。却没想到有人感兴趣。就简单说一说用法吧。
首先，把下面这个函数粘贴到function.php里

```
function history_today($post_year, $post_month,$post_day ){
global $wpdb;
//SQL语句里的项目可以随意改良,想要加什么效果请在主贴回复,@lifishake愿意为你服务
$sql = "select ID, year(post_date_gmt) as h_year, post_title, comment_count FROM
$wpdb->posts WHERE post_password = '' AND post_type = 'post' AND post_status = 'publish'
AND year(post_date_gmt)!='$post_year' AND month(post_date_gmt)='$post_month' AND day(post_date_gmt)='$post_day'
order by post_date_gmt";
$histtory_post = $wpdb->get_results($sql);
if( $histtory_post ){
foreach( $histtory_post as  $post ){
$h_year = $post->h_year;
$h_post_title = $post->post_title;
$h_permalink = get_permalink( $post->ID );
//注意下边,输出的格式可以自行调整,不愿意加年的把$h_year去掉即可
$h_post .= "<li>$h_year:&nbsp;&nbsp;$h_post_title</li>";
}
}
$content='';
if ( $h_post ){
$content = $content.$h_post;
}
echo $content;
return $content;
}
```

对于这个函数，我在现在的主题中两处用到了它。
第一个是用在calendar的下方。

```
<li><?php get_calendar(); ?></li>
<?php $post_year = date('Y'); $post_month = date('m');	$post_day = date('j');
history_today($post_year, $post_month, $post_day); ?>
```

其实这个用法是假的，跟calendar一点儿关系都没有，即使点击calendar进了archive里，显示的也还是历史上的“今天”，因为date()取出来的就是今天。我只不过是觉得把“历史上的今天”放在那个位置比较合适而已。
至于“历史上的帖子发出的那一天”，用法是这样的：
如果在single里直接调用，那么照下边的样式粘贴：

```
<?php
echo '<h3>历史上的今天:</h3>' ;
$post_year = get_the_time('Y');
$post_month = get_the_time('m');
$post_day = get_the_time('j');
history_today($post_year, $post_month, $post_day);
?>
```

如果是在~~single~~sidebar里，则要多加一个是否是single的判断条件：

```
<?php if ( is_single() ){
echo '<h3>历史上的今天:</h3>' ;
$post_year = get_the_time('Y');
$post_month = get_the_time('m');
$post_day = get_the_time('j');
history_today($post_year, $post_month, $post_day);}
?>
```

**备注:**
此代码实现的其实是“历史上不是这一年的月日相同的这一天”。如果真要实现的话，把第一段代码中的

```
year(post_date_gmt) != '$post_year'
```

改成

```
year(post_date_gmt) < '$post_year'
```

即可。

**Q&A:**
留着答疑。