---
title: "Wordpress创建页面显示包含某些指定的tag的文章 – aoao.life"
date: 2019-08-06 15:38:04
---

[俍注兄](https://pewae.com/gaan/aHR0cHM6Ly9vbmVpbmYuY29tL3RvcGlj)昨天发邮件，让我帮他搞一个根据“关键字”自动输出的文章列表。
瞅了一下，他说的其实不是“关键字”，而是“tag”。

这东西一点儿也不难。我尽量解释的详细一点，这样就省得们再来问我了。
因为我一直用英文后台，所以并不知道一些关键字的中文名称是什么。所以会出现中英文混杂的情况，应该不会影响大家的理解吧。

开始。

## 1、做一个页面的模板。

这个从WP4.7开始就有了。有两种玩法。因为并不是重点，所以只说一种。把主题中的page.php复制一份，命名成page-{slug}.php，或者page-{id}.php。其中的slug或者id就是你要做成的新page的slug或者id，可以在编辑页面查到。
比如老俍的页面叫topic，那么就把这个页面做成page-topic.php
[关于页面的官方说明](https://pewae.com/gaan/aHR0cHM6Ly9kZXZlbG9wZXIud29yZHByZXNzLm9yZy90aGVtZXMvdGVtcGxhdGUtZmlsZXMtc2VjdGlvbi9wYWdlLXRlbXBsYXRlLWZpbGVzLw==)

## 2、删除原page中显示的内容。

跟页面布局有关的内容留着，对显示的内容适当修改。
比如我现在的主题里，page.php长酱婶：

```
<?php get_header(); ?>

<div class="wrap">
<div id="primary" class="content-area">
<main id="main" class="site-main" role="main">

<?php
while ( have_posts() ) : the_post();

get_template_part( 'template-parts/page/content', 'page' );

// If comments are open or we have at least one comment, load up the comment template.
if ( comments_open() || get_comments_number() ) :
comments_template();
endif;

endwhile; // End of the loop.
?>

</main><!-- #main -->
</div><!-- #primary -->
</div><!-- .wrap -->

<?php get_footer();
```

因为我的想法是在page里不放任何东西，所以要把代码里的"while"内容删除。

```
while ( have_posts() ) : the_post();

get_template_part( 'template-parts/page/content', 'page' );

// If comments are open or we have at least one comment, load up the comment template.
if ( comments_open() || get_comments_number() ) :
comments_template();
endif;

endwhile; // End of the loop.
```

如果老俍想把页面里的图片放到page内容里的话，就保留while...endwhile;里的部分内容。但我不建议这么做，而是在这个页面里单独写。
这时去后台新建或者编辑一个叫“topic”的page，打开的时候看见只有主题的header和footer，就说明前两步成功了。

## 3、实现根据tag找主题功能。

继续修改page-{slug}.php，或者page-{id}.php
先粘个主函数进去。注意放在php覆盖的范围里，不要放在外面。
最关键的步骤是用了个WP_Query函数。这个函数非常厉害，参数变化多端。想调整看[官方文档](https://pewae.com/gaan/aHR0cHM6Ly9kZXZlbG9wZXIud29yZHByZXNzLm9yZy9yZWZlcmVuY2UvY2xhc3Nlcy93cF9xdWVyeS8=)。
要注意的是用这个参之后一定要调用wp_reset_postdata，恢复默认的数据结果集。

```
function liang_query_by_tag($mytagID,$mytitle,$limits) {
$arg = array();
$arg['posts_per_page'] = $limits;
$arg['tag__in'] = array($mytagID);
$arg['order'] = 'DESC';
$query=new WP_Query($arg);

if ($query->have_posts()) {
$header2 = sprintf("<h2>%s</h2><ul>",$mytitle);//不一定是h2，不一定带ul，想要什么格式自己发挥，想分栏可以多传before、after之类的参数进来。
echo $header2;
}
while ( $query->have_posts() ) : $query->the_post();
the_title( '<li><a href="' . esc_url( get_permalink() ) . '" rel="bookmark">', '</a></li>' ); //格式自理
endwhile;
$more_link= sprintf('<li><a href="%1$s" rel="external nofollow" title="%2$s">[ 更多 ]</a></li>',get_tag_link($mytagID),$mytitle); //格式自理
echo $more_link;
echo "</ul>";//如果前面没有ul这里当然也不用关
wp_reset_postdata();//重要！！否则你的其余的循环就不好用
}
```

然后修改page里的正文内容，给出适当的参数。我的例子放了三组tag，可以任意添加。需要对不同的tag设不同格式的，可以多传个before after之类的东西进去。
另外category跟tag其实是一回事。写得差不多了才想起来有通用的写法。懒得改了。

```
<div class="wrap">
<div id="primary" class="content-area">
<main id="main" class="site-main" role="main">
<?php
$myshows = array(
array(
'tag_id' => 38,      //要显示的tagID.在后台能查到
'tag_title' => '写BUG', //显示的标题,随便写
'limits' => 5            //最多显示的条数
),
array(
'tag_id' => 39,
'tag_title' => '业余爱好',
'limits' => 5
),
array(
'tag_id' => 69,
'tag_title' => '不知所云',
'limits' => 20
),
);//所有要显示的tag信息
foreach ($myshows as $myshow){
liang_query_by_tag($myshow['tag_id'], $myshow['tag_title'], $myshow['limits']);
}
?>
</main><!-- #main -->
</div><!-- #primary -->
</div><!-- .wrap -->
```

最后做成php的代码。想直接用是不行的，起码tagid你得改一下……

```
<?php

get_header();

function liang_query_by_tag($mytagID,$mytitle,$limits) {
$arg = array();
$arg['posts_per_page'] = $limits;
$arg['tag__in'] = array($mytagID);
$arg['order'] = 'DESC';
$query=new WP_Query($arg);

if ($query->have_posts()) {
$header2 = sprintf("<h2>%s</h2><ul>",$mytitle);//不一定是h2，不一定带ul，想要什么格式自己发挥，想分栏可以多传before、after之类的参数进来。
echo $header2;
}
while ( $query->have_posts() ) : $query->the_post();
the_title( '<li><a href="' . esc_url( get_permalink() ) . '" rel="bookmark">', '</a></li>' ); //格式自理
endwhile;
$more_link= sprintf('<li><a href="%1$s" rel="external nofollow" title="%2$s">[ 更多 ]</a></li>',get_tag_link($mytagID),$mytitle); //格式自理
echo $more_link;
echo "</ul>";//如果前面没有ul这里当然也不用关
wp_reset_postdata();//重要！！否则你的其余的循环就不好用
}
?>

<div class="wrap">
<div id="primary" class="content-area">
<main id="main" class="site-main" role="main">
<?php
$myshows = array(
array(
'tag_id' => 38,      //要显示的tagID.在后台能查到
'tag_title' => '写BUG', //显示的标题,随便写
'limits' => 5            //最多显示的条数
),
array(
'tag_id' => 39,
'tag_title' => '业余爱好',
'limits' => 5
),
array(
'tag_id' => 69,
'tag_title' => '不知所云',
'limits' => 20
),
);//所有要显示的tag信息
foreach ($myshows as $myshow){
liang_query_by_tag($myshow['tag_id'], $myshow['tag_title'], $myshow['limits']);
}
?>
</main><!-- #main -->
</div><!-- #primary -->
</div><!-- .wrap -->

<?php get_footer();
```

## 4、再强调一次，一定要有一个跟你创建的page-xxx.php一样的，slug或者id是xxx的页面！