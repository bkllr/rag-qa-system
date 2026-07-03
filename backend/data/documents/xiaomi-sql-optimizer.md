# 小米 SQL 智能优化系统

小米开源的 SQL 智能优化系统，利用 AI 技术自动分析和优化数据库查询性能。

## 项目概述

该系统结合机器学习和数据库优化技术，自动识别慢查询并提供优化建议。

## 核心功能

### 1. 慢查询识别

```sql
-- 系统自动标记执行时间超过阈值的查询
-- 例如：执行时间 > 1s 的查询会被标记为慢查询
SELECT * FROM orders WHERE status = 'pending' AND created_at > '2024-01-01';
```

### 2. 索引推荐

基于查询模式分析，自动推荐合适的索引：

```sql
-- 推荐索引
CREATE INDEX idx_orders_status_created ON orders(status, created_at);
```

### 3. 执行计划分析

解析 EXPLAIN 输出，识别性能瓶颈：

```
Seq Scan on orders  (cost=0.00..154.6 rows=3567)
  Filter: (status = 'pending')
→ 推荐：添加 status 字段索引
```

### 4. SQL 重写建议

```sql
-- 原始 SQL（低效）
SELECT * FROM users WHERE YEAR(created_at) = 2024;

-- 优化建议（高效，可使用索引）
SELECT * FROM users WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';
```

## 技术架构

```
数据库慢查询日志
    │
    ├── SQL 解析器（AST 解析）
    │
    ├── 特征提取
    │     ├── 表结构信息
    │     ├── 索引信息
    │     └── 数据分布统计
    │
    ├── AI 模型推理
    │     ├── 分类：查询类型识别
    │     └── 回归：执行时间预测
    │
    └── 优化建议生成
          ├── 索引推荐
          ├── SQL 重写
          └── 分区建议
```

## 常见优化模式

| 模式 | 问题描述 | 优化方案 |
|:--|:--|:--|
| 全表扫描 | 缺少索引导致 Seq Scan | 添加合适索引 |
| 索引失效 | 函数操作导致索引失效 | 改写条件表达式 |
| N+1 查询 | 循环中执行单条查询 | 改为批量查询 |
| 大表 JOIN | 缺少过滤条件 | 添加 WHERE 条件 |
| 子查询低效 | 嵌套子查询执行慢 | 改为 JOIN |
