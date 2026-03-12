---
title: 闲话OAUTH | aoao.life
date: 2018-12-01 09:24:49
updated: 2026-03-01 06:20:12
---

作为一面全栈工程师(偏重前端)，对待老大交代下来的后端任务也是需要认真完成的。前段时间，有个工作，要通过淘宝的OAUTH进行授权，进而获取到access\_token，通过access\_token来作为授权码，进行所有需要登录权限的API访问，这些API 包括但不限于用户，商品，交易，评价，物流等API.

## 过程

在这里也无须去科普OAUTH2.0协议到底是什么了,感兴趣的可以自己去查wiki.

我来说的仍然是我自己的理解,所以OAUTH到底做了什么呢?它是一直验证机制,这个机制实现了两步验证,仍然以淘宝API获取access\_token为例,淘宝认为开发者访问用户的信息,是以应用为单位的,每一个应用需要一个app\_id,app\_secret,我们是先要通过app\_id 来置换到一个叫做code的字段,这个字段只是作为一个过渡,我们能够通过code值,再调取一个api,才能够最终获取到access\_token.

拿实际例子来说,

**、授权操作步骤**

    此处以正式环境获取acccess\_token为例说明，如果是沙箱环境测试，需将请求入口地址等相关数据换成沙箱对应入口地址，操作流程则同正式环境一致。  
    实际进行授权操作时，测试的数据 client\_id、client\_secret、redirect\_uri 均需要根据自己创建的应用实际数据给予替换，不能拿示例中给出的值直接进行测试，以免影响实际测试效果。下图为Server-side flow 授权方式流程图，以下按流程图逐步说明。  
![授权步骤](http://upload-images.jianshu.io/upload_images/48180-daa679ca3643bb11.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**1）拼接授权url**  
拼接用户授权需访问url ，示例及参数说明如下：  
<https://oauth.taobao.com/authorize?response_type=code&client_id=23075594&redirect_uri=http://www.oauth.net/2/&state=1212&view=web>

| 参数说明 |
| --- |
| 名称 |
| client\_id |
| response\_type |
| redirect\_uri |
| state |
| view |

**2）引导用户登录授权**  
引导用户通过浏览器访问以上授权url，将弹出如下登录页面。用户输入账号、密码点“登录”按钮，即可进入授权页面。  
![授权](http://upload-images.jianshu.io/upload_images/48180-bdff42029bd50cbc.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**3）获取code**  
上图页面，若用户点“授权”按钮后，TOP会将授权码code 返回到了回调地址上，应用可以获取并使用该code去换取access\_token；  
若用户未点授权而是点了“取消”按钮，则返回如下结果，其中error为错误码，error\_description为错误描述。分别如下图所示：![错误](http://upload-images.jianshu.io/upload_images/48180-784ed87b1c50d9ea.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**4）换取access\_token**

方式1（推荐）：

通过taobao.top.auth.token.create api接口获取access\_token（授权令牌）。api服务地址参考[http://open.taobao.com/docs/doc.htm?docType=1&articleId=101617&treeId=1](http://open.taobao.com/docs/doc.htm?spm=a219a.7386781.3.7.tO1lHe&docType=1&articleId=101617&treeId=1)

## 最后

说起来,我最早使用OAUTH进行登录或者授权操作,还是早些年在用微博的时候,如果OAUTH的应用已经非常广泛了,了解它对我们,无论前端开发还是后端开发都有很多好处.

# 参考链接

<http://open.taobao.com/doc.htm?docId=102635&docType=1>

<http://open.taobao.com/api.htm?docId=285&docType=2>