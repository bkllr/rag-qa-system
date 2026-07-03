# Python 代码整洁之道

## 命名规范

```python
# 好
user_list: list[User]
MAX_RETRY_COUNT = 3
def get_user_by_id(user_id: int) -> User: ...

# 差
ul = []
max = 3
def get(u): ...
```

## 函数设计

```python
# 好：小函数，单一职责
def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def send_welcome_email(user: User) -> None:
    if not validate_email(user.email):
        raise ValueError(f"无效邮箱: {user.email}")
    email_service.send(user.email, template="welcome")
```

## 早返回模式

```python
# 好：减少嵌套
def process(data):
    if not data:
        return None
    if not validate(data):
        raise ValueError("无效数据")
    return transform(data)
```
