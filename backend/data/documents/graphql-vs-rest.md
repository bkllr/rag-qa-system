# GraphQL vs REST

## REST
- 多端点: /users, /users/1/posts
- 服务端定义返回结构
- 可能过度获取或不足

## GraphQL
- 单端点: /graphql
- 客户端指定返回字段
- 精确获取所需数据

| 场景 | 推荐 |
|:--|:--|
| 简单CRUD | REST |
| 复杂嵌套查询 | GraphQL |
| 移动端 | GraphQL |