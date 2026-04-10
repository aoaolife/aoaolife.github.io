---
title: "在Ubuntu20.04（控制台）下自动挂载NTFS文件系统的U盘 – aoao.life"
date: 2023-07-04 16:11:36
---

首先，请确认rootfs的版本是Ubuntu20.04。高版本或低版本不好用概不负责。
其次，这份方案是为了解决 1）挂载NTFS U盘 和 2）控制台模式这两个问题。如果是Ubuntu桌面系统，那么解决的办法一大把。
第三，我是在自己编译操作系统的时候遇到的问题，所以首先要确保内核里编译了FUSE（File Systems —>FUSE） 和 NTFS文件系统（File Systems —>DOS/FAT/EXFAT/NT Filesystems —>NTFS file system support + NTFS write support + NTFS Read-Write file system support）

## 1.安装必要的工具

`apt-get install -y fuse
apt-get install -y ntfs-3g`

## 2.创建udev在systemd中的配置

`vi /etc/systemd/system/systemd-udevd.service`
然后写入如下内容

```
#保留默认配置
.include /usr/lib/systemd/system/systemd-udevd.service
[Service]
#以用户态身份Mount
PrivateMounts=no
```

这样做是为了修改方便。直接去修改/usr/lib/systemd/system/systemd-udevd.service也是一样的。
有价值的只有最后一行。据说在Ubuntu20.04以前的版本里，写成MountFlags=shared。这是我遇到的第一个坑。

## 3.创建新的udev规则

`vi /etc/udev/rules.d/99-usb-mount.rules`
文件名开头是规则的执行顺序，尽量用99-开头，意味着最后执行。后缀要是rules。中间随意。

然后写入下面内容

```
KERNEL=="sd?[1-9]", SUBSYSTEM=="block", ACTION=="add", RUN+="/bin/bash /etc/udev/rules.d/usb-disk-monitor.sh %k"
KERNEL=="sd?[1-9]", SUBSYSTEM=="block", ACTION=="remove", RUN+="/bin/bash /etc/udev/rules.d/usb-disk-monitor.sh %k"
```

两条规则的意思是，检知到sdnX设备（通常是U盘）有add/remove动作时，执行同目录下的usb-disk-monitor.sh脚本。%k是udev规则中自动生成的变量，kernel name，也就是sda1、sdb1这种名字。脚本里要用到，所以作为参数传进去。
为了避免意外，所有路径都写全路径。

## 4.创建mount执行的脚本

`vi /etc/udev/rules.d/usb-disk-monitor.sh`
有人说这个脚本不放这个位置也可以。我没试。

```
#!/bin/bash
DEV_NAME=$1
#输出到串口
FLOG=/dev/ttyPS0
echo "" >> $FLOG
echo $(date) >> $FLOG
MNT_PATH=/run/media/
if [ ! -d "$MNT_PATH" ]; then
mkdir -p "$MNT_PATH"
fi
DEST_NAME=$MNT_PATH$DEV_NAME
if [ "$ACTION" = "add" ]; then
/bin/mkdir -p $DEST_NAME &>> $FLOG
/usr/bin/systemd-mount --no-block --collect $DEVNAME $DEST_NAME &>> $FLOG

elif [ "$ACTION" = remove ]; then
/usr/bin/systemd-mount --umount $DEST_NAME &>> $FLOG
/bin/rmdir $DEST_NAME &>> $FLOG
fi
```

这个文件遇到了第二个坑和第三个坑。
第二个坑是shell的判断语句，Ubuntu里不能写“==”，只能写“=”。
第三个坑就是mount命令本身。如果用ID_FS_TYPE进行判断，执行mount -t vfat挂载FAT32格式的U盘，没任何问题。但是如果用mount -t ntfs-3g命令挂载NTFS格式的U盘，挂载看着是成功了，但访问U盘时会出现“Transport endpoint not connected”错误。这其实在udev的官方文档里有专门的说明，udev的规则里不能用mount命令对FUSE文件系统进行挂载。如果进行操作，挂载进程会在几秒后被杀掉。解决办法就是换成systemd-mount。我没去查这个命令在哪个包里，反正我做的系统里就有。
另外挂载的位置是在/run/media/。有需要变的自己去改脚本里的MNT_PATH变量即可。
还有，这个脚本里如果不作重定向，是看不到任何输出的。我的基板上串口0是/dev/ttyPS0。如果有需要请自行调整。

都配置好之后，重启，然后就可以看到现象了。
理论上重启udev服务也可以做到生效，但强烈不推荐。