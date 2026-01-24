---
title: AI图片生成

date: 2025-09-26
updated: 2025-09-26 12:00:00
---
谷歌发布了图像模型 Gemini 2.5 Flash Image（项目名 [Nano Banana](https://aistudio.google.com/models/gemini-2-5-flash-image)）。

![](https://img.aoao.life/bg2025091305.webp)

谷歌称它是目前“**最先进的图像生成和编辑模型**”。

我试用后，感觉确实很强，而且免费使用，打开[官网](https://aistudio.google.com/prompts/new_chat?model=gemini-2.5-flash-image-preview)（下图）就能用。

![](https://img.aoao.life/bg2025092111.webp)

（备注：如果你访问不了官网，周刊讨论区也有接入官方 API 的[第三方网站](https://github.com/search?q=repo%3Aruanyf%2Fweekly+nano+banana&type=issues)，不过大部分要收费。）

对于这个模型，网友发现了各种神奇的用法，有人甚至收集成了一个 [Awesome 仓库](https://github.com/PicoTrex/Awesome-Nano-Banana-images)。

![](https://img.aoao.life/bg2025092113.webp)

我从这个仓库里面，挑了几个很实用的例子，分享给大家。需要说明的是，我想其他图像模型也能做这些事，大家可以试试。

### （1）人像处理

图像模型的最常见任务，一定是人像处理。我们先上传一张生活照片。

![](https://img.aoao.life/bg2025091308.webp)

然后，让模型将其转成证件照，提示词如下。

> 请为照片里面的人物生成1寸证件照，要求白底，职业正装，睁眼微笑。

![](https://img.aoao.life/bg2025091309.webp)

这个效果有点惊人啊。它意味着，人物的表情、发型、妆容、服饰、姿势都是可以改变的。

下面就是改变人物表情，让其侧脸对着镜头微笑。

![](https://img.aoao.life/bg2025091319.webp)

![](https://img.aoao.life/bg2025091320.webp)

改变人物的姿势，“将下面第二张图片的人物，改成第一张图片的姿势。”

![](https://img.aoao.life/bg2025091316.webp)

![](https://img.aoao.life/bg2025091317.webp)

![](https://img.aoao.life/bg2025091318.webp)

照相馆以后危险了，肖像照、旅游照、集体照都可以交给 AI 了。

### （2）建筑处理

图像模型的另一个用途是家居装潢，要看家装效果图就让 AI 生成，更改装潢配色和家具，都是小 case。

下面是一个难度更高的例子，上传一张户型图，让它变成 3D 模型渲染图。

![](https://img.aoao.life/bg2025091310.webp)

![](https://img.aoao.life/bg2025091311.webp)

从照片提取建筑模型，也挺神奇。

![](https://img.aoao.life/bg2025091323.webp)

![](https://img.aoao.life/bg2025091324.webp)

### （3）包装处理

下面，让模型更改物品的包装，“将图二的漫画形象，贴到图一的包装盒，生成一张专业的产品照”。

![](https://img.aoao.life/bg2025091313.webp)

![](https://img.aoao.life/bg2025091314.webp)

![](https://img.aoao.life/bg2025091315.webp)

![](https://img.aoao.life/bg2025092112.webp)

书籍的封面、软件的包装盒，也可以同样生成。

### （4）地图处理

图像模型的另一个大市场是地图应用（地理信息），只不过还没想到可以收费的玩法。下面就是一个创新的用例。

上传一张地图，上面用箭头标注你选定的地点，让模型“生成沿着红色箭头看到的场景。”

![](https://img.aoao.life/bg2025092114.webp)

![](https://img.aoao.life/bg2025092115.webp)

它甚至可以从地形等高线图，生成红色箭头处的实景图。

![](https://img.aoao.life/bg2025091326.webp)

![](https://img.aoao.life/bg2025091327.webp)

<div style="text-align: right;">—— 搬石头砸别人的脚</div>