---
title: ansible-manage-windows-server
description: ansible-manage-windows-server
date: 2022-09-20 16:43:47
tags:
categories:
---

####  Windows Server Ansible Setup
##### 1.Upgrade Powershell to V4.0 above

```powershell
1. 检查powershell版本
get-host

2. 下载并安装Microsoft .NET Framework 4.5
下载地址：
https://download.microsoft.com/download/B/A/4/BA4A7E71-2906-4B2D-A0E1-80CF16844F5F/dotNetFx45_Full_setup.exe

3. 下载并安装powershell4.0(Windows Management Framework 4.0 )
下载地址：
https://download.microsoft.com/download/3/D/6/3D61D262-8549-4769-A660-230B67E15B25/Windows6.1-KB2819745-x64-MultiPkg.msu
```

> 注意： 先安装.NET Framework 4.5 ，然后安装powershell4.0，安装完成之后重启windows服务器

##### 2. Enable Winrm and Enable Powershell Remote Management 

```powershell
1. 查看powershell执行策略
get-executionpolicy

2. 更改powershell执行策略为remotesigned
set-executionpolicy remotesigned

3. 配置winrm service并启动服务
winrm quickconfig

4. 查看winrm service启动监听状态
winrm enumerate winrm/config/listener

5. 修改winrm配置，启用远程连接认证
winrm set winrm/config/service/auth '@{Basic="true"}'
winrm set winrm/config/service '@{AllowUnencrypted="true"}'
```

##### 3. Windows firewall open for Winrm 

```powershell
查看winrm service启动监听状态
winrm enumerate winrm/config/listener
添加防火墙信任规则，允许5985端口通过
```

##### 4.  Ansible master 

###### 1. Ansible master configure

```bash
# 添加windows客户端连接信息
vim /etc/ansible/hosts
[win]
172.16.37.3 ansible_ssh_user="Administrator" ansible_ssh_pass="Westlife@#ibm" ansible_ssh_port=5985 ansible_connection="winrm" ansible_winrm_server_cert_validation=ignore

# 安装winrm 模块
pip search pywinrm # pip search 没办法用了
pi p install pywinrm # 无法安装，需要具体版本
pip install "pywinrm>=0.2.2"  # 这样安装
```

###### 2. 测试ping探测windows客户主机是否存活

```bash
ansible win -m win_ping
```

###### 3. 测试文件管理

```bash
测试在windows主机执行远程创建目录
# ansible win -m win_file -a 'dest=c:\config_dir state=directory'

测试将ansible主机上的/etc/hosts文件同步到windows主机的指定目录下
# ansible win -m win_copy -a 'src=/etc/hosts dest=c:\config_dir\hosts.txt'

删除文件
# ansible win -m win_file -a 'dest=c:\config_dir\hosts.txt state=absent'

删除目录
# ansible win -m win_file -a 'dest=c:\config_dir2 state=absent'
```

###### 4. 测试远程执行cmd命令

```bash
# ansible win -m win_shell -a 'ipconfig'
```

###### 5. 远程重启windows服务器

```bash
# ansible 172.16.10.23 -m win_reboot

# ansible 172.16.10.23 -m win_shell -a 'shutdown -r -t 0'
```

###### 6. Windows服务管理

```bash
Ansible命令格式：
ansible [主机|主机组] -m win_shell -a “net stop|start 服务名”
```

###### 7. 测试创建用户(远程在windows客户端上创建用户)

```bash
# ansible win -m win_user -a "name=winuser passwd=windows"
```

###### 8. 使用举例

```bash
ansible-console
root@all (3)[f:10]$ cd win
root@win (1)[f:10]$ list
172.16.37.3
root@win (1)[f:10]$ win_hostname name=win2k2016  #更改主机名
172.16.37.3 | CHANGED => {
    "changed": true,
    "old_name": "WIN-UIS7GLE4Q9K",
    "reboot_required": true
}
root@win (1)[f:10]$ win_reboot msg="Ansible reboot in next 15s!!!" pre_reboot_delay=15  #重启机器
172.16.37.3 | CHANGED => {
    "changed": true,
    "elapsed": 190,
    "rebooted": true
}
root@win (1)[f:10]$ win_
Display all 106 possibilities? (y or n)
win_acl                      win_environment              win_netbios                  win_scheduled_task
win_acl_inheritance          win_eventlog                 win_nssm                     win_scheduled_task_stat
win_audit_policy_system      win_eventlog_entry           win_optional_feature         win_security_policy
win_audit_rule               win_feature                  win_owner                    win_service
win_certificate_store        win_file                     win_package                  win_share
```
#### 常用的ansible 模块


参考地址：

[https://docs.ansible.com/ansible/latest/modules/modules_by_category.html](http://www.yunweipai.com/go?_=1c6a53dc99aHR0cHM6Ly9kb2NzLmFuc2libGUuY29tL2Fuc2libGUvbGF0ZXN0L21vZHVsZXMvbW9kdWxlc19ieV9jYXRlZ29yeS5odG1s)

---

常用的模块：

`ping`，`command` ，`shell` ，`script`，`copy` ， `fetch`，`hostname`，`file`，`unarchive`  ， `archive`，`yum`，`cron`，`service`，`user` ， `group`，`lineinfile` ，`replace`，`setup`...

command & shell:

```bash
# 注意区别和相同
# command 不能识别变量以及引号内容
root@unix (2)[f:10]$ command echo $HOSTNAME
172.16.37.2 | CHANGED | rc=0 >>
$HOSTNAME
172.16.37.4 | CHANGED | rc=0 >>
$HOSTNAME
root@unix (2)[f:10]$ shell echo $HOSTNAME
172.16.37.2 | CHANGED | rc=0 >>
ansible-master
172.16.37.4 | CHANGED | rc=0 >>
ansible-node1
root@node1 (1)[f:10]$ shell echo passwd |passwd --stdin test
172.16.37.4 | CHANGED | rc=0 >>
更改用户 test 的密码 。
passwd：所有的身份验证令牌已经成功更新。
root@node1 (1)[f:10]$ command echo passwd |passwd --stdin test
172.16.37.4 | CHANGED | rc=0 >>
passwd |passwd --stdin test
```

unarchive & archive:

```bash
ansible all -m unarchive -a 'src=/tmp/foo.zip dest=/data copy=no mode=0777'
ansible all -m unarchive -a 'src=https://example.com/example.zip dest=/data copy=no'
ansible websrvs -m archive  -a 'path=/var/log/ dest=/data/log.tar.bz2 format=bz2  owner=wang mode=0600'
```

cron:

```bash
#备份数据库脚本
[root@centos8 ~]#cat mysql_backup.sh 
mysqldump -A -F --single-transaction --master-data=2 -q -uroot |gzip > /data/mysql_date +%F_%T.sql.gz
#创建任务
ansible 10.0.0.8 -m cron -a 'hour=2 minute=30 weekday=1-5 name="backup mysql" job=/root/mysql_backup.sh'
ansible websrvs   -m cron -a "minute=*/5 job='/usr/sbin/ntpdate 172.20.0.1 &>/dev/null' name=Synctime"
#禁用计划任务
ansible websrvs   -m cron -a "minute=*/5 job='/usr/sbin/ntpdate 172.20.0.1 &>/dev/null' name=Synctime disabled=yes"
#启用计划任务
ansible websrvs   -m cron -a "minute=*/5 job='/usr/sbin/ntpdate 172.20.0.1 &>/dev/null' name=Synctime disabled=no"
#删除任务
ansible websrvs -m cron -a "name='backup mysql' state=absent"
ansible websrvs -m cron -a 'state=absent name=Synctime'
```

service:

```bash
ansible all -m service -a 'name=httpd state=started enabled=yes'
ansible all -m service -a 'name=httpd state=stopped'
ansible all -m service -a 'name=httpd state=reloaded’
ansible all -m shell -a "sed -i 's/^Listen 80/Listen 8080/' /etc/httpd/conf/httpd.conf"
ansible all -m service -a 'name=httpd state=restarted' 
```

user & group:

```bash
#创建用户
ansible all -m user -a 'name=user1 comment=“test user” uid=2048 home=/app/user1 group=root'
ansible all -m user -a 'name=nginx comment=nginx uid=88 group=nginx groups="root,daemon" shell=/sbin/nologin system=yes create_home=no  home=/data/nginx non_unique=yes'
#删除用户及家目录等数据
ansible all -m user -a 'name=nginx state=absent remove=yes'
#创建组
ansible websrvs -m group  -a 'name=nginx gid=88 system=yes'
#删除组
ansible websrvs -m group  -a 'name=nginx state=absent'
```

lineinfile:

ansible在使用sed进行替换时，经常会遇到需要转义的问题，而且ansible在遇到特殊符号进行替换时，存在问题，无法正常进行替换 。其实在ansible自身提供了两个模块：lineinfile模块和replace模块，可以方便的进行替换功能：相当于sed，可以修改文件内容

```bash
ansible all -m   lineinfile -a "path=/etc/selinux/config regexp='^SELINUX=' line='SELINUX=enforcing'"
ansible all -m lineinfile  -a 'dest=/etc/fstab state=absent regexp="^#"'
```
replace:

该模块有点类似于sed命令，主要也是基于正则进行匹配和替换

```bash
ansible all -m replace -a "path=/etc/fstab regexp='^(UUID.*)' replace='#\1'"  
ansible all -m replace -a "path=/etc/fstab regexp='^#(.*)' replace='\1'"
```

setup:

setup 模块来收集主机的系统信息，这些 facts 信息可以直接以变量的形式使用，但是如果主机较多，会影响执行速度，可以使用`gather_facts: no`

```bash
ansible all -m setup
ansible all -m setup -a "filter=ansible_os_family
ansible all -m setup -a "filter=ansible_hostname"
```

  https://www.cnblogs.com/keerya/p/7987886.html
