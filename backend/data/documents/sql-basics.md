# SQL 基础语法

## SELECT 查询

```sql
SELECT name, age FROM users WHERE age > 18 ORDER BY age DESC LIMIT 10;
```

## JOIN 连接

| JOIN类型 | 说明 |
|:--|:--|
| INNER JOIN | 返回两个表匹配的行 |
| LEFT JOIN | 返回左表所有行 |
| RIGHT JOIN | 返回右表所有行 |

## 索引优化

```sql
CREATE INDEX idx_users_age ON users(age);
CREATE INDEX idx_users_name_age ON users(name, age);
```

## 聚合函数

- COUNT: 计数
- SUM: 求和
- AVG: 平均值
- MAX/MIN: 最大/最小值
