---
title: "制作ARM基板上运行的Ubuntu20.04的rootfs – aoao.life"
date: 2023-05-31 16:56:58
---

## 事前准备

一台Ubuntu工作机，最好是同样的Ubuntu20.04。因为编译的时候要用到开发机的配置文件。如果版本不一样的话，低编高根本执行不下去，高编低也会有警告。
工作机的语言设置成与基板一致（英语）

## 安装必要工具

其中debootstrap就是ubuntu提供的制作工具。另外两个是chroot的前提。

```
apt-get install qemu-user-static debootstrap binfmt-support
```

## 开发机（不包括chroot）的动作

整个制作过程的中间一部分是利用chroot命令进入下载目录，然后以登录要做成的根文件系统的方式修改的，所以以chroot作为分界。
可以把开发机上的动作存成outer.sh，把chroot内的动作存成inner.sh，便于以后操作。
本文中所有工具和编译链都是arm64，如果要编32位系统请自行查找替换，应该也没几处。
具体解释见注释吧

```
# focal是ubuntu20.04的代号。Ubunntu不同的版本有不同的代号。
export targetdir=ubuntu20.04-rootfs
export distro=focal
# 打包好的根文件系统直接放到tftp服务目录，便于更新，非必须。
export tftpdir=/var/tftp

mkdir                                           $PWD/$targetdir

# debootstrap是Ubuntu创建文件系统的工具
# 架构根据实际基板和操作系统直接选。
sudo debootstrap --arch=arm64 --foreign $distro $PWD/$targetdir

# qemu是整个步骤的一个灵魂，不拷贝进去chroot命令会失败
sudo cp /usr/bin/qemu-aarch64-static            $PWD/$targetdir/usr/bin
# 保证目录内的网络环境
sudo cp /etc/resolv.conf                        $PWD/$targetdir/etc
# 如果把提到的chroot后的动作存成一个shell的话，
sudo cp ./inner.sh			                    $PWD/$targetdir/
# 不进行mount的话某些安装动作会失败
sudo mount -vt proc proc                        $PWD/$targetdir/proc
sudo mount -vt devpts devpts -o gid=5,mode=620  $PWD/$targetdir/dev/pts

sudo chroot $PWD/$targetdir
# ====接下来的动作要在已经下载的文件系统目录中进行====

# 从chroot文件夹中exit之后回到这里
# 反挂载proc
sudo umount $PWD/$targetdir/proc
sudo umount $PWD/$targetdir/dev/pts
# 删除chroot用的工具
sudo rm -f  $PWD/$targetdir/usr/bin/qemu-aarch64-static
sudo rm -f  $PWD/$targetdir/work_in_ubuntu.sh

# 打包并拷贝。非要进入文件夹内再打包是为了保证解包后的文件路径不出麻烦。
cd $PWD/$targetdir && sudo tar -zvcf rootfs-ubuntu.tar.gz . && sudo mv rootfs-ubuntu.tar.gz $tftpdir &&  cd -
```

其实在外层开发环境中能干的事情不多。

## 目标系统chroot的动作

可干的事情非常多。简单说就是在命令行下安装和配置Ubuntu的各种服务。
下面的内容可以存成一个inner.sh
当然也可以手动一行一行执行。
这里我遇到了三个难点。第一是语言包的问题，我一开始开发环境是中文，导致里面的语言怎么设都报警告，切换成英文万事大吉。第二是网络配置，Ubuntu20.04默认的netplan没配明白，安装了network-manager之后还是配了半天。第三是关于U盘自动挂载的，那个更麻烦，不过不影响rootfs本身的功能，以后有机会再写。

