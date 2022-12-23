---
title: ansible-detailed-start
description: ansible-detailed-start
date: 2022-09-20 15:52:28
tags: Ansible
categories: Linux
---

1. 简介
    ansible是新出现的自动化运维工具，基于Python开发，集合了众多运维工具（puppet、cfengine、chef、func、fabric）的优点，实现了批量系统配置、批量程序部署、批量运行命令等功能。
    ansible是基于模块工作的，本身没有批量部署的能力。真正具有批量部署的是ansible所运行的模块，ansible只是提供一种框架。主要包括：
    (1)、连接插件connection plugins：负责和被监控端实现通信；
    (2)、host inventory：指定操作的主机，是一个配置文件里面定义监控的主机；
    (3)、各种模块核心模块、command模块、自定义模块；
    (4)、借助于插件完成记录日志邮件等功能；
    (5)、playbook：剧本执行多个任务时，非必需可以让节点一次性运行多个任务。

   - github地址：https://github.com/ansible/ansible/
   - 官网地址：https://docs.ansible.com
   - 在线playbook分享平台：https://galaxy.ansible.com

2. 特性
- (1)、no agents：不需要在被管控主机上安装任何客户端；
- (2)、no server：无服务器端，使用时直接运行命令即可；
- (3)、modules in any languages：基于模块工作，可使用任意语言开发模块；
- (4)、yaml，not code：使用yaml语言定制剧本playbook；
- (5)、ssh by default：基于SSH工作；
- (6)、strong multi-tier solution：可实现多级指挥。

3. 优点
- (1)、轻量级，无需在客户端安装agent，更新时，只需在操作机上进行一次更新即可；
- (2)、批量任务执行可以写成脚本，而且不用分发到远程就可以执行；
- (3)、使用python编写，维护更简单，ruby语法过于复杂；
- (4)、支持sudo。

参考链接：
  https://www.cnblogs.com/chenxianpao/p/7360349.html

  https://www.cnblogs.com/keerya/p/7987886.html
