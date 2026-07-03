# MySQL 索引优化

## 索引类型
- B+Tree: 最常用，适合范围查询
- Hash: 等值查询快
- 全文索引: 文本搜索

## 创建原则
1. WHERE/JOIN/ORDER BY 字段建索引
2. 区分度高的字段优先
3. 联合索引最左前缀原则
4. 避免过多索引影响写入

```sql
CREATE INDEX idx_email ON users(email);
EXPLAIN SELECT * FROM users WHERE email = 'test@test.com';
```