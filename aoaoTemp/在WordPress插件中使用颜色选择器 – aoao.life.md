---
title: "在WordPress插件中使用颜色选择器 – aoao.life"
date: 2017-06-23 14:56:38
---

从WP3.5开始，后台就默认支持了颜色选择器（color-picker.js）。因为主题有封装好的类可以用，所以这里给出在插件中的调用方法。
WP默认的用的是[Iris](https://automattic.github.io/Iris/)家的，只支持RGB。有需要RGBA的请用关键字自行搜索。

1.在插件初始化的地方加入指定元素的响应程序

```
function color_picker_assets() {
wp_enqueue_style( 'wp-color-picker' );
wp_enqueue_script( 'my-color-picker-handle', plugins_url('my-plugin.js', __FILE__ ), array( 'wp-color-picker' ), false, true );
}
add_action( 'admin_enqueue_scripts', 'color_picker_assets' );
```

因为是插件后台用，所以只要在admin的时候加载就好了。

2.js中增加处理函数

```
(function ($) {
$(function () {
$('#mail-border-color').wpColorPicker();
});
}(jQuery));
```

关键的元素标志，用id或者class都可以。多次使用的时候还是id好一点

3.在插件的option页里增加插件调用。

```
<input type= 'text' name='myplugin_settings[mail_border_color]' id='mail-border-color'  value='<?php if ( isset( $options['mail_border_color'] ) ) echo $options['mail_border_color']; else echo "#FFC000"; ?>' />
```

因为用name跟options产生了关联，所以更新的时候就自动保存了，非常方便。

所谓会了不难，难了不会。就这么简单。