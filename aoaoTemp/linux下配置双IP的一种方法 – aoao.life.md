---
title: "linux下配置双IP的一种方法 – aoao.life"
date: 2024-02-19 08:36:23
---

Linux的网络设备配置文件存放在/etc/sysconfig/network-scripts里面，对于网中的第块网卡，配置文件名一般为 ifcfg-eth0 如果需要为第一个网络设备绑定多一个IP地址，只需要在/etc/sysconfig/network-scripts目录里面创建一个名为ifcfg-eth0:0的文件，内容样例为：

DEVICE=”eth0:0″
IPADDR=”211.100.10.119″
NETMASK=”255.255.255.0″
ONBOOT=”yes”

其中的DEVICE为设备的名称，IPADDR为此设备的IP地址，NETMASK为子网掩码，ONBOOT表示在系统启动时自动启动。
如果需要再绑定多一个IP地址，只需要把文件名和文件内的DEVICE中的eth0:x加一即可。LINUX最多可以支持255个IP别名。

配置完成后需要运行/etc/rc.d/init.d/network restart重新启动网络服务。