# FastAPI 快速入门

FastAPI 是一个现代、快速的 Python Web 框架，基于标准 Python 类型提示，支持异步编程，并自带交互式 API 文档。

## 安装

```bash
pip install fastapi uvicorn[standard]
```

## 第一个应用

```python
from fastapi import FastAPI

app = FastAPI(title="My API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}
```

启动服务：

```bash
uvicorn main:app --reload --port 8000
```

## 路径参数

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}
```

类型提示 `int` 会自动进行参数验证，传入非整数会返回 422 错误。

## 查询参数

```python
@app.get("/items/")
async def list_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

## 请求体

使用 Pydantic 模型定义请求体：

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.post("/items/")
async def create_item(item: Item):
    return {"created": item}
```

## 响应模型

```python
class ItemResponse(BaseModel):
    id: int
    name: str
    price: float

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: Item):
    return ItemResponse(id=1, name=item.name, price=item.price)
```

## 自动文档

FastAPI 自动生成交互式 API 文档：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
