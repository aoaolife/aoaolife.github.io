---
title: "CVS在FC4上的配置 – aoao.life"
date: 2021-07-04 21:37:35
---

FC4上已经自带好了CVS，我们要做的只是对它进行配置。

1． 编辑/etc/xinet.d/cvs 文件，它的主要内容包括

```
service cvspserver

{
disable = no
port                    = 2401
socket_type             = stream
protocol                = tcp
wait                    = no
user                    = root
passenv                 = PATH
server                  = /usr/bin/cvs
env                     = HOME=/var/cvsroot
server_args           = -f –allow-root=/var/cvsroot pserver
#       bind                    = 127.0.0.1
}
```

其中 server_args中有两个参数，一个是源代码库的位置，一个是认证方式。一般认证方式不需要改，需要动的是源码库的位置。另外需要自己添加一下env的内容。其余的选项基本不用动。当有超过一个库需要建的时候，在server_args行添加。比如server_args = -f –allow-root=/var/cvsroot –allow-root=/var/cvsroot2 pserver 即可。这个文件的名字（cvs）其实是可以随便起的。

2． 重新启动xinetd服务，CVS就启动了
开启一个终端，登陆后运行$export CVSROOT=:pserver:cvs@192.168.100.90:2401 var/cvsroot
$cvs login
输入密码，没有出错提示表示登陆成功。

3． 建立一个cvsroot用户，一个cvs组。将CVSROOT的用户和组设成cvsroot.cvs，权限777。

4． 建立各个项目组的用户组和管理员。用户设置为不可登陆。

5． 此时可以分别建立各个项目的库。采用winCVS工具导入的方式进行上传。上传后，对不同的项目加以区别。例如linux项目，根目录的用户和用户组就是cvslinux.cvslinux，权限755。大多数目录的用户和用户组都是cvslinux，权限755。所有用户都可以进行操作的目录，权限设为775。不希望其他组看到的内容，权限设成750。

**cvs中默认一个用户checkout代码时候，会在当前模块下生成一个锁文件，如果这个用户对当前模块没有写权限，读是不可能的。配合上面的权限设置，必须改一下cvs服务器配置。改成不在当前模块目录下生成锁文件，把锁文件集中到一个所有用户都有读写权限的目录。修改配置文件CVSROOT/config：
# Put CVS lock files in this directory rather than directly in the repository.
#LockDir=/var/lock/cvs
把LockDir之前的注释取消就可以了。