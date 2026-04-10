---
title: 斐讯N1 刷入小钢炮系统后的注意事项 | aoao.life
date: 2021-01-14 06:30:16
updated: 2026-03-01 06:20:12
---

<http://rom.nanodm.net/>

你可以在小钢炮的官网看到最新的系统

刷入小钢炮本身没有太多好说的，官网有他的详细说明和注意事项。这里我可以多提一句，如果是通过降级的方式刷入系统的话，那么有可能由于时机的原因，刷入系统后，各个应用无法正常使用，这个时候，只需要插上U盘，从U盘启动，重新再刷入一遍EMMC即可。

最终的效果

主路由网关

`192.168.31.1`

小钢炮IP

`192.168.31.36`

小钢炮内docker Openwrt地址

`192.168.31.18`

# 1. 系统网络改静态路由（system network）

我们刚刚拿到一台N1盒子之后，刷入了小钢炮，这个时候，我们通过网线直连的方式将N1盒子接入的网络中，由于ip地址是DHCP，所以我们需要登陆到路由器后台，才可以看到小钢炮的ip地址，进而登陆系统。但是我们不想每次都这么麻烦，所以需要将系统网络改为静态ip，这样我们只需要记住一个内网ip的地址就可以了。

例如，我的主路由地址是`192.168.31.1`, 我想给小钢炮分配的ip地址为`192.168.31.36`

就可以在`system/network` 中进行相关修改。

# 2. 计划任务

可以直接在图形界面中编写相应的`crontab`添加或编辑计划任务，具体是`System/Scheduled Tasks`

在这里，可以看到其实已经有了一条给aria2添加tracker的计划任务，我们只需要给它前面的`#`去掉即可

|  |  |
| --- | --- |
| ``` 1 ``` | ``` 0 * * * */7 /usr/local/bin/addtracker-aria2 ``` |

当然了，我们这个计划任务是给aria2添加最新的tracker， 如果我们想要立刻添加tracker，而不通过计划任务的话，则只需要执行：

`/usr/local/bin/addtracker-aria2`

需要注意的是，由于这个脚本里面的远程地址是`*.githubusercontent.com` ，因此可能无法访问，获取不到最新的tracker，我自己就遇到了这种情况，报了404.

解决办法，可以像这篇文章写的那样，在`/etc/hosts` 里面添加一行

`199.232.96.133 raw.githubusercontent.com`

再次执行上述脚本，就没有问题了。需要注意的是，当脚本执行完毕后，会写系统日志，系统日志可以在小钢炮的界面上查看（`状态/系统日志`），也可以通过命令行找到

系统日志存储位置：

`/var/log/messages.`

其实在这里，可以多说两句，系统日志，在其他的类linux系统中，可能叫做其他别的名字，所以不要被名字所困惑，我自己之前，就一直在找syslog这个文件，发现找不到

# 3 config docker 下载地址

修改小钢炮docker 下载地址

`vi /etc/docker/daemon.json`

添加一行

`"graph": "/media/1ae6b9fc-47bd-47e6-b403-bba26910b79e/download"`

为啥要这么做呢？因为我使用了外置的移动硬盘，我当然想把docker的存储路径改到这里，这样我就可以安装更多的docker应用，同样的道理，我也可以把我的aria2或者qb的下载路径指定到我的移动硬盘，只不过，由于修改docker下载地址，需要使用命令行，容易被忽视，所以在这里，单独拿出来说下。

由于我是把docker的安装路径放到了移动硬盘上，所以有时候会出现小钢炮重启之后，无法找到对应的路径的问题（移动硬盘迟迟没有识别出来）。这个时候，也不需要做其他工作，鉴于上面的情况非常少，只需要将小钢炮再重启一次就可以了。

# 4 配置docker openwrt

`docker network create -d macvlan --subnet=192.168.31.0/24 --gateway=192.168.31.1 -o parent=eth0 macnet`

`docker run --restart always -d --name=OpenWrt --network macnet --privileged unifreq/openwrt-aarch64:r20.10.20 /sbin/init`

`docker exec -it OpenWrt bash`

在`docker openwrt`的命令行,通过

`vi /etc/config/network` 修改ip地址为

`192.168.31.18`

通过浏览器访问`192.168.31.18` 再进一步修改详细的网络配置，如网关，DNS等，进行软路由的配置，这些我在视频里都讲了，就不再提了。

如果要本地的docker 镜像可以按照这个方法

|  |  |
| --- | --- |
| ``` 1 2 ``` | ``` docker import openwrt-x86-64-generic-rootfs.tar.gz lean_openwrt docker run --restart always -d --name=2021.10-OpenWrt --network macnet --privileged 2021.10-openwrt /sbin/init ``` |

# 5.启动项设置 （start up）

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 ``` | ``` #!/bin/sh # this script will be executed during boot.  touch /var/lock/subsys/local ip link set eth0 promisc on ip link add mynet link eth0 type macvlan mode bridge  ip addr add 192.168.31.10 dev mynet ip link set mynet up ip route add 192.168.31.18 dev mynet ``` |