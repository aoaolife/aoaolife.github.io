---
title: "从Bluehost虚拟主机搬迁到LinodeVPS – aoao.life"
date: 2020-08-21 13:51:44
---

陈同学张嘴了，朋友托不敢辞，把搬家过程记录一下，也许会对后来人有所助益。
搬家这事儿实在不新鲜了，路子早被趟出来了。下面大多数步骤都是照着官方文档做的，少部分得到了热心人士的帮助，自己的心得很少很少。

1.申请VPS。
花钱的事儿，人家一定能给你办得妥妥当当的。定下用VPS之后，先尝试的是Vultr。但这个站不知为什么说我的信用卡刷不了，所以只剩下Linode一个选择了。
先搜了一个Linode的10刀优惠码，在注册用户的时候填了进去，确实有优惠。这玩意儿随便一搜到处都是，我就不帮别人做推广了。
绑定信用卡的惯例是要刷一小笔钱再返给你，选5美元的就是了。
这时账户里就有15美元，可以开通VPS了。

然后照着~~Linode的官方说明~~一步一步做就行了。
套餐选最便宜的，机房我选了东京。
创建好VPS后，点击那个LinodeXXXXXXX，再选择“Deploy an Image”，创建一个镜像。
CentOS，Fedora和Ubuntu对我来说都是老朋友，就选了一个CentOS。因为yum比apt-get少四个字母。
然后选择镜像大小。这个地方我不是很了解剩下的地方能干嘛，所以就把20G都分了。
再往下的Root密码就非常重要了，因为没有double-check，所以一定要谨慎。
☆创建完成后记得点“Boot”。

3.安装必要的服务
先在“Remote Access”里找到SSH的信息。我喜欢用的客户端是Bitvise，因为连命令行带SFTP都带了。Linode默认是带SSH和SFTP服务的，不然还玩个屁啊。
接下来开始装各种服务，这就跟Linode关系不大了。
有的教程推荐的是“什么什么一键安装包”，痞子鱼推荐了宝塔面板，johntitor推荐了easypanle，我自己又搜到了一个AMHpanle一个WDCP，一个VestaCP。本着小马过河的精神，我把这几个玩意儿都试了一遍。其实……都差不多。本来宝塔那个是挺好的，但我对它的cn域名实在是很害怕，最后我选的是VestaCP，我对把代码托管在github上的东西有天然的好感。
vestacp的[安装文档](https://vestacp.com/docs/)。
但这里有些顺序问题，所以重点说明一下。

3.1 安装vestacp面板。
vestaCP的[安装说明](https://vestacp.com/install/)。
注意要是不选默认服务的话，下面有个按钮重新生成安装命令。
我没有选ftp服务和邮件服务，http选的是nginx+php-fpm，SQL仍旧是mysql。DNS用的name和yum用的remi都被我带着了。默认的防火墙还行，也留着。
☆安装完成后一定要留意admin的默认密码，等会登录网页版管理工具要用到它。

3.2 配置web服务和数据库
http://XXXXXXXX.members.linode.com:8083登录vesta。
user–edit，修改密码和默认语言。DNS改成ns1.linode.com和ns2.linode.com

点击“Web服务”，然后点绿色加号，在第一个框里输入域名。虽然这个时候域名还没转移，但我们现在配置的是服务器信息，放心去做吧。
注意这里有个“高级选项”，把SSL选上吧。
我搬家过程中唯一卡住的地方就是这个SSL设置，因为好像vestaCP在为两个不同的web服务做SSL的时候有点问题。关了一个就好了。

然后选择数据库。照提示做就好了。

DNS服务。好像是自动添加的？反正非常省心，加上全默认就行了。
总之我爱死这个面板了，该有的有，不该有的不出来惹事儿。

最后有人说LNMP体系下php里没有mail()函数，要装一个sendmail。

```
yum install sendmail
```

有没有用不知道，反正提示是有新服务装上了，而且邮件好使了。当它好用呗。

4.原站备份
包括数据库备份和文件备份。这方面的工具多如牛毛。我一直用BackWPup这个插件。
要准备的只有文件跟导出的SQL数据库文件两部分而已。

5.数据转移
等待过程中可以先把数据准备好。下面的步骤我都是按照安装了VestaCP写的。
把文件打包传到服务器上，解压缩。如果是tar格式，运行

```
sudo -u admin tar -vxf XXX.tar.gz
```

。
如果是zip，就运行unzip命令，如果提示找不到，就装一个。
注意一定要打包传，否则会慢得你不要不要的！
解压缩之后把所有内容拷贝到/home/admin/web/xxx.com/public_html/ 下即可。
因为不涉及到换域名，所以这一步非常简单。
☆如果上一条命令没用sudo的话，这次记得要把public_html下的所有文件user和group都改成admin。
☆把目录下原来那个index删掉!

接下来导入SQL文件。

```
# mysql -u admin_your_sql_user -p
SQL#> use admin_your_db_name
SQL#> source /absolute/path/to/your/sql/file/***.sql
```

有控制台就是好，直接敲比用网页版的mysqladmin快多了。
☆然后记得改一下config.php。因为VestaCP强制DB用户名和数据库用admin_开头，所以想跟原来完全一样是很难做到的。

6.域名转移
方室提供了一个很好的域名服务商namesilo。
完全参照[这篇文章](https://www.liaosam.com/bluehost-migrate-to-linode-domains.html)就好了：
域名转入要交一年的费用。好在namesilo支持支付宝。
搬家过程中namesilo会给原域名所有人发邮件，所以要确定你的邮箱能收到邮件。这封邮件大概10分钟就到了，一定要记得点击里面的链接进行确认。
☆过一会儿bluehost也会给你发一封信。意思是如果你同意转移或者要取消，点链接。选择域名以及domain transfer以后，里面有两个链接，第一个是确认，第二个是取消。
然后进到linode的主页，按照上面文章说的，添加两条A记录。其实选默认也可以。
剩下的就是等。
根本用不了两天那么久，就是等待DNS renew + 等两封邮件的时间。
心急的话，收到namesilo的成功确认信之后，就可以一直ping域名，直到它不能解析，再过一小会儿就好了。
namesilo搞定之后，回到bluehost，把DNS记录都给删了。
bluehost的动作很快，前脚把域名转走了，后脚你申请的SSH服务就给停了（也有可能是删DNS记录的原因）。
最后，新DNS生效以后，记得把原来服务器上的东西都删掉。

7.Shadowsocks
不装这玩意儿简直辜费VPS了。
倒也没什么好说的，非常简单，按照官方文档一步一步来就行。
倒是客户端的使用有点麻烦，每一项都要跟你服务器上配置得一模一样才可以。

最后，非常感谢~~痞子鱼~~、~~johntitor~~、[石樱灯笼](https://www.catscarlet.com/)、~~掩耳~~、[陈大猫](https://chidd.net/)，他们坚定了我换VPS的决心。
以及感谢所有在我需要帮助的时候伸出圆手的朋友们。