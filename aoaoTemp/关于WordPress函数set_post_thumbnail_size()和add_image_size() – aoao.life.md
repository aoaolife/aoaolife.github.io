---
title: "关于WordPress函数set_post_thumbnail_size()和add_image_size() – aoao.life"
date: 2016-05-11 19:06:04
---

set_post_thumbnail_size()是add_image_size()的子集，他俩的作用都是定义一个上传图片的规格。set_post_thumbnail_size相当于默认指定缩略图的名称为“post-thumbnail”的图像规格。
也就是说

```
set_post_thumbnail_size( $width, $height, $crop );
```

等价于

```
add_image_size( 'post-thumbnail', $width, $height, $crop );
```

[via](https://pewae.com/gaan/aHR0cDovL3dvcmRwcmVzcy5zdGFja2V4Y2hhbmdlLmNvbS9xdWVzdGlvbnMvMTA4NTcyL3NldC1wb3N0LXRodW1ibmFpbC1zaXplLXZzLWFkZC1pbWFnZS1zaXpl)

那么，指定图像规格的意义是什么呢？
要知道，不进行特殊定制的话，WP的特色图链接的是内部媒体库里的图。当对媒体库的图片进行添加和修改的时候，WP会根据已经注册的文件规格自行创建若干个处理后的图片。如果注意观察uploads目录，你会看到一堆名为XXX-560×320.jpg、XXX-300×205.jpg、XXX-150×150.jpg的文件。这些就是WP根据规格列表自动生成的缩略图文件。WordPress默认已经支持了large（1024×1024）、medium_large（768×768）、medium（500×500）和thumb（150×150）四种规格。加上原文件是5个，如果再有post-thumbnail就是6个了。这么玩是完全不体谅空间受得了受不了啊！所以要我说，自己写主题要取缩略图的时候，直接用已经存在的四种规格里的一种就算了，跟服务器空间过不去就是跟钱过不去。
默认的四种规格的定义，可以在Settings->Media里进行修改。当原图规格不足某个级别的时候，这个级别的缩略图就不会生成。比如默认设置下上传一张图片“rora.png”是280×120，那么WP会另外多生成一张thumb规格的rora-150×150.png（thumb）出来，而不会生成mdeium和large级别的缩略图。
其实这四个默认的规格是可以采用一些手段屏蔽掉的。但不建议这么做。因为后台用到的地方很多，屏掉了属于花样作死，根据不同的浏览器能欣赏到不同的红叉。但在setting里都给改成150×150的小规格是种不错的办法。

一票取得缩略图、附件图和媒体图片的函数，都是靠着定义好的规格来取得或者显示图片的。还是以上面的图片做例子，

```
the_post_thumbnail( 'large' );
the_post_thumbnail( 'full' );
the_post_thumbnail();
```

三种调用方法，都会显示rora.png原图。其中第一种会因为找不到这个规格的文件而返回原图。

而

```
the_post_thumbnail( 'thumb' );
```

则是会显示rora-150×150.png。
这类函数有一大票。wp_get_attachment_image_src， wp_get_attachment_image， wp_get_attachment_link，the_post_thumbnail，get_the_post_thumbnail都可以根据不同的规格定义取不同的图片。

虽然WP已经有了三种定义，但毕竟是可以手动更改的。所以主题开发者们为了让图片符合自己的设计都喜欢增加一种或者多种规格供自己驱驰。那么问题来了，WP媒体库设计得比较蠢，它只在新文件上传或者旧文件编辑的时候才会生成剪裁后的文件。于是乎，旧主题生成的旧规格文件删除不了成了垃圾；新主题要用到的新规格找不到对应文件，就只能用原图。

因此安利两个插件。
thumbnail-cleaner（https://wordpress.org/plugins/thumbnail-cleaner）可以检索uploads目录，查找过期的缩略图。
regenerate-thumbnails（https://wordpress.org/plugins/regenerate-thumbnails/）能够重建缩略图。
建议经常换主题的朋友们尝试使用。