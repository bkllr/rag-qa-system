# 向量检索与相似度计算

向量检索是 RAG 系统的核心环节，通过计算向量之间的距离来找到最相关的文档。

## 向量化

将文本转换为固定维度的浮点数向量：

```python
# 查询向量化
query_vector = embeddings.embed_query("什么是RAG?")
# 维度取决于模型，text2vec-base-chinese 是 768 维

# 文档向量化
doc_vectors = embeddings.embed_documents(["文档1", "文档2"])
```

## 相似度度量

### 余弦相似度

衡量向量方向的一致性，值域 [-1, 1]，越大越相似：

```python
import numpy as np

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
```

### 欧氏距离

衡量向量绝对距离，值越小越相似：

```python
def euclidean_distance(v1, v2):
    return np.sqrt(np.sum((v1 - v2) ** 2))
```

### Chroma 中的距离

Chroma 默认使用 L2（欧氏距离），返回的 score 是距离值：
- score 越小，表示越相似
- score 为 0 表示完全相同

## 归一化 Embedding

使用归一化后的 embedding，余弦相似度等价于点积：

```python
embeddings = HuggingFaceEmbeddings(
    model_name="shibing624/text2vec-base-chinese",
    encode_kwargs={"normalize_embeddings": True},
)
```

## Top-K 检索

```python
# Chroma 检索 Top-4 最相关的文档片段
results = vectorstore.similarity_search_with_score(query, k=4)

# 按相似度排序（Chroma 返回的是距离，需要取反或反转）
results_sorted = sorted(results, key=lambda x: x[1])  # 距离从小到大
```

## 检索质量优化

### 1. 调整 chunk_size

- 太小（100）：语义不完整
- 太大（1000）：噪音太多
- 推荐：300-500 字符

### 2. 增加 chunk_overlap

```python
# overlap=50 保证切片边界处的语义连续性
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
```

### 3. 调整 K 值

- K=2: 精确但可能遗漏
- K=4: 平衡推荐值
- K=8: 召回高但噪音多

### 4. MMR 检索

最大边际相关性，兼顾相关性和多样性：

```python
results = vectorstore.max_marginal_relevance_search(
    query, k=4, fetch_k=20, lambda_mult=0.5
)
```
