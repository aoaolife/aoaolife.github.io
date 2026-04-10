---
title: "用iptables进行外网端口到内网的映射 – aoao.life"
date: 2023-12-14 20:06:56
---

目标:通过外网访问内网特定机器上的特定服务.
外网服务器SERVERA,外网卡eth1 ip 218.25.111.111,内网卡eth0 192.168.100.32
内网FTP服务器SERVERB,ip 192.168.100.128
内网HTTP及其它服务器SERVERC,ip 192.168.100.96

1.在root下建立脚本文件fw.sh,内容如下

```
#!/bin/sh
echo "Starting iptables rules.........."
modprobe ip_nat_ftp
modprobe ip_conntrack_ftp
echo 1> /proc/sys/net/piv4/ip_forward #不同的linux系统位置不同.目的是打开ip转发服务
iptables -F -t nat #清除原有列表
iptables -t nat -A POSTROUTING -s 192.168.100.0/24 -o eth1 -j SNAT --to 218.25.111.111 #内网ip转发,192.168.100.0/24指内网网段的所有地址
iptables -t nat -A PREROUTING -i eth1 -d 218.25.111.111 -p tcp --dport 21 -j DNAT --to 192.168.100.128:21#ftp服务
iptables -t nat -A PREROUTING -i eth1 -d 218.25.111.111 -p tcp --dport 20 -j DNAT --to 192.168.100.128:20#ftp服务

iptables -t nat -A PREROUTING -i eth1 -d 218.25.111.111 -p tcp --dport 22 -j DNAT --to 192.168.100.96:22 #ssh服务
iptables -t nat -A PREROUTING -i eth1 -d 218.25.111.111 -p tcp --dport 80 -j DNAT --to 192.168.100.96:80 #http服务
```

其实上面的内容也可以直接修改iptables的文件,但不知道为什么效果不好.

2.

```
chmod 755 fw.sh
```

3.

```
vi /etc/rc.d/rc.local
增加 /root/fw.sh
```

**4.修改SERVERB 和SERVERC的默认网关为192.168.100.32**