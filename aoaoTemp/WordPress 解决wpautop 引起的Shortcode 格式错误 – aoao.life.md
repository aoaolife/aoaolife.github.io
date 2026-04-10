---
title: "WordPress 解决wpautop 引起的Shortcode 格式错误 – aoao.life"
date: 2020-03-18 17:34:33
---

先声明，本人升到5.0以后觉得古腾堡太恶心，又给降回4.x了，所以下面的方法只适用于WordPress4.x版本。

为了操作方便，我自己的魔改版插件使用了好几个自定义的ShortCode。比如我的插入豆瓣资料的短代码。
但是一直有显示上的瑕疵没有解决。加入的div跟后面的文字之间一直有格式问题。
之前以为是css没学好，直到今天跟踪调试，才意外发现了真正的原因。

WordPress的默认the_content 的Filter 列表里，有一个“wpautop”。这个函数用于优化文章内容。尤其对于我这种使用后台文本编辑器的，它会在每行文字的前后加上<p>标签，并且把换行变成html的<br />。因为是默认的添加，所以优先级是10。

跟踪一下数据的变化。帖子里的原始数据是这样的：

```
[关键字 id="4301043" type="movie" score="6" alt="传染病" ]
应景看一下，没有太多感觉，片子的质量一般。
喜欢凯特温斯莱特片中的造型。
结局失败。
```

先调用优先度为10的wpautop，内容变成酱婶：

```
<p>
[关键字 id="4301043" type="movie" score="6" alt="传染病"]
应景看一下，没有太多感觉，片子的质量一般。<br />
喜欢凯特温斯莱特片中的造型。<br />
结局失败。</p>
```

可以看出，两端增加了<p>和</p>，中间每一行都增加了回车。

然后在优先度11的时候，调用我的代码，调完后内容如下：

```
<p><div class="apip-item"><div class="mod  "><div class="v-overflowHidden doulist-subject"><div class="apiplist-post"><img src="https://pewae.com/wp-content/gallery/douban_cache/4301043.jpg"></div><div class="apiplist-score apip-score-minus">-1</div><div class="title"><a href="https://movie.douban.com/subject/4301043/" class="cute" target="_blank" rel="external nofollow">传染病</a></div><div class="rating"><span class="allstardark"><span class="allstarlack" style="width:70%"></span><span class="allstarlight" style="width:60%"></span></span><span class="rating_nums">(7-1) </span></div><div class="abstract">导演 :史蒂文·索德伯格<br >演员: 玛丽昂·歌迪亚/马特·达蒙/劳伦斯·菲什伯恩/裘德·洛<br >类型: 剧情/科幻/惊悚<br >国家/地区: 美国/阿联酋<br/>年份: 2011</div></div></div></div><br />
应景看一下，没有太多感觉，片子的质量一般。<br />
喜欢凯特温斯莱特片中的造型。<br />
结局失败。</p>
```

从第一个p标签到第一个换行标签里包含的内容是我函数的返回值。也就是方括号的部分被替换掉了，方括号以外的内容，shortcode函数是处理不了的。

捣乱的就是wpautop加上的头尾的p标签。
要知道，<p> 和</p>之间出现div是绝对错误的。这样的source code绝对经不起任何工具的验证。这也是导致显示格式出现问题的真正原因。Chrome解析的时候，把div前后的各半拉p都补全，成了前后各一组；而FF则舍弃了前面的，在div后面补了两组。

找到了原因，解决的方法就简单了，只要让wpautop在shortcode之后执行就行了。先移除，再加回来即可。这种方案一搜索到处都是[via](https://pewae.com/gaan/aHR0cHM6Ly9ibmtzLnh5ei9yZXNvbHZpbmctd3BhdXRvcC1hbmQtc2hvcnRjb2Rlcy8=)
因为shortcode的优先级是11，所以第三个参数设成12。有人建议这里改成99，我是不同意的。因为对the_content下手的钩子实在太多了，随意把wpautop放得太靠后，说不定会引起其他问题。

```
remove_filter('the_content','wpautop');
add_filter('the_content','wpautop',12);
```

这就是终极解决方案吗？在看了源代码之后，我产生了疑问。因为在4.x之前，shortcode的优先度是9，恰好在wpautop这个古老的filter之前。那么任何一个有脑子的程序员都不会在4.2版本贸然把shortcode的实现优先度调成11而不提供解决方案。
再仔细看代码，有了。原来还有一个shortcode_unautop函数是给wpautop擦屁股的，专门把误加的p和br再给改回去。很遗憾这个函数写得有瑕疵，正则表达式只能hold住

```
[关键字]
内容
[/关键字]
```

这一种情况。
其余

```
①[关键字]
②[关键字]内容[/关键字]
③[关键字 /]
④[关键字]
[/关键字]
```

这些个情况，统统处理不了。而官方的例子里都没写自定义的短代码必须要关掉，这四种写法其实都对。简而言之，屁股没擦干净。

还是那句话，the_content上的钩子太多，改动越小越好。于是终极方案（[via](https://pewae.com/gaan/aHR0cHM6Ly9naXN0LmdpdGh1Yi5jb20vam9leXovOTYzYmNkZDEyZTg0YTFmMzM1MmQ=)）出炉，原理是只要把没擦干净的屁股再擦一遍就好。

```
if( !function_exists('wpex_fix_shortcodes') ) {
function wpex_fix_shortcodes($content){
$array = array (
'[' => '[',
']' => ']',
']' => ']'
);
$content = strtr($content, $array);
return $content;
}
add_filter('the_content', 'wpex_fix_shortcodes');
}
```

这个函数使用默认优先级10，而且肯定会加在wpautop与shortcode_unautop的后面。完美！
其实该函数在我偷主题和插件代码的时候见过很多次，我一直不知它是干嘛用的……