---
title: kubectl-manage-multiple-k8s-cluster
date: 2022-09-16 16:29:09
tags: 
  - kubernets
  - kubecm 
categories: kubernets
#description: 'kubectl-manage-multiple-k8s-cluster'
---

> Usually when we execute `kubectl` command it will load default k8s configuration from `$HOME/.kube/config`

**But what if we have multiple k8s cluster, How we gonna manage them at same time ?**

if we have on-premise k8s and azure k8s:
  - KUBECONFIG
  
  ```bash
  [root@node1 k8s-configs]# ll
  total 20
  -rw-r--r--. 1 root root 9657 Sep 15 13:23 aksconfig
  -rw-r--r--. 1 root root 5534 Sep 15 13:06 k8sconfig
  [root@node1 k8s-configs]# pwd
  /root/k8s-configs
  [root@node1 k8s-configs]# export KUBECONFIG=/root/k8s-configs/aksconfig:/root/k8s-configs/k8sconfig
  [root@node1 k8s-configs]# echo $KUBECONFIG
  /root/k8s-configs/aksconfig:/root/k8s-configs/k8sconfig
  [root@node1 k8s-configs]# kubectl config get-contexts
  CURRENT   NAME         CLUSTER      AUTHINFO                   NAMESPACE
  *         aks          aks          clusterUser_azarclab_aks   arc
            onpremises   kubernetes   kubernetes-admin
  [root@node1 k8s-configs]# echo 'export KUBECONFIG=/root/k8s-configs/aksconfig:/root/k8s-configs/k8sconfig' >>/etc/profile.d/k8s.sh
  [root@node1 k8s-configs]# kubectl get node
  NAME                             STATUS     ROLES   AGE   VERSION
  aks-agent1-71585651-vmss00000b   NotReady   agent   23d   v1.22.11
  aks-agent2-71585651-vmss00000b   NotReady   agent   8d    v1.22.11
  aks-agent2-71585651-vmss00000c   NotReady   agent   8d    v1.22.11
  aks-agent2-71585651-vmss00000d   NotReady   agent   8d    v1.22.11
  aks-master-71585651-vmss000005   NotReady   agent   23d   v1.22.11
  [root@node1 k8s-configs]# kubec
  kubecm   kubectl
  [root@node1 k8s-configs]# kubectl config use-context
  aks         onpremises
  [root@node1 k8s-configs]# kubectl config use-context onpremises
  Switched to context "onpremises".
  [root@node1 k8s-configs]# kubectl get node
  NAME    STATUS   ROLES                  AGE     VERSION
  node1   Ready    control-plane,master   7d19h   v1.20.7
  node2   Ready    worker                 7d19h   v1.20.7
  node3   Ready    worker                 7d19h   v1.20.7
  ```
  - kubecm
  https://github.com/sunny0826/kubecm
  ```bash
[root@node1 ~]# wget https://github.com/sunny0826/kubecm/releases/download/v0.21.0/kubecm_v0.21.0_Linux_x86_64.tar.gz
[root@node1 ~]# tar -zxvf kubecm_v0.21.0_Linux_x86_64.tar.gz
[root@node1 ~]# echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin
[root@node1 ~]# mv kubecm /usr/local/sbin
[root@node1 ~]# kubecm merge -f k8s-configs/ -c
Loading kubeconfig file: [k8s-configs//aksconfig k8s-configs//k8sconfig]
Context Add: aksconfig
Context Add: k8sconfig
[root@node1 ~]# kubectl config get-contexts
CURRENT   NAME         CLUSTER      AUTHINFO                   NAMESPACE
          aks          aks          clusterUser_azarclab_aks   arc
*         onpremises   kubernetes   kubernetes-admin
[root@node1 ~]# kubecm version
Version: 0.21.0
GoOs: linux
GoArch: amd64
[root@node1 ~]# kubecm list
+------------+--------------+-----------------------+--------------------+-----------------------------------+--------------+
|   CURRENT  |     NAME     |        CLUSTER        |        USER        |               SERVER              |   Namespace  |
+============+==============+=======================+====================+===================================+==============+
|            |   aksconfig  |   cluster-9hdtmk5k4h  |   user-9hdtmk5k4h  |   https://xxxxxxxxxxxxxxxx.hcp.e  |      arc     |
|            |              |                       |                    |        astus.azmk8s.io:443        |              |
+------------+--------------+-----------------------+--------------------+-----------------------------------+--------------+
|      *     |   k8sconfig  |   cluster-c5bdhf8kc6  |   user-c5bdhf8kc6  |     https://10.157.21.24:6443     |    default   |
+------------+--------------+-----------------------+--------------------+-----------------------------------+--------------+

Cluster check succeeded!
Kubernetes version v1.20.7
Kubernetes master is running at https://10.157.21.24:6443
[Summary] Namespace: 8 Node: 3 Pod: 40
[root@node1 ~]# kubectl config use-context
aks         onpremises
[root@node1 ~]# kubectl config use-context aks
Switched to context "aks".
[root@node1 ~]# kubecm list
+------------+--------------+-----------------------+--------------------+-----------------------------------+--------------+
|   CURRENT  |     NAME     |        CLUSTER        |        USER        |               SERVER              |   Namespace  |
+============+==============+=======================+====================+===================================+==============+
|            |   aksconfig  |   cluster-9hdtmk5k4h  |   user-9hdtmk5k4h  |   https://xxxxxxxxxxxxxxxx.hcp.e  |      arc     |
|            |              |                       |                    |        astus.azmk8s.io:443        |              |
+------------+--------------+-----------------------+--------------------+-----------------------------------+--------------+
|      *     |   k8sconfig  |   cluster-c5bdhf8kc6  |   user-c5bdhf8kc6  |     https://10.157.21.24:6443     |    default   |
+------------+--------------+-----------------------+--------------------+-----------------------------------+--------------+

Cluster check succeeded!
Kubernetes version v1.20.7
Kubernetes master is running at https://10.157.21.24:6443
[Summary] Pod: 40 Namespace: 8 Node: 3
  ```

