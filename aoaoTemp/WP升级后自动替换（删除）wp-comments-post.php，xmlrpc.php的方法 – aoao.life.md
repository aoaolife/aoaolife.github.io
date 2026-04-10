---
title: "WP升级后自动替换（删除）wp-comments-post.php，xmlrpc.php的方法 – aoao.life"
date: 2021-12-29 22:11:49
---

在升级4.7之前，把一直想做的一个功能实现了，跟大家分享一下。
这个功能就是，升级后自动替换或删除某些文件。这个功能很无聊，只是能节省一点儿连FTP拖拽文件的时间罢了。但要知道，对于程序员来说，能不动手就不动手才是王道。

一直以来我的替换对象是wp-comments-post.php，xmlrpc.php。
wp-comments-post.php可谓是spam之源，自动spam工具最喜欢找这个文件。wordpress官方虽然提供了好几个保护方案，但总是道高一尺魔高一丈，所以把它干掉才是最省心的。
但是，comment提交仍旧依赖该文件的主题，**【不要】**删除此文件。

xmlrpc.php提供了一票外部API，给第三方工具使用，~~@路易斯~~喜欢用的离线编辑工具，欧美WP玩家最喜欢的Jetpack工具，或者自动同步微博到博客的插件之类都依赖于这套API。而一旦WP内部权限管理出现问题，这个文件就是最可能的安全漏洞的入口。
所以，有外部工具连接wordpress需求的，**【不要】**删除此文件。

我之所以用替换而不是删除，是听说攻击者的工具找不到文件的消耗要大于能找到文件但文件内容为空的消耗。所以我采用wp_die()这种带偏方向的方法。
至于删除文件、留空或者wp_die()这三种方法哪个更好，我表示不知道，毕竟不专业。

如果想跟我一样用替换的办法，首先要在wordpress的根目录下建一个wp-sub目录，在里面放一个名为wp-go-die.php的文件。文件的内容如下：

```
<?php
wp_die();
```

然后在“合适的地方”增加下面的代码。要删除的用下面两句，替换的不用改。
WP_Filesystem_Base这个类提供了文件操作的函数，包括copy，move，delete，exist，mkdir，rmdir等等。
因为代码很简单，所以有别的需求的小伙伴可以自行修改代码，对付自己想对付的文件。
真正难的地方是如何找到合适的钩子。

```
add_action( 'upgrader_process_complete', 'my_remove_default_risk_files', 11, 2 );

function my_remove_default_risk_files( $upgrader_object, $options )
{
if( 'update' === $options['action'] && 'core' === $options['type'] )
{
global $wp_filesystem;
$wp_dir = trailingslashit($wp_filesystem->abspath());
$wp_filesystem->copy( $wp_dir.'wp-sub/wp-go-die.php', $wp_dir.'wp-comments-post.php', true );
$wp_filesystem->copy( $wp_dir.'wp-sub/wp-go-die.php', $wp_dir.'xmlrpc.php', true );
//$wp_filesystem->delete($wp_dir.'wp-comments-post.php');
//$wp_filesystem->delete($wp_dir.'xmlrpc.php');
}
}
```