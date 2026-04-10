---
title: "使用google-code-prettify实现代码高亮 – aoao.life"
date: 2021-04-20 22:24:43
---

首先感谢坏猫的方法。
因为我这两天其实一直就在筹划干掉玻璃泉的wp-code-highlight插件，今天看到坏猫的办法之后，正好两厢参照，作出了自己的方案。

首先，说说为什么要干掉wp-code-highlight。因为一直在谋划心目中的完美主题，其中一个先期工作就是要让所有css和js可控。而很不幸wp-code-highlight的js和css不是按照wp的正统方式追加的，也就是说，我要么使用这个插件，要么不用，但无法做到启用后限定js的作用范围。

因为坏猫那边说得已经很详细了，所以我这里的侧重点是如何分页面控制加载js。
我这里的习惯是把这种可以与主题分开的控制项目，单独做成一个插件，这样即使换了主题，代码也可以生效。如果想要在自己的主题里实现，尽管加到functions.php里好了，具体的不同参照注释。能自己改代码的应该都能看懂……

第一步，追加触发动作

```
add_action('plugins_loaded', 'apip_init');
//add_action( 'after_setup_theme', 'apip_init' ); /*如果是主题,用这句*/
function apip_init()
{
add_action('get_header','apip_header_actions') ;
add_action('get_footer','apip_footer_actions') ;

add_action('admin_print_footer_scripts','apip_quicktags');
}
```

第二步，在header动作里追加对于文章内容的过滤项。加上这个，就不用修改既存的《pre》标签了。

```
function apip_header_actions()
{
if ( in_category('code_share') )
/*定义一个categroy，只有这个类别的才加载css，可以提高一丢丢速度。或者换成in_tag然后追加一个tag也可*/
{
add_filter('the_content', 'apip_code_highlight') ;
}
}

//下面这个函数要感谢玻璃泉。不加的话双引号会引起内容错乱。
function wch_stripslashes($code){
$code=str_replace('\"', '"',$code);
$code=htmlspecialchars($code,ENT_QUOTES);
return $code;
}

//如果想要行号，在prettyprint 后面加上一个 linenums
function apip_code_highlight($content) {
return preg_replace("/<pre(.*?)>(.*?)<\/pre>/ise",
"'<pre class=" prettyprint ">'.wch_stripslashes('$2').'</ pre>'", $content);
}
```

第三步，在footer里加css和js。一般来说css和js要在footer里加。但因为已经对类别进行了限制，所以跟第二步的写到一起其实也影响不大。

```
function apip_footer_actions()
{
if ( in_category('code_share') )
{
?>
<script type="text/javascript">
window.onload = function(){prettyPrint();};
</script>
<?php
//如果是主题,下面两个函数换成template_dir_url( __FILE__ )
wp_enqueue_script('prettify_js', plugin_dir_url( __FILE__ ) . 'js/prettify.js', array('jquery'), null, true);
wp_enqueue_style( 'prettify_style', plugin_dir_url( __FILE__ ) . 'css/prettify.css' );
}
}
```

第四步，追加编辑画面的标签

```
function apip_quicktags()
{
?>
<script type="text/javascript" charset="utf-8">
QTags.addButton( 'eg_pre', 'pre', '<pre>\n', '\n</ pre>\n', 'p' );
</script>
<?php
}
```

[js和css的下载地址](https://pewae.com/gaan/aHR0cDovL2NvZGUuZ29vZ2xlLmNvbS9wL2dvb2dsZS1jb2RlLXByZXR0aWZ5L2Rvd25sb2Fkcy9saXN0)，自备梯子。

===== Update.2019.8.7 =====
因为php7不支持preg_replace第一个参数的/e选项，所以第二步的第三段代码要作如下修改：

```
function apip_code_highlight($content) {
$result = preg_replace_callback('/<pre(.*?)>(.*?)<\/pre>/is', function ($matches) {
return '<pre class=" prettyprint ">' . wch_stripslashes($matches[2]) . '</ pre >'; } , $content);
return $result ;
}
```