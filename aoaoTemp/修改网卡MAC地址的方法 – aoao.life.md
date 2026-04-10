---
title: "修改网卡MAC地址的方法 – aoao.life"
date: 2022-01-09 23:56:59
---

◆Windows2000/XP 的修改
1 、在 HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\
{4D36E972-E325-11CE-BFC1-08002BE10318}\0000 、 0001 、 0002 等主键下，
查找 DriverDesc ，内容为你要修改的网卡的描述，如“ Realtek RTL8029(AS)-based PCI Ethernet Adapter ”。
2 、如果在0001下找到了1中的DriverDesc ,在其下，添加一个字符串，命名为 NetworkAddress ，其值设为你要的 MAC 地址（注意地址还是连续写）。
如： 00E0DDE0E0E0 。

3 、然后到其下 Ndi\params 中添加一项名为 NetworkAddress 的主键，在该主键下添加名为 default 的字符串，
其值是你要设的 MAC 地址，要连续写，如： 000000000000 。（实际上这只是设置在后面提到的高级属性中的“初始值”，
实际使用的 MAC 地址还是取决于在第 2 点中提到的 NetworkAddress 参数，这个参数一旦设置后，
以后高级属性中的值就是 NetworkAddress 给出的值而非 default 给出的了。）

4 、在 NetworkAddress 的主键下继续添加名为 ParamDesc 的字符串，其作用为指定 NetworkAddress 主键的描述，
其值可自己命名，如“ Network Address ”，这样在网卡的高级属性中就会出现 Network Address 选项，
就是你刚在注册表中加的新项 NetworkAddress ，以后只要在此修改 MAC 地址就可以了。继续添加名为 Optional 的字符串，
其值设为“ 1 ”，则以后当你在网卡的高级属性中选择 Network Address 项时，右边会出现“不存在”选项。

5 、重新启动你的计算机，打开网络邻居的属性，双击相应网卡项会发现有一个 Network Address 的高级设置项，
可以用来直接修改 MAC 地址或恢复原来的地址(选中不存在)。

◆ Win9x 的修改

1 、在 HKEY_LOCAL_MACHINE\system\Currentcontrolset\services\class\net\0000 、 0001 、 0002 等下，
找到 DriverDesc 字符串。

2 、在其下，添加一个字符串，名字为 NetworkAddress ，其值设为你要的 MAC 地址，注意要连续写。如： 00E0DDE0E0E0 。

3 、然后到其下 Ndi\params 中添加一项名为 NetworkAddress 的主键，在该主键下添加名为 default 的字符串，
其值写你要设的 MAC 地址，注意要连续的写，如 00E0DDE0E0E0 。

4 、继续添加名为 ParamDesc 的字符串，其作用为指定 NettworkAddress 主键的描述，其值可自己命名，
如“ Network Address ”，这样以后打开网络邻居的属性，这样在网卡的高级属性中就会出现 Network Address 选项，
就是你刚在注册表中加的新项 NetworkAddress ，以后只要在此修改 MAC 地址就可以了。

继续添加名为 Optional 的字符串，其值设为“ 1 ”，则以后当你在网卡的高级属性中选择 Network Address 项时，
右边会出现“没有显示”选项。

◆ WinNT 下改网卡地址的方法：

1 、打开注册表，定位到 HKEY_LOCAL_MACHINE->SYSTEM->CurrentControlSet->Services

2 、找到网卡的键值，在 Parameters 项里添加字串值 NetworkAddress ，其值设为你要修改的 MAC 地址，
如：“ 00E0DDE0E0E0 ”。