# WebSocket 协议

WebSocket 是全双工通信协议，适合实时应用。

## 与 SSE 对比

| 特性 | WebSocket | SSE |
|:--|:--|:--|
| 方向 | 双向 | 服务器→客户端 |
| 协议 | ws:// | HTTP |
| 复杂度 | 较高 | 低 |

## Python 实现

```python
# FastAPI WebSocket
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        await ws.send_text(f"Echo: {data}")
```

## JavaScript 客户端

```javascript
const ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = (event) => console.log(event.data);
ws.send("Hello Server!");
```
