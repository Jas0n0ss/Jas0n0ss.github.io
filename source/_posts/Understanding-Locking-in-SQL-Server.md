---
title: Understanding-Locking-in-SQL-Server
description: Understanding-Locking-in-SQL-Server
date: 2022-09-20 01:03:51
tags: 
  - SQL Server
  - Deadlock
  - Performance
categories: 'SQL Server'
---
{% youtube -zgFVWCieVI %}

> Thinking

- What is Resource types in locking of SQL Server?
- What is Lock Modes in SQL Server?

It gives live view of looking at different type of lock modes as well as the resources types where the locks are placed. It describes in greater detail about RID, Key, Page, Extent, Table and DB Resource types in SQL Server Locking concept. It also explains Shared Locks, Update Lock, Exclusive Locks, Intent Lock, Schema Lock and Bulk Update locks in SQL Server.

```sql
--Script that you can run to look at Live Locks and resource types in SQL Server:
exec sp_lock;
GO
```

