# 小米 Open-Falcon 监控系统

Open-Falcon 是小米开源的互联网级企业级监控系统，具有强大的数据采集、存储和告警能力。

## 项目概述

- **GitHub**: https://github.com/open-falcon/falcon-plus
- **开发语言**: Go（后端）、Python（插件）
- **特点**: 分布式、高可用、水平扩展
- **适用场景**: 大规模服务器集群监控

## 核心组件

### 1. Agent（数据采集）

部署在每台被监控的机器上，负责采集系统指标：

```
CPU 使用率、内存使用率、磁盘 IO、网络流量等
```

### 2. Transfer（数据转发）

接收 Agent 上报的数据，转发到存储后端：

```
Agent → Transfer → Graph (存储) / Judge (告警判断)
```

### 3. Graph（数据存储）

基于 RRDTool 的时序数据存储组件，负责存储和查询历史数据。

### 4. Judge（告警判断）

对比当前值与历史值，判断是否触发告警规则。

### 5. Alarm（告警分发）

接收 Judge 的告警事件，分发到各种通知渠道（邮件、短信、微信等）。

### 6. Dashboard（可视化）

Web 界面展示监控数据和告警信息。

## 架构流程

```
被监控机器
    │
    ├── Agent（采集指标）
    │
    ├── Transfer（数据转发）
    │     │
    │     ├── Graph（存储历史数据）
    │     │     │
    │     │     └── Query / Dashboard（查询展示）
    │     │
    │     └── Judge（告警判断）
    │           │
    │           └── Alarm（告警分发）
    │                 │
    │                 ├── 邮件 / 短信
    │                 └── 微信 / 钉钉
    │
    └── HBS（心跳服务器，管理 Agent 配置）
```

## 与 Prometheus 对比

| 特性 | Open-Falcon | Prometheus |
|:--|:--|:--|
| 开发语言 | Go | Go |
| 数据存储 | RRDTool / MySQL | TSDB |
| 查询语言 | 自有 API | PromQL |
| 分布式 | 原生支持 | 需 Federation |
| 适用规模 | 大规模集群 | 中大规模 |

## 安装部署

```bash
# 下载二进制
wget https://github.com/open-falcon/falcon-plus/releases/download/v0.3.1/open-falcon-v0.3.1.tar.gz

# 解压
mkdir -p /opt/falcon
tar -zxvf open-falcon-v0.3.1.tar.gz -C /opt/falcon

# 启动
cd /opt/falcon
./open-falcon start all
```
