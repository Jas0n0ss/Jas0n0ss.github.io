---
title: Linux client with AD authentication login windows SQL Server
date: 2022-09-16 16:35:02
tags: 
  - AD
  - SQL Server
description: Linux client with AD authentication login windows SQL Server
---

> Pre-Work

- linux should join AD same as SQL Server
- setspn on windows SQL Server for linux

> Windows SQL Server

```powershell
C:\Users\Administrator>setspn -L sqladmin
Registered ServicePrincipalNames for CN=sqladmin,CN=Users,DC=sqlrepro,DC=edu:
        MSSQLSvc/primarydc.sqlrepro.edu:1433
        MSSQLSvc/primarydc:1433
        MSSQLSvc/2016cl.sqlrepro.edu:1433

C:\Users\Administrator>setspn -S MSSQLSvc/linux.sqlrepro.edu:1433 sqlrepro\sqladmin     # linux.sqlrepro.edu is linux server which joined AD
Checking domain DC=sqlrepro,DC=edu

Registering ServicePrincipalNames for CN=sqladmin,CN=Users,DC=sqlrepro,DC=edu
        MSSQLSvc/linux.sqlrepro.edu:1433
Updated object

C:\Users\Administrator>setspn -L sqladmin
Registered ServicePrincipalNames for CN=sqladmin,CN=Users,DC=sqlrepro,DC=edu:
        MSSQLSvc/linux.sqlrepro.edu:1433
        MSSQLSvc/primarydc.sqlrepro.edu:1433
        MSSQLSvc/primarydc:1433
        MSSQLSvc/2016cl.sqlrepro.edu:1433
```
> linux:

```bash
[sqladmin@sqlrepro.edu@linux ~]$ hostname
linux.sqlrepro.edu
[sqladmin@sqlrepro.edu@linux ~]$ realm -v join -U "administrator@SQLREPRO.EDU" SQLREPRO.EDU
 * Resolving: _ldap._tcp.sqlrepro.edu
 * Performing LDAP DSE lookup on: 192.168.2.50
 * Successfully discovered: sqlrepro.edu
realm: Already joined to this domain
[sqladmin@sqlrepro.edu@linux ~]$ id sqladmin@SQLREPRO.EDU
uid=1626404604(sqladmin@sqlrepro.edu) gid=1626400513(domain users@sqlrepro.edu) groups=1626400513(domain users@sqlrepro.edu)
[sqladmin@sqlrepro.edu@linux ~]$ kinit sqladmin@SQLREPRO.EDU
Password for sqladmin@SQLREPRO.EDU:
[sqladmin@sqlrepro.edu@linux ~]$ klist
Ticket cache: KEYRING:persistent:1626404604:1626404604
Default principal: sqladmin@SQLREPRO.EDU

Valid starting       Expires              Service principal
08/15/2022 02:52:21  08/15/2022 12:52:21  krbtgt/SQLREPRO.EDU@SQLREPRO.EDU
        renew until 08/22/2022 02:52:18
[sqladmin@sqlrepro.edu@linux ~]$ whoami
sqladmin@sqlrepro.edu
[sqladmin@sqlrepro.edu@linux ~]$ sqlcmd -S primarydc -E -Q'select system_user'
                                                                                                           
---------------------------------------------------------------------------
SQLREPRO\sqladmin                                                                                          

(1 rows affected)

```
