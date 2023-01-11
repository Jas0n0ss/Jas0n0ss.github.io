---
title: jelyll Tutorial
description: jelyll Tutorial
date: 2023-01-11 21:10:28
tags: jelyll
categories: [nginx,jelyll]
---

######  语言环境准备

##### 安装`Ruby`最新版

- 源码编译安装（推荐）

  ```bash
  wget https://cache.ruby-china.com/pub/ruby/2.7/ruby-2.7.0.tar.gz && tar -zxf ruby-2.7.0.tar.gz
  cd ruby-2.7.0 && ./configure && make && make install
  # 编译期间可能缺少相应的库，遇到问题自行Google
  ```

- `yum`源安装

  ```bash
  yum install ruby -y 
  ```

##### 安装以及简单配置`Jekyll`

- 修改`gem`下载源

  ```bash
  gem sources --remove https://rubygems.org/
  gem source -a https://gems.ruby-china.com
  ```

- 通过`gem`安装

  ```bash
  gem install jekyll -y
  ```

- 初始化`jekyll`网站目录结构

  ```bash
  mkdir /data/web/jekyll -p && jekyll new -d /data/web/jekyll
  tree /data/web/jekyll
  .
  ├── 404.html
  ├── about.markdown
  ├── _config.yml
  ├── Gemfile
  ├── Gemfile.lock
  ├── index.markdown
  └── _posts
      └── 2020-11-19-welcome-to-jekyll.markdown
  ```

- 开启服务

  ```bash
  cd /data/web/jekyll && jekyll serve --dtach # --dtach 后台运行
  # 可能会遇见各种样子的错误，按照提示fix，实在启动不了，可以尝试下面方式
  bundle exec jekyll serve  
  Configuration file: /mdata/web/jekyll/_config.yml
              Source: /mdata/web/jekyll
         Destination: /mdata/web/jekyll/_site
   Incremental build: disabled. Enable with --incremental
        Generating... 
         Jekyll Feed: Generating feed for posts
                      done in 0.977 seconds.
   Auto-regeneration: enabled for '/mdata/web/jekyll'
      Server address: http://127.0.0.1:4000/
    Server running... press ctrl-c to stop.
  ```

  看到服务已经启动在本地`4000`端口了.

##### Nginx 反向代理`4000`端口

- `nginx`安装（略）

- `nginx`反向代理配置

  ```nginx
  server {
  	server_name www.example.com;
    listen 80;
    index index.html;
    location / {
      	http_proxy http://127.0.0.1:4000;
    }
  }
  ```

- nginx 直接访问

``nginx``可以把`jekyll`生成的静态网站目录作为`nginx`的根目录,`jekyll`服务不可断掉，因为你新写的文章需要持续转换为``静态网页文件``才可以访问.

- `nginx.conf`

  ```nginx
  server {
  	server_name www.example.com;
    listen 80;
    location / {
      	index index.html;
      	root /data/web/jekyll/_site;
    }
  }
  ```

###### 新添加文章

新建的文件以`markdown`语法创作，完成后文件名必须是``yyyy-mm-dd-name-name.md``的格式保存到`/data/web/jekyll_posts`目录下，jekyll才会转换格式。

###### 升华部分

除了这种简单方式还可以用`github+github pages+jekyll ` 或者``gitlab+gitlab pages+jekyll`` 则两种结构组合的方式，去自动持续集成，本地完成编辑push后，自动触发自动构建发布.

###### 推荐的主题以及使用方法

- 使用 `Sphinx`

  - [Sphinx 配置方法](https://cloud.tencent.com/developer/article/1525551)

  - [Sphinx主题](https://sphinx-rtd-theme.readthedocs.io/en/latest/installing.html)

  - https://github.com/readthedocs/sphinx_rtd_theme

- `jekyll`主题

  - [jekyll-rtd-theme](https://rundocs.io/)

  - https://github.com/hubowestlife/jekyll-rtd-theme

  - https://github.com/hubowestlife/HardCandy-Jekyll

  ---

  ```yaml
  image: ruby:2.6
  
  variables:
    JEKYLL_ENV: production
    LC_ALL: C.UTF-8
    
  before_script:
    - gem install bundler:2.1.4
    - gem install jekyll-rtd-theme
    - bundle install
  
  test:
    stage: test
    script:
      - bundle exec jekyll build -d test
    artifacts:
      paths:
        - test
    except:
      - master
  
  pages:
    stage: deploy
    script:
      - bundle exec jekyll build -d public
    artifacts:
      paths:
        - public
    only:
      - master
  ```

  

  
