# FastAPI 流式响应（StreamingResponse）

FastAPI 支持通过 `StreamingResponse` 实现流式响应，适用于大文件下载、SSE 推送、LLM 流式输出等场景。

## 基本用法

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def generate():
    for i in range(10):
        yield f"data: 第 {i} 条消息\n\n"

@app.get("/stream")
async def stream():
    return StreamingResponse(generate(), media_type="text/event-stream")
```

## Server-Sent Events (SSE)

SSE 是一种允许服务器向客户端推送实时数据的协议，基于 HTTP 长连接：

```python
import json
import asyncio

async def sse_generator():
    for i in range(5):
        data = {"count": i, "message": f"消息 {i}"}
        yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
        await asyncio.sleep(1)
    yield "data: [DONE]\n\n"

@app.post("/api/chat/stream")
async def chat_stream():
    return StreamingResponse(
        sse_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
```

## 关键要点

1. **media_type**: SSE 必须设为 `text/event-stream`
2. **数据格式**: 每条消息以 `data: ` 开头，以 `\n\n` 结尾
3. **异步生成器**: 使用 `async def` + `yield` 实现流式生成
4. **背压控制**: 异步生成器天然支持背压，不会一次性生成所有数据

## CORS 配置

流式接口也需要配置 CORS：

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```
