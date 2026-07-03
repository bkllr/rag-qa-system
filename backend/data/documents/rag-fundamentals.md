# RAG 检索增强生成原理

RAG（Retrieval-Augmented Generation，检索增强生成）是一种结合信息检索和大语言生成的技术架构。

## 为什么需要 RAG

大语言模型（LLM）存在以下局限：

1. **知识截止**: 训练数据有截止日期，不知道最新信息
2. **幻觉问题**: 可能生成看似合理但实际错误的内容
3. **领域知识不足**: 对特定领域的知识了解有限
4. **无法访问私有数据**: 无法直接使用企业内部文档

RAG 通过在生成前检索相关文档来缓解这些问题。

## RAG 工作流程

```
用户问题
  │
  ├── 1. 向量检索：在知识库中搜索相关文档片段
  │
  ├── 2. 上下文构建：将检索结果拼接为 context
  │
  ├── 3. Prompt 构建：将 context + question 组装为提示词
  │
  ├── 4. LLM 生成：调用大模型生成回答
  │
  └── 5. 返回结果：回答 + 来源引用
```

## 核心组件

### Embedding 模型

将文本转换为向量表示：

```python
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="shibing624/text2vec-base-chinese"
)

# 文本转向量
vector = embeddings.embed_query("什么是RAG?")
# 文档转向量
vectors = embeddings.embed_documents(["文档1", "文档2"])
```

### 向量数据库

存储文档向量，支持相似度检索：

```python
from langchain_chroma import Chroma

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
)

# 存入文档
vectorstore.add_documents(documents)

# 检索
results = vectorstore.similarity_search_with_score("查询内容", k=4)
```

### 检索器

LangChain 的检索器接口：

```python
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

# 检索
docs = retriever.invoke("查询内容")
```

## RAG 的优势

| 对比项 | 纯 LLM | RAG |
|:--|:--|:--|
| 知识更新 | 需要重新训练 | 更新文档库即可 |
| 准确性 | 可能幻觉 | 基于文档回答 |
| 私有数据 | 无法使用 | 直接支持 |
| 可追溯性 | 无法引用来源 | 可提供来源引用 |
| 成本 | 训练成本高 | 只需文档管理 |
