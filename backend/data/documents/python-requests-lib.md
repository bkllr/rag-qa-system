# Python requests 库详解

```python
import requests

# GET 请求
resp = requests.get("https://api.example.com/data")
data = resp.json()

# POST 请求
resp = requests.post(
    "https://api.example.com/submit",
    json={"name": "test"},
    headers={"Authorization": "Bearer token"},
)

# 超时与重试
resp = requests.get(url, timeout=5)

# 会话（复用连接）
session = requests.Session()
session.headers.update({"User-Agent": "MyApp/1.0"})
resp = session.get(url)
```

## 响应处理
- resp.status_code: HTTP 状态码
- resp.json(): JSON 解析
- resp.text: 文本内容
- resp.content: 二进制内容
