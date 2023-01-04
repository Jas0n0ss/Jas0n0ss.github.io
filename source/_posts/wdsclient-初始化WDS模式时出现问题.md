---
title: wdsclient:初始化WDS模式时出现问题
description: wdsclient:初始化WDS模式时出现问题
date: 2023-01-04 13:48:39
tags: [pxe,wds]
categories: wds
---

#### **Issue description:**

When I use windows employment service to install windows server, encountered such error msg:

![image-20230104135142586](../images/image-20230104135142586.png)

When I checked WDS logs find client can't get IP address caused this , So I double checked and the configuration on WDS:

![image-20230104135331180](../images/image-20230104135331180.png)

`Definitely, this is wrong`!!!. I use DHCP service on my router to provide IP address to clients, So I change to get IP from `DHCP `like below, then restart the client problem solved.

![image-20230104135633546](../images/image-20230104135633546.png)

![image-20230104135738728](../images/image-20230104135738728.png)
