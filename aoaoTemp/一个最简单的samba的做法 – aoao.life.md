---
title: "一个最简单的samba的做法 – aoao.life"
date: 2024-04-18 07:57:45
---

1.vim /etc/samba/smb.conf,写下下列东东:
`[global] workgroup = my group
server string = Samba Server
null password = yes
guest ok = yes
security = share
encrypt password = yes
[homes] comment = Home Directory
browseable = no
writable = yes
[documents] path = /var/samba/documents
directory mask = 0775
writable = yes
public = yes`

其余内容都不必理会.
2.建目录/var/samba/document,并设权限777
3.关闭SELINUX.具体方法,编辑/etc/selinux/config,把SELINUX=后面的东西改成disabled.保存,重启.
4.service smb restart

搞定!