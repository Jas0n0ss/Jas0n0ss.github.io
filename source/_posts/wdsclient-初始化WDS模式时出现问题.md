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

Configurations like below, `Definitely, this is wrong`!!!. I use DHCP service on my router to provide IP address to clients, So I change to get IP from `DHCP `like below, then restart the client problem solved.

![image-20230104135633546](../images/image-20230104135633546.png)

![image-20230104135738728](../images/image-20230104135738728.png)

Checking on system up application logs:

![image-20230104140740661](../images/image-20230104140740661.png)

![image-20230104140813839](../images/image-20230104140813839.png)

> Reference

https://social.technet.microsoft.com/Forums/windows/en-US/8feca2eb-c8c7-4ced-8932-e34d7ffaa83e/wds-event-772-not-pxe-booting-with-server-2016-and-gen-2-hyperv-vm-or-physical-pc#:~:text=Event%20772%20WDSServer%3A%20An%20error%20occurred%20while%20trying,be%20able%20to%20receive%20requests%20on%20this%20interface.

---

https://learn.microsoft.com/zh-cn/windows/deployment/wds-boot-support

I also meet errors, I followed MS official documentation issue solved.

![WDS 弃用通知](../images/wds-deprecation-20230104141727686.png)
