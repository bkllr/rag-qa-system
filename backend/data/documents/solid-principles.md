# SOLID 原则在 Python 项目中的实践

## 单一职责原则（SRP）

每个类只负责一件事：

```python
# 不好：一个类做太多事
class RAGSystem:
    def load_docs(self): ...
    def build_index(self): ...
    def search(self): ...
    def generate_answer(self): ...

# 好：职责分离
class DocumentLoader: ...
class VectorStore: ...
class RAGEngine: ...
```

## 开闭原则（OCP）

对扩展开放，对修改关闭：

```python
class BaseLoader(ABC):
    @abstractmethod
    def load(self, path: str) -> list[Document]: ...

class MarkdownLoader(BaseLoader): ...
class PDFLoader(BaseLoader): ...
class HTMLLoader(BaseLoader): ...  # 新增，无需修改原有代码
```

## 依赖倒置原则（DIP）

```python
# 依赖接口而非具体实现
class RAGEngine:
    def __init__(self, vector_store: AbstractVectorStore, llm: AbstractLLM):
        self.vector_store = vector_store
        self.llm = llm
```
