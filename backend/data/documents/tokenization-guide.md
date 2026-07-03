# 分词器原理与实践

## 分词方法

### BPE（Byte Pair Encoding）

迭代合并高频字符对，GPT 系列使用：

```python
# 训练示例
corpus = "low low low lower"
# 合并 'l' + 'o' → 'lo'
# 合并 'lo' + 'w' → 'low'
```

### WordPiece

类似 BPE，但按语言模型似然选择合并，BERT 使用。

### SentencePiece

直接处理原始 Unicode 字符，不依赖预分词。

## 中文分词

```python
from tokenizers import Tokenizer

tokenizer = Tokenizer.from_pretrained("bert-base-chinese")

tokens = tokenizer.encode("你好世界！").tokens
# ['[CLS]', '你', '好', '世', '界', '！', '[SEP]']
```

## Token 数估算

- 英文：1 token ≈ 0.75 词
- 中文：1 token ≈ 1.5 字
- 代码：1 token ≈ 0.5 字符
