# HTTP REST API 设计规范

## URL 命名规范

```
GET    /api/users          # 列表
POST   /api/users          # 创建
GET    /api/users/{id}     # 详情
PUT    /api/users/{id}     # 全量更新
PATCH  /api/users/{id}     # 部分更新
DELETE /api/users/{id}     # 删除
```

## 响应状态码

| 状态码 | 含义 |
|:--|:--|
| 200 | 成功 |
| 201 | 创建成功 |
| 204 | 删除成功（无返回体）|
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 422 | 参数验证失败 |
| 500 | 服务器错误 |

## 响应格式

```json
{
    "data": { ... },
    "meta": {
        "page": 1,
        "page_size": 10,
        "total": 100
    }
}
```

## 错误响应

```json
{
    "error": "NOT_FOUND",
    "message": "用户不存在",
    "detail": {"user_id": 999}
}
```
