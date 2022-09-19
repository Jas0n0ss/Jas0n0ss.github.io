---
title: sys.fn_trace_gettable
date: 2022-09-16 17:31:32
tags: 'SQL Server'
---

#### In SQL Server, move/import a .trc file to a trace table

https://docs.microsoft.com/en-us/sql/relational-databases/system-functions/sys-fn-trace-gettable-transact-sql?view=sql-server-ver16

> `sys.fn_trace_gettable`

```sql
USE AdventureWorks;
GO
SELECT * INTO temp_trc
FROM fn_trace_gettable('c:\temp\mytrace.trc', default);
GO
--- check data from table
SELECT * FROM temp_trc
```
