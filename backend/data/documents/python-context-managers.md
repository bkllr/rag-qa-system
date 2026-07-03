# Python 上下文管理器协议

上下文管理器通过 `with` 语句确保资源的正确获取和释放。

## 使用 with 语句

```python
# 文件操作：自动关闭
with open("file.txt", "r") as f:
    content = f.read()

# 锁管理：自动释放
with threading.Lock():
    critical_section()
```

## 自定义上下文管理器

### 类方式

```python
class DatabaseConnection:
    def __init__(self, host):
        self.host = host

    def __enter__(self):
        self.conn = connect(self.host)
        return self.conn

    def __exit__(self, exc_type, exc_val, traceback):
        self.conn.close()
        return False  # 不抑制异常
```

### 生成器方式

```python
from contextlib import contextmanager

@contextmanager
def timer(name):
    import time
    start = time.time()
    yield
    print(f"{name}: {time.time() - start:.2f}s")
```
