---
title: docker笔记 | aoao.life
date: 2021-02-28 11:41:16
updated: 2026-03-01 06:20:12
---

[玩转Dockerの第一弹，入门篇。原理及背景知识](https://www.youtube.com/watch?v=isr6cPKy8eg&pbjreload=102)

这个视频带我入门

# 我用到的一些常用命令

## docker pull

|  |  |
| --- | --- |
| ``` 1 2 ``` | ``` docker pull user/repo ``` |

拉取镜像，这里要注意国内源可能很慢，需要换源

## docker build

本地测试，需要进行docker build 生成image

## docker images

查看生成的docker image

## docker rm vs docker image rm

前者是移除容器，如果容器在运行当中，可以使用docker rm container\_id -f 的命令。 后者是移除镜像。后者也可以简写为 `docker rmi`

移除所有的没有用到的image 镜像：

<https://stackoverflow.com/questions/33913020/docker-remove-none-tag-images>

|  |  |
| --- | --- |
| ``` 1 2 ``` | ``` docker rmi $(docker images --filter "dangling=true" -q --no-trunc) -f ``` |

那么又为什么会出现none镜像呢？

<https://stackoverflow.com/questions/53221412/why-the-none-image-appears-in-docker-and-how-can-we-avoid-it>

## docker run options

### –restart 简写-r

There are four restart policies you can choose from — Off, On-failure, Unless-stopped, and Always. As the terms state, ‘Off’ means that the container won’t be restarted if it fails or stops. ‘On-failure’ ensures the container restarts only in the case of a failure that’s not caused by the user. ‘Unless-stopped’ restarts the container only when any user executes a command to stop the container, not when it fails because of an error. ‘Always’ restarts the container whether the it’s caused by an error, or is executed by a user, or if Docker is restarted.

### –volume简写 -v

卷的概念要清楚

local\_path:docker\_path

对path进行映射

### –port 简写 -p

端口号进行映射

### –name 简写 -n

给docker 容器起一个名字，便于以后进行管理

## docker ps

查看所有容器的状态，包括容器名称，id，运行时常，运行状态等等。

### 踩坑

<https://stackoverflow.com/questions/37471929/docker-container-keeps-on-restarting-again-on-again/37473466>

容器一直重启

一个原因是容器设置了restart选项为always。 而容器又发生了错误，根本起不来，于是就陷入了往复重启之中。我自己遇到的问题，就是我的容器，在build的时候，只支持了x86平台，而不支持ARM平台，导致在我的笔记本上容器能够跑起来，但是在我的另外一台机器上，就跑不起来容器，一直重启。这个时候，需要注意的是，由于我当时给容器设置的选项是后台run，不看日志，所以一直处于一脸懵逼的状态，直到我把容器在前台启动，才显示错误日志，通过错误日志才发现原来是因为build平台有问题。

如果想要看docker log可以运行：

|  |  |
| --- | --- |
| ``` 1 ``` | ``` docker logs --tail 50 --follow --timestamps mediawiki_web_1 ``` |

<https://stackoverflow.com/questions/59000007/standard-init-linux-go207-exec-user-process-caused-exec-format-error>

看起来是因为build的系统不同引起的。

## docker help

### docker run –help

对于每一个子的功能，都可以通过docker xxx –help查看详细的使用说明

查看帮助信息

# 使用docker 镜像

需要注意，一定要看支持的OS的架构，一般来说如果你的机器是X86架构，那么一般的web应用应该都能支持，这个时候你需要注意的是那些Loi，也就是物联网应用是否支持。同理，如果你的机器是ARM架构的，你需要看那个web应用是否支持ARM。

我们可以在dockerhub上很方便地查看到这些信息。如果支持x86，会标注linux/amd64。如果支持ARM，会标注linux/arm64。

如果是我们自己编译build image，更需要注意这一点了

通过GitHub actions编译，可以使用v2，带platforms参数的actions进行编译。

# 使用watchtower 自动更新container

<https://containrrr.dev/watchtower/arguments/#poll_interval>

docker run –run-once -d   
 –name watchtower2   
 -v /var/run/docker.sock:/var/run/docker.sock   
 containrrr/watchtower

|  |  |
| --- | --- |
| ``` 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 ``` | ``` Scheduling¶ Cron expression in 6 fields (rather than the traditional 5) which defines when and how often to check for new images. Either --interval or the schedule expression can be defined, but not both. An example: --schedule "0 0 4 * * *"  Argument: --schedule, -s Environment Variable: WATCHTOWER_SCHEDULE Type: String Default: -   Poll interval¶ Poll interval (in seconds). This value controls how frequently watchtower will poll for new images. Either --schedule or a poll interval can be defined, but not both.  Argument: --interval, -i Environment Variable: WATCHTOWER_POLL_INTERVAL Type: Integer Default: 86400 (24 hours) ``` |

如果想要立刻更新某个容器，可以使用：

|  |  |
| --- | --- |
| ``` 1 2 3 4 ``` | ``` docker run --rm \     -v /var/run/docker.sock:/var/run/docker.sock \     containrrr/watchtower \     --run-once \ ``` |