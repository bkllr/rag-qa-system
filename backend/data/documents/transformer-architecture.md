# Transformer 架构详解

Transformer 是 Google 2017 年提出的架构，彻底改变了 NLP 领域。

## 核心组件

### Self-Attention

```
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V
```

计算序列中每个位置与其他位置的相关性权重。

### Multi-Head Attention

多个独立的 Attention 头并行计算，从不同子空间提取特征：

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model=512, n_heads=8):
        self.heads = nn.ModuleList([
            SelfAttention(d_model // n_heads)
            for _ in range(n_heads)
        ])
```

### Position Encoding

由于 Transformer 没有循环结构，需要位置编码注入位置信息：

```python
PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

## Encoder-Decoder 结构

- Encoder：处理输入序列，生成上下文表示
- Decoder：自回归生成输出序列
