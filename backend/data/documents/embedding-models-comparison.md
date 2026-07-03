# Embedding 模型对比与选择

## 主流中文 Embedding 模型

| 模型 | 维度 | 大小 | 中文效果 | 速度 |
|:--|:--|:--|:--|:--|
| text2vec-base-chinese | 768 | 400MB | 优秀 | 中等 |
| bge-large-zh-v1.5 | 1024 | 1.3GB | 最佳 | 较慢 |
| m3e-base | 768 | 420MB | 良好 | 中等 |
| stella-base-zh | 768 | 400MB | 良好 | 较快 |

## 选择因素

1. 任务场景：检索/分类/聚类
2. 算力限制：GPU/CPU
3. 延迟要求：实时/离线
4. 存储成本：向量维度影响存储

## 评估方法

```python
from sentence_transformers import evaluation

evaluator = evaluation.EmbeddingSimilarityEvaluator(
    sentences1=["查询1"], sentences2=["文档1"], scores=[0.9]
)
score = evaluator(model)
```
