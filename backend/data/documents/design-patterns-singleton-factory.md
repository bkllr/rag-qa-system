# 单例与工厂模式在 RAG 系统中的应用

## 单例模式

在 RAG 系统中，LLM 和 Embedding 模型应该使用单例模式避免重复加载：

```python
class LLMManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.model = load_model()
            self._initialized = True
```

优势：避免重复初始化，节约内存和启动时间。

## 工厂模式

文档加载器使用工厂模式：

```python
class LoaderFactory:
    def create_loader(self, file_path: str):
        ext = Path(file_path).suffix.lower()
        if ext == ".pdf":
            return PyPDFLoader(file_path)
        elif ext in (".md", ".txt"):
            return TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError(f"不支持的文件格式: {ext}")
```

## 策略模式

检索策略可以动态切换：

```python
class RetrievalStrategy(ABC):
    @abstractmethod
    def retrieve(self, query: str, k: int) -> list: ...

class SimilarityStrategy(RetrievalStrategy): ...
class MMRStrategy(RetrievalStrategy): ...
class HybridStrategy(RetrievalStrategy): ...
```
