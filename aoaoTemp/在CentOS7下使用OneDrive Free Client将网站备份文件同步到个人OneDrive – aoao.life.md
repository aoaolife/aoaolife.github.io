---
title: "在CentOS7下使用OneDrive Free Client将网站备份文件同步到个人OneDrive – aoao.life"
date: 2023-11-09 15:48:38
---

标题应该能说明想干嘛了是吧？注意，这里的“OneDrive Free Client（https://github.com/abraunegg/onedrive）”是个特指，是一个开源的Linux下访问巨硬OneDrive的工具。
这玩意儿安装起来颇费周折，故此撰文记录一下。
首先，这个工具有两个开发者。原开发者skilion（https://github.com/skilion/onedrive）2021年后放弃了维护，转而被abraunegg（https://github.com/abraunegg/onedrive）接手继续开发。但是A君的文档写得实在是乱七八糟，我到原库查看了S君的文档，才顺利地装了下来。
总之就是玩这个东东，开始的安装和授权相当麻烦，后面的配置和启动都不值一提。

## 安装

※可能是使用D语言开发的缘故，本工具需要编译安装，不同Linux发行版的编译环境的配置方法不同，这里只写CentOS7 的，其余版本的编译环境安装方法请自行在官网文档（https://github.com/abraunegg/onedrive/blob/master/docs/INSTALL.md）里查找，大同小异。

### 安装编译环境

```
sudo yum groupinstall 'Development Tools'
sudo yum install libcurl-devel sqlite-devel
curl -fsS https://dlang.org/install.sh | bash -s dmd-2.099.0
```

除libcurl-devel和sqlite-devel外，如果提示少啥库就装啥库，

### 下载代码、编译、安装

```
git clone https://github.com/abraunegg/onedrive.git
cd onedrive
#使用编译需要的环境变量
source ~/dlang/dmd-2.099.0/activate
./configure
make clean; make;
sudo make install
#恢复原始环境变量
deactivate
```

这里的“2.099.0”，就是上一步安装的dmd的版本，不同的版本需要根据官网的说明进行替换。
因为这玩意儿卸载的时候也要make，所以建议代码留着别删。

### 在个人账户下给此APP授权访问

Linux控制台下，不带参数运行onedrive，窗口上会给出一个访问链接。把Authorize this app visiting:后面的内容复制粘贴到浏览器。

```
onedrive
Configuring Global Azure AD Endpoints
Authorize this app visiting:

#复制控制台上的下面这个链接↓↓↓
https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx&scope=Files.ReadWrite%20Files.ReadWrite.All%20Sites.ReadWrite.All%20offline_access&response_type=code&prompt=login&redirect_uri=https://login.microsoftonline.com/common/oauth2/nativeclient

Enter the response uri:
```

访问后会要求输入你的onedrive账号和密码。之后弹出是否同意此APP访问账户的窗口，选同意。
![onedrive_app_auth](./images/4758d248ed40df564cd149201610d2ac.png)
同意后**浏览器上一片空白**，但是邮箱里会收到一封确认信。我安装时卡在这里好久，完全看不出已经可以继续了。此时把白屏的地址栏上的内容复制下来备用。
什么？你没有账号和密码？那把这篇博文叉了吧。

回到Linux控制台，在Enter the response url: 后面粘贴上刚才复制的内容，回车

```
Configuring Global Azure AD Endpoints
Authorize this app visiting:

https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx&scope=Files.ReadWrite%20Files.ReadWrite.All%20Sites.ReadWrite.All%20offline_access&response_type=code&prompt=login&redirect_uri=https://login.microsoftonline.com/common/oauth2/nativeclient

#把浏览器上的链接粘贴到冒号后面↓↓↓
Enter the response uri: https://xxxxxxxxxxxxxxxxxx

Application has been successfully authorised, however no additional command switches were provided.

Please use 'onedrive --help' for further assistance in regards to running this application.
```

OK，至此最离谱的部分都过去了。
此时其实已经可以用了，什么都不改，执行同步命令，你的OneDrive就会跟~/OneDrive血脉相连了。但这还不够，因为我只想上传网站备份，在linux上保留整个onedrive毫无必要。所以接下来要对默认配置进行修改。

## 配置

### 配置文件

