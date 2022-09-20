---
title: Linux client  login windows SQL Server with keytab
date: 2022-09-16 16:37:40
tags: 
  - AD
  - SQL Server
#description: Linux client  login windows SQL Server with keytab
---

#### Linux client  login windows SQL Server with keytab
https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-active-directory-authentication?view=sql-server-ver16
- create sql login `SQLREPRO\sqlroot` and request kdc ticket
```bash
[sqlroot@sqlrepro.edu@linux ~]$ kinit sqlroot@SQLREPRO.EDU
Password for sqlroot@SQLREPRO.EDU:
[sqlroot@sqlrepro.edu@linux ~]$ kvno sqlroot@SQLREPRO.EDU
kvno: Server not found in Kerberos database while getting credentials for sqlroot@SQLREPRO.EDU
[sqlroot@sqlrepro.edu@linux ~]$ kvno MSSQLSvc/primarydc.SQLREPRO.EDU:1433@SQLREPRO.EDU
MSSQLSvc/primarydc.SQLREPRO.EDU:1433@SQLREPRO.EDU: kvno = 2
[root@linux ~]# sqlcmd -S primarydc -Usa -Q 'CREATE LOGIN [SQLREPRO\sqlroot] FROM WINDOWS'-Q 'CREATE LOGIN [SQLREPRO\sqlroot] FROM WINDOWS'
[root@linux ~]# sqlcmd -S primarydc -Usa -Q ' SELECT name  FROM sys.server_principals WHERE name like "%sqlroot%"'
Password:
name
--------------------------------------------------------------------------------------------------------------------------------
SQLREPRO\sqlroot

(1 rows affected)
```
- create keytab on windows for user `sqlrepro\sqlroot`
```powershell
ktpass /princ MSSQLSvc/primarydc.SQLREPRO.EDU:1433@SQLREPRO.EDU /ptype KRB5_NT_PRINCIPAL /crypto aes256-sha1 /mapuser SQLREPRO\sqlroot /out sqlroot.keytab -setpass -setupn /kvno 2 /pass MyPasswo0d1
ktpass /princ MSSQLSvc/primarydc.SQLREPRO.EDU:1433@SQLREPRO.EDU /ptype KRB5_NT_PRINCIPAL /crypto rc4-hmac-nt /mapuser SQLREPRO\sqlroot /in sqlroot.keytab /out sqlroot.keytab -setpass -setupn /kvno 2 /pass MyPasswo0d1
ktpass /princ MSSQLSvc/primarydc.SQLREPRO.EDU:1433@SQLREPRO.EDU /ptype KRB5_NT_PRINCIPAL /crypto aes256-sha1 /mapuser SQLREPRO\sqlroot /in sqlroot.keytab /out sqlroot.keytab -setpass -setupn /kvno 2 /pass MyPasswo0d1
ktpass /princ MSSQLSvc/primarydc.SQLREPRO.EDU:1433@SQLREPRO.EDU /ptype KRB5_NT_PRINCIPAL /crypto rc4-hmac-nt /mapuser SQLREPRO\sqlroot /in sqlroot.keytab /out sqlroot.keytab -setpass -setupn /kvno 2 /pass MyPasswo0d1
ktpass /princ sqlroot@SQLREPRO.EDU /ptype KRB5_NT_PRINCIPAL /crypto aes256-sha1 /mapuser SQLREPRO\sqlroot /in sqlroot.keytab /out sqlroot.keytab -setpass -setupn /kvno 2 /pass MyPasswo0d1
ktpass /princ sqlroot@SQLREPRO.EDU /ptype KRB5_NT_PRINCIPAL /crypto rc4-hmac-nt /mapuser SQLREPRO\sqlroot  /in sqlroot.keytab /out sqlroot.keytab -setpass -setupn /kvno 2 /pass MyPasswo0d1
```
- copy the keytab to linux server and grant required permission
```bash
# copy the sqlroot.keytab to linux server with winscp
[root@linux ~]# chmod 755 /home/sqlroot@sqlrepro.edu/sqlroot.keytab
[root@linux ~]# chown sqlroot@SQlREPRO.EDU:mssql /home/sqlroot@sqlrepro.edu/sqlroot.keytab
[sqlroot@sqlrepro.edu@linux ~]$ kinit sqlroot@SQLREPRO.EDU -k -t sqlroot.keytab
[sqlroot@sqlrepro.edu@linux ~]$ kvno MSSQLSvc/primarydc.SQLREPRO.EDU:1433@SQLREPRO.EDU
MSSQLSvc/primarydc.SQLREPRO.EDU:1433@SQLREPRO.EDU: kvno = 2
[sqlroot@sqlrepro.edu@linux ~]$ klist
Ticket cache: KEYRING:persistent:1626404610:krb_ccache_Hw8mQWy
Default principal: sqlroot@SQLREPRO.EDU

Valid starting       Expires              Service principal
08/15/2022 04:27:47  08/15/2022 14:27:44  MSSQLSvc/primarydc.SQLREPRO.EDU:1433@SQLREPRO.EDU
        renew until 08/22/2022 04:27:44
08/15/2022 04:27:44  08/15/2022 14:27:44  krbtgt/SQLREPRO.EDU@SQLREPRO.EDU
        renew until 08/22/2022 04:27:44
```
- test connection
```bash
[sqlroot@sqlrepro.edu@linux ~]$ sqlcmd -S primarydc -E -Q 'select system_user'
                                                                                                                   
----------------------------
SQLREPRO\sqlroot                                                                                                   

(1 rows affected)

```