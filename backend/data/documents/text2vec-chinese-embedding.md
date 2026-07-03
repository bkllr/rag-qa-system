# text2vec-base-chinese 中文 Embedding 模型

text2vec-base-chinese 是一个专门为中文文本设计的 Embedding 模型，基于 BERT 架构微调。

## 模型信息

- **全称**: shibing624/text2vec-base-chinese
- **架构**: BERT-base
- **维度**: 768
- **最大长度**: 512 tokens
- **语言**: 中文
- **许可**: Apache 2.0

## 安装

```bash
pip install sentence-transformers langchain-huggingface
```

## 在 LangChain 中使用

```python
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="shibing624/text2vec-base-chinese",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

# 单文本向量化
vector = embeddings.embed_query("什么是检索增强生成？")
print(f"维度: {len(vector)}")  # 768

# 批量向量化
texts = ["RAG技术", "向量数据库", "大语言模型"]
vectors = embeddings.embed_documents(texts)
```

## 首次运行

首次运行时会自动从 HuggingFace 下载模型：
- 模型大小约 500MB
- 下载后缓存在 `~/.cache/huggingface/` 目录
- 后续运行直接从缓存加载

## 与英文模型对比

| 模型 | 语言 | 维度 | 中文效果 |
|:--|:--|:--|:--|
| text2vec-base-chinese | 中文 | 768 | 优秀 |
| all-MiniLM-L6-v2 | 英文 | 384 | 较差 |
| multilingual-e5-base | 多语言 | 768 | 良好 |

## 在 RAG 中的应用

```python
# 1. 文档向量化并存储
embeddings = HuggingFaceEmbeddings(model_name="shibing624/text2vec-base-chinese")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
vectorstore.add_documents(documents)

# 2. 查询向量化并检索
results = vectorstore.similarity_search_with_score("如何使用FastAPI?", k=4)
```

## 性能优化

1. **GPU 加速**: 将 `device` 改为 `"cuda"` 可以大幅提升速度
2. **批量处理**: 使用 `embed_documents()` 批量处理，比循环 `embed_query()` 快得多
3. **缓存**: 使用单例模式避免重复加载模型
4. **归一化**: 开启 `normalize_embeddings=True` 提升检索效果
