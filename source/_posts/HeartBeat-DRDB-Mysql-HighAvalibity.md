---
title: HeartBeat-DRDB-Mysql-high-Availability
description: HeartBeat-DRDB-Mysql-high-Availability
date: 2022-09-20 15:19:33
tags: 
  - Mysql
  - DRDB
  - high Availability
categories: DataBase
---
**1.方案简介**

本方案采用Heartbeat双机热备软件来保证数据库的高稳定性和连续性，数据的一致性由DRBD这个工具来保证。默认情况下只有一台mysql在工作，当主mysql服务器出现问题后，系统将自动切换到备机上继续提供服务，当主数据库修复完毕，又将服务切回继续由主mysql提供服务。

**2.方案优缺点**

优点：安全性高、稳定性高、可用性高，出现故障自动切换。

缺点：只有一台服务器提供服务，成本相对较高，不方便扩展，可能会发生脑裂。

**3.软件介绍**

Heartbeat介绍

官方站点：http://linux-ha.org/wiki/Main_Page

heartbeat可以资源(VIP地址及程序服务)从一台有故障的服务器快速的转移到另一台正常的服务器提供服务，heartbeat和keepalived相似，heartbeat可以实现failover功能，但不能实现对后端的健康检查

DRBD介绍

官方站点：http://www.drbd.org/

DRBD(DistributedReplicatedBlockDevice)是一个基于块设备级别在远程服务器直接同步和镜像数据的软件，用软件实现的、无共享的、服务器之间镜像块设备内容的存储复制解决方案。它可以实现在网络中两台服务器之间基于块设备级别的实时镜像或同步复制(两台服务器都写入成功)/异步复制(本地服务器写入成功)，相当于网络的RAID1，由于是基于块设备(磁盘，LVM逻辑卷)，在文件系统的底层，所以数据复制要比cp命令更快。DRBD已经被MySQL官方写入文档手册作为推荐的高可用的方案之一

**4.方案拓扑**

![](/images/182048487448428.png)

**5.方案适用场景：**

适用于数据库访问量不太大，短期内访问量增长不会太快，对数据库可用性要求非常高的场景。

参考链接：https://www.cnblogs.com/gomysql/p/3674030.html
