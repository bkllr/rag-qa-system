# JWT 认证机制

## 结构: Header.Payload.Signature

## Python 使用
```python
import jwt
token = jwt.encode({"user_id": 123}, secret, algorithm="HS256")
payload = jwt.decode(token, secret, algorithms=["HS256"])
```

## 优势
- 无状态，适合分布式系统
- 自包含，无需查数据库

## 注意事项
- Payload 不加密（base64编码）
- 无法撤销（除非黑名单）
- 需设置合理过期时间