---
title: ladp-server-on-rhel-server
description: Install & Configure Openldap Server & Client in Redhat Enterprise Linux 7
date: 2022-09-20 17:52:23
tags: LADP
categories: Linux
---

{% youtube ZO4DyRb-5KI %}

ldapserver.nehraclasses.com 192.168.1.170
ldapclient.nehraclasses.com 192.168.1.180

### Server Configuration:

1. Install the required LDAP Packages.
  ```bash
  [root@ldapserver ~]# yum -y install openldap* migrationtools
  ```

2. Create a LDAP root passwd for administration purpose
  ```bash
  [root@ldapserver ~]# slappasswd
  New password:
  Re-enter new password:
  ```

3. Edit the OpenLDAP Server Configuration
  ```bash
  [root@ldapserver ~]# vim /etc/openldap/slapd.d/cn=config/olcDatabase={2}hdb.ldif
  ```

4. Provide the Monitor privileges.
  ```bash
  [root@ldapserver cn=config]# vim /etc/openldap/slapd.d/cn=config/olcDatabase={1}monitor.ldif
  [root@ldapserver cn=config]# slaptest -u
  config file testing succeeded
  ```

5. Enable and Start the SLAPD service.
  ```bash
  [root@ldapserver cn=config]# systemctl start slapd
  [root@ldapserver cn=config]# systemctl enable slapd
  [root@ldapserver cn=config]# netstat -lt | grep ldap
  ```

6. Configure the LDAP Database.
  ```bash
  [root@ldapserver cn=config]# cp /usr/share/openldap-servers/DB_CONFIG.example /var/lib/ldap/DB_CONFIG
  [root@ldapserver cn=config]# chown -R ldap:ldap /var/lib/ldap/
  Add the following LDAP Schemas.
  [root@ldapserver cn=config]# ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/cosine.ldif
  [root@ldapserver cn=config]# ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/nis.ldif
  [root@ldapserver cn=config]# ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/inetorgperson.ldif
  ```

7. Create the self-signed certificate
  ```bash
  [root@ldapserver cn=config]# openssl req -new -x509 -nodes -out /etc/pki/tls/certs/nehraclassesldap.pem -keyout /etc/pki/tls/certs/nehraclassesldapkey.pem -days 365
  Verify the created certificates under the location /etc/pki/tls/certs/
  [root@ldapserver cn=config]# ll /etc/pki/tls/certs/*.pem
  ```

8. Create base objects in OpenLDAP.
  ```bash
  [root@ldapserver cn=config]# cd /usr/share/migrationtools/
  [root@ldapserver migrationtools]# vim migrate_common.ph
  $DEFAULT_MAIL_DOMAIN = "nehraclasses.com";
  $DEFAULT_BASE = "dc=nehraclasses,dc=com";
  $EXTENDED_SCHEMA = 1;
  ```

9. Generate a base.ldif file for your Domain.
  ```bash
  [root@ldapserver migrationtools]# touch /root/base.ldif
  ```

10. Create Local Users.
    ```bash
    [root@ldapserver migrationtools} # useradd ldapuser1
    [root@ldapserver migrationtools} # useradd ldapuser2
    [root@ldapserver migrationtools] # echo "redhat" | passwd --stdin ldapuser1
    [root@ldapserver migrationtools] # echo "redhat" | passwd --stdin ldapuser2
    [root@ldapserver migrationtools]# grep ":10[0-9][0-9]" /etc/passwd /root/passwd
    [root@ldapserver migrationtools]# grep ":10[0-9][0-9]" /etc/group  /root/group
    [root@ldapserver migrationtools]# ./migrate_passwd.pl /root/passwd /root/users.ldif
    [root@ldapserver migrationtools]# ./migrate_group.pl /root/group /root/groups.ldif
    ```

11. Import Users in to the LDAP Database.
    ```bash
    [root@ldapserver migrationtools]# ldapadd -x -W -D "cn=Manager,dc=nehraclasses,dc=com" -f /root/base.ldif
    [root@ldapserver migrationtools]# ldapadd -x -W -D "cn=Manager,dc=nehraclasses,dc=com" -f /root/users.ldif
    [root@ldapserver migrationtools]# ldapadd -x -W -D "cn=Manager,dc=nehraclasses,dc=com" -f /root/groups.ldif
    ```

12. Test the configuration.
    ```bash
    [root@ldapserver migrationtools]# ldapsearch -x cn=ldapuser1 -b dc=nehraclasses,dc=com
    [root@ldapserver migrationtools]# ldapsearch -x -b 'dc=nehraclasses,dc=com' '(objectclass=*)'
    ```

13. Stop Firewalld to allow the connection.
    ```bash
    [root@ldapserver migrationtools]# systemctl stop firewalld
    [root@ldapserver migrationtools]# setenforce 0
    ```

14. NFS Configuration to export the Home Directory.
    ```bash
    [root@ldapserver ~]# vim /etc/exports
    /home (rw,sync)
    # Enable and restart rpcbind and nfs service.
    [root@ldapserver ~]# yum -y install rpcbind nfs*
    [root@ldapserver ~]# systemctl start rpcbind
    [root@ldapserver ~]# systemctl start nfs
    [root@ldapserver ~]# systemctl enable rpcbind
    [root@ldapserver ~]# systemctl enable nfs
    # Test the NFS Configuration.
    [root@ldapserver ~]# showmount -e
    ```

    ---

### Client Configuration:

1. Ldap Client Configuration to use LDAP Server.
  ```bash
  [root@ldapclient ~]# yum install -y openldap-clients nss-pam-ldapd rpcbind* nfs*
  ```

2. Start & Enable the services.

   ```bash
   # systemctl start rpcbind
   # systemctl start nfs
   # systemctl enable rpcbind
   # systemctl enable nfs
   ```
3. Mount the LDAP Users Home Directory.

   ```bash
   # vim /etc exports
   /home/ *(rw)
   # showmount -e localhost
   ```

4. Configure LDAP Authentication.

   ```bash
   # authconfig-tui
   ```
5. Mount the /home directory.

   ```bash
   # Make the entry in AutoFS.
   # mount ldapserver.nehraclasses.com:/home   /home
   
   ```

6. Test the Client Configuration.
  ```bash
  [root@ldapclient ~]# getent passwd ldapuser1
  ldapuser1:x:1000:1000:ldapuser1:/home/ldapuser1:/bin/bash
  ```

7. Switch in the account of ldap user and create some files.

   ```bash
   su - ldapuser1
   # Now go to the Ldapserver, and verify the files for ldapuser1 in his home directory.
   cd /home/ldapuser1
   ls -lh
   ```

You have successfully configured the LDAP Server & LDAP Client in RHEL 7.

