# FastAPI 依赖注入系统

FastAPI 的依赖注入系统是最强大的特性之一，通过 `Depends` 实现。

## 基本用法

```python
from fastapi import FastAPI, Depends

def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
async def get_users(db: Database = Depends(get_db)):
    return db.query("SELECT * FROM users")
```

## 依赖嵌套

```python
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Database = Depends(get_db),
) -> User:
    user_id = decode_token(token)
    return db.get_user(user_id)

@app.get("/me")
async def me(user: User = Depends(get_current_user)):
    return user
```

## 带参数的依赖

```python
def pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/items/")
async def items(page: dict = Depends(pagination)):
    return get_items(**page)
```
