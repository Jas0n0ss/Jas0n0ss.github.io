---
title: SQL Server Availability Groups On Linux with Pacemaker 
description: SQL Server Availability Groups On Linux with Pacemaker 
date: 2022-09-19 18:20:14
tags: SQL Server
categories: SQL Server
---

{% youtube HpoRqs5QzRQ %}
---

* Installing SQL Server High Availability Package
* Installing and Enabling SQL Server Agent if its not installed and enabled already
* Enable SQL server High Availability on each Node
* Creating AG Group EndPoint and Certificates
* Copy Certificates of each node into all other Nodes
* Change ownership and group association to mysql(User)
* Restore each Certificate with authenticated user ( create user if you don't have already one)
* Grant AG Group using SSMS
* Create SQL Server Login and Permission for Pacemaker
* Create Availability Group resource in pacemaker
* Create IP for Listener in PackeMaker
* Create Listener using same IP
* Test Failover

- Install SQL Server High Availability Package
```bash
sudo yum install mssql-server-ha
```
-  Enable AlwaysOn Avaiability Groups and resetart SQL Server on both nodes
```bash
sudo /opt/mssql/bin/mssql-conf set hadr.hadrenabled  1
sudo systemctl restart mssql-server
```
- Open SSMS and create Certificate for each node
```sql
---Node Name : TBSLinuxNode1
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'Pass@123';
GO
CREATE CERTIFICATE TBSLinuxNode1_Cert
WITH SUBJECT = 'TBSLinuxNode1 AG Certificate';
GO
BACKUP CERTIFICATE TBSLinuxNode1_Cert
TO FILE = '/var/opt/mssql/data/TBSLinuxNode1_Cert.cer';
GO

CREATE ENDPOINT TBSSQLAG
STATE = STARTED
AS TCP (
    LISTENER_PORT = 5022,
    LISTENER_IP = ALL)
FOR DATABASE_MIRRORING (
    AUTHENTICATION = CERTIFICATE TBSLinuxNode1_Cert,
    ROLE = ALL);
GO
```
```sql
---Now samething on Node2 (TBSLinuxNode2)
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'Pass@123';
GO
CREATE CERTIFICATE TBSLinuxNode2_Cert
WITH SUBJECT = 'TBSLinuxNode2 AG Certificate';
GO
BACKUP CERTIFICATE TBSLinuxNode2_Cert
TO FILE = '/var/opt/mssql/data/TBSLinuxNode2_Cert.cer';
GO

CREATE ENDPOINT TBSSQLAG
STATE = STARTED
AS TCP (
    LISTENER_PORT = 5022,
    LISTENER_IP = ALL)
FOR DATABASE_MIRRORING (
    AUTHENTICATION = CERTIFICATE TBSLinuxNode2_Cert,
    ROLE = ALL);
GO
```
- Copy Certificate of one node to other using SCP 
```bash
# on Node1
scp -r root@TBSLinuxNode1:/var/opt/mssql/data/TBSLinuxNode1_Cert.cer 
root@TBSLinuxNode2:/var/opt/mssql/data/TBSLinuxNode1_Cert.cer
# On Node 2
scp -r root@TBSLinuxNode2:/var/opt/mssql/data/TBSLinuxNode2_Cert.cer 
root@TBSLinuxNode1:/var/opt/mssql/data/TBSLinuxNode2_Cert.cer
# Change Ownership of certificate to mssql on each node(In my case I have only two nodes)
sudo chown mssql:mssql TBSLinuxNode2_Cert.cer
sudo chown mssql:mssql TBSLinuxNode1_Cert.cer
```

- Create instance Level SQL User (TBSAGUser in my case on each node) using SSMS
Open SSMS and create User
```sql
---Restore certificate of Other Nodes into the present node using SSMS below: Login to TBSLinuxNode1
CREATE CERTIFICATE TBSLinuxNode2_Cert
AUTHORIZATION TBSAGUser
FROM FILE = '/var/opt/mssql/data/TBSLinuxNode2_Cert.cer';
---Grant permission to connec to the endpoint of TBSLinuxNode1
GRANT CONNECT ON ENDPOINT::TBSSQLAG TO TBSAGUser;
---Let's do the same thing by connecting to TBSLinuxNode2 and restore TBSLinuxNode1.cert
CREATE CERTIFICATE TBSLinuxNode1_Cert
AUTHORIZATION TBSAGUser
FROM FILE = '/var/opt/mssql/data/TBSLinuxNode1_Cert.cer';
---Grant permission to connec to the endpoint of TBSLinuxNode2
GRANT CONNECT ON ENDPOINT::TBSSQLAG TO TBSAGUser;
```
- Create Availability Group using SSMS with Cluster type External
```bash
# Create a new login or use the same login to give Pacemaker permission and provide view server permission, I will give 

#sysadmin to this user just for this demo

# On all Nodes Edit vi /var/opt/mssql/secrets/passwd using emacs and update with user and password that you created for 

Pacemaker and save it

TBSAGUser
Pass@123
# Hold down the CTRL key and then press X, then C, to exit and save the file
# setup right permission
sudo chmod 400 /var/opt/mssql/secrets/passwd

# Create the AG resource in the Pacemaker cluster
sudo pcs resource create TBSLinuxRG ocf:mssql:ag ag_name=TBSLinuxAG meta failure-timeout=30s --master meta notify=true

# Create IP resource for Listener 
sudo pcs resource create LinuxSQLProdList ocf:heartbeat:IPaddr2 ip=192.168.1.104 cidr_netmask=24

# Create an ordering constraint to ensure that the AG resource is up and running before the IP address. While the colocation 

#constraint implies an ordering constraint, this enforces it
sudo pcs constraint order promote TBSLinuxRG-master then start LinuxSQLProdList

# Let's Test Failover
```