```
# 现在已经不是刚才的环境了，所以要重设一遍环境变量。
export distro=focal
export LANG=C
export hostname=myboard

#debootstrap的位置不一样了。
/debootstrap/debootstrap --second-stage

#指定ubuntu的源文件位置。可以替换成清华源、阿里云源之类。注意替换的时候网址里要用<strong>ubuntu-ports</strong>，否则ubuntu指向的都是x86_64的源，就白忙活了。
cat <<EOT > /etc/apt/sources.list
deb http://ports.ubuntu.com/ubuntu-ports focal main restricted universe multiverse
deb-src http://ports.ubuntu.com/ubuntu-ports focal main restricted universe multiverse
deb http://ports.ubuntu.com/ubuntu-ports focal-updates main restricted universe multiverse
deb-src http://ports.ubuntu.com/ubuntu-ports focal-updates main restricted universe multiverse
deb http://ports.ubuntu.com/ubuntu-ports focal-security main restricted universe multiverse
deb-src http://ports.ubuntu.com/ubuntu-ports focal-security main restricted universe multiverse
EOT

cat <<EOT > /etc/apt/apt.conf.d/71-no-recommends
APT::Install-Recommends "0";
APT::Install-Suggests   "0";
EOT

# 更新已安装的服务
apt-get -y update
apt-get -y upgrade

# 安装各种工具。可以写在一起，但分开的好处是便于增删改。
# 第一波是（自认为）系统必须的
# 1.locale
apt-get install -y locales dialog
#设语言，语言要先改了，不然会影响一些工具的安装。
#这里会弹一个对话框，就正常选就行。
dpkg-reconfigure locales
update-locale LANG="en_US.UTF-8" LANGUAGE="en_US:en"
# 设时区
echo "Asia/Shanghai" > /etc/timezone
dpkg-reconfigure -f noninteractive tzdata

# 2.网络工具
# ifconfig默认不带，需要装。
apt-get install -y net-tools
# Ubuntu默认的网络配置没配明白，于是需要借助network-manager工具
apt-get install -y network-manager

# 3.进程工具，ps，kill什么的
apt-get install -y psmisc

# 4.网络时间
apt-get install -y ntpdate ntp

# 5.NTFS文件系统工具（主要是U盘）
apt-get install -y fuse ntfs-3g

# 6.busybox
apt-get install -y busybox

# 工具安装先放一放，开始搞配置
# hostname可以随便起，但不能没有
echo $hostname > /etc/hostname

# fstab
# 我的fstab下面这样，实际根据自己基板的情况自行替换
#fstab
cat <<EOT> /etc/fstab
/dev/root            /                    auto       defaults              1  1
/dev/mmcblk0p1       /boot                auto       defaults              0  0
proc                 /proc                proc       defaults              0  0
tmpfs                /var/volatile        tmpfs      defaults              0  0
EOT

# #非常重要#
# 这个文件是告诉Ubuntu有哪些可以用的串口。不写这个文件会出现加载到文件系统后串口就失去回显了
cat <<EOT > /etc/securetty
ttyPS0
ttyPS1
ttyS0
ttyS1
ttyS2
ttyS3
ttyUSB0
ttyUSB1
ttyUSB2
ttyGS0
EOT

# 配置网络环境，IP地址通过DHCP获取。
cat << EOT > /etc/netplan/eth0.yaml
network:
version: 2
renderer: networkd
ethernets:
enp3s0:
dhcp4: y
dhcp6: n
EOT

# #非常重要#
# 刚才安装的network-manager的默认配置，不写的话系统启动之后网卡是down的
cat <<EOT >/etc/NetworkManager/conf.d/10-globally-managed-devices.conf
[keyfile]
unmanaged-devices=none
EOT

# 时间同步脚本
cat << EOT > /usr/lib/networkd-dispatcher/routable.d/ntp-restart
#!/bin/sh
/usr/sbin/service ntp restart
EOT

# 配置用户
# 修改root用户密码，可以自行发挥。这种写法为了避免出现交互界面，少打字
echo root:root | chpasswd

# 追加一个ubuntu用户
useradd -p $(openssl passwd -crypt ubuntu) ubuntu
echo "ubuntu ALL=(ALL:ALL) ALL" > /etc/sudoers.d/ubuntu

# 安装其它需要的工具，不一一解释了，每个项目需求都不一样，酌情增减。
apt-get install -y  build-essential
apt-get install -y  kmod
apt-get install -y  iperf
apt-get install -y  curl
apt-get install -y  usbutils
apt-get install -y  hwinfo
apt-get install -y  openssh-server

# 清除安装产生的临时文件
apt-get clean

#自动退出，exit后就回到外层了
exit
```

## 再次修改文件系统

弄懂上面两步的话就很简单。如果是单纯的拷贝往文件夹里拷就行。如果要增删改服务，就是外层的debootstrap不要做，逐行执行命令直到chroot，然后修改配置或者apt安装反安装。注意反安装的话remove之后最好执行一遍purge，删除未使用的配置文件。不要乱改语言。退出前记得clean。