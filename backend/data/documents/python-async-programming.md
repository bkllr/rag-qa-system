# Python 异步编程详解

Python 的异步编程通过 `asyncio` 库实现，使用 `async/await` 语法编写并发代码。

## 基本概念

### 协程

协程是异步函数，使用 `async def` 定义：

```python
import asyncio

async def hello():
    print("Hello")
    await asyncio.sleep(1)
    print("World")
```

### 事件循环

事件循环是异步编程的核心，负责调度协程的执行：

```python
async def main():
    await hello()

# 运行事件循环
asyncio.run(main())
```

## 并发执行

使用 `asyncio.gather()` 并发执行多个协程：

```python
async def fetch_data(url):
    await asyncio.sleep(1)  # 模拟网络请求
    return f"Data from {url}"

async def main():
    urls = ["url1", "url2", "url3"]
    # 并发请求，总耗时约 1 秒而非 3 秒
    results = await asyncio.gather(*[fetch_data(url) for url in urls])
    print(results)
```

## 异步上下文管理器

```python
class AsyncTimer:
    async def __aenter__(self):
        self.start = asyncio.get_event_loop().time()
        return self

    async def __aexit__(self, *args):
        elapsed = asyncio.get_event_loop().time() - self.start
        print(f"耗时: {elapsed:.2f}s")
```

## 异步迭代器

```python
async def async_range(n):
    for i in range(n):
        await asyncio.sleep(0.5)
        yield i

async def main():
    async for num in async_range(5):
        print(num)
```

## 在 FastAPI 中使用异步

FastAPI 原生支持异步，路由函数可以直接用 `async def`：

```python
@app.get("/api/data")
async def get_data():
    data = await fetch_from_db()
    return {"data": data}
```
