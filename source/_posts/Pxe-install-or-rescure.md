---
title: Pxe-install-or-rescure.md
description: Pxe-install-or-rescure.md
date: 2022-09-19 19:11:18
tags: pxe

---

```bash
[root@localhost ~]# yum install httpd tftp-server dhcpd syslinux system-config-kickstart -y 
```
- 配置HTTP共享

***
```
[root@localhost ~] mkdir /var/www/html/redhat{73,73,68} -p
[root@localhost ~] mount /iso/rhel-server7.2****.iso /var/www/html/redhat72
[root@localhost ~] mount /iso/rhel-server7.3***.iso /var/www/html/redhat73
[root@localhost ~] mount /iso/rhel-server6.8***.iso /var/www/html/redhat68
[root@localhost ~] service httpd start
[root@localhost ~] chkconfig httpd on
```
***
- system-config-kickstart:

> 运行system-config-kickstart，最后把ks.cfg文件保存到httpd共享的不同目录下，可以用ksvalidator命令检查语法错误，中共配合三个ks文件分别保存在/var/www/html/ks7,ks72,ks68目录下

```bash
[root@localhost ~] system-config-kickstart
[root@localhost ~] ksvalidator # 检查ks.cfg语法
```
- Tftp-server:

```rust
[root@localhost ~]# vim /etc/xinetd.d/tftp 
13         server_args             = -s /var/lib/tftpboot
 14         disable                 = no  #yes修改为no
 15         per_source              = 11
 16         cps                     = 100 2
[root@localhost linux]# cd /var/lib/tftpboot/
[root@localhost tftpboot]# cp /var/www/html/redhat72/isolinux/vmlinuz redhat72/
[root@localhost tftpboot]# cp /var/www/html/source/redhat72/isolinux/initrd.img redhat72/
# redhat6.8和redhat7.3一样，从挂载镜像中将initrd.img,vmlinuz 复制到http共享目录中的对应文件夹
[root@localhost tftpboot]# mkdir pxelinux.cfg 
[root@localhost tftpboot]# cp /var/www/html/redhat73/isolinux/isolinux.cfg ./pxelinux.cfg/default
[root@localhost tftpboot]# cp /var/www/html/source/redhat73/isolinux/vesamenu.c32 .
# isolinux.cfg和vesamenu.c32任意一个系统的考个过来都可以
[root@localhost tftpboot]# cp /usr/share/syslinux/pxelinux.0 .
# pxelinux.0 此文件是在安装主机获得dhcp分配的ip以后要读取的文件

[root@localhost tftpboot]# cat pxelinux.cfg/default
default vesamenu.c32
timeout 30  #30代表3秒选择时间，默认600（即一分钟）
display boot.msg
...
menu separator # insert an empty line
menu separator # insert an empty line

##########################################################################
################# INSTALL CONFIG OPTION BEGIN ############################
##########################################################################

label linux
  menu label ^Install RedHat 7.3 Linux # install menu
  kernel redhat73/vmlinuz
  #此处不再需要写repo地址了，因为在ks.cfg文件中已经指定了从哪里获取相应的镜像,也指定了安装过程中的各种选择
  append initrd=redhat73/initrd.img  ks=http://192.168.1.100/ks7/ks.cfg  

label linux
  menu label ^Install RedHat 7.2 Linux 
  #此处也必须要指定内核文件的准确位置，默认读取的内核文件在tftpboot下，此处我们部署的是多个版本，故具体版本读取相应目录下的文件
  kernel redhat72/vmlinuz
  append initrd=redhat72/initrd.img  ks=http://192.168.1.100/ks72/ks.cfg 

label linux
  menu label  ^Install RedHat 6.8 Linux
  kernel redhat68/vmlinuz
  append initrd=redhat68/initrd.img  ks=http://192.168.1.100/ks6/ksmini.cfg 

############# END LINE FOR LEBEL INSTALL OPTIONS ######################################


######################################################
######### Rescue Mode for all options config     #####
######################################################

# utilities submenu
menu begin ^Rescue Mode
  menu title Rescue Mode

 label rescue
  menu indent count 5
  menu label ^Rescue mode for RedHat 7.3 
  text help
  If the system will not boot, this lets you access files
  and edit config files to try to get it booting again.
  endtext
  kernel redhat73/vmlinuz
  append initrd=redhat73/initrd.img repo=http://192.168.1.100/source/redhat73 rescue quiet
  #挽救环境必须写repo地址，此处不是安装，故也不需要ks文件，所以此处必须指定从哪里获取挽救环境所需要的资源

 label rescue
  menu indent count 5
  menu label ^Rescue mode for RedHat 7.2 
  text help
  If the system will not boot, this lets you access files
  and edit config files to try to get it booting again.
  endtext
  kernel redhat72/vmlinuz
  append initrd=redhat72/initrd.img repo=http://192.168.1.100/source/redhat72 rescue quiet


 label rescue
  menu indent count 5
  menu label ^Rescue mode for RedHat 6.8 
  text help
  If the system will not boot, this lets you access files
  and edit config files to try to get it booting again.
  endtext
  kernel redhat68/vmlinuz
  append initrd=redhat68/initrd.img repo=http://192.168.1.100/source/redhat68  rescue quiet

label returntomain
  menu label Return to ^main menu
  menu exit

menu end

###################### END LINE FOR RESCUE MODE ########################################
```
```bash
[root@localhost ~]# systemctl start tftp
[root@localhost ~]# systemctl enable tftp
```

- DHCP的配置：

```
[root@localhost tftpboot]# cat /etc/dhcp/dhcpd.conf |grep -v '#' 
option domain-name "example.com";
option domain-name-servers 192.168.1.100;
default-lease-time 600;
max-lease-time 7200;
log-facility local7;

subnet 192.168.1.0 netmask 255.255.255.0 {
  range 192.168.1.20 192.168.1.99;
  option routers 192.168.1.250;
  next-server 192.168.1.100;
  filename "pxelinux.0"; # 这里很重要，对应TFTP哪里的设定
}
```
- Firewall

```bash
[root@localhost tftpboot]# firewall-cmd --add-service=httpd --permanent 
[root@localhost tftpboot]# firewall-cmd --add-service=tftp --permanent 
[root@localhost tftpboot]# firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: br0 enp8s0 wlp9s0
  sources: 
  services: dhcpv6-client ftp http ssh tftp ##说明添加上了
  ports: 4505/tcp 4506/tcp
  protocols: 
  masquerade: yes
  forward-ports: 
  sourceports: 
  icmp-blocks: 
  rich rules: 
  rule family="ipv4" source address="192.168.0.10" masquerade
```
![这里写图片描述](/images/pxe1.png)
![这里写图片描述](/images/pxe2.png)
![这里写图片描述](/images/pxe3.png)
