---
title: "WordPress从某网站不问自取的方法 – aoao.life"
date: 2020-09-11 17:13:06
---

捣鼓了一个函数，可以从某网站自动获取想要的情报。
跟WordPress关系不太大，主要就是在php里写了一堆我不擅长的正则。
例子里取的内容是电影的。音乐和读书的类似，自己追加正则就是了。没有的项目也自己增加正则就好了。抓取不是目的，目的是提供一个思路。
**注意：本文写于2020年9月11日，正则表达式配合的是当天的某网站的格式，不保证以后也可以用！**

```
function wp_fetch_from_douban($url) {
$response = @wp_remote_get(
htmlspecialchars_decode($url),
array(
'timeout'  => 1000,
)
);
if ( is_wp_error( $response ) || !is_array($response) )
{
return array();
}
preg_match_all('/(<div id="mainpic"[\s\S]+?<\/div>)|(<div id="info"[\s\S]+?<\/div>)|(<strong .+? property="v:average">.+?(<\/strong>|>))/',wp_remote_retrieve_body($response),$matches);
if (is_array($matches) && is_array($matches[0]) && count($matches[0])>=3) {
$mainpic_div_str = $matches[0][0];
$info_div_str = $matches[0][1];
$score_str = $matches[0][2];

//图
preg_match('/(?<=img src=").*?(?=")/',$mainpic_div_str,$match_imgs);
if (is_array($match_imgs)) {
$ret['pic'] = $match_imgs[0];
}

//分
preg_match('/(?<= property="v:average"\>).*?(?=\<)/',$score_str, $match_score);
if (is_array($match_score)) {
$ret['average_score'] = $match_score[0];
}

$info_grep_keys = array(
array('pattern'=>'/(?<="v:directedBy"\>).*?(?=\<)/', 'item'=>'director(s)'),
array('pattern'=>'/(?<="v:starring"\>).*?(?=\<)/', 'item'=>'actor(s)'),
array('pattern'=>'/(?<="v:genre"\>).*?(?=\<)/', 'item'=>'genre(s)'),
array('pattern'=>'/(?<=\<span property="v:initialReleaseDate" content=").*?(?=")/', 'item'=>'release_date(s)'),
);

foreach ($info_grep_keys as $grep) {
unset($matches);
preg_match_all( $grep['pattern'], $info_div_str, $matches);
if (is_array($matches) && is_array($matches[0]) && count($matches[0])>=1) {
if(count($matches[0])>1) {
$ret[$grep['item']] = implode(',', $matches[0]);
}
else {
$ret[$grep['item']]  = $matches[0][0];
}
}
}
}
//var_dump($ret) ;
return $ret;
}
```