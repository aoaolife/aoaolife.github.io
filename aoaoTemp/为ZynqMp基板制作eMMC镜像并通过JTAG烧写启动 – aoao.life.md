---
title: "为ZynqMp基板制作eMMC镜像并通过JTAG烧写启动 – aoao.life"
date: 2023-05-16 16:07:40
---

最最重要的事情最先说，ZynqMP的U，开发环境是Ubuntu20.04 + Petalinux 2022.1，烧写工具是Vitis 2021.2。环境不一样的请酌情参照。

友军做了一块基板：ZynqMP的U，有JTAG、串口、网卡、USB Host、QSPI Flash、EEPROM、eMMC，没有SD卡。
第一批的板子出了点小瑕疵，网络芯片焊错方向了，导致网根本没有好使的可能。
目标很简单，让基板先能跑起来Petalinux再说。

弯弯绕绕踩了好多坑，才尝试出最终的办法：U-BOOT、镜像和根文件系统用官方推荐的放SD卡（eMMC）的形式，其余的问题由JTAG解决。
要说的是这不是唯一的解决方案，其实QSPI、USB甚至串口都是可以利用的资源，只是咱水平没到那个程度而已。

确定这条路也是因为能找到比较详细的教程。但是这个过程踩了两个大坑：
1：最容易搜到的那份制作镜像的教程，只有BOOT分区，并没有包括根文件系统。
2：最容易搜到的那份JTAG烧写eMMC的教程，是基于Petalinux 2018的，那时Vitis甚至都不叫Vitis！启动命令和加载的文件都不一样。

反正最后这份方案搞出来颇有些邪门歪道的感觉。
下面开始:

## 1 制作一个eMMC镜像的模板文件

### 1.1 在Linux下创建一个新的空文件

根据生成文件的大小，创建一个256M的镜像文件，其中第一个BOOT分区64M，后面192M用来放根文件系统。如果精打细算的话这两部分都可以再缩小些。不过这只是网卡不能用的临时方案，没必要那么仔细。

```
dd bs=1M if=/dev/zero of=~/emmc_template.img count=256
```

### 1.2 查看开发机上的Loop设备

```
df -h
```

然后找一个空的loop号备用。Ubuntu下会看到好多Loop设备，九成九是被镜像服务snapd给占了。这服务没什么用，把它卸载掉就可以愉快地使用loop0了。具体卸载方法自己搜。

### 1.3 把文件模板挂载到loop设备上

losetup这个命令的作用就是把文件伪装成块设备。

```
sudo losetup /dev/loop0 ~/emmc_template.img
```

### 1.4 使用分区命令fdisk来对镜像文件分区

执行命令fdisk，进入fdisk的交互模式

```
sudo fdisk /dev/loop0
```

这部分内容其实跟xilinx官网的教程一模一样，只不过官网搞的是SD卡，咱们搞的是个镜像文件。

#### 1.4.1 创建第一个分区，并设置成DOS的启动分区

依次输入如下命令，创建第一个分区。
其中的2048是default值，可以直接敲回车。稍微解释一下63M的来历：因为分区表刚好占了1M，这样分让BOOT分区和分区表一起占64M，取整数便于计算。

```
n
p
1
2048
+63M
```

将刚创建的分区改成FAT32类型

```
t
c
```

再为这个分区增加引导属性

```
a
```

#### 1.4.2 创建第二个分区

第二个分区是linux分区，除了一个p以外没什么可说的。

```
n
p
2
[回车]
[回车]
```

#### 1.4.3 保存退出

这一步执行结束会报警告，说分区表无法重新读取，你本来也没用它的分区表，无视即可。

```
p
w
```

### 1.5 使用分区命令fdisk来对镜像文件分区

挂载镜像文件系统并格式化。之前的losetup命令只能到块设备一步，不能进一步读取分区表，所以要换成kpartx这个武器。

```
sudo kpartx -av ~/emmc_template.img
```

执行成功后，会出现挂载了两个loopXpY的提示。如果像前面例子一样操作的是loop0，那么出现的就是loop0p1和loop0p2。

### 1.6 分别格式化BOOT分区和rootfs分区

第二条命令有人说会不到，我没有遇到。遇到的人说可以上/usr/sbin下面找一下。

```
sudo mkfs.vfat -F 32 -n BOOT /dev/mapper/loop0p1
sudo mkfs.ext4 -L rootfs /dev/mapper/loop0p2
```

至此创建了两个分区，这个文件跟SD卡长得一样了，第一个坑绕过去了。
※ 注意，如果只有一个工程，可以在这一步后面直接向两个分区内拷贝文件。我使用的时候因为要用到多个工程，所以保留了一份空模板。

### 1.7 解除文件挂载

```
sudo kpartx -dv /dev/loop0
```

### 1.8 解除loop挂载

```
sudo losetup -d /dev/loop0
```

