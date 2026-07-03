# 小米 Pegasus 分布式键值存储

Pegasus 是小米开源的分布式键值存储系统，基于 RocksDB 构建，提供高可靠、高可用的数据服务。

## 项目概述

- **GitHub**: https://github.com/apache/incubator-pegasus
- **开发语言**: C++（后端）、Java/Python/Go（客户端 SDK）
- **底层存储**: RocksDB
- **一致性协议**: PacificA（类似 Raft）
- **适用场景**: 大规模高并发键值存储

## 核心特性

1. **高可用**: 基于 PacificA 协议实现多副本一致性
2. **水平扩展**: 支持在线分片迁移和负载均衡
3. **高性能**: 毫秒级延迟，百万级 QPS
4. **多语言 SDK**: 支持 C++、Java、Python、Go 等

## 架构设计

```
┌──────────────────────────────────────────┐
│              Client SDK                  │
│     (Java / Python / Go / C++)           │
├──────────────────────────────────────────┤
│              Meta Server                 │
│   (集群管理、分片分配、负载均衡)            │
├──────────────────────────────────────────┤
│           Replica Server                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │  分片1   │  │  分片2   │  │  分片3   │  │
│  │ Primary  │  │ Primary  │  │ Primary  │  │
│  │ Secondary│  │ Secondary│  │ Secondary│  │
│  └─────────┘  └─────────┘  └─────────┘  │
├──────────────────────────────────────────┤
│              RocksDB                     │
│         (本地持久化存储)                   │
└──────────────────────────────────────────┘
```

## 数据模型

Pegasus 采用 Hash 分片模型：

- **分区键（hashkey）**: 用于分片路由
- **排序键（sortkey）**: 同一 hashkey 下排序
- **值（value）**: 任意二进制数据

```
hashkey: "user:1001"
  sortkey: "name"     → value: "张三"
  sortkey: "age"      → value: "25"
  sortkey: "email"    → value: "zhangsan@example.com"
```

## 基本操作

```java
// Java SDK 示例
PegasusClient client = PegasusClientFactory.createClient(config);

// 写入
client.set("user:1001", "name", "张三", 0);

// 读取
String value = client.get("user:1001", "name", 0);

// 删除
client.del("user:1001", "name", 0);

// 批量读取同一 hashkey 下的所有 sortkey
List<Pair<String, String>> all = client.multiGetAll("user:1001", 0);
```

## 与 Redis 对比

| 特性 | Pegasus | Redis |
|:--|:--|:--|
| 数据模型 | Hash + SortKey | 多种数据结构 |
| 持久化 | 强持久化 | RDB/AOF |
| 数据量 | TB 级 | GB 级 |
| 一致性 | 强一致 | 最终一致 |
| 适用场景 | 大数据量 KV | 缓存/小数据 |

## 应用场景

- 用户画像存储
- 消息历史记录
- 商品元数据
- 实时特征存储
