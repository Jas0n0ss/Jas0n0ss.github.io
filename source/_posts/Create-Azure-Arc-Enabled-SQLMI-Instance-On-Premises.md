---
title: Create Azure Arc-enabled SQLMI Instance On-Premises
tags: 
  - Azure Arc Data Service
  -	SQL Server
  - SQLMI
categories: 
  -	SQL Server
  -	Kubernets
#description: 'Create Azure Arc-enabled SQLMI Instance On-Premises'
---

## Create Azure Arc-enabled SQLMI Instance On-Premises

### Prerequisites & environments

| Servers  | CPU & MEM  |    Role    |    OS     |
| :------: | :--------: | :--------: | :-------: |
| node1.io | 4Core 16GB | k8s master | centos7.8 |
| node2.io | 4Core 20GB | k8s worker | centos7.8 |
| node3.io | 4Core 20GB | k8s worker | centos7.8 |

### Setup k8s clsuter on-premises

[Setup k8s clsuter on-premises on Ubuntu](https://github.com/microsoft/sql-server-samples/tree/master/samples/features/sql-big-data-cluster/deployment/kubeadm/ubuntu)


#### Instructions

- Start a sudo shell context and Execute `setup-k8s-prereqs.sh` script on each machine
- Execute `setup-k8s-master.sh `script on the machine designated as Kubernetes master (not under sudo su as otherwise you'll setup K8S .kube/config permissions for root)
- After successful initialization of the Kubernetes master, follow the kubeadm join commands output by the setup script on each agent machine
- Execute `setup-volumes-agent.sh` script on each agent machine to create volumes for local storage
- Execute `kubectl apply -f local-storage-provisioner.yaml` against the Kubernetes cluster to create the local storage provisioner. This will create a Storage Class named "local-storage".

### Create data controller:
[create-data-controller-indirect-cli](https://docs.microsoft.com/en-us/azure/azure-arc/data/create-data-controller-indirect-cli?tabs=windows)

```bash
[root@node1 arc]# kubectl get storageclasses.storage.k8s.io
NAME            PROVISIONER                    RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
local-storage   kubernetes.io/no-provisioner   Delete          WaitForFirstConsumer   false                  39h  
[root@node2 ~]# cat /etc/fstab | grep data
UUID=49d8fe73-dfc5-4bca-9006-7c3feebdf3fc /data xfs defaults 0 0
[root@node2 ~]# df -Th | grep '/data'
/dev/sdb1                 xfs       500G  568M  500G   1% /data
tmpfs                     tmpfs     9.8G  4.0M  9.8G   1% /var/lib/kubelet/pods/5092d08d-a693-4550-b127-35ce23c261cc/volumes/kubernetes.io~empty-dir/data
[root@node2 ~]# ls /data/local-storage/
vol1   vol11  vol13  vol15  vol17  vol19  vol20  vol22  vol24  vol26  vol28  vol3   
[root@node1 arc]# kubectl get pv -n local-storage
NAME                CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM                                            STORAGECLASS    REASON   AGE
local-pv-119ebf20   499Gi      RWO            Delete           Available                                                    local-storage            23h
local-pv-1245a771   499Gi      RWO            Delete           Available                                                    local-storage            23h
local-pv-13a47426   499Gi      RWO            Delete           Bound       arc/logs-metricsdb-0                             local-storage            39h
[root@node1 arc]# az arcdata dc create --connectivity-mode indirect --name onpremises --k8s-namespace arc --subscription xxxx-xxxxx-xxxx-xxxx --resource-group azarclab --location eastus --storage-class local-storage --profile-name azure-arc-kubeadm --infrastructure onpremises --use-k8s
Subscription 'xxxx-xxxxx-xxxx-xxxx' not recognized.
To not see this warning, first login to Azure.

Using subscription 'xxxx-xxxxx-xxxx-xxxx'.

Monitoring administrator username:admin
Monitoring administrator password:
Confirm Monitoring administrator password:

Deploying data controller

NOTE: Data controller creation can take a significant amount of time depending on
configuration, network speed, and the number of nodes in the cluster.

Data controller successfully deployed.
{}
[root@node1 arc]# kubectl get datacontroller -n arc
NAME         STATE
onpremises   Ready
[root@node1 arc]# kubectl get pod -n arc | grep -v sql
NAME                           READY   STATUS      RESTARTS   AGE
arc-bootstrapper-job-94x7m     0/1     Completed   0          14h
bootstrapper-cbf5bf94d-z9l95   1/1     Running     1          14h
control-f5d8t                  2/2     Running     0          14h
controldb-0                    2/2     Running     0          14h
logsdb-0                       3/3     Running     0          14h
logsui-896pw                   3/3     Running     3          14h
metricsdb-0                    2/2     Running     2          14h
metricsdc-2lr8t                2/2     Running     0          14h
metricsdc-79h4t                2/2     Running     2          14h
metricsui-zjwnr                2/2     Running     0          14h
```

### Create SQLMI instance
[create-sql-managed-instance-with-azure-cli](https://docs.microsoft.com/en-us/azure/azure-arc/data/create-sql-managed-instance?tabs=indirectly)

```bash      
PS C:\Users\hubo> az sql mi-arc create --name sql1 --k8s-namespace arc --use-k8s --time-zone Asia/Shanghai --agent-enabled true --dev --tier BusinessCritical --replicas 2
Deploying sql1 in namespace `arc`
sql1 is Ready
[root@node1 arc]# kubectl get pod -n arc
NAME                           READY   STATUS      RESTARTS   AGE
arc-bootstrapper-job-94x7m     0/1     Completed   0          14h
bootstrapper-cbf5bf94d-z9l95   1/1     Running     1          14h
control-f5d8t                  2/2     Running     0          14h
controldb-0                    2/2     Running     0          14h
logsdb-0                       3/3     Running     0          14h
logsui-896pw                   3/3     Running     3          14h
metricsdb-0                    2/2     Running     2          14h
metricsdc-2lr8t                2/2     Running     0          14h
metricsdc-79h4t                2/2     Running     2          14h
metricsui-zjwnr                2/2     Running     0          14h
sql1-0                         4/4     Running     0          31m
sql1-1                         4/4     Running     0          31m
sql1-ha-0                      2/2     Running     0          32m
```
### Connect with SQLMI insatnce
```
[root@node1 arc]# kubectl get sqlmi -n arc
NAME   STATUS   REPLICAS   PRIMARY-ENDPOINT     AGE
sql1   Ready    2          10.157.21.15,32697   22m
[root@node1 arc]# yum install mssql-tools -y
[root@node1 arc]# /opt/mssql-tools/bin/sqlcmd -S 10.157.21.15,32697 -Uadmin -Q 'select @@version'
Password:                                                                                                                                                                     
--------------------------------------------------------
Microsoft Azure SQL Managed Instance - Azure Arc - 16.0.312.4243 (X64)
        Jul  2 2022 13:16:53
        Copyright (C) 2022 Microsoft Corporation
        Business Critical (64-bit) on Linux (Ubuntu 20.04.4 LTS) <X64>

(1 rows affected)
```
### Manager data with Azure Data Studio

Azure Data Studio:
https://docs.microsoft.com/en-us/sql/azure-data-studio/download-azure-data-studio?view=sql-server-ver16

![](/images/1715511-20220909100338097-1615601437.png)

kibana Dashboard:
![](/images/1715511-20220909100450574-1462693194.png)

Grafana Dashboard
![](/images/1715511-20220909100700776-934704336.png)