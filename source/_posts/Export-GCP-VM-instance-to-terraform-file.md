---
title: Export GCP VM instance to terraform file
description: Export GCP VM instance to terraform file
date: 2022-12-23 00:21:30
tags: Terraform
categories: devops
---

Reference:
https://cloud.google.com/docs/terraform/resource-management/export

# install gcloud
https://cloud.google.com/sdk/docs/install

```bash
⚡ curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-412.0.0-linux-x86_64.tar.gz
⚡ tar -zxvf google-cloud-cli-412.0.0-linux-x86_64.tar.gz
⚡ ./google-cloud-sdk/install.sh --help
⚡ ./google-cloud-sdk/install.sh
# gcloud completion
⚡ source ./google-cloud-sdk/*.inc 
# 
⚡ gcloud auth login
gcloud config set project <PROJECT_ID>
⚡ gcloud compute instances list                                                                                                                           jason@JasondeMBP
NAME        ZONE               MACHINE_TYPE  PREEMPTIBLE  INTERNAL_IP  EXTERNAL_IP     STATUS
tw          asia-east1-a       e2-micro                   10.140.0.10  xxxx           RUNNING
xray-ipsec  asia-east1-b       e2-micro                   10.140.0.3   xxxx           RUNNING
sg          asia-southeast1-a  e2-micro                   10.148.0.2   xxxx           RUNNING
hk          asia-east2-a       e2-micro                   10.170.0.4   xxxx           RUNNING
vps-msft    asia-east2-a       e2-medium                  10.170.0.3   xxxx           RUNNING
# login the instance 
⚡ gcloud compute ssh  sg --zone=asia-southeast1-a
jason@sg:~$ hostnamectl
   Static hostname: sg
         Icon name: computer-vm
           Chassis: vm
        Machine ID: d5dde3aa3431f96bb23d56a1166bc345
           Boot ID: b8a1e4c3f7f040a2b2630e70f02c780a
    Virtualization: kvm
  Operating System: Ubuntu 20.04.5 LTS
            Kernel: Linux 5.15.0-1025-gcp
      Architecture: x86-64
jason@sg:~$ ping -c 3 google.com
PING google.com (172.217.194.138) 56(84) bytes of data.
64 bytes from si-in-f138.1e100.net (172.217.194.138): icmp_seq=1 ttl=115 time=0.957 ms
64 bytes from si-in-f138.1e100.net (172.217.194.138): icmp_seq=2 ttl=115 time=0.330 ms
64 bytes from si-in-f138.1e100.net (172.217.194.138): icmp_seq=3 ttl=115 time=0.304 ms
```

# install config-connector and export

```bash
⚡ gcloud components install config-connector
⚡ gcloud beta resource-config bulk-export \                                                                                                               127 ↵ jason@JasondeMBP
  --resource-types=ComputeInstance \
  --project=studied-beanbag-370602 \
  --resource-format=terraform \
\ --path=/Users/jason/Desktop/terraform-GCP-VM

Exporting resource configurations to [/Users/jason/Desktop/terraform-GCP-VM]...done.
Exported resource configuration(s) to [/Users/jason/Desktop/terraform-GCP-VM].
⚡ tree Desktop/terraform-GCP-VM                                                                                                                           130 ↵ jason@JasondeMBP
Desktop/terraform-GCP-VM
└── projects
    └── studied-beanbag-370602
        └── ComputeInstance
            ├── asia-east1-a
            │   └── tw.tf
            ├── asia-east1-b
            │   └── xray-ipsec.tf
            ├── asia-east2-a
            │   ├── hk.tf
            │   └── vps-msft.tf
            └── asia-southeast1-a
                └── sg.tf

7 directories, 5 files
```



