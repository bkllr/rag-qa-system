# CORS 跨域资源共享

## 为什么需要 CORS
浏览器同源策略阻止跨域请求，CORS允许服务器声明哪些源可以访问。

## 预检请求 (OPTIONS)
浏览器先发 OPTIONS 确认服务器允许跨域，通过后才发实际请求。

## FastAPI 配置
```python
app.add_middleware(CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```