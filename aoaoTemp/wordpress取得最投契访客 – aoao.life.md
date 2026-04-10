---
title: "wordpress取得最投契访客 – aoao.life"
date: 2026-02-24 12:06:08
---

因为“搬砖阶段”装得实在太辛苦，索性给自己的blog写个无聊的功能。

本人一直致力于减少无意义的留言，所以想到了一个“把跟我聊得最开心的人当作友链”的主意。这个主意的亮点在于不是你留言的字数多就能上榜，而是我愿意跟你多聊，你才能上榜。不仅能促进有意义的回复，而且省去了维护友链的麻烦。
下面看代码。
其实代码的核心是一段SQL语句。我把它封进第一个函数里。其意义是取得*半年之内*我回复的字数累计最高的*13个人*的姓名、邮箱和链接。

```
function apip_get_links()
{
global $wpdb;
$limit = 13; //取多少条，可以自己改
$scope = "6 MONTH"; //可以使用的时间关键字:SECOND,MINUTE,HOUR,DAY,WEEK,MONTH,QUARTER,YEAR...
$sql = "SELECT comment_author_email, comment_author_url, comment_author, SUM(comment_length) as words_sum
FROM $wpdb->comments aa
INNER JOIN
(
SELECT comment_parent, char_length(comment_content) as comment_length
FROM $wpdb->comments
WHERE  user_id <> 0
AND DATE_SUB( CURDATE( ) , INTERVAL $scope ) <= comment_date_gmt
)
AS bb
WHERE aa.comment_ID = bb.comment_parent
GROUP BY comment_author_email
ORDER BY words_sum DESC
LIMIT $limit";
$result = $wpdb->get_results($sql);
return $result;
}
```

第二个函数，用来输出链接。这么写只是为了把显示逻辑跟数据源分开。如果想手动添加到某个php里，调用这个函数就够了。css请自理。

```
function apip_link_page(){
$links = apip_get_links();
$ret = '<ul class = "apip-links">' ;
foreach ( $links as $link ){
$parm = sprintf( '<li><div class="commenter-link vcard">%1$s</div><a href="%2$s" target="_blank" class="url">%3$s</a></li>',
get_avatar( $link->comment_author_email, 32),
$link->comment_author_url,
$link->comment_author) ;
$ret.= $parm;
}
$ret.='</ul>';
echo $ret;
}
```

第三步，添加short_code，以便在页面里直接调用。

```
add_shortcode('mylink', 'apip_link_page');
```

新建一个页面，在里面加上短代码（换成半角方括号）
【mylink】
即可。

P.S 我的排行榜还真是毫无意外发生啊！