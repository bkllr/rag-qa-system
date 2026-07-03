# Python 异常处理最佳实践

## try/except/finally/else

```python
try:
    result = dangerous_operation()
except ValueError as e:
    print(f"值错误: {e}")
except (KeyError, IndexError) as e:
    print(f"键/索引错误: {e}")
else:
    print(f"成功，结果: {result}")
finally:
    cleanup()
```

## 自定义异常

```python
class RAGError(Exception):
    def __init__(self, message: str, source: str = ""):
        self.source = source
        super().__init__(message)

class DocumentNotFoundError(RAGError): ...
class EmbeddingError(RAGError): ...
```

## 异常链

```python
try:
    process_data()
except ValueError as e:
    raise RAGError("数据处理失败") from e
```

## 最佳实践

1. 不要捕获裸 `except:`（会吞掉 SystemExit 等）
2. 使用 `finally` 释放资源
3. 提供有意义的错误信息
4. 使用异常链保留原始异常信息
