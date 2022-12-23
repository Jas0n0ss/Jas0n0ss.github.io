---
title: Prometheus Tutorial
description: Prometheus Tutorial
date: 2022-12-23 17:54:45
tags: Prometheus
categories: Monitor
---

## 0 简介

Prometheus是最初在SoundCloud上构建的开源系统监视和警报工具包 。自2012年成立以来，许多公司和组织都采用了Prometheus，该项目拥有非常活跃的开发人员和用户社区。现在，它是一个独立的开源项目，并且独立于任何公司进行维护。为了强调这一点并阐明项目的治理结构，Prometheus 在2016年加入了 Cloud Native Computing Foundation，这是继Kubernetes之后的第二个托管项目。

- 强大的多维度数据模型。
- 时间序列数据通过 metric 名和键值对来区分。
- 所有的 metrics 都可以设置任意的多维标签。
- 数据模型更随意，不需要刻意设置为以点分隔的字符串。
- 可以对数据模型进行聚合，切割和切片操作。
- 支持双精度浮点类型，标签可以设为全 unicode。
- 灵活而强大的查询语句（PromQL）：在同一个查询语句，可以对多个 metrics 进行乘法、加法、连接、取分数位等操作。
- 易于管理： Prometheus server 是一个单独的二进制文件，可直接在本地工作，不依赖于分布式存储。
- 高效：平均每个采样点仅占 3.5 bytes，且一个 Prometheus server 可以处理数百万的 metrics。
- 使用 pull 模式采集时间序列数据，这样不仅有利于本机测试而且可以避免有问题的服务器推送坏的 metrics。
- 可以采用 push gateway 的方式把时间序列数据推送至 Prometheus server 端。
- 可以通过服务发现或者静态配置去获取监控的 targets。
- 有多种可视化图形界面。
- 易于伸缩。

## 1 基础环境

| 环境/组件  | 版本               | 下载地址                                                     |
| ---------- | ------------------ | ------------------------------------------------------------ |
| 操作系统   | CentOS7.6          | https://archive.kernel.org/centos-vault/7.6.1810/isos/x86_64/CentOS-7-x86_64-Minimal-1810.iso |
| Prometheus | 2.25.0             | https://github.com/prometheus/prometheus/releases/download/v2.25.0/prometheus-2.25.0.linux-amd64.tar.gz |
| Go         | 1.16               | https://golang.org/dl/go1.16.linux-amd64.tar.gz              |
| Grafana    | yum install latest | https://mirror.tuna.tsinghua.edu.cn/help/grafana/            |

## 2 安装Prometheus

### 2.1 安装

```bash
tar zxf prometheus-2.25.0.linux-amd64.tar.gz -C /opt
mv /opt/prometheus-2.25.0.linux-amd64 /opt/prometheus
```

### 2.2 配置开机自启动

```bash
vim /usr/lib/systemd/system/prometheus.service
[Unit]
Description=prometheus service
 
[Service]
User=root
ExecStart=/opt/prometheus/prometheus --config.file=/opt/prometheus/prometheus.yml --storage.tsdb.path=/opt/prometheus/data
 
TimeoutStopSec=10
Restart=on-failure
RestartSec=5
 
[Install]
WantedBy=multi-user.target
systemctl daemon-reload
systemctl enable prometheus
```

### 2.3 启动服务

```bash
systemctl start prometheus
systemctl status prometheus
```

### 2.4 验证

浏览器打开IP:9090端口即可打开 prometheus 自带的监控页面：

