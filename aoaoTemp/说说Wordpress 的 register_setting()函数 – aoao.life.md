---
title: "说说Wordpress 的 register_setting()函数 – aoao.life"
date: 2021-04-14 23:34:28
---

折腾控件的时候一般会在配置页面遇到register_setting()这个函数。它的作用是把一组option注册给WP系统，以便供get_option(), add_option(), update_option()等函数使用。
几乎所有的插件用到这个函数的时候只有两种用法：第一、第二个参传相同的字符串，第三个参传校验函数或者为空。因为读取、保存什么的都是用第二个参$option_name作为识别标志，所以给人感觉这个函数传这一个参就够了。那么第一和第三个参究竟是干嘛的呢？

```
function register_setting( $option_group, $option_name, $args = array() ) {
global $new_whitelist_options, $wp_registered_settings;

$defaults = array(
'type'              => 'string',
'group'             => $option_group,
'description'       => '',
'sanitize_callback' => null,
'show_in_rest'      => false,
);
//...
}
```

第一个参，名叫$option_group。
group和name一看就是俩词，所以第一感觉插件们不分青红皂白传两个相同的名进去是不对的。上官网查手册，果然说默认允许的group有general，discussion，reading，misc什么的——这不就是WP默认的Setting标题嘛！总不可能只支持默认吧。
只好翻看源代码。一经分析，原来这个group还**真·就·没·啥·大·用**。系统中有个$new_whitelist_options全局变量，在调用register_setting函数的时候会先去全局变量里判断一圈，有没有关键的key重复了，仅此而已。
那么这第一个参存在的意义是什么呢？
人家WordPress小组写个函数，又不是只给插件作者用的，人家自己也用。他们家自己写配置项的时候就是用这个函数注册的，内部那么多人，当然要对配置进行分组，然后检查有效性什么的了。所以插件作者注册自己的option的时候，就别跟着默认项添乱了。前两个参把两个相同的名字塞进来，一点儿错都没有！

第三个参，是个可选参，类型是数组。
那么传函数就用错了吗？不是的。传函数是旧接口。
看register_setting这个函数的版本历史。在4.7.0的时候，第三个参才变成了数组。而现在的函数实现的时候还保留了那么一小段，专门处理了传函数的情况。数组参中除了sanitize_callback是函数以外，其他几个成员根本就不是给本地Wordpress服务用的，而是为REST API提供的接口。写插件的时候基本用不上，所以也根本不用传。除非你的插件是专门给REST API用的。
sanitize_callback这根独苗倒是挺有用的。这个函数被认为用来处理注册的option项。像什么链接规范化啊，数值有效性检查啊，都可以放在这个函数里做。后台选项比较多的时候，还是应该把这个函数给实装上为好。

register_setting还有个兄弟，叫unregister_setting，作用就是干掉注册的settings呗。一般register_setting在admin_init的钩子里。但是admin_init并没有相反的退出的钩子，这下就尴尬了。我这抄插件也玩了三年五载的了，就没见过有人调用过register_setting这个函数的。理论上非要调的话恐怕应该用register_deactivation_hook在插件被反激活的时候。

下一个话题，这个sanitize_callback的回调函数又是什么时候调用呢？
add_option和update_option的时候。
add_option和update_option跟register_setting的关系就是，如果你注册了回调函数，我就去调用一下检查函数；没注册，照样不耽误我更新选项。毕竟register_setting是2.7才增加的函数，另外两个从1.0就有了。

结论就是，对于普通插件来说，如果register_setting不传第三个参的话，根本就不用调。