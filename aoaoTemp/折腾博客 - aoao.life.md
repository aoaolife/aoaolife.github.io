---
title: 折腾博客 - aoao.life
date: 2026-02-06 00:00:00
updated: 2026-02-06 00:00:00
---

自从原用Readd模版因为wordpress更新出现bug无法使用后，先是换成“二0一五”模版，这2天又换成现在的“Dashscroll”模版，还是不太满意，最喜欢的还是简洁单栏文字模版。

**殃及池鱼**

自己和博友都发现今早博客页面访问速度很慢，下午却又恢复顺畅，我瞎猜可能跟今天阿里千问搞红包活动太火爆导致阿里云机房资源紧张有关系，博客用的是阿里云。

前几天微信没禁止元宝在微信分享红包时我倒是抢了10多块钱红包提现，阿里千问的红包我就没参与了。

**修复Gravatar**

换模版后首页Gravatar头像和文章页评论列表的头像都无法正常调取，且影响页面打开速度。

在functions.php文件中将secure.gravatar.com、cn.gravatar.com定向到国内访问地址cn.cravatar.com，并访问gravatar.com重新创建邮箱头像。

不足：似乎修改后的gravatar头像未能及时同步，当下头像看到的还是默认gravatar-logo。

--**20260207补充**--

1、Gravatar头像同步问题已解决，安装WP-China-Yes插件，它能将Gravatar头像等WordPress官方服务替换为国内镜像，其中就包括Cravatar。

2、取消左侧搜索框，简化页面。

3、取消文章页内容下方的“社交分享图标”和“上下文”引导，简化页面。

本文著作权归作者 [ aoao.life ] 享有，未经作者书面授权，禁止转载，封面图片来源于 [ 互联网 ] ，本文仅供个人学习、研究和欣赏使用。如有异议，请联系博主及时处理。

[Wordpress](https://www.leolin86.com/tag/wordpress/)[Typecho](https://www.leolin86.com/tag/typecho/)