---
title: openshift-setup-with-ansible-playbook
description: openshift-setup-with-ansible-playbook
date: 2022-09-20 17:02:06
tags: 
  -	Ansible
  - Openshift
  -	Playbook
categories: DevOps
---

---
Nodes:  
  - master: ocmaster.eastasia.cloudapp.azure.com
  - compute:  occompute.eastasia.cloudapp.azure.com
  - infra:  ocinfra.eastasia.cloudapp.azure.com
----------------------------------------------------------------------------------------------------



```bash
# Nodes all:
  
  sudo yum install -y wget git zile net-tools bind-utils iptables-services bridge-utils bash-completion kexec-tools sos psacct openssl-devel httpd-tools python-cryptography python2-pip python-devel python-passlib java-1.8.0-openjdk-headless "@Development Tools"
  sudo yum update -y
  sudo yum insttall docker -y && systemctl start docker && systemctl enable docker && systemctl status docker
  sudo yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
  sudo sed -i -e "s/^enabled=1/enabled=0/" /etc/yum.repos.d/epel.repo
```

```bash
# master node：

  sudo ssh-keygen 
  sudo for host in ocmaster.eastasia.cloudapp.azure.com occompute.eastasia.cloudapp.azure.com \
  ocinfra.eastasia.cloudapp.azure.com ; do ssh-key-copy ${host};done
  sudo subscription-manager register --username <email> --password PyPassword1 --auto-attach && yum-config-manager --enable rhel-7-server-ansible-2.9-rpms
  sudo yum install ansible git -y
  sudo git clone https://github.com/openshift/openshift-ansible.git && cd openshift-ansible && git fetch && git checkout release-3.11
```
```bash
  sudo vim hosts.ini
  # Create an OSEv3 group that contains the masters, nodes, and etcd groups
  [OSEv3:children]
  masters
  nodes
  etcd

  # Set variables common for all OSEv3 hosts
  [OSEv3:vars]
  # SSH user, this user should allow ssh based auth without requiring a password
  ansible_ssh_user=root
  # If ansible_ssh_user is not root, ansible_become must be set to true
  ansible_become=true
  openshift_master_default_subdomain=app.ocmaster.eastasia.cloudapp.azure.com
  deployment_type=origin

  [nodes:vars]
  openshift_disable_check=disk_availability,memory_availability,docker_storage
  [masters:vars]
  openshift_disable_check=disk_availability,memory_availability,docker_storage
  # uncomment the following to enable htpasswd authentication; defaults to DenyAllPasswordIdentityProvider
  openshift_master_identity_providers=[{'name': 'htpasswd_auth', 'login': 'true', 'challenge': 'true', 'kind': 'HTPasswdPasswordIdentityProvider'}]

  # host group for masters
  [masters]
  ocmaster.eastasia.cloudapp.azure.com

  # host group for etcd
  [etcd]
  ocmaster.eastasia.cloudapp.azure.com

# host group for nodes, includes region info
  [nodes]
  ocmaster.eastasia.cloudapp.azure.com  openshift_node_group_name='node-config-master'
  occompute.eastasia.cloudapp.azure.com  openshift_node_group_name='node-config-compute'
  ocinfra.eastasia.cloudapp.azure.com  openshift_node_group_name='node-config-infra'
```

```bash
  sudo ansible-playbook -i hosts.ini playbooks/prerequisites.yml
  sudo ansible-playbook -i hosts.ini playbooks/deploy_cluster.yml
```
