---
title: Offline install docker
description: Offline install docker
date: 2022-12-23 19:41:54
tags: docker
categories: devops
---

> 场景

有时候会面临这样的场景，环境不允许连接到外部网络，但是又需要安装Docker的场景，下面我们来用离线二进制的方式安装Docker。

https://download.docker.com/linux/static/stable/x86_64/

```bash
wget https://download.docker.com/linux/static/stable/x86_64/docker-20.10.9.tgz  # 下载二进制离线安装包
# https://raw.githubusercontent.com/liumiaocn/easypack/master/docker/install-docker.sh
wget https://raw.githubusercontent.com/liumiaocn/easypack/master/docker/install-docker.sh  # 一个自动化解压并复制二进制文件到相应PATH
chmod +x install-docker.sh
./install-docker.sh docker-20.10.9.tgz
docker version --short
```

> 一键自动化安装

```bash
curl -fsSL get.docker.com | CHANNEL=stable sh
```

