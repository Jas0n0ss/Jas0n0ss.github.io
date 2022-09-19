---
title: How to Find Blocking and Deadlock in SQL Server
description: How to Find Blocking and Deadlock in SQL Server
date: 2022-09-20 00:41:33
tags: 
  - SQL Server
  - Performers
  - Deadlock
categories: 'SQL Server'
---

{% youtube uxlkQ1FbKyQ %}
---
- What is deadlock in SQL Server?
- What is Blocking in SQL Server?
- What is difference between deadlock and blocking in SQL Server?
- How to create deliberate deadlock for learning purposes?
- What are the deadlock traces in SQL Server?
- How to turn on deadlock traces on and off in SQL Server?
- How and where to check deadlock information in SQL Server?
---

```sql
--How to check blocking in SQL Server
Exec sp_who;
GO

--How to turn on and off traces and check Traces on SQL Server
DBCC TRACESTATUS();

--How to check If Deadlock traces are enabled or disabled
DBCC TRACESTATUS(1204,1222, -1)

--How to Turn Deadlock Traces on SQL Server
DBCC TRACEON(1204,1222, -1)

--How to Turn deadlock Traces Off
DBCC TRACEOFF(1204,1222, -1)
```

- How to create deliberate deadlock
```sql
-- Tran1

CREATE TABLE DemoDeadLock1 (SessionNumber INT)
INSERT DemoDeadLock1 SELECT 1

CREATE TABLE DemoDeadLock2 (SessionNumber INT)
INSERT DemoDeadLock2 SELECT 1
```

```sql
--Tran2 in new session
BEGIN TRAN
UPDATE  DemoDeadLock1 SET  SessionNumber= 1
```
```sql
--Tran3
BEGIN TRAN
UPDATE  DemoDeadLock2 SET SessionNumber = 1
UPDATE  DemoDeadLock1 SET SessionNumber = 1
```
- Let's update Demodeadlock2 table in our Tran2 session
```sql
UPDATE DemoDeadLock2 SET SessionNumber = 1
```

