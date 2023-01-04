---
title: how to restore files with git
description: how to restore files with git
date: 2023-01-04 17:21:32
tags: git
categories: devops
---

> sometimes we may git delete some files by mistake, well. Don't panic, there is way to restore deleted files:

Here's example of simulating remove file:

```bash
~/Desktop/Jas0n0ss.github.io (main*) » touch test                                                                                                                
~/Desktop/Jas0n0ss.github.io (main*) » git add test && git commit -m 'test' && git push
~/Desktop/Jas0n0ss.github.io (main*) » rm -f test # remove test file
~/Desktop/Jas0n0ss.github.io (main*) » git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	deleted:    test   # status showing the file have been removed
```

Here's example of restores the file:

```bash
~/Desktop/Jas0n0ss.github.io (main*) » git reset HEAD test
Unstaged changes after reset:
D	test
~/Desktop/Jas0n0ss.github.io (main*) » git checkout test
Updated 1 path from the index
~/Desktop/Jas0n0ss.github.io (main*) » ll test   # the file have been restored
.rw-r--r-- 0 jason  4 1 17:33 test
~/Desktop/Jas0n0ss.github.io (main*) » git status
On branch main
Your branch is up to date with 'origin/main'.
```

> more usage of `git` command:

https://www.runoob.com/git/git-basic-operations.html

