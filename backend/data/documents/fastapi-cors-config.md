# FastAPI CORS 跨域配置

CORS（跨域资源共享）是浏览器的安全机制，限制网页从不同域名请求资源。FastAPI 通过中间件处理 CORS。

## 配置方式

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 参数说明

| 参数 | 说明 | 推荐值 |
|:--|:--|:--|
| allow_origins | 允许的源列表 | 开发环境指定具体端口 |
| allow_credentials | 是否允许携带 Cookie | True |
| allow_methods | 允许的 HTTP 方法 | `["*"]` 或具体方法 |
| allow_headers | 允许的请求头 | `["*"]` 或具体头 |

## 开发 vs 生产

开发环境可以宽松配置，生产环境必须严格限制：

```python
# 开发环境
allow_origins=["*"]

# 生产环境
allow_origins=["https://your-domain.com"]
```

## 常见问题

1. **SSE 跨域问题**: StreamingResponse 的 SSE 请求也需要 CORS 支持
2. **预检请求**: 浏览器会先发 OPTIONS 请求，CORSMiddleware 会自动处理
3. **allow_origins=["*"] 与 allow_credentials=True 冲突**: 不能同时使用
