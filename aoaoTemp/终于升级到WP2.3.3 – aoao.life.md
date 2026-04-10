---
title: "终于升级到WP2.3.3 – aoao.life"
date: 2022-02-15 23:33:35
---

终于决定升级到2.3了.主要是因为

```
美味书签
```

的自动发布问题.
其实只要替换一下xmlrpc文件就可以,但是毕竟2.0用了两年了,好多插件都只能看不能动.正好一起了.

升级前先在本地简单模拟了一下,遇到了几个问题.但都还好解决.

**1.升级后Categories(分类)会出现乱码.**
这可能是因为升级数据库的脚本有问题导致的.解决的方法也很简单,修改wp-config.php文件,增加如下内容

```
define('DB_CHARSET', 'utf8');
define('DB_COLLATE', 'utf8_general_ci');
```

即可

**2.升级后插件UTW和ELA均失效**
其实ELA并没有失效.但是它有一项是基于UTW的tag的.所以干脆把这两个都停掉.基于WP本身的tag用法可以参考

```
这里
```

在single.php和index.php中,关于单独文章相关的tag,都是换成了

```
the_tags();
```

~~至于相关帖子,由于没有找到UTW_ShowRelatedPostsForCurrentPost 的合适替代者,暂时搁置.~~
相关帖子UTW_ShowRelatedPostForCurrentPost也找到了合适的替代者.
~~Wasabi’s Related Posts（http://easyprxies.info/index.php?hl=f5&q=uggc%3A%2F%2Fjnfnov.cojvxv.pbz%2FEryngrq%2520Ragevrf）~~结合~~水煮鱼的WP23_Related_Posts（http://fairyfish.net/2007/09/12/wordpress-23-related-posts-plugin/）~~
因为老外的那个插件不支持中文,而水煮鱼的又不能自定义格式.所以就两者结合了一下.有感兴趣的朋友的话我也可以放出来.

**3.tag导入.**
其实相当简单,在manage–import里一点一点按照操作进行就可以了.但是一定要停掉UTW先!

**4.Page-Navi更新**
因为2.0的和2.3的根本就相当于两个插件了.只是更新以后要有自己的css了,还没来得及改.