使用默认配置是不需要配置文件的。但要修改配置的话，需要先下载配置文件。（呃，其实也可以完全手搓）
下载到下面两个位置都可以生效。
~/.config/onedrive/
/etc/onedrive/
默认这两个文件都是不存在的，想修改默认配置的时候再创建它们即可。
因为上传备份这件事只能以root身份运行，所以这里这两个位置也没差多少。如果多用户公用服务器的话，当然是各人配各人的。

### 下载配置文件

```
mkdir -p ~/.config/onedrive
wget https://raw.githubusercontent.com/abraunegg/onedrive/master/config -O ~/.config/onedrive/config
```

### 编辑配置文件

```
vim ~/.config/onedrive/config
```

找到”sync_dir”字段，去掉前面的“#”号，并改成备份文件所在的**上一级目录**。对于bt面板来说，备份目录是”/www/backup”。为了数据安全，当然可以另存到其它位置。不过那样还需要另外启cron进行搬运，对我来说太麻烦了。
另外我还修改了监视时间。网站一天备份一次，默认的300秒对我来说太频繁了，根本用不上。
还有一个monitor_fullscan_frequency，是全盘同步频率，乘以monitor_interval得到的是扫整个folder的时间间隔。现在的使用场景根本不需要作全盘同期，所以随便改改就好，我这里给监视时间设成4小时，全盘同期设成了12小时。
另外还有很多项目可以设，对我来说没需要，看都没看。有需要的在这里（https://github.com/abraunegg/onedrive/blob/master/docs/USAGE.md#the-default-configuration-file-is-listed-below）自己查。

`#sync_dir="~/OneDrive"
sync_dir = "/www"
#monitor_interval="300"
monitor_interval="14400"
# monitor_fullscan_frequency = "12"
monitor_fullscan_frequency = "3"`

### 创建同步文件列表

此软件提供了单独的文件列表功能，如果创建了此列表，则【只】同步此列表中出现的内容。这正是我想要的。也正是因为有这个功能，上面才会把同步文件夹指定到备份目录的上一级目录。

```
vim ~/.config/onedrive/sync_list
```

配置文档（https://github.com/abraunegg/onedrive/blob/master/docs/USAGE.md#performing-a-selective-sync-via-sync_list-file）上写得很清楚，就不解释了。这里只要同步database和site这两个目录就够了
`/backup/site/*.tar.gz
/backup/database/*.sql.gz`

至此，配置完成。

## 测试及初次运行

先“空跑”一下，根据log判断是否是自己想要的配置。

```
onedrive --synchronize --verbose --dry-run --resync
```

注意，每次修改了configure中的sync_dir，skip_dir，skip_file，drive_id，或者sync_list的话，要加上”–resync”这个参数。

配置无误的话，去掉”–dry-run”进行首次同步

```
onedrive --synchronize --verbose --resync
```

查看一下个人目录，会发现备份文件已经咔咔上传了。

## 服务

注意：启动服务之前，一定要成功地先进行过至少一次手动执行命令；如果改动了上文提到的configure或者sync_list，一定要执行过resync，否则服务无法成功启动。

### 启动

```
systemctl start onedrive
```

### 开机自启动

```
systemctl enable onedrive
```

stop，restart，disable，status也一样，玩服务器的都懂，就不废话了。

## 命令

命令列表（https://github.com/abraunegg/onedrive/blob/master/docs/USAGE.md#all-available-commands）里啥都有。列几个用得到的。

### 查看配置

```
onedrive --display-config
```

### 执行同步

```
onedrive --synchronize
```

显示详细加 –verbose，空跑加–dry-run，重新全部同期加–resync

### 只同步某个目录

```
onedrive --synchronize --single-directory 'dir_name'
```

### 只下载

```
onedrive --synchronize --download-only
```

### 只上传

```
onedrive --synchronize --upload-only
```

## 反安装

这个必须要提一下，因为这货反安装也需要make。
记得安装时建议保留原代码不？这里用到。删了也行，重新下呗。

```
cd onedrive
source ~/dlang/dmd-2.099.0/activate
sudo make uninstall
deactivate
rm -f ~/.config/onedrive/refresh_token
```

以上。这下我再也不用担心服务器供应商跑路了。