步骤1的内容在开发机上只需要执行一次。

## 2.编译并制作镜像

工程创建、编译的事情官网都有详细说明，就不再细说了。

### 2.1 编译

执行

```
cd <$proj>/images/linux/
petalinux-build
petalinux-package --boot --format BIN --fsbl zynqmp_fsbl.elf --u-boot u-boot.elf --pmufw pmufw.elf --fpga *.bit --force
```

下列编译出的文件，以及**所有的.elf**文件都会在下一步用到，把他们拷贝到Vitis服务器上的某目录<$dest>下备用。（我用的是Windows版Vitis）
BOOT.BIN
boot.scr
bootgen.bif
image.ub
system.dtb

### 2.2 制作镜像

#### 2.2.1 拷贝模板到当前目录

```
rm -rf emmc.img
cp ~/emmc_template.img ./emmc.img
```

#### 2.2.2 创建两个挂载点

开发机上只需要执行一次

```
sudo mkdir /mnt/imgboot/
sudo mkdir /mnt/imgrootfs/
```

#### 2.2.3 挂载文件镜像到文件系统

```
sudo kpartx -av emmc.img
```

#### 2.2.4 挂载分区

```
sudo mount /dev/mapper/loop0p1 /mnt/imgboot/
sudo mount /dev/mapper/loop0p2 /mnt/imgrootfs/
```

#### 2.2.5 把文件搞到对应的分区去

boot分区是拷贝，rootfs是解包，注意解包有个参数大C。

```
sudo cp BOOT.BIN /mnt/imgboot/
sudo cp image.ub /mnt/imgboot/
sudo cp boot.scr /mnt/imgboot/
sudo tar -zxvf ./rootfs.tar.gz -C /mnt/imgrootfs/
```

※ 想搞些自己开发的应用和测试程序也可以在这个位置搞，拷贝到/mnt/imgrootfs/下即可。

#### 2.2.6 解除挂载

```
sudo umount /dev/mapper/loop0p1
sudo umount /dev/mapper/loop0p2
sudo kpartx -d emmc.img
```

然后把这个emmc.img也拷贝到Vitis那头备用。

## 3.烧写image

基于xsa文件创建一个Vitis的Hello World工程。我们不用它，只是借用它生成的调试环境。连好JTAG线和串口0。

### 3.1 JTAG启动

把下面的文件存成名为jtagboot.tcl的文本文件，放到前面提到的<$dest>目录下。

```
#Disable Security gates to view PMU MB target
targets -set -filter {name =~ "PSU"}

#By default, JTAGsecurity gates are enabled
#This disables security gates for DAP, PLTAP and PMU.
mwr 0xffca0038 0x1ff
after 500

#Load and run PMU FW
targets -set -filter {name =~ "MicroBlaze PMU"}
dow pmufw.elf
con
after 500

#Reset A53, load and run FSBL
targets -set -filter {name =~ "Cortex-A53 #0"}
rst -processor
dow zynqmp_fsbl.elf
con

#Give FSBL time to run
after 5000
stop

#Load DTB
#就是这一步最坑!从某版本开始加载U-BOOT前必须先把设备树下载到0x100000。
dow -data "system.dtb" 0x100000

#Other SW...
dow u-boot.elf
dow bl31.elf
con
```

基板设成JTAG启动模式并上电。
在Vitis的xsct窗口先执行

```
cd <your_drive>/<$dest>
```

注意斜线是Linux格式

然后执行

```
source jtagboot.tcl
```

脚本执行结束后，**串口**上会出现boot的倒计时。此时一定要在串口上按回车。

### 3.2 下载镜像文件到基板

走JTAG线，所以还是在xsct窗口里执行

```
dow -data emmc.img 0x2A00000
```

最后那个参是内存地址。2A00000并没有什么特别的意义，只是一个不太小不太大的值。

### 3.3 烧写镜像到emmc

上一步比较慢，我的环境大概需要大于20分钟。提示到100%之后，在串口执行下面命令，把内存的内容写到eMMC上。数字参分别是内存地址，eMMC目标起始地址，block数。block数=字节数/512

```
mmc write 0x2A00000 0 80000
```

这一步完成后，切换到eMMC启动即可。

## 4 只更新操作系统

JTAG烧写实在是慢，如果在开发初始阶段需要频繁烧写内核，可以只烧前面64M。

### 4.1 分割镜像文件

利用Linux下的dd命令，取生成emmc.img的前64M。

```
dd bs=1M if=emmc.img of=sdboot.img count=64
```

仍旧拷贝到Vitis服务器。

### 4.2 JTAG启动

同3.1

### 4.3 下载boot分区到基板

只是文件名不一样

```
dow -data sdboot.img 0x2A00000
```

### 4.4 烧写镜像到emmc

只有最后的块大小不一样。

```
mmc write 0x2A00000 0 20000
```

完。