[![img](../images/prometheus-native-ui.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/prometheus-native-ui.png)

## 3 安装Grafana

普罗米修斯默认的页面可能没有那么直观，我们可以安装grafana使监控看起来更直观。

### 3.1 配置清华大学的yum源

打开浏览器输入地址：`https://mirror.tuna.tsinghua.edu.cn/help/grafana/`，复制CentOS/Redhat用户部分：

```bash
vim /etc/yum.repos.d/grafana.repo
[grafana]
name=grafana
baseurl=https://mirrors.tuna.tsinghua.edu.cn/grafana/yum/rpm
repo_gpgcheck=0
enabled=1
gpgcheck=0
yum makecache
```

### 3.2 安装Grafana

```bash
yum install grafana -y
```

### 3.3 启动服务

```bash
systemctl daemon-reload
systemctl enable grafana-server
systemctl start grafana-server
```

### 3.4 访问Grafana

浏览器访问IP:3000端口，即可打开grafana页面，默认用户名密码都是admin，初次登录会要求修改默认的登录密码：

[![img](../images/grafana-login.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/grafana-login.png)

[![img](../images/grafana-login-pass.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/grafana-login-pass.png)

[![img](../images/grafana-login-home.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/grafana-login-home.png)

### 3.5 添加Prometheus数据源

点击主界面的“Add your first data source”并选择Prometheus：

[![img](../images/grafana-add-first-source.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/grafana-add-first-source.png)

[![img](../images/grafana-select.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/grafana-select.png)

Dashboards页面选择“Prometheus 2.0 Stats”进行Import：

[![img](../images/prometheus-dashboard.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/prometheus-dashboard.png)

Settings页面填写普罗米修斯地址并保存：

[![img](../images/prometheus-settings.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/prometheus-settings.png)

切换到我们刚才添加的“Prometheus 2.0 Stats”即可看到整个监控页面：

[![img](../images/prometheus-dashboard-2.0.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/prometheus-dashboard-2.0.png)

## 4 一些常用监控示例

### 4.1 监控Linux机器(node_exporter)

- 下载地址：

```
https://github.com/prometheus/node_exporter/releases/download/v1.1.1/node_exporter-1.1.1.linux-amd64.tar.gz
```

- 被监控的机器安装node_exporter：

```bash
tar zxf node_exporter-1.1.1.linux-amd64.tar.gz -C /opt
mv /opt/node_exporter-1.1.1.linux-amd64 /opt/node_exporter
```

- 启动服务：

配置开机自启动：

```bash
vim /usr/lib/systemd/system/node_exporter.service
[Unit]
Description=node_exporter service
 
[Service]
User=root
ExecStart=/opt/node_exporter/node_exporter
 
TimeoutStopSec=10
Restart=on-failure
RestartSec=5
 
[Install]
WantedBy=multi-user.target
systemctl daemon-reload
systemctl enable node_exporter
```

启动服务：

```bash
systemctl start node_exporter
systemctl status node_exporter
```

- Prometheus配置文件添加监控项：

```bash
vim /opt/prometheus/prometheus.yml
  - job_name: 'linux-node'
    static_configs:
    - targets: ['192.168.0.112:9100']
      labels:
        instance: linux-node1
```

重启Prometheus：

```bash
systemctl restart prometheus
```

- grafana导入画好的dashboard：

Json文件下载地址：[node-exporter_rev5.json](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/node-exporter_rev5.json)

或者使用ID导入的方式：`8919`

[![img](../images/ne-manage.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/ne-manage.png)

[![img](../images/ne-import.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/ne-import.png)

[![img](../images/ne-upload.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/ne-upload.png)

修改名字，选择我们前文创建好的数据源，点击导入即可：

[![img](../images/ne-rename1.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/ne-rename1.png)

下面这个提示是grafana缺少相关显示需要用到的插件piechart，grafana的默认插件目录是/var/lib/grafana/plugins，可以将下载好的插件解压到这个目录，重启grafana即可

[![img](../images/ne-no-plugin.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/ne-no-plugin.png)

插件下载地址：[grafana-piechart-panel](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/grafana-piechart-panel-5f249d5.zip)

```bash
unzip -q grafana-piechart-panel-5f249d5.zip -d /var/lib/grafana/plugins/
systemctl restart grafana-server
```

查看已安装插件：

```bash
/usr/sbin/grafana-cli plugins ls
installed plugins:
grafana-piechart-panel @ 1.3.3
```

Tips：安装插件还有另外一种命令行方式：

```bash
grafana-cli plugins install grafana-piechart-panel
grafana-cli plugins install digiapulssi-breadcrumb-panel
grafana-cli plugins install grafana-polystat-panel
 
systemctl restart grafana-server
```

再刷新grafana页面，即可看到我们刚才设置好的node监控：

[![img](../images/ne-success.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/ne-success.png)

### 4.2 监控MySQL(mysqld_exporter)

- 在被监控服务器创建监控用户：

```bash
GRANT REPLICATION CLIENT, PROCESS ON *.* TO 'mysqld_exporter'@'127.0.0.1' identified by 'mysqld_exporter';
GRANT SELECT ON performance_schema.* TO 'mysqld_exporter'@'127.0.0.1';
flush privileges;
```

- 下载地址：

```
https://github.com/prometheus/mysqld_exporter/releases/download/v0.12.1/mysqld_exporter-0.12.1.linux-amd64.tar.gz
```

- 被监控的机器安装mysqld_exporter：

```bash
mkdir -p /opt
tar zxf mysqld_exporter-0.12.1.linux-amd64.tar.gz -C /opt
mv /opt/mysqld_exporter-0.12.1.linux-amd64 /opt/mysqld_exporter
cd /opt/mysqld_exporter
```

- 设置配置文件，user为数据库登录用户，password为这个用户的密码：

```bash
vim .my.cnf
 
[client]
host=127.0.0.1
port=3306
user=mysqld_exporter
password=mysqld_exporter
```

- 配置开机自启动并启动服务：

```bash
vim /usr/lib/systemd/system/mysqld_exporter.service
[Unit]
Description=mysqld_exporter service
 
[Service]
User=root
ExecStart=/opt/mysqld_exporter/mysqld_exporter --config.my-cnf=/opt/mysqld_exporter/.my.cnf
 
TimeoutStopSec=10
Restart=on-failure
RestartSec=5
 
[Install]
WantedBy=multi-user.target
systemctl daemon-reload
systemctl enable mysqld_exporter
systemctl start mysqld_exporter
systemctl status mysqld_exporter
```

- prometheus配置文件中加入mysql监控并重启：

```bash
vim /opt/monitor/prometheus/prometheus.yml
  - job_name: 'mysqld-node'
    static_configs:
    - targets: ['192.168.1.235:9104']
      labels:
        instance: mysqld-node1
```

重启服务：

```bash
systemctl restart prometheus
```

模板Json文件下载地址：[mysql_rev1.json](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/mysql_rev1.json)

- 导入已经画好的dashboard，数据源选择刚刚创建好的 `prometheus` 数据源即可：

[![img](../images/mysqld-6.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/mysqld-6.png)

[![img](../images/mysqld-7.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/mysqld-7.png)

[![img](../images/mysqld-8.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/mysqld-8.png)

[![img](../images/mysqld-9.png)](https://picture-bed-iuskye.oss-cn-beijing.aliyuncs.com/prometheus/mysqld-9.png)

Tips: 导入模板那里也可以采用输入grafana id的方式进行import，这里我们不用上传该json文件，而是输入id `7362`，然后点击 `load` 按钮即可：

[![img](../images/grafana-import-id.png)](https://oss.iuskye.com/article/2021-03-30/grafana-import-id.png)

[![img](../images/grafana-import-rename.png)](https://oss.iuskye.com/article/2021-03-30/grafana-import-rename.png)

[![img](../images/grafana-import-mysql.png)](https://oss.iuskye.com/article/2021-03-30/grafana-import-mysql.png)

### 4.3 监控Redis(redis_exporter)

- 下载地址：

```
https://github.com/oliver006/redis_exporter/releases/download/v1.20.0/redis_exporter-v1.20.0.linux-amd64.tar.gz
```

- 安装redis_exporter：

```bash
mkdir -p /opt/redis_exporter
tar zxf redis_exporter-v1.20.0.linux-amd64.tar.gz -C /opt/redis_exporter
```

- 配置开机自启动并启动服务：

```bash
vim /usr/lib/systemd/system/redis_exporter.service
[Unit]
Description=redis_exporter service
 
[Service]
User=root
ExecStart=/opt/redis_exporter/redis_exporter -redis.addr redis://192.168.1.235:6379 -redis.password 123456
 
TimeoutStopSec=10
Restart=on-failure
RestartSec=5
 
[Install]
WantedBy=multi-user.target
systemctl daemon-reload
systemctl enable redis_exporter
systemctl start redis_exporter
systemctl status redis_exporter
```

- prometheus配置文件中加入redis监控并重启：

```bash
vim /opt/prometheus/prometheus.yml
  - job_name: 'redis-node'
    static_configs:
    - targets: ['192.168.0.116:9121']
      labels:
        instance: redis-node1
```

重启服务：

```bash
systemctl restart prometheus
```

- grafana导入画好的dashboard：

Grafana ID: 4074 或者 14091

[![img](../images/grafana-redis-dash.png)](https://oss.iuskye.com/article/2021-03-30/grafana-redis-dash.png)

### 4.4 监控Elasticsearch(elasticsearch_exporter)

- 下载地址：

```
https://github.com/justwatchcom/elasticsearch_exporter/releases/download/v1.1.0/elasticsearch_exporter-1.1.0.linux-amd64.tar.gz
```

- 安装elasticsearch_exporter：

```bash
mkdir -p /opt
tar zxf elasticsearch_exporter-1.1.0.linux-amd64.tar.gz -C /opt/
mv /opt/elasticsearch_exporter-1.1.0.linux-amd64 /opt/elasticsearch_exporter
```

- 配置开机自启动并启动服务：

```bash
vim /usr/lib/systemd/system/elasticsearch_exporter.service
[Unit]
Description=elasticsearch_exporter service
 
[Service]
User=root
ExecStart=/opt/elasticsearch_exporter/elasticsearch_exporter --es.uri=http://elastic:123456@127.0.0.1:9200
 
TimeoutStopSec=10
Restart=on-failure
RestartSec=5
 
[Install]
WantedBy=multi-user.target
vim /usr/lib/systemd/system/elasticsearch_exporter.service
systemctl daemon-reload
systemctl enable elasticsearch_exporter
systemctl start elasticsearch_exporter
systemctl status elasticsearch_exporter
```

- prometheus配置文件中加入elasticsearch监控并重启：

```bash
vim /opt/prometheus/prometheus.yml
  - job_name: 'elasticsearch-node'
    static_configs:
    - targets: ['192.168.0.116:9114']
      labels:
        instance: elasticsearch-node1
```

- 这里提供一段通过公网https协议进行监控的配置项：

```bash
  - job_name: 'es-node'
    static_configs:
    - targets: ['mmbapoc.zhizhangyi.com:9070']
      labels:
        instance: es-node1
    scheme: https
    metrics_path: /es/node1
```

解释一下：scheme指定pull数据的协议为https，metrics_path指定Exporter机器上Nginx反向代理匹配路径，见下文。

- Nginx反向代理配置：

```bash
    location /es/node1 {
        proxy_pass   http://127.0.0.1:9114/metrics;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
```

解释一下，该Nginx部署在内网中，Prometheus通过公网请求Nginx，然后由Nginx反向代理到Exporter服务器。

- 重启服务：

```bash
systemctl restart prometheus
```

- grafana导入画好的dashboard：

Grafana ID: 2322

[![img](../images/grafana-es-dash.png)](https://oss.iuskye.com/article/2021-03-30/grafana-es-dash.png)

### 4.5 监控Rabbitmq(rabbitmq_exporter)

- 下载地址：

```
https://github.com/kbudde/rabbitmq_exporter/releases/download/v1.0.0-RC8/rabbitmq_exporter-1.0.0-RC8.linux-amd64.tar.gz
```

- 安装rabbitmq_exporter：

```bash
mkdir -p /opt
tar zxf rabbitmq_exporter-1.0.0-RC8.linux-amd64.tar.gz -C /opt
mv /opt/rabbitmq_exporter-1.0.0-RC8.linux-amd64 /opt/rabbitmq_exporter
```

- 配置开机自启动并启动服务：

```bash
vim /usr/lib/systemd/system/rabbitmq_exporter.service
[Unit]
Description=rabbitmq_exporter service
 
[Service]
User=root
ExecStart=/opt/rabbitmq_exporter/rabbitmq_exporter -config-file /opt/rabbitmq_exporter/config.json
 
TimeoutStopSec=10
Restart=on-failure
RestartSec=5
 
[Install]
WantedBy=multi-user.target
vim /opt/rabbitmq_exporter/config.json
 
{
    "rabbit_url": "http://127.0.0.1:15672",
    "rabbit_user": "rabbitadmin",
    "rabbit_pass": "123456",
    "publish_port": "9119",
    "publish_addr": "",
    "output_format": "TTY",
    "ca_file": "ca.pem",
    "cert_file": "client-cert.pem",
    "key_file": "client-key.pem",
    "insecure_skip_verify": false,
    "exlude_metrics": [],
    "include_queues": ".*",
    "skip_queues": "^$",
    "skip_vhost": "^$",
    "include_vhost": ".*",
    "rabbit_capabilities": "no_sort,bert",
    "enabled_exporters": [
            "exchange",
            "node",
            "overview",
            "queue"
    ],
    "timeout": 30,
    "max_queues": 0
}
vim /usr/lib/systemd/system/rabbitmq_exporter.service
systemctl daemon-reload
systemctl enable rabbitmq_exporter
systemctl start rabbitmq_exporter
systemctl status rabbitmq_exporter
```

- prometheus配置文件中加入rabbitmq监控并重启：

```bash
vim /opt/prometheus/prometheus.yml
  - job_name: 'rabbitmq-node'
    static_configs:
    - targets: ['192.168.0.116:9119']
      labels:
        instance: rabbitmq-node1
```

- 这里提供一段通过公网https协议进行监控的配置项：

```bash
  - job_name: 'rabbitmq-node'
    static_configs:
    - targets: ['mmbapoc.zhizhangyi.com:9070']
      labels:
        instance: rabbitmq-node1
    scheme: https
    metrics_path: /rabbitmq/node1
```

解释一下：scheme指定pull数据的协议为https，metrics_path指定Exporter机器上Nginx反向代理匹配路径，见下文。

- Nginx反向代理配置：

```bash
    location /rabbitmq/node1 {
        proxy_pass   http://127.0.0.1:9119/metrics;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
```

解释一下，该Nginx部署在内网中，Prometheus通过公网请求Nginx，然后由Nginx反向代理到Exporter服务器。

- 重启服务：

```bash
systemctl restart prometheus
```

- grafana导入画好的dashboard：

Grafana ID: 10120

[![img](../images/grafana-mq-dash1.png)](https://cdn.iuskye.com/article/2021-03-30/grafana-mq-dash1.png)

[![img](../images/grafana-mq-dash2.png)](https://cdn.iuskye.com/article/2021-03-30/grafana-mq-dash2.png)

### 4.6 监控JMX(jmx_exporter)

以下配置与业务联系紧密，不具有广泛参考性！

[源码地址](https://github.com/prometheus/jmx_exporter) | [编译后下载地址](https://oss.iuskye.com/article/2021-03-31/jmx_prometheus_javaagent-0.15.0.jar)

将上述jar文件上传至项目目录下，我们以 `mmba-service` 为例，将jar包存放在 `mmba-service/classes/jmx_prometheus_javaagent-0.15.0.jar`。

修改 `mmba-service` 服务的启动参数：

- 原来：

```bash
nohup java -Dconfig.cluster=${ZOOKEEPER_URL} -Xmx1G -Xms1G -classpath \
        ./:../lib/* com.uusafe.analyze.mmba.service.App >/dev/null 2>&1 &
```

- 修改后：

```bash
nohup java -javaagent:./jmx_prometheus_javaagent-0.15.0.jar=9501:./config_jmx.yml \
    -Dcom.sun.management.jmxremote.ssl=false \
    -Dcom.sun.management.jmxremote.authenticate=false \
    -Dcom.sun.management.jmxremote.port=5555 \
    -Dconfig.cluster=${ZOOKEEPER_URL} \
    -Xmx1G -Xms1G \
    -classpath ./:../lib/* com.uusafe.analyze.mmba.service.App >/dev/null 2>&1 &
```

主要区别是：

```bash
-javaagent:./jmx_prometheus_javaagent-0.15.0.jar=9501:./config_jmx.yml \
    -Dcom.sun.management.jmxremote.ssl=false \
    -Dcom.sun.management.jmxremote.authenticate=false \
    -Dcom.sun.management.jmxremote.port=5555 \
```

`config_jmx.yml` 配置文件内容：

```bash
---
startDelaySeconds: 0
hostPort: 127.0.0.1:5555
ssl: false
lowercaseOutputName: false
lowercaseOutputLabelNames: false
```

注意端口要一致，启动服务Java服务。

配置Nginx代理：

```bash
    location /java/mmba/service {
        proxy_pass   http://127.0.0.1:9501/metrics;
          proxy_set_header Host $http_host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
    }
```

这个路径是自定义的路径，要与下文中 `prometheus` 的配置文件中 `metrics_path` 值匹配。

重载Nginx：

```bash
/opt/nginx/sbin/nginx -s reload
```

修改 `prometheus` 配置文件：

```bash
sudo vim prometheus.yml
  - job_name: 'mmba-service'
    static_configs:
    - targets: ['mmba116.test.com:9070']
      labels:
        instance: mmba-service
    scheme: https
    metrics_path: /java/mmba/service
```

重启 `prometheus` 服务：

```bash
sudo systemctl restart prometheus
```

登录grafana面板配置 `dashboard`：

导入模板那里输入 `grafana id` 为 `10519` 。

示例截图：

[![img](../images/jmx-dash.png)](https://oss.iuskye.com/article/2021-03-31/jmx-dash.png)

## 5 常用网站

- prometheus download: `https://prometheus.io/download/`
- prometheus exporter: `https://prometheus.io/docs/instrumenting/exporters/`
- grafana dashboard: `https://grafana.com/dashboards`
- grafana plugins: `https://grafana.com/plugins`
