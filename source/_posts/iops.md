---
title: iops
description: iops
date: 2022-09-21 15:30:16
tags: iops
categories: Performance
---

### IOPS

https://learn.microsoft.com/zh-cn/azure/virtual-machines/disks-benchmarks

- IOPS test on windows-DISKSPD 
https://github.com/microsoft/diskspd/releases/download/v2.1/DiskSpd.ZIP
https://learn.microsoft.com/en-us/azure-stack/hci/manage/diskspd-overview
EXAMPLE:
```Powershell
PS C:\Users\hubo\Desktop\DiskSpd\amd64> .\diskspd.exe -c20G -w100 -b8K -F4 -r -o128 -W30 -d30 -Sh testfile.dat > OUTPUT.TXT
# view the result
notepad OUTPUT.TXT
Command Line: C:\Users\hubo\Desktop\DiskSpd\amd64\diskspd.exe -c20G -w100 -b8K -F4 -r -o128 -W30 -d30 -Sh testfile.dat
*******************************************************************************
actual test time:	30.00s
thread count:		4
proc count:		8

CPU |  Usage |  User  |  Kernel |  Idle
-------------------------------------------
   0|  20.83%|   2.08%|   18.75%|  79.17%
   1|  12.40%|   1.51%|   10.89%|  87.60%
   2|  17.40%|   2.45%|   14.95%|  82.60%
   3|  19.64%|   0.83%|   18.80%|  80.36%
   4|  15.47%|   2.60%|   12.86%|  84.53%
   5|  12.45%|   1.98%|   10.47%|  87.55%
   6|  20.21%|   2.86%|   17.34%|  79.79%
   7|  14.74%|   5.42%|    9.32%|  85.26%
-------------------------------------------
avg.|  16.64%|   2.47%|   14.17%|  83.36%

Total IO
thread |       bytes     |     I/Os     |    MiB/s   |  I/O per s |  file
------------------------------------------------------------------------------
     0 |      2655838208 |       324199 |      84.42 |   10806.30 | testfile.dat (20GiB)
     1 |      2686033920 |       327885 |      85.38 |   10929.16 | testfile.dat (20GiB)
     2 |      2670919680 |       326040 |      84.90 |   10867.67 | testfile.dat (20GiB)
     3 |      2653806592 |       323951 |      84.36 |   10798.04 | testfile.dat (20GiB)
------------------------------------------------------------------------------
total:       10666598400 |      1302075 |     339.07 |   43401.17

Read IO
thread |       bytes     |     I/Os     |    MiB/s   |  I/O per s |  file
------------------------------------------------------------------------------
     0 |               0 |            0 |       0.00 |       0.00 | testfile.dat (20GiB)
     1 |               0 |            0 |       0.00 |       0.00 | testfile.dat (20GiB)
     2 |               0 |            0 |       0.00 |       0.00 | testfile.dat (20GiB)
     3 |               0 |            0 |       0.00 |       0.00 | testfile.dat (20GiB)
------------------------------------------------------------------------------
total:                 0 |            0 |       0.00 |       0.00

Write IO
thread |       bytes     |     I/Os     |    MiB/s   |  I/O per s |  file
------------------------------------------------------------------------------
     0 |      2655838208 |       324199 |      84.42 |   10806.30 | testfile.dat (20GiB)
     1 |      2686033920 |       327885 |      85.38 |   10929.16 | testfile.dat (20GiB)
     2 |      2670919680 |       326040 |      84.90 |   10867.67 | testfile.dat (20GiB)
     3 |      2653806592 |       323951 |      84.36 |   10798.04 | testfile.dat (20GiB)
------------------------------------------------------------------------------
total:       10666598400 |      1302075 |     339.07 |   43401.17
```
**WRITE IOPS: 43401.17**

- IOPS test on Linux-fio
  https://learn.microsoft.com/zh-cn/azure/virtual-machines/disks-benchmarks#fio

```bash
# RHEL
sudo yum -y install fio
# Ubuntu
sudo apt-get install fio
```
> WRITE IOPS:

```bash
[root@node1 ~]# cat /data/fiowrite.ini
[global]
size=30g
direct=1
iodepth=256
ioengine=libaio
bs=4k
numjobs=4

[writer1]
rw=randwrite
directory=/mnt/nocache
[root@node1 ~]# mkdir /mnt/nocache/
[root@node1 ~]# sudo fio --runtime 60 /data/fiowrite.ini
writer1: (g=0): rw=randwrite, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=libaio, iodepth=256
...
fio-3.7
Starting 4 processes
writer1: Laying out IO file (1 file / 30720MiB)
writer1: Laying out IO file (1 file / 30720MiB)
writer1: Laying out IO file (1 file / 30720MiB)
writer1: Laying out IO file (1 file / 30720MiB)
Jobs: 4 (f=4): [w(4)][100.0%][r=0KiB/s,w=20.8MiB/s][r=0,w=5313 IOPS][eta 00m:00s]
```
**Write IOPS : 5313** 

> READ IOPS

```bash
[root@node1 ~]# cat >/data/fioread.ini
[global]
size=30g
direct=1
iodepth=256
ioengine=libaio
bs=4k
numjobs=4

[reader1]
rw=randread
directory=/data/readcache
[root@node1 ~]# mkdir /data/readcache
[root@node1 ~]# sudo fio --runtime 60 /data/fioread.ini
[root@node1 ~]# sudo fio --runtime 60 /data/fioread.ini
reader1: (g=0): rw=randread, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=libaio, iodepth=256
...
fio-3.7
Starting 4 processes
reader1: Laying out IO file (1 file / 30720MiB)
reader1: Laying out IO file (1 file / 30720MiB)
reader1: Laying out IO file (1 file / 30720MiB)
reader1: Laying out IO file (1 file / 30720MiB)
Jobs: 4 (f=4): [r(4)][100.0%][r=45.5MiB/s,w=0KiB/s][r=11.6k,w=0 IOPS][eta 00m:00s]
```

**Read IOPS : 11.6k**