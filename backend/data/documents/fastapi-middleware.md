# FastAPI 中间件开发

中间件在请求处理前后执行，用于日志、认证、请求修改等。

## 自定义中间件

```python
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    elapsed = time.time() - start
    response.headers["X-Process-Time"] = str(elapsed)
    return response
```

## 日志中间件

```python
import logging

@app.middleware("http")
async def log_middleware(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"  -> {response.status_code}")
    return response
```

## 错误处理中间件

```python
from fastapi.responses import JSONResponse

@app.middleware("http")
async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )
```
