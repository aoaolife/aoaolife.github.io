---
title: 【PLC】进阶过程中问题梳理 | aoao.life
date: 2015-05-29 07:40:49
updated: 2026-03-01 06:20:12
---

#自动洗衣机的电位器监测水位问题  
由于我们做的是自动洗衣机模型，基本的要求是让洗衣机能够实现流程化工作，之后需要的是接上变频器使洗衣机能够在稳定转速下运行，这时候，我们已经完成到此，下一步就是用电位器来监测水位的变化并将这个模拟量信号通过PLC内部的A/D 转化成数字量在触摸屏上显示出来

可是在实际使用过程中，很多问题不能解释。于是：

加入了一个论坛：中国工控人论坛，发了[这个帖子](http://www.chinakong.com/forum/disp.asp?id=436782&display=1)

> 大家好，这是我在这里的第一个帖子，我是一名在校大学生，现在在用GE的fanuc plc来进行课程设计，我的题目是自动洗衣机。现在遇到的问题是：我希望实现的目标是用5v的电源供电的电位器来监测洗衣机水位的变化，但是我虽然能够通过模拟量输入的模块（ALG600）来将电位器的输出电压给到PLC，但是这个值是一个定值。水位的监测理论上应该是一个变化的值，需要用到传感器，需要用到进水电磁阀，可是怎样来控制，我就不会了。

> 其实最终目的还是用电位器来监测水位变化并将之显示在触摸屏上，谁能够给一个思路呢？

无奈的是，这个论坛实际上并不活跃，我随意翻了翻论坛，就能够很随意地翻到几年前的帖子，每个帖子的回帖寥寥，这与我之前见到的众多讨论激烈的计算机方面相关论坛形成了鲜明的对比。当然，也可能是因为我自己表述的问题，总之，这个帖子到目前为止还没有人回帖。

后来我甚至将洗衣机模块和机械手的模块拆开看，但是却只看到了里面的PCB板，铜线和几个和LEB接在一起的电阻，还有一个小的减速电机，这让我更有理由推测，这个洗衣机的模块内部，是没有传感器这么复杂的东西的。但是问题在于，机械手的程序，说明中提到了传感器，但是看例程，却发现，好像也只是加入了几个TMR的延时block而已。

一个新的设想：既然洗衣机模块内部本身十分简单，它的模拟效果，只是通过LED灯来实现的，比如说是进水，但是其实从你看到角度来说，也只不过是你看到了进水灯亮了而已。它通过用这样的效果来给人模拟的效果。

（20150510）于是，我放弃了用电位器来监测水位的方法，由于我的程序中，用到了计时器TMR tenths，所以可以考虑，将这个值的变化过程在触摸屏上用如柱状图的形式显示出来，看上去就像是在进水。仍然需要验证。

**在这个时候，事实上我还是不太能够理解PLC梯形图中的I0001,I0002这些东东的意义的，我甚至不知道这些是数字量输入信号，I0001就是对应的数字量输入1号插槽，所以实际上到这个时候，梯形图程序我还没有完全看懂，直到后来，我将洗衣机模块和机械手模块连接的时候，才终于意识到原来梯形图中的I,Q这些值是与PLC上的插槽一一对应的**

#洗衣机甩干问题

在接下来的使用过程中，由于同学CLL的设计中加入了我们的洗衣机模块，我才发现，我们一直以来的洗衣机模块的设计都是错误的。我们最初对于洗衣机工作的流程其实并没有清晰的概念，只是经过测试，发现了‘按下启动按钮之后，洗衣机的进水灯开始亮，当再按下上限水位按钮的时候，进水灯灭与此同时，运行的绿色指示灯亮，而当正反转三圈之后，出水指示灯亮，’到了这里，其实是应当按下下限水位按钮的，来使洗衣机进行脱水甩干操作。我们往往是直接按下停止按钮。

我们认为下限水位按钮没有用了，其实并非如此。这也告诉我，磨刀不误砍柴工。当然，我们也一直没能正确理解上限水位和下限水位的概念，这里还是CLL同学告诉的我，因为只是模拟（前面讲过，拆开之后只是简单的电阻和电机），没有传感器，所以需要上下限水位的按钮来操作。

#机械手与洗衣机结合-对I,Q的再次理解

后来，希望将机械手和洗衣机结合起来用。这个时候，发现了一个以前一直没有注意的问题，但却严重影响了我的进度。也就是在最初的时候，我们按照实验指导书来接线，完全不理会PLC的输入，输出规则，而当我们将两个模块结合在一起使用时，就不得不考虑这些了。由于之前的设定中，输入，输出点是有冲突的，所以需要修改这些量。这里还要特别注意的是,我误将I看成了1，也就是说我将数字量输入I1简单地看成了11，于是乎，我开始就不知所措了。后来又在实验指导书上得到启发，才发现我的理解是错误的。于是将冲突的输入输出点，进行了修改。以实现其功能。后来发现，其实不光是I,Q这些属性的变量存在这个问题，就连M,R这些属性的变量也存在这些问题，导致的一个基本的不正常的现象是：当洗衣机模块和机械手模块同时连接到PLC时，发现当按动机械手上某个按钮时，洗衣机模块上某个灯亮，而究其原因，其实就是因为虽然他们是以主程序和子程序的形式显示的，但是他们的变量是统一的，需要对之前单独的变量在重复时做一个修改。

**知识点：从这里跌跌撞撞的学习可以看出，其实我们是在摸索中才理解了M,Q,I,R这些变量地址不能冲突这些知识点的，事实上早就应该想到，但是因为这些意识并不深刻，就像之前提到的共地的概念那样并不深刻，需要经过实践，告诉自己的大脑，看见没，理论正确，就是这么回事。**

另外，已经从DL那里拿到了机械手自动实现的程序，于是就对之进行了修改，本来打算将机械手梯形图作为子程序，将洗衣机梯形图放到main程序里，但实际上，后来经过同学LSH的提示，发现，其实即便是两个模块组合在一个梯形图中，也不过只有3，4十行程序，完全可以省略掉子程序。

于是接下来的工作是，对两者结合的程序进行调理，使之完成我们的需求。也就是：**首先按动控制机械手的自动按钮，使机械手可以自动将衣物送入洗衣机中，这个时候提升或者下降都需要电机的转动作为配合，当机械手即将回到原位时，触发自动洗衣机开始工作，首先进水，然后是正转反转3次，接下来出水，甩干。这样的过程中需要保持模块上各个灯的显示正常，电机转动正常（实际连线之后是接入了6个继电器，4个继电器接机械手模块来控制机械手模块4个输出量接变频器，2个继电器接洗衣机模块来控制洗衣机模块上正转反转的两个输出接变频器）。达到从机械手开始工作到洗衣机完成洗衣机的全过程。当然还有必要保持单独的工作，互不影响，比如只用机械手提取衣物或只用洗衣机来洗衣物，无需机械手的操作**

于是在以上的思想的指引下，开始对梯形图程序进行debug，截至到20150519仍然出现有几个问题，如：

- 将程序下载到梯形图中后，第一次运行正常，第二次运行就乱了。  
  设想：由于程序做了很大的改动，缺少复位清零，导致在第一次运行之后，原来为0的，如M0001变为了1.这样使程序与之前程序不同，导致错乱。解决办法，加入必要的清零模块，如moov bool等。
- 在洗衣机运行到正反转结束之后，会出现进水灯和排水灯先后点亮的现象，经过了修改，也始终不能解决。  
  解决办法，调试。

# 关于变频器的连线问题：

经过和JHG的讨论，原来理解并不深刻的变频器连线问题也有了更深刻的理解，首先PLC的模拟量输出模块会引出来接到变频器上，这里的作用是用PLC来控制变频器的输入电压，而变频器的输入电压又和他的输出频率有直接的联系。

变频器的输出线接到电机上，可以控制电机的频率和转速。  
变频器还会接继电器之后再接数字量的输入，来实现电机的正转和反转功能。

# GE 工业触摸屏的小知识：

Quickpanel windows ce 50M 内存，lifecycle生命周期将尽。  
Qucikpanel+ 500M 内存

Windows Embedded Compact,[6] formerly Windows Embedded CE and Windows CE, is an operating system subfamily developed by Microsoft as part of its Windows Embedded family of products. Unlike Windows Embedded Standard, which is based on Windows NT, Windows Embedded Compact uses an exclusive hybrid kernel.[7] Microsoft licenses Windows CE to original equipment manufacturers (OEMs), who can modify and create their own user interfaces and experiences, with Windows CE providing the technical foundation to do so.

The current version of Windows Embedded Compact supports x86 and ARM processors with board support package (BSP) directly.[8] The MIPS and SHx architectures have kernel support.  
Windows Embedded Compact（曾被稱為Microsoft Windows CE），為微軟研發的嵌入式作業系統，可以應用在各種嵌入式系統，或是硬體規格較低的電腦系統（例如很少的記憶體，較慢的中央處理器等）。微軟並未定義CE縮寫由來，一般解釋則有Compact Edition、Customer Embedded、Consumer Electronics等等。在2008年4月15日舉行的嵌入式系统大会上，微軟宣布將Windows CE更名為Windows Embedded Compact，與Windows Embedded Enterprise、Windows Embedded Standard和Windows Embedded POSReady組成Windows Embedded系列產品

以上来自wkipedia。

Windows Embedded Compact 7  
Windows Embedded Compact 7 is a componentized, real-time operating system designed for small-footprint devices at the edge of enterprise networks. With support for x86 and ARM architectures, Windows Embedded Compact 7 allows devices to leverage the latest innovations in hardware, and equips developers and device manufacturers with the tools they need to create nimble, enterprise-class intelligent system solutions, while reducing time to market.

来自微软官网： windows ed8  
Windows Embedded 8  
The Windows Embedded 8 family of platforms and tools helps companies extend their operational intelligence, using their existing IT infrastructure and industry devices that securely exchange data with back-end systems. Offering the same rich, multi-touch experience as Windows 8 and Windows Phone 8.1, Windows Embedded 8.1 delivers compelling user experiences on a range of industry devices.  
When you standardize all your enterprise devices on the Windows platform, you make everything simpler with a single operating and development platform; extend the power and intuitive experience of Windows 8 to specialized devices and invest in the future with a technology partner who is committed to your success. You’ll also capitalize on your existing IT investments, lowering your cost of ownership by taking advantage of your existing infrastructure, integrating new device experiences with other Microsoft assets, right out of the box. Management is streamlined because your devices work smoothly alongside PCs and servers. By customizing device experiences for your users, you enable intuitive, rich interfaces and deliver a targeted and consistent device experience.