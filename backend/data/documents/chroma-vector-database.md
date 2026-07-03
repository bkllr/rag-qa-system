# Chroma 向量数据库使用指南

Chroma 是一个开源的向量数据库，支持嵌入式运行，无需额外部署服务。

## 安装

```bash
pip install chromadb langchain-chroma
```

## 基本用法

### 持久化模式

```python
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="shibing624/text2vec-base-chinese")

# 创建持久化向量存储
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
    collection_name="rag_documents",
)
```

### 存入文档

```python
from langchain_core.documents import Document

docs = [
    Document(page_content="RAG是检索增强生成", metadata={"source": "rag.md"}),
    Document(page_content="Chroma是向量数据库", metadata={"source": "chroma.md"}),
]

# 添加文档（自动向量化并存储）
vectorstore.add_documents(docs)
```

### 相似度检索

```python
# 返回文档列表
results = vectorstore.similarity_search("什么是RAG?", k=4)

# 返回文档 + 相似度分数
results_with_scores = vectorstore.similarity_search_with_score("什么是RAG?", k=4)

for doc, score in results_with_scores:
    print(f"Score: {score:.4f}")
    print(f"Source: {doc.metadata['source']}")
    print(f"Content: {doc.page_content[:100]}")
```

## 路径最佳实践

使用绝对路径，避免相对路径在不同工作目录下出问题：

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CHROMA_PATH = str(BASE_DIR / "chroma_db")

vectorstore = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings,
)
```

## 检索策略

| 策略 | 方法 | 说明 |
|:--|:--|:--|
| 纯相似度 | similarity_search | 按余弦相似度排序 |
| 相似度+分数 | similarity_search_with_score | 额外返回距离分数 |
| MMR | max_marginal_relevance_search | 兼顾相关性和多样性 |

## 管理操作

```python
# 获取集合信息
collection = vectorstore._collection
count = collection.count()  # 已存储的向量数

# 删除所有数据
vectorstore.delete_collection()

# 按 ID 删除
vectorstore.delete(ids=["id1", "id2"])
```

## 注意事项

1. Chroma 的 score 是距离（越小越相似），不是相似度
2. 持久化目录不要放在 git 中（加入 .gitignore）
3. 更新文档时需要先删除旧的再添加新的
