# Python 设计模式实战

## 单例模式

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

## 工厂模式

```python
class LoaderFactory:
    _loaders = {}

    @classmethod
    def register(cls, ext, loader_cls):
        cls._loaders[ext] = loader_cls

    @classmethod
    def create(cls, ext):
        return cls._loaders[ext]()

# 注册
LoaderFactory.register(".txt", TextLoader)
LoaderFactory.register(".pdf", PDFLoader)
```

## 观察者模式

```python
class EventBus:
    def __init__(self):
        self._handlers = {}

    def on(self, event, handler):
        self._handlers.setdefault(event, []).append(handler)

    def emit(self, event, **data):
        for handler in self._handlers.get(event, []):
            handler(**data)
```
