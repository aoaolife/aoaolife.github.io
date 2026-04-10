---
title: "MySQL常用命令 – aoao.life"
date: 2020-11-09 15:47:24
---

FC上都是整合了Mysql的,除非对版本有特殊要求,不必重装.
**一.启动MySQL**
service mysqld restart
**二.登录mysql**
mysql -uroot
**三.创建一个库**
登录以后
>create database mydb;
**四.为root改密码**
mysqladmin password 新密码
**五.增加一个用户**
GRANT ALL PRIVILEGES ON *.* TO 新用户@localhost
IDENTIFIED BY ‘用户密码’ WITH GRANT OPTION;
**六.删除一个库**
登录以后
>drop database mydb;
**七.备份数据库内容**
mysqldump -p 数据库名 > 备份文件.sql
**八.导入数据库内容**
mysql -uroot -p密码 数据库名 <./备份文件.sql