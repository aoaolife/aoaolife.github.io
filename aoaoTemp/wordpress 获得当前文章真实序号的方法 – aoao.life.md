---
title: "wordpress 获得当前文章真实序号的方法 – aoao.life"
date: 2024-03-07 21:43:15
---

想在主题里利用一下这个小功能。
那些抄来抄去的都包了浆的所谓办法都是在后续的ID上作文章，根本没有切中问题的本质。因为在wordpress的设计思想中，万物皆post，根本没把ID的增长当回事。想通过限制自动保持、自动版本、限制媒体什么的解决方案是缘木求鱼，根本不治本。
其实“取连续的文章序号”换个思路，就是取“截止当前发表时间，它的前面还有多少篇”这么一个简单问题。刚好wordpress的核心类WP_Query支持根据时间检索，而时间检索的参数里刚好有个’before’。一拍即合。
下面就是代码。注意：此代码要在loop内部使用。

```
get_real_post_id() {
if ( !is_single() ){
return;
}
global $post;
if ( 'publish' !== $post->post_status
&& 'private' !== $post->post_status) {
return;
}
$args = array(
'post_type' => 'post',
'post_status' => array('publish', 'private'),
'post_per_page' => -1,
'fields' => 'ids',
'date_query' => array(
'before' => $post->post_date,
),
);
$the_query = new WP_Query($args);
return $the_query->post_count;
}
```

简单解释一下：
因为要用到post的ID、post_status和post_date，所以直接用了loop循环中存在的全局变量$post。不用这个全局变量，改用get系列的函数也是一样的。
检索的post类型，我用的是publish和private。这个参是个数组，可以根据需要自行增减。
fields设成ids，意思是返回值接受id。这么写是因为有人说这样可以加快执行速度，并没有实际证据。

date_query是重头戏。
before可以接受的是date string。而无论你的时间格式设成什么样，$post->post_date都刚好是个标准的时间字符串，而且还精确到秒，所以直接放进去即可。
这里其实省略了一个默认参“column”=“post_date”，也就是给before参赋的值。可以选择的还有“post_date_gmt”，“post_modified”，“post_modified_gmt”。都是字面意思，有需要自己替换就行。
还有就是，before默认生成的运算符是小于等于，也就是取得的数包括了当前贴自身。如果要取得除自己以外的数量，自行减1，或者增加参数post__not_in均可达到目的。

对了还有，get_posts跟WP_Query本质上是一个东西，同样的参数，用get_posts调用，也能起到同样的效果。但是实际执行时，get_posts为了得到返回值，需要多执行一次qurey。而使用WP_Query的时候，直接取成员post_count即可，并不需要把post真的检索出来，相对来说效率更高。

此方案的优点是动态获取，删帖或者转换帖子类型，甚至无耻地修改发帖时间，都不会影响序号的连续性。
缺点就是进行了一次数据库操作，会耽误一丢丢时间。不过据说WP_Query默认操作的是缓存，影响应该没那么大。
以上。