---
title: "scp不能拷贝的一个原因 – aoao.life"
date: 2022-11-08 10:16:55
---

当遇到提示
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED! @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that the RSA host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
77:ae:3e:fd:d3:a9:02:c5:16:2a:bc:5f:06:99:d4:b2.
Please contact your system administrator.
Add correct host key in /root/.ssh/known_hosts to get rid of this message.
Offending key in /root/.ssh/known_hosts:3
RSA host key for 192.168.100.137 has changed and you have requested strict checking.
时,意味着你的目标的host发生了一点变化,这时要**删除源端的/root/.ssh/known_hosts**文件