# API 安全最佳实践

## 认证与授权

```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/api/secure")
async def secure_endpoint(token: str = Depends(security)):
    user = verify_token(token)
    return {"user": user}
```

## 输入验证

```python
from pydantic import BaseModel, Field, validator

class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., pattern=r'^[\w.-]+@[\w.-]+\.\w+$')
    age: int = Field(..., ge=0, le=150)

    @validator('name')
    def name_no_html(cls, v):
        if '<' in v or '>' in v:
            raise ValueError('名称不能包含 HTML 标签')
        return v
```

## 常见攻击防护

1. SQL 注入：使用参数化查询
2. XSS：转义输出、CSP 头
3. CSRF：使用 CSRF Token
4. 速率限制：防止暴力破解
