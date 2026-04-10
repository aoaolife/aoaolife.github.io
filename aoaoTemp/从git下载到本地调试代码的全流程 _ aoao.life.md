---
title: 从git下载到本地调试代码的全流程 | aoao.life
date: 2016-12-02 11:18:49
updated: 2026-03-01 06:20:12
---

安装git  
安装node

# 安装

git clone

进入项目文件夹

由于在git上不止有一个分支（branch），主分支（master）存放稳定版本的代码，开发(develop)分支存放正在开发中的代码，因此需要先切换分支到develop分支

在当前项目目录下执行

|  |  |
| --- | --- |
| ``` 1 ``` | ``` git checkout develop ``` |

当看到命令行目录出现

|  |  |
| --- | --- |
| ``` 1 ``` | ``` （develop） ``` |

则表示已经完成切换分支。

下载node的依赖模块

|  |  |
| --- | --- |
| ``` 1 ``` | ``` npm install ``` |

如果下载没有速度，不能完成下载，使用cnpm，替换cnpm，方法：

|  |  |
| --- | --- |
| ``` 1 ``` | ``` npm install -g cnpm --registry=https://registry.npm.taobao.org ``` |

详细介绍：<https://npm.taobao.org/>

npm install 完成之后

|  |  |
| --- | --- |
| ``` 1 ``` | ``` npm start ``` |

待出现

|  |  |
| --- | --- |
| ``` 1 ``` | ``` webpack:bundle build is now finished ``` |

浏览器打开：

|  |  |
| --- | --- |
| ``` 1 ``` | ``` http://localhost:8989 ``` |

这时候已经可以进行本地代码调试了。

# 提交代码

在当前项目目录下执行操作

|  |  |
| --- | --- |
| ``` 1 2 ``` | ``` git add . ``` |

将代码改动缓存区

|  |  |
| --- | --- |
| ``` 1 ``` | ``` git commit -n ``` |

进入vi编辑器界面，进行添加commit信息

按下 insert键，切换到可输入状态

这个时候可以添加commit信息

按下ESC键，切换为功能选择状态

这个时候 :wq 或者 ZZ  
保存了 commit 信息，并且推出了vi编辑器界面  
(更多vi命令操作:[vi命令大全](http://www.cnblogs.com/88999660/articles/1581524.html) )

执行：

|  |  |
| --- | --- |
| ``` 1 ``` | ``` git pull ``` |

将远程代码拉取到本地，如果发现有冲突，则进行合并

最后将代码提交到develop分支上

|  |  |
| --- | --- |
| ``` 1 ``` | ``` git push origin develop ``` |

更多git 操作：[Git教程](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/)

# 项目结构

项目页面的代码存放在 src文件夹内

src/routes/Home/components 文件夹内是我们经常要改动的组件

各个文件的具体功能见 **文件内注释** 或 **自行理解** 或 **联系本人** :blush:

# react 及ant design 相关学习资料

- [react技术栈教程](http://www.ruanyifeng.com/blog/2016/09/react-technology-stack.html)
- [antd 文档](https://ant.design/docs/react/introduce)

# 其他

- 推荐使用sublime text3 ,atom,webstorm 等编辑器，它们通过安装对应的babel,jsx插件，能够更好的支持es6，jsx语法。