---
title: "WORDPRESS数据库查询历史上的几月几日没发过贴 – aoao.life"
date: 2018-10-02 10:09:31
---

如果看不懂标题的话，就不要往下看了。

首先，这是个酝酿已久却很无聊的想法。差不多从看到“历史上的今天”的代码的那天起，我就在想这个操作的逆操作应该如何进行。
又担心这么做违背本能，会不自觉地填坑，殊为不美，所以这一拖就差不多又是4年，我猜坑已经被我填得差不多了吧（其实并没有）。

这个玩法对于历史不够久或者坚持每天发文的人来说又毫无用处，差不多仅供我这种又老又懒的人来自娱自乐。

下面开始。
因为本人只在工作第一年的菜鸟时期玩过数据库，稍微高级的办法都不会，就像一个只会分步计算不会写拖式的小学低年级生，所以办法是蛮幼稚的，有好方案请指出。

1.建立一张写满月-日的辅助表格wp_t_static_dates。
表格的列属性使用字符串而不是数字。

```
CREATE TABLE `wp_t_static_dates` (
`the_month` varchar(2) DEFAULT NULL,
`the_date` varchar(2) DEFAULT NULL
)
```

2.然后往辅助表格里填满数据。
正统的方法是使用存储过程，我不会。我是用EXCEL拽出一年的日期，然后用Notepad++批量替换得到的。
补0是为了后面排序方便。

```
INSERT INTO `wp_t_static_dates` (`the_month`, `the_date`) VALUES
('01', '01'),
('01', '01'),
('01', '02'),
...
('12', '29'),
('12', '30');
```

3.创建月-日-发帖数的视图。
临时表和视图都可以。我喜欢用视图。月-日的组合为了方便调用GROUP BY
表格做好以后，就可以直接查询出“几月几日发文最多”了。但咱的目标是最少，所以还需要一步。

```
CREATE VIEW `wp_v_post_count_by_month_date`  AS  (
SELECT `d`.`the_month` AS `the_month`,
d`.`the_date` AS `the_date`,
CONCAT(`d`.`the_month`,'-',`d`.`the_date`) AS `the_com`,
COUNT(`d`.`the_date`) AS `cnt`
FROM (`wp_posts` `p` JOIN `wp_t_static_dates` `d`)
WHERE (
(`p`.`post_password` = '')
AND (`p`.`post_type` = 'post')
AND (`p`.`post_status` = 'publish')
AND (month(`p`.`post_date`) = `d`.`the_month`)
AND (dayofmonth(`p`.`post_date`) = `d`.`the_date`))
GROUP BY CONCAT(`d`.`the_month`,'-',`d`.`the_date`)
ORDER BY CONCAT(`d`.`the_month`,'-',`d`.`the_date`),`d`.`the_month`,`d`.`the_date`)
```

4.查询在第一张表中有记录而在视图中无记录的数据（即为没有发帖的日期）
我知道这个办法很笨，但是我真的一直用不好LEFT JOIN。

```
SELECT DISTINCT `wp_t_static_dates`.`the_month`,`wp_t_static_dates`.`the_date`
FROM `wp_t_static_dates`,`wp_v_post_count_by_month_date`
WHERE `wp_t_static_dates`.`the_month` = `wp_v_post_count_by_month_date`.`the_month`
AND `wp_t_static_dates`.`the_date` NOT IN (
SELECT `wp_v_post_count_by_month_date`.`the_date`
FROM `wp_v_post_count_by_month_date`
WHERE `wp_t_static_dates`.`the_month` = `wp_v_post_count_by_month_date`.`the_month`)
```

OK，结果出炉。本博截止发帖前还有8天没覆盖到。你呢？