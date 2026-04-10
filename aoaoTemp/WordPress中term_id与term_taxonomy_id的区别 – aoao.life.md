---
title: "WordPress中term_id与term_taxonomy_id的区别 – aoao.life"
date: 2020-04-10 15:35:46
---

调用WordPressAPI，尤其在进行查表的时候，常常会看到参数里同时支持term_id与term_taxonomy_id这两个长得很像的东西，而且互换之后好像也没什么效果，一样能用。
那么这俩玩意究竟有没有区别呢？
有。
这个问题其实是好几个历史遗留问题的叠加。

## term是什么？

在WordPress里，我觉得对term最准确的理解是“称谓”，它可以是任何一个名词。
term_id就是这个名词的代号。
WordPress2.3开始支持tag功能。在那以前，WP只有category。开始支持tag功能后，WP的开发团队认为tag和category其实本质上是同一种东西，就给他们归了一个共通的属性，叫term。后来增加的文章格式，或者用户自定义taxonomy，也都“继承”了term。
term是没有实体的，离开了具体的tag或者category或者用户自定义taxonomy，term什么都不是。

## taxnomy是什么？

taxnomy的本意是分类学。之所以出现这么个晦涩的词，WP团队也是被逼的。因为category本身就是“种类”的意思啊，category从有WordPress那天就有了，完全没有替换和转义的可能。
既然term并没有实体，那么每个具体的实现就应该分开。tag是一种taxonomy，category也是一种taxonomy。在数据库当中每一条具体的tag或者category的信息，都记录在表wp_term_taxonomy当中。这个表是真正干活的，每一条记录都不能重复。
term_taxonomy_id实际上是term*taxonomy产生的id的意思。
另有一张名为wp_term_relationships的表，记录的是各种taxonomy与post的关联关系，这张表里用的就是term_taxonmy_id。

## 实例

表wp_term_taxonomy里不存名字。用户能看到的内容都存在另外一张表wp_terms里。多个taxonomy重名的时候，能节省一条记录——我觉得当时设计成两张表的唯一理由就是这个。

举个栗子，有一个tag，叫“游戏”；有个category，名字也是“游戏”。在WP4.6以前的版本里，这两种“游戏”在表wp_terms会共用一个term_id，有同一个slug名。但是它们在wp_term_taxonomy里是两条记录，term_taxonmy_id不同。
两张表格内存储的内容，见下表。

*wp_terms*

|  |  |  |  |
| --- | --- | --- | --- |
| term_id | name | slug | term_group |
| **1** | 游戏 | game | 0 |
| 2 | 音乐 | music | 0 |

*wp_term_taxonomy*

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| term_taxonomy_id | term_id | taxonomy | description | parent | count |
| 1 | **1** | category |  | 0 | 1 |
| 2 | **1** | post_tag |  | 0 | 1 |
| 3 | 2 | category |  | 0 | 9 |

请注意加粗部分区别。

## 重大变更

到了WP4.2，WP内部发现了给tag改名会出现bug，为了解决这个问题，不同的term_taxonomy再也不使用相同的term名（taxonomy term splitting）。自此，wp_terms里的条目数与wp_term_taxonomy中变得一致，两个引人误会的id也变得再无差别。（其实两张表也可以合并了）

## 结论

term_id用在与tag名、category名相关的功能上；term_taxonmy_id用在与post关联的功能上。
在WP4.2之后，二者再无区别。