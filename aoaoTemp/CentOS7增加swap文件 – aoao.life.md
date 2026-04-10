---
title: "CentOS7增加swap文件 – aoao.life"
date: 2017-07-20 12:53:56
---

创建Linos虚拟机的时候选择了默认，使用VestaCP的时候又用了默认。
两个默认导致1G内存吃紧，MySQL经常因为申请不到空间而挂掉，而MySQL的监视线程就会去重启MySQL，重启时内存仍旧不足，就此挂掉。
尝试了好多办法缩减https和mySQL服务所占用的内存，有好用的有不好用的，总之杯水车薪。

既然节流不行，那就换个思路试试开源吧。关键字一搜，果然CentOS增加swap文件是非常方便的。
所以这是一个说穿了一文不值的解决方案。

1.用命令查看你的内存和扩展分区是不是不够用

```
swapon -s
free -m
```

够用了非要加也没人拦着。

2.查看硬盘空间

```
df -h
```

3.创建SWAP文件

```
sudo fallocate -l 1G /swapfile
```

1G是大小，按需。创建到根下。

4.把文件转成SWAP

```
sudo chmod 600 /swapfile
```

```
sudo mkswap /swapfile
```

```
sudo swapon /swapfile
```

可以用

```
free -m
```

验证是否创建成功

5.固定文件
上面创建的文件在重启以后需要重新转换，所以要在启动的时候添加选项

```
sudo vi /etc/fstab
```

在最后增加

```
/swapfile   swap    swap    sw  0   0
```

大功告成！