---
title: upgrade-k8s
description: upgrade-k8s
date: 2022-09-21 17:35:31
tags: k8s
categories: k8s
---

STEPS:
- upgrade master node
- disable schedule on worker node
- upgrade worker node

> upgrade master node

```bash
[root@node1 ~]# kubectl get node
NAME    STATUS   ROLES                  AGE   VERSION
node1   Ready    control-plane,master   13d   v1.20.7
node2   Ready    worker                 13d   v1.20.7
node3   Ready    worker                 13d   v1.20.7
```
```bash
[root@node1 ~]# yum install kubectl-1.20.15 kubelet-1.20.15 kubeadm-1.20.15
[root@node1 ~]# kubeadm upgrade plan
[root@node1 ~]# kubeadm upgrade apply v1.20.15
[root@node1 ~]# kubectl get node
NAME    STATUS   ROLES                  AGE   VERSION
node1   Ready    control-plane,master   13d   v1.20.15
node2   Ready    worker                 13d   v1.20.7
node3   Ready    worker                 13d   v1.20.7
```
> disable schedule on worker node

```bash
[root@node1 ~]# kubectl drain node2 --ignore-daemonsets --delete-emptydir-data
[root@node1 ~]# kubectl get node
NAME    STATUS                     ROLES                  AGE   VERSION
node1   Ready                      control-plane,master   13d   v1.20.15
node2   Ready,SchedulingDisabled   worker                 13d   v1.20.7
node3   Ready                      worker                 13d   v1.20.7
```

```bash
# Worker Node2
[root@node2 ~]# yum install kubectl-1.20.15 kubelet-1.20.15 kubeadm-1.20.15
[root@node2 ~]# systemctl daemon-reload
[root@node2 ~]# systemctl restart kubelet
[root@node1 ~]# kubectl get node
NAME    STATUS                     ROLES                  AGE   VERSION
node1   Ready                      control-plane,master   13d   v1.20.15
node2   Ready,SchedulingDisabled   worker                 13d   v1.20.15
node3   Ready                      worker                 13d   v1.20.7
[root@node1 ~]# kubectl uncordon node2
node/node2 uncordoned
[root@node1 ~]# kubectl get node
NAME    STATUS                     ROLES                  AGE   VERSION
node1   Ready                      control-plane,master   13d   v1.20.15
node2   Ready                      worker                 13d   v1.20.15
node3   Ready                      worker                 13d   v1.20.7
```
Same step on worker `node3` as on worker `node2`, after upgrade complete:
```bash
[root@node1 ~]# kubectl get node
NAME    STATUS   ROLES                  AGE   VERSION
node1   Ready    control-plane,master   13d   v1.20.15
node2   Ready    worker                 13d   v1.20.15
node3   Ready    worker                 13d   v1.20.15
```
set k8s node role:
```bash
[root@node1 ~]# kubectl label node node1 node-role.kubernetes.io/worker=worker
```

