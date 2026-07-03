# Python 装饰器原理与应用

装饰器是 Python 中一种强大的语法糖，用于在不修改原函数的前提下扩展其功能。

## 基本语法

装饰器本质上是一个接收函数并返回新函数的高阶函数：

```python
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} 耗时 {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)
    print("完成")
```

## 带参数的装饰器

如果装饰器本身需要参数，需要再嵌套一层：

```python
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"你好, {name}!")
```

## 使用 functools.wraps 保留元信息

装饰器会丢失原函数的元信息（`__name__`, `__doc__` 等），使用 `functools.wraps` 可以保留：

```python
from functools import wraps

def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

## 类装饰器

类也可以作为装饰器，通过实现 `__call__` 方法：

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"第 {self.count} 次调用 {self.func.__name__}")
        return self.func(*args, **kwargs)
```

## 实际应用场景

- **日志记录**: 自动记录函数调用
- **性能监控**: 测量函数执行时间
- **权限校验**: 检查用户权限
- **缓存**: 缓存函数结果（如 `functools.lru_cache`）
- **重试机制**: 自动重试失败的调用
