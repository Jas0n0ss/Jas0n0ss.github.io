---
title: zerossl request free ssl certificate with acme.sh
description: zerossl request free ssl certificate with acme.sh
date: 2023-01-03 15:46:01
tags: [zerossl,ssl]
categories: nginx
---

### install acme.sh

https://github.com/acmesh-official/acme.sh

https://blog.freessl.cn/acme-quick-start/

```bash
root@nas:~#  yum install -y curl socat   
root@nas:~#  wget -qO- get.acme.sh | bash
root@nas:~#  alias acme.sh=~/.acme.sh/acme.sh
root@nas:~#  crontab -l
* * * * * [ -f /etc/krb5.keytab ] && [ \( ! -f /etc/opt/omi/creds/omi.keytab \) -o \( /etc/krb5.keytab -nt /etc/opt/omi/creds/omi.keytab \) ] && sleep 5 && /opt/omi/bin/support/ktstrip /etc/krb5.keytab /etc/opt/omi/creds/omi.keytab >/dev/null 2>&1 || true
7 0 * * * "/root/.acme.sh"/acme.sh --cron --home "/root/.acme.sh" > /dev/null
```

### request ssl

```bash
# make sure you have registered real account xxxx@outlook.com on https://zerossl.com
root@nas:~# acme.sh --register-account -m xxxx@outlook.com
# if you don't have websrv on http port 80
root@nas:~# ~/.acme.sh/acme.sh  --issue -d mydomain.com   --standalone
# if you already have a websrv nginx runing on local host
root@nas:~# ~/.acme.sh/acme.sh --issue  -d <mydomain.com>  --nginx
# install ssl certificate to the path
root@nas:~# ~/.acme.sh/acme.sh --installcert -d <mydomain.com> --key-file /etc/pki/tls/private/ca.key --fullchain-file /etc/pki/tls/certs/ca.crt
```

### Nginx configure

```nginx
server {
    listen 80; # redirect to 443
    server_name AAA.example.cn www.AAA.example.cn;
    rewrite ^(.*)$  https://$host$1 permanent; 
    # return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl; # redirect to https
    server_name AAA.example.cn www.AAA.example.cn;
    ssl_certificate "/etc/pki/tls/certs/ca.crt";
    ssl_certificate_key "/etc/pki/tls/private/ca.key";
    location / {
                  proxy_pass http://127.0.0.1:8090;
                  proxy_set_header X-Real-IP $remote_addr;
                  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                  proxy_set_header Host $http_host;
                  proxy_set_header X-NginX-Proxy true;
                  proxy_redirect default;
    }
}
```

```bash
nginx -s reload && 
```

