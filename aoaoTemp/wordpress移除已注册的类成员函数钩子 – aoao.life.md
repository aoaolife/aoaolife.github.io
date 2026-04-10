---
title: "wordpress移除已注册的类成员函数钩子 – aoao.life"
date: 2017-01-27 14:30:47
---

[书接上文](https://pewae.com/2017/01/wodrpress_widget_display_specified_hook_list.html)，找到钩子的目的是为了干掉它。
add_filter和add_action函数的第二个参数，可以是散兵游勇的单个函数，也可以是某个类的成员函数。

```
add_filter('the_content','func');
```

这种形式注册的钩子，可以直接用

```
remove_filter('the_content','func');
```

删掉。
但

```
add_action('init', array($this, 'func2'), 9);
```

这种形式注册的钩子，在类以外就无法删除了。因为你根本无法获得$this这玩意儿。
所幸我找到了解决方案，封装了一个函数。只要给函数多传一个类名，就可以删除了。
函数实现如下：

```
function remove_anonymous_object_hook( $tag, $class, $method )
{
$filters = $GLOBALS['wp_filter'][ $tag ];

if ( empty ( $filters ) )
{
return;
}
foreach ( $filters as $priority => $filter )
{
foreach ( $filter as $identifier => $function )
{
if ( is_array( $function)
and is_a( $function['function'][0], $class )
and $method === $function['function'][1]
)
{
//action也可以用remove_filter删除。
remove_filter(
$tag,
array ( $function['function'][0], $method ),
$priority
);
}
}
}
}
```

对于wprdpress底层来说，filter和action其实是同一个东西，所以这个函数可以对付filter和action。
如果函数是static函数，用这个函数是无法删掉的，而应该用

```
remove_filter('the_content','class::func3');
```

进行删除。

代码来源（http://wordpress.stackexchange.com/questions/57079/how-to-remove-a-filter-that-is-an-anonymous-object）