---
title: "WordPress实现在归档范围内查找相邻文章 – aoao.life"
date: 2019-11-12 09:38:48
---

多年前，贝总曾经问过我，能不能增加一个“上一篇”、“下一篇”在某某类别里跳转的功能。

狭义上说，get_previous_post()/get_next_post()/get_post_navagation()这三个函数都有“in_same_term”，“excluded_terms”，“taxonomy”这三个参数。配合使用，可以实现在相同类别和标签范围内跳转的功能。
但是，这几个函数使用起来非常死板，意味着某个类别或者标签的文章，相邻文章就只能在该种别内部迭代，永远跳不出圈外。
而且，这几个默认函数对搜索结果，日期归档的结果也毫无办法。

所谓“归档范围内查找相邻文章”是这样的：
当读者点击过某种类别的归档或者搜索关键字，取得过文章列表后，点击任意文章标题后，获取的相邻文章均在之前的文章列表范围之内。
直到读者点击不属于这种类别的文章链接或者文章集合链接后，退出之前的特殊范围，回归时间顺序的相邻文章。
这种特定的类别集合，可以是年/月/日/作者的归档，可以是某个类别或者标签，也可以是搜索结果。
比如点击“2010年12月”，进入一个20篇文章的归档页面。从这个页面上点击任何一篇文章开始阅读。那么从此开始的“上一篇”“下一篇”将始终限定在这20篇文章的范围内。直到点击主页或者直接跳到随机文章后，再不限定在20篇文章的范围内。

之前其实已经搞过一个方案，通过cookie识别不同读者，然后通过向数据库写入临时数据的方式记录结果集。这么做是因为WordPress并不支持Session，页面跟页面之间只能通过数据库进行数据传递，所以效果非常不理想，一直没公布。
直到前几天，忽然想通了，WordPress虽然不支持Session，但PHP支持啊……
于是问题迎刃而解。核心思路是在用户的浏览过程中，记录临时变量。

下面是具体代码：

## 第一步：开启SESSION

```
function demo_register_session()
{
if( !session_id() )
{
session_start();
}
}

add_action('init', 'demo_register_session');
```

## 第二步：在进入归档类页面时记录文章集，超出前回结果范围时清除记录

```
function demo_keep_query(){
global $wp_query;

if (isset($_SESSION['last_tax'])) {
$old_tax = $_SESSION['last_tax'];//上一次的记录结果
}
else {
$old_tax = '';
}
$new_tax='';
if (is_search()||is_archive()) {
if ( is_search() ){
$new_tax = "搜索结果:" . get_search_query( false ) ;
}
else if ( is_category() ){
$new_tax = "分类:" . single_cat_title( '', false );
}
else if ( is_tag() ){
$new_tax = "标签:" . single_tag_title( '', false );
}
else if ( is_year() ) {
$new_tax = "年:" . get_the_date('Y') ;
}
else if ( is_month() ) {
$new_tax = "月:" . get_the_date('F Y');
}
else if ( is_day() ) {
$new_tax = "日:" . get_the_date(get_option('date_format'));
}
else {
//其它归档类型不处理且清空之前的数据。
//应该是剩下一个is_author()。这个类型对于只有一个作者的博客没意义，多人博客可以仿照上面的格式添加。
$_SESSION['last_tax'] = '';
$_SESSION['tax_ids'] = array();
return;
}
if ($new_tax != $old_tax) {
//新结果集与上一次不一致
$vars = $wp_query->query_vars;
$myquery = new WP_Query( $vars );
$vars['order'] = "ASC";//所有archive类的默认排序都是时间降序的，不更改的话会导致“上一篇”“下一篇”正好相反
$vars['posts_per_page'] = 9999;//官方文档说可以设-1，实际测试设-1会出错，还是设成正的吧。改变这个值，让所有结果出现在一页里。
if ($myquery->post_count == 1 && $myquery->max_num_pages == 1){
wp_reset_postdata();//如果只有一条则没必要存
$_SESSION['last_tax'] = '';
$_SESSION['tax_ids'] = array();
return;
}
//保存临时数据
$_SESSION['last_tax'] = $new_tax;
$_SESSION['tax_ids'] = wp_list_pluck( $myquery->posts, 'ID' );//存结果的ID
wp_reset_postdata();//恢复默认循环体
}
}
else if (!is_single()) {
//is_attach()之类的，清空
$_SESSION['last_tax'] = '';
$_SESSION['tax_ids'] = array();
}
else {
//single
$ID = get_the_ID();
if (empty($old_tax)||!isset($_SESSION['tax_ids'])||count($_SESSION['tax_ids']) == 0) {
//上一次没有记录，说明在主循环内，什么都不做。
return;
}
if (FALSE===array_search($ID, $_SESSION['tax_ids'])) {
//有记录，但是当前post不在其范围内，应该跳出结果。
$_SESSION['last_tax'] = '';
$_SESSION['tax_ids'] = array();
return;
}
}
}
add_action('template_redirect', 'demo_keep_query', 9 );//优先度略高于默认钩子,避免意外
```

## 第三步：增加取文章的函数。

get_previous_post()/get_next_post()/get_post_navagation()这三个函数允许加钩子的时机非常不合适，不如重写。
三个函数不用全部写，针对自己的主题，用哪个写哪个。

```
function demo_get_prev_post() {
if (isset($_SESSION['last_tax'])&& isset($_SESSION['tax_ids']) && count($_SESSION['tax_ids'])>1) {
$ID = get_the_ID();
$pos = array_search($ID, $_SESSION['tax_ids']);//找当前post_ID在结果中的位置
if ( FALSE === $pos ) {
return NULL;
}
$count = count($_SESSION['tax_ids']);
if ( $pos > 0) {
return get_post($_SESSION['tax_ids'][$pos -1]);//取前一篇
}
else {
return NULL;
}
}
else{
return get_previous_post();
}
}

function demo_get_next_post() {
if (isset($_SESSION['last_tax'])&& isset($_SESSION['tax_ids'])&& count($_SESSION['tax_ids'])>1) {
$ID = get_the_ID();
$pos = array_search($ID, $_SESSION['tax_ids']);//找当前post_ID在结果中的位置
if ( FALSE === $pos ) {
return NULL;
}
$count = count($_SESSION['tax_ids']);
if ( $pos < $count - 1) {
return get_post($_SESSION['tax_ids'][$pos +1]);//取后一篇
}
else {
return NULL;
}
}
else{
return get_next_post();
}
}

function demo_get_post_navagation($args=array()){
$args = wp_parse_args( $args, array(
'prev_text'          => '%title',
'next_text'          => '%title',
'screen_reader_text' => '文章导航',
) );
/*
'in_same_term'       => false,
'excluded_terms'     => '',
'taxonomy'           => 'category',
这三个参数被忽略。
*/

if ( !is_single() ){
return;
}

$ID = get_the_ID();
if (isset($_SESSION['last_tax'])&& isset($_SESSION['tax_ids'])&& count($_SESSION['tax_ids'])>1) {
$pos = array_search($ID, $_SESSION['tax_ids']);
if ( FALSE === $pos ) {
the_post_navigation($args);
return;
}
$count = count($_SESSION['tax_ids']);
$next_id = 0;
$previous_id = 0;
$previous="";
$next="";
if ( $pos < $count - 1) {
$next_id = $_SESSION['tax_ids'][$pos +1];
}
if ($pos > 0 ) {
$previous_id = $_SESSION['tax_ids'][$pos -1];
}
if ($previous_id > 0)
{
$previous = str_replace( '%title', get_the_title( $previous_id ), $args['prev_text'] );
$previous = '<a href="'.get_permalink( $previous_id).'" rel="prev">'.$previous.'</a>';
$previous = '<div class="nav-previous">'.$previous.'</div>';
}
if ($next_id > 0)
{
$next = str_replace( '%title', get_the_title( $next_id ), $args['next_text'] );
$next = '<a href="'.get_permalink( $next_id ).'" rel="next">'.$next.'</a>';
$next = '<div class="nav-next">'.$next.'</div>';
}
if ( "" === $desc = $_SESSION['last_tax'] )
{
$desc = $args['screen_reader_text'];
}
$navigation = _navigation_markup( $previous . $next, 'post-navigation', $desc );
echo $navigation;
}
else{
the_post_navigation($args);
return;
}
}
```

## 第四步:修改主题

用demo_XXXX替换single.php导航部分原有的函数即可。代码略。

==== UPDATE 2019/11/12 ====
代码更新，修正了“上一篇”“下一篇”顺序正好相反的问题。