# SSE Server-Sent Events 详解

SSE（Server-Sent Events）是一种允许服务器通过 HTTP 长连接向客户端推送实时数据的协议。

## SSE vs WebSocket vs 轮询

| 特性 | SSE | WebSocket | 轮询 |
|:--|:--|:--|:--|
| 通信方向 | 服务器→客户端 | 双向 | 客户端→服务器 |
| 协议 | HTTP | WebSocket | HTTP |
| 复杂度 | 低 | 高 | 低 |
| 实时性 | 高 | 高 | 低 |
| 浏览器支持 | 原生支持 | 原生支持 | 原生支持 |

## SSE 数据格式

SSE 使用纯文本格式，每条消息由字段组成：

```
data: 消息内容\n
\n

data: {"type": "token", "content": "你好"}\n
\n
```

### 字段说明

- `data`: 消息内容（必须）
- `event`: 事件类型（可选）
- `id`: 事件 ID（可选）
- `retry`: 重连间隔毫秒（可选）

## 前端实现

### EventSource（原生 API）

```javascript
const eventSource = new EventSource("/api/stream");

eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log(data);
};

eventSource.onerror = (error) => {
    console.error("SSE 错误:", error);
    eventSource.close();
};
```

### fetch + ReadableStream（支持 POST）

EventSource 只支持 GET 请求，POST 请求需要用 fetch + ReadableStream：

```javascript
async function streamChat(question, onToken) {
    const response = await fetch("/api/chat/stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const text = decoder.decode(value);
        const lines = text.split("\n");

        for (const line of lines) {
            if (line.startsWith("data: ")) {
                const data = JSON.parse(line.slice(6));
                if (data.type === "token") {
                    onToken(data.content);
                }
            }
        }
    }
}
```

## 后端实现（FastAPI）

```python
import json
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def generate():
    for i in range(10):
        data = {"type": "token", "content": f"第{i}条"}
        yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
        await asyncio.sleep(0.5)

    yield f"data: {json.dumps({'type': 'done'})}\n\n"

@app.post("/api/chat/stream")
async def stream():
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )
```

## 关键注意事项

1. **Content-Type**: 必须为 `text/event-stream`
2. **分隔符**: 每条消息以 `\n\n` 结尾
3. **编码**: 使用 UTF-8 编码，中文需要 `ensure_ascii=False`
4. **连接保持**: 服务器需要保持连接不断开
5. **断线重连**: 浏览器原生支持自动重连
