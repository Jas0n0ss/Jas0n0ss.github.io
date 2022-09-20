---
title: nginx-dav+aliyundrive-fuse
description: nginx-dav+aliyundrive-fuse
date: 2022-09-19 11:01:01
tags: [webdav,Nginx]
categories: Nginx
---

##### 源码编译Nginx Dav模块
https://www.cnblogs.com/aboa/p/16453738.html

```bash
yum install -y gcc make libpcre3-dev libssl-dev zlib1g-dev libxml2-dev libxslt-dev libgd-dev libgeoip-dev git
wget https://nginx.org/download/nginx-1.22.0.tar.gz
tar zxvf nginx-1.22.0.tar.gz && cd nginx-1.22.0
git clone https://github.com/arut/nginx-dav-ext-module.git
./configure --prefix=/usr/local/nginx \
            --with-http_dav_module \
            --with-http_image_filter_module=dynamic \
            --with-mail_ssl_module \
            --add-module=./nginx-dav-ext-module
make -j32 && make install
```

##### 配置Nginx

```nginx
mkdir include /etc/nginx/conf/ -p && mkdir /var/lib/nginx/
cat >/etc/nginx/conf/dav.conf<<EOF
server {
    server_name dav.bo.io;
    listen 80;
    location / {
      set \$dest \$http_destination;
      if (-d \$request_filename) {
        rewrite ^(.*[^/])\$ \$1/;
        set \$dest \$dest/;
      }
      if (\$request_method ~ MKCOL) {
        rewrite ^(.*[^/])\$ \$1/ break;
      }
      root /data/aliyun/;
      autoindex on;
      dav_methods PUT DELETE MKCOL COPY MOVE;
      dav_ext_methods PROPFIND OPTIONS;
      create_full_put_path on;
      client_max_body_size 0M;
      dav_access user:rw group:rw all:rw;
      auth_basic \"Authorized Users Only\";
      auth_basic_user_file /etc/nginx/webdavpasswd;
    }
}
EOF
```

##### Nginx service

```bash
echo admin:$(openssl passwd -crypt Passw0rd1)>/etc/nginx/webdavpasswd
cat >/usr/lib/systemd/system/nginx.service<<EOF
[Unit]
Description=A high performance web server and a reverse proxy server
After=network.target
[Service]
Type=forking
PIDFile=/run/nginx.pid
ExecStartPre=/usr/local/nginx/sbin/nginx -t -q -g 'daemon on; master_process on;'
ExecStart=/usr/local/nginx/sbin/nginx -g 'daemon on; master_process on;'
ExecReload=/usr/local/nginx/sbin/nginx -g 'daemon on; master_process on;' -s reload
ExecStop=-/sbin/start-stop-daemon --quiet --stop --retry QUIT/5 --pidfile /run/nginx.pid
TimeoutStopSec=5
KillMode=mixed
[Install]
WantedBy=multi-user.target">/usr/lib/systemd/system/nginx.service
EOF
#
systemctl enable nginx && systemctl start nginx
```

##### 挂载aliyun drive

https://github.com/messense/aliyundrive-fuse

```bash
mkdir -p /data/aliyun && yum install fuse3.x86_64 -y
pip3 install aliyundrive-fuse
nohup aliyundrive-fuse -r <refresh-token> -w /var/run/aliyundrive-fuse /data/aliyun &
tail nohup.out
```
![](/images/1715511-20220707104850982-1417025050.png)
![](/images/1715511-20220707105612244-309876970.png)
![](/images/1715511-20220707105636870-1265084229.png)
![](/images/1715511-20220707105648389-2100144054.png)

