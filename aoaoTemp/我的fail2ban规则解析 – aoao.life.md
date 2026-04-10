---
title: "我的fail2ban规则解析 – aoao.life"
date: 2023-09-08 21:26:27
---

这份东西是专门写给@不亦乐乎和我自己的。他那边提出问题，刚好我这里快到换VPS的季节了，拿出来温习一下正合适。
我虽然是个程序员，但开发的方向跟网络基本无关，所有的网站建设方面相关的东西也一样是半吊子。有说的不对的地方，欢迎斧正。

fail2ban是个监控服务。配合firewalld使用，能够起到阻止某些IP对网站进行恶意访问的作用。
我的最初的配置方法来自[大鸟博客](https://pewae.com/gaan/aHR0cHM6Ly93d3cuZGFuaWFvLm9yZy80MDM2Lmh0bWw=)，人家比我厉害多了，讲的也详细，这里就不再赘述了。

这篇是想说说我自己针对各种攻击行为而制定出的规则。

## jail.local

先看我的/etc/fail2ban/jail.local文件。
其中ssh字段和nginx-cc字段都跟大鸟的没什么区别，只是频度不一样。这里不要以为禁闭时间短是好事。我为了一劳永逸，另外写了一个脚本去检查fail2ban的log。2天内触犯规则5次的IP会被我直接drop。

```
[DEFAULT]
ignoreip = 127.0.0.1/8
bantime  = 86400
findtime = 600
maxretry = 5
banaction = firewallcmd-ipset
action_l = %(banaction)s[name=%(__name__)s, bantime="%(bantime)s", port="%(port)s", protocol="%(protocol)s", logpath=%(logpath)s, chain="%(chain)s"]
action = %(action_l)s

[sshd]
enabled = true
filter  = sshd
port    = 22
action = %(action_l)s
logpath = /var/log/secure

[nginx-cc]
enabled = true
port = http,https
filter = nginx-cc
action = %(action_l)s
maxretry = 8
findtime = 361
bantime = 14400
logpath = /wwwlogs/pewae.com.log

[nginx-http1_1]
enabled = true
port = http,https
filter = nginx-http1_1
action = %(action_l)s
maxretry = 1
findtime = 14400
bantime = 1000000
logpath = /wwwlogs/nowhere.org.log

[nginx-x00]
enabled = true
port = http,https
filter = nginx-x00
action = %(action_l)s
maxretry = 1
findtime = 600
bantime = 7200
logpath = /wwwlogs/pewae.com.log

[wordpress]
enabled = true
port = http,https
filter = wordpress
action = %(action_l)s
maxretry = 3
findtime = 7200
bantime = 1800
logpath = /wwwlogs/pewae.com.log
```

重点说说后面三个字段是怎么来的。

## nginx-http1_1

该规则的配置如下:
/etc/fail2ban/filter.d/nginx-http1_1.conf

```
[Definition]
failregex = <HOST> -.*- .*HTTP/1.* .* .*$
ignoreregex =
```

乍看这是条很严厉的规则，把所有的http1的连接都给抓了。
但是，请注意一下jail.local中，这条规则所监视的文件。这并不是我网站真正的log。而是利用了宝塔面板的“默认站点”功能，指向的空域名所对应的log。
下面是典型的空网站log：
`5.181.80.95 - - [07/Sep/2023:04:11:31 +0800] "GET //myadmin/scripts/setup.php HTTP/1.1" 404 146 "-" "-"
118.123.105.93 - - [07/Sep/2023:09:02:59 +0800] "\x16\x03\x03\x01\xA6\x01\x00\x01\xA2\x03\x03:\x85Q\xC2\xDA" 400 150 "-" "-"
35.203.211.136 - - [07/Sep/2023:12:10:57 +0800] "GET / HTTP/1.1" 200 917 "-" "Expanse, a Palo Alto Networks company, searches across the global IPv4 space multiple times per day to identify customers' presences on the Internet. If you would like to be excluded from our scans, please send IP addresses/domains to: scaninfo@paloaltonetworks.com"`
这种log是通过扫IP而不是访问域名产生的，所以肯定不是好东西。全抓就对了。像第三条那种还解释自己扫IP的原因，你解释个P啊！

## nginx-x00

该规则的配置如下:
/etc/fail2ban/filter.d/nginx-x00.conf

```
[Definition]
failregex = ^<HOST> .* ".*\\x.*" 400 .* .*$
ignoreregex =
```

意思是抓取命令列以x开头，然后服务器返回400错误的日志。
这种日志长这样：
`87.251.64.11 - - [07/Sep/2023:14:56:56 +0800] "\x12\x01\x00^\x00\x00\x01\x00\x00\x00$\x00\x06\x01\x00*\x00\x01\x02\x00+\x00\x01\x03\x00,\x00\x04\x04\x000\x00\x01\x05\x001\x00$\x06\x00U\x00\x01\xFF\x04\x07\x0C\xBC\x00\x00\x00\x00\x00\x00\x15\xD0\x00 \x00\x00\x00\x00\x00\x00\x00\xC0\x0CU\x04\xFF\x01\x00\x00\x0C\x00\x00\x00\x00\x00\x00\x00\x00\x00U\x04\xFF\x01\x00\x00\xFE\xFF\xFF\xFF\x01" 400 150 "-" "-"`
一看就不是好鸟，对吧？

## wordpress

这组是专门针对针对WP的攻击行为的。至此无脑的大规模CC已经被大鸟博客的CC规则拦下了，但是我还是想要对付那些针对WP的王八蛋。忘了抄自哪里，而且我自己也有贡献。
该规则的配置如下:
/etc/fail2ban/filter.d/wordpress.conf

```
[Definition]
failregex = ^<HOST> .*POST /wp-comments-post.php.* .*HTTP/1.* .* .*$
^<HOST> .*POST /xmlrpc.php.* .*HTTP/1.* .* .*$
^<HOST> .*POST /wp-login.php.* .*HTTP/1.* .*404 .* .*$
^<HOST> .*/wp-config.php.* .*HTTP/1.* .* .*$
^<HOST> .*/wp-content/plugins/.* .*HTTP/1.* .*404 .* .*$
^<HOST> .*/wp-content/themes/.* .*HTTP/1.* .*404 .* .*$
^<HOST> .*(GET|POST|HEAD).* .*HTTP/1.* .*404 .* .*$

ignoreregex = ^<HOST> .*GET /[0-9]{4}/[0-9]{2}/.* .*HTTP/1.* .*404 .* .*$
```

逐条详细说明一下：
阻止规则第一条：防止直接调用wp-comments-post.php，这是阻止某些spam的行为。
阻止规则第二条：禁止调用xmlrpc功能。注意我自己是不用离线工具的，所以可以这么设。如果要用离线工具，或者整合了网站app什么的，要把这一条删掉或者设白名单。
阻止规则第三条：禁止暴力攻击wp-login.php，比如强行试密码之类。其实我自己的login都改名了，但看到这样的行为仍旧是神烦。
阻止规则第四条：wp-config.php的重要性不言而喻，想get的都不是好人。注意这条和上条，你自己登录的时候，本机是在白名单里的，所以不受影响。
阻止规则第五第六条：禁止操作插件和主题目录。注意有些插件如果有互动要放开。
阻止规则第七条：禁止GET、POST、HEAD以外的命令。

放行规则：这条正则是我正常的permalink的格式，如果抓不到，可能是我改了permalink，所以放行。

我所定义的规则就是这些。其实还是有挺多可以改善的地方，比如我其实想禁止除后台控制台外所有的POST行为，但是又搞不清原理。
再比如CC的规则其实挺不好界定的，容易误伤。我现在的频率就经常把一些频繁的feed抓取行为认成CC，继而ban掉。像十年之约的爬虫就被我手动捞出过两次，现在索性不管了。
再再比如access.log里也一堆粑粑。但是我不太清楚这个log是怎么产生的，也就没敢加规则。
哦对了，filter.d里的配置文件，正则的写法有点恶心，但是好在有一条命令是可以测试的。但是那条命令都被我忘了好几年了。

以上。