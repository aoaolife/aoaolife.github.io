---
title: "VestaCP拯救邮件大作战（未遂） – aoao.life"
date: 2020-08-21 13:51:44
---

之前@子痕兄说我的邮件进了垃圾邮件，并给指点了一条阳关大道。但是一来那套方案步骤多，尤其我懒得改现在的邮件回复格式；二来改成google邮件也不能保证国内的奇葩们就正常接收了，所以看看就算了。前几天贝总又说收不到留言，就尝试改进一番。

先说结论。没改好。
而且下面的配置文件只是VestaCP+CentOS的，其余系统一律不了解。全中国用vestaCP的可能就俩人……

找到的第一种方法是去~~https://postmaster.google.com~~验证域名。
google让在DNS里添加一条TXT记录和一条CNAME。
正好域名快续费了，上namesilo顺手改了呗。
等了十五分钟，再验证还是报没找到记录。
我记得搬家的时候改DNS，生效都没用这么久。于是在vestaCP的DNS面板以及Linode的DNS上都加了这两条记录。五分钟之后就验证通过了。我也不知道究竟是改哪边生的效。

尝试登录webmail发邮件的时候，一直登录失败。
关键字一搜，原来是vestaCP在一次升级的时候，脚本写错了，exim的配置文件被覆盖了。需要修改**/etc/dovecot/dovecot.conf**，在后面加上

```
namespace inbox {
inbox = yes
}
```

邮件发出，仍旧进垃圾箱。

又找到了一篇详细的文章（via）。这是篇非常完整的文章。对照一看，卧槽，vestaCP的DNS面板里一个不少，我全设了啊！！

先检查一遍吧。
首先是SPF。在DNS里追加一条TXT记录就可以。有多种加法。我用的是域名验证。

```
v=spf1 a mx pewae.com ?all
```

此时我幡然醒悟，vestaCP面板上的DNS莫不是不好用吧！好不容易回忆起来，上次折腾SVN未果的时候，在其官方论坛上看到一个人说开DNS被攻击，我把本机的DNS已经停掉了！
下面动作就好办了，把这些个记录搬到linodes的DNS上就好了。

除了SPF，还有DKIM。这是一对儿公钥密钥。照粘就是了。vestaCP的密钥文件是

```
/home/admin/conf/mail/%domain%/dkim.pem
```

公钥则放在

```
/usr/local/vesta/data/users/%username%/mail/%domain%.pub
```

via（https://github.com/serghey-rodin/vesta/issues/320）
需要搬运的是两条TXT记录

```
mail._domainkey 	k=rsa; p=XXXXXX
_domainkey 	t=y; o=~;
```

最后还有一个DMARC。也是搬运一条记录完事。

```
_dmarc 	v=DMARC1; p=none
```

等一阵之后，找个地方验证一下。
(~~http://dkimvalidator.com~~)
这个网站会自动生成一个邮箱，让你用自己的邮箱给它发邮件，然后出一份报告，看这几项是否已经加好。
从验证结果看，这么折腾完以后，是不应该被认为垃圾邮件了。

给自己的gmail、163、outlook、qq邮件分别发信，gmail和163在垃圾邮件里，outlook完全正常，而qq邮箱一点儿反应都没有，跟贝总报的情况一样。
查看一下本地的log，发现错误提示跟往贝总那儿发一样，都是什么IP超上限了。顺着这个关键字找，找到一堆骂腾讯的。

```
2018-08-29 11:53:35 1furXt-0007FC-7X ** XXXXXXX@qq.com R=dnslookup T=remote_smtp
H=mx3.qq.com [103.7.30.40] X=TLSv1.2:AES128-SHA256:128 CV=yes: SMTP error from
remote mail server after end of data: 550 Ip frequency limited [MSasc89YXQNeMRrc
kgRVoZZLLdRlxGMr225Uyud+GaUu71uvUhT562A= Blocked IP XXX.XXX.XXX.XXX]. http://serv
ice.mail.qq.com/cgi-bin/help?subtype=1&&id=20022&&no=1000725
```

既然是非战之罪，就只好先到这儿吧，等哪天心血来潮了再说吧。
其实任何重要问题都没解决。