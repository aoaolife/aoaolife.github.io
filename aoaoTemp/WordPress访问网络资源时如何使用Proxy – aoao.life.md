---
title: "WordPress访问网络资源时如何使用Proxy – aoao.life"
date: 2020-03-27 07:39:52
---

几天前在[@梓喵出没](https://pewae.com/gaan/aHR0cHM6Ly93d3cuYXppbWlhby5jb20vNTk0Ny5odG1s)那里获悉WordPress有一套自己的HTTP命令API的时候，瞥到了一丝改进本地调试环境的曙光。心里就像种了草，这些天一番捣鼓，终于被我搞通了几个函数的前世今生。
虽然梓猫出没那里后面一篇也是说这套API的，但他的侧重点跟我这篇的侧重点毫无关联。

为啥我要研究WordPress怎么使用代理呢？这跟我的调试环境有关。本人一般在公司的xampp下调试WordPress插件和主题。这不是重点，重点是我们公司的网络访问是有白名单的，大多数网址都被公司的小墙拦下了。于是很多插件的网络功能没法调。如果能设代理当然就海阔凭鱼跃了不是？

**第一个问题，WordPress如何设置代理？**

很简单，我在十几年前就知道了。添加或修改wp-config.php文件。

```
define('WP_PROXY_HOST', '127.0.0.1');   //代理IP或host名
define('WP_PROXY_PORT', '25378');       //代理端口号
define('WP_PROXY_USERNAME', '');        //必要时加
define('WP_PROXY_PASSWORD', '');        //必要时加
```

几个字段一目了然，知道代理是什么的自然知道它们是什么，不解释。

**第二个问题，WordPress如何使用默认代理？**

答案是，使用wp_remote_request()系列API，WordPress会自动使用配置好的代理。
这组WordPress的API，包括wp_remote_request()，wp_remote_post()，wp_remote_get()，wp_remote_head ()等。详情见[已被429的官网](https://pewae.com/gaan/aHR0cHM6Ly9kZXZlbG9wZXIud29yZHByZXNzLm9yZy9yZWZlcmVuY2UvZnVuY3Rpb25zL3dwX3JlbW90ZV9yZXF1ZXN0Lw==)。
正常使用最多的就是wp_remote_post()和wp_remote_get()了。参数太多，需要改的却不多。举两个常用例子说明一下：
例1 调用API。

```
$url = "https://free-api.heweather.com/s6/weather/now?key=".HE_WEATHER_TOKEN."&location=CN101121501";
$args = array(
'sslverify' => false,
'headers' => array(
'Content-Type' => 'application/json;charset=UTF-8',
'Accept' => 'application/json',
),);
$response = wp_remote_get($url,$args);

if ( is_wp_error($response) ) {
return;
}
else {
$cache = json_decode(wp_remote_retrieve_body($response),true);
}
```

上面这段代码是我所使用的“和天气”API获取实时天气的代码。其中，header里追加了json和编码，一般含中文内容的需要加编码的参，而json的参其实可加可不加。
有的API要求在header里加特殊参数以用来“对暗号”，照例追加便是。
返回值，WP自带了一个is_wp_error()函数，特好用，就不用自己费劲判断一堆数组套数组了。
返回的内容用wp_remote_retrieve_body()函数的好处同样是不用判断一堆套娃数组。

例2 将图片保存到服务器

```
preg_match('/avatar\/([a-z0-9]+)\?s=(\d+)/',$source,$tmp);
$local = PLUGIN_DIR.'/wp-content/gallery/gravatar_cache/'.$tmp[1];
$default =  home_url('/','https').'wp-content/gallery/gravatar_cache/default.png';
$dest = home_url('/','https').'wp-content/gallery/gravatar_cache/'.$tmp[1];
$url = 'http://www.gravatar.com/avatar/'.$tmp[1].'?s=64&d='.$default.'&r=G';
$response = wp_remote_get(
htmlspecialchars_decode($url),
array(
'timeout'  => 300,
'stream'   => true,
'filename' => $local
)
);
if (is_wp_error($response)) {
return '<img alt="" src="'.$default.'" class="avatar avatar-'.$tmp[2].'" width="'.$tmp[2].'" height="'.$tmp[2].'" />';
}
return '<img alt="" src="'.$dest.'" class="avatar avatar-'.$tmp[2].'" width="'.$tmp[2].'" height="'.$tmp[2].'" />';
```

参数要注意两点，一个是stream=true，另一个filename是本地文件名。

**第三个问题，要是不用WordPress函数，却想使用WordPress的Proxy，该怎么做？**

简单。php一定有办法。改变函数的上下文即可。
还是一个取文件的例子：

```
$cxContext = stream_context_create();
$proxy = new WP_HTTP_Proxy();
if ($proxy->is_enabled()) {
$proxy_str = $proxy->host().":".$proxy->port();
$stream_default_opts = array(
'http'=>array(
'proxy'=>$proxy_str,
'request_fulluri' => true,
),
'ssl' => array(
'verify_peer' => false,
'verify_peer_name' => false,
'allow_self_signed' => true
), );
$cxContext = stream_context_create($stream_default_opts);
}
file_put_contents("./temp", file_get_contents($filename,false, $cxContext));
```

WP里提供了一个使用Proxy的类,名叫WP_HTTP_Proxy。很遗憾这个类没提供静态方法，所以只能声明实例后再调用。其实直接使用WP_PROXY_HOST和WP_PROXY_PORT也没有任何问题。
ssl那个参数跟目的地有关，不加有的服务器会报SSL错误。
如果Proxy需要用户名和密码的话，则要麻烦一点，用户名和密码要加到参数的header部分里。

```
$auth = base64_encode(WP_PROXY_USERNAME.":".WP_PROXY_PASSWORD);
$stream_default_opts = array(
'http'=>array(
'proxy'=>WP_PROXY_HOST.":".WP_PROXY_PORT,
'request_fulluri' => true,
),
'header' => "Proxy-Authorization: Basic $auth",
);
```

好了，这组对于大多数人没什么卵用的方法就介绍到这里。我想除了我这种本地调试环境有特殊上网需求的，恐怕没什么人会在服务器端再配个代理服务器吧。
说不定可以用来解决429问题？本人表示服务器在境外，从没遭遇过429，科科。