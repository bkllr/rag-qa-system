# LangChain 文档加载器

LangChain 提供了丰富的文档加载器，支持从各种数据源加载文档。

## 文本文件加载

### TextLoader

加载纯文本和 Markdown 文件：

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader("document.md", encoding="utf-8")
docs = loader.load()
# docs[0].page_content 是文件内容
# docs[0].metadata["source"] 是文件路径
```

### PyPDFLoader

加载 PDF 文件，按页拆分：

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("document.pdf")
docs = loader.load()
# 每个 Document 对应 PDF 的一页
# docs[0].metadata["page"] 是页码
```

## 批量加载

### DirectoryLoader

从目录批量加载文件：

```python
from langchain_community.document_loaders import DirectoryLoader

loader = DirectoryLoader(
    "./documents",
    glob="**/*.md",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
)
docs = loader.load()
```

## Document 对象结构

```python
from langchain_core.documents import Document

doc = Document(
    page_content="文档内容...",
    metadata={
        "source": "file.md",
        "page": 1,
        "author": "张三",
    }
)
```

## 文本切片

加载后的文档需要切片才能进行向量检索：

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],
)

chunks = splitter.split_documents(docs)
```

### 切片策略选择

| 策略 | 适用场景 | 特点 |
|:--|:--|:--|
| RecursiveCharacterTextSplitter | 通用文本 | 递归分隔符，保持语义完整性 |
| CharacterTextSplitter | 简单文本 | 单一分隔符 |
| TokenTextSplitter | LLM 输入 | 按 token 数切分 |
| MarkdownHeaderTextSplitter | Markdown 文档 | 按标题层级切分 |

## 中文文档注意事项

1. **编码**: 必须指定 `encoding="utf-8"`，否则中文会乱码
2. **分隔符**: 中文文本应使用中文标点作为分隔符
3. **chunk_size**: 中文字符数与 token 数不同，建议按字符数设置
