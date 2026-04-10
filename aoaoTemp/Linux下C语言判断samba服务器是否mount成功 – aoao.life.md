---
title: "Linux下C语言判断samba服务器是否mount成功 – aoao.life"
date: 2024-01-13 22:06:02
---

最新的项目需要向网络共享服务器定时上传资料。但是客户的网络环境不知道咋配的，mount的执行总是有延时，并且还经常掉线。所以在上传文件之前我必须判断mount的目录是否是一个samba共享目录。
在我的环境下，这个共享文件夹是/mnt/smb/。这个文件夹有如下特性：
1：如果mount成功，它就是共享服务器的根文件夹，否则只是一个普通的Linux文件夹。
2：如果启动时网络有问题，那么fstab的自动mount（cifs方式）会执行失败。
3：fstab不归我管，也就是我没有改变mount时机的权力。
4：如果启动时网络没有问题，而后来断网，那么这个文件夹的仍旧处于挂载状态。所以使用mount命令是走不通的。
查找资料以后，我决定采用ping+判断文件夹文件系统的方法，来判断文件夹是否已经被mount。

## 用ping命令结合popen函数判断网络情况

断网是mount失败的充分非必要条件。之所以要先判断网络联通情况，是因为如果网络是中途切断的，cifs有一个180秒的漫长等待时间。此期间去调用（网络文件夹）的文件系统，也会等到cifs判断网络切断的时间点，才返回一个“网络临时切断”的errno（具体值忘了）。而这个cifs的等待时间以后，再去取网络文件夹的文件系统，就会立即返回Host挂了的errno（具体值也忘了）了。
为了节省这个最多达到180秒的时间，我ping一下不就行了。当然，如果服务器把ICMP给封了，当我没说。

```
static int ping_server(const char* ip_addr)
{
int ret = 0;
if (!ip_addr)
{
return ret;
}
char buffer[1024] = {0};
char str_cmd[MAX_PATH] = {0};
sprintf(str_cmd, "ping -c 1 -W 2 %s", ip_addr);
FILE* pipe = popen(str_cmd, "r");
if (!pipe)
{
printf("exec ping popen failed. ERROR:%d:%s", errno, strerror(errno));
return ret;
}
sleep(1);
int rd = fread(buffer, 1, 1024, pipe);
if (rd <=0)
{
printf("exec ping timeout.");
}
else if( NULL != strstr( buffer, "ttl=" ) )
{
ret = 1;
}
pclose(pipe);
return ret;
}
```

popen函数是个挺有趣的函数，它在stdio.h里就有。作用是起一个process来执行shell命令。跟system相比，它的等待过程更灵活，获取命令在屏幕上的输出内容也更方便。
这里的fread有点魔性。因为我写的ping命令配合参数，意思是ping一次，等待2秒。而我在fread之前只等了1秒。这样，如果断网，我在等待1秒后读取的屏幕内容为空，便可以立刻返回，而不必等待整个ping命令结束。判断接通就很简单了，看输出的内容里有没有“ttl=”的文字，常规操作。

## 用statfs函数判断文件夹文件系统属性

这个函数用起来就有点麻烦了。
首先要引一个系统头文件“sys/vfs.h”。然后里面那些相貌清奇的文件系统的宏定义被一层一层引用，很难找。于是我索性自己重新定义了一下，好孩子千万不要学。
文档在[这里](https://man7.org/linux/man-pages/man2/statfs.2.html)

```
#include <sys/vfs.h>
#ifndef SMB2_MAGIC_NUMBER
#define SMB2_MAGIC_NUMBER     0xfe534d42
#endif
static int is_smb_fs(void)
{
struct statfs fs;
int ret = statfs("/mnt/smb", &fs);

if (0 == ret && (SMB2_MAGIC_NUMBER == fs.f_type))
{
printf(   "check smb dir [mnt/smb] ret = %d status = %llx", ret, fs.f_type);
return 1;
}
return 0;
}
```

## 将上面两个函数封装成进一个函数

```
static int is_smb_folder_connected(const char* ip_addr)
{
if (ping_server(ip_addr))
{
return is_smb_fs();
}
return 0;
}
```

main函数略。
收工。