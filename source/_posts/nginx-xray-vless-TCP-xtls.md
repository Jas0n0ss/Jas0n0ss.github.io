---
title: nginx+xray+vless+TCP+xtls
description: nginx+xray+vless+TCP+xtls
date: 2022-12-29 13:47:30
tags: xray
categories: [web,nginx]
---

> 性能

经实测 Vless+TCP+xtls-rprx-direct 比 Vmess+ws+tls+web 延迟降低一半，Chrome首页加载、Google搜索速度均有明显改善，非常建议使用。

> 配置服务器

### 一键脚本配置

https://github.com/Jas0n0ss/xray

```bash
# 云主机确保开启80和443端口，以及一个可用的域名解析到本地机器
wget https://raw.githubusercontent.com/Jas0n0ss/xray/main/Xray-TLS%2BWeb-setup.sh
chmod +x Xray-TLS+Web-setup.sh
./Xray-TLS+Web-setup.sh
```

### Xray 面板配置

相对来讲适合小白用户，图形化配置，具体可参考以下链接：

https://oss.msft.vip/x-ui/

### 基于CentOS 7/8手动配置

#### update yum repo

```bash
[root@LinuxVm ~]# sudo sed -i -e "s|mirrorlist=|#mirrorlist=|g" /etc/yum.repos.d/CentOS-*
[root@LinuxVm ~]# sudo sed -i -e "s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g" /etc/yum.repos.d/CentOS-*
```

#### Firewall and selinux

```bash
[root@LinuxVm ~]# firewall-cmd --permanent --add-service=https
[root@LinuxVm ~]# firewall-cmd --permanent --add-service=http
[root@LinuxVm ~]# firewall-cmd --reload
```

#### Install Xary-core

```bash
[root@LinuxVm ~]# bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install -u root
[root@LinuxVm ~]# xray -version
```

#### Configure Xray

```json
[root@LinuxVm ~]# uuidgen
1e059d00-9c73-48c7-abac-f69734f86706
[root@LinuxVm ~]# vim /usr/local/etc/xray/config.json
{
    "log": {
     "access": "/var/log/xray/access.log",
     "error": "/var/log/xray/error.log",
     "loglevel": "debug"
    }, 
    "inbounds": [
        {
            "listen": "0.0.0.0", 
            "port": 443, 
            "protocol": "vless", 
            "settings": {
                "clients": [
                    {
                        "id": "****", // 填写UUID,可以用uuidgen命令生成
                        "level": 0, 
                        "email": "a@b.com",
                        "flow":"xtls-rprx-direct"
                    }
                ], 
                "decryption": "none", 
                "fallbacks": [
                    {
                        "dest": 1234
                    }
                ]
            }, 
            "streamSettings": {
                "network": "tcp", 
                "security": "xtls", 
                "xtlsSettings": {
                    "serverName": "****", //换成自己的域名
                    "alpn": [
                        "http/1.1"
                    ], 
                    "certificates": [
                        {
                            "certificateFile": "/etc/pki/tls/certs/****.crt", // 换成你的证书，绝对路径
                            "keyFile": "/etc/pki/tls/private/****.key"  // 换成你的私钥，绝对路径
                        }
                    ]
                }
            }
        }
    ], 
    "outbounds": [
        {
            "protocol": "freedom", 
            "settings": { }
        }
    ]
}
# 写完可以验证一下
[root@LinuxVm ~]# /usr/local/bin/xray -test -config=/usr/local/etc/xray/config.json
```

#### Service manage

```bash
[root@LinuxVm ~]# systemctl enable xray && systemctl start xray
[root@LinuxVm ~]# service xray status
[root@LinuxVm ~]# service xray start
[root@LinuxVm ~]# service xray stop
[root@LinuxVm ~]# service xray restart
# 仅更新geoip.dat和geosite.dat：
[root@LinuxVm ~]# bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install-geodata
# 移除xray：
[root@LinuxVm ~]# bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ remove --purge
```

#### Configure nginx

```nginx
[root@LinuxVm ~]# yum install -y nginx
[root@LinuxVm ~]# vim /etc/nginx/nginx.conf
server {
    listen 80 ;
    server_name xxx; ## 换成自己的域名
    rewrite ^(.*)$ https://${server_name}$1 permanent; 
    if ($request_method  !~ ^(POST|GET)$) { return  501; }
    autoindex off;
    server_tokens off;
 }
server{
        listen 1234;
        server_name xxx; ## 换成自己的域名

	location /{
		root  /usr/share/nginx/html; 
	}
	
	index index.php index.html index.htm;
	
	if ($request_method  !~ ^(POST|GET)$) { return 501; }
        autoindex off;
        server_tokens off;
 }
# 可以做一个403伪页面放在下面目录
/usr/share/nginx/html/
```

#### start service

```bash
[root@LinuxVm ~]# nginx -t
[root@LinuxVm ~]# systemctl enable nginx && systemctl start nginx
[root@LinuxVm ~]# tail -f /var/log/xray/access.log
```

