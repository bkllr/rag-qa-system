# 大语言模型微调方法

## 全量微调 vs 高效微调

| 方法 | GPU 需求 | 训练时间 | 效果 |
|:--|:--|:--|:--|
| 全量微调 | 8×A100 | 数天 | 最佳 |
| LoRA | 1×A100 | 数小时 | 接近全量 |
| QLoRA | 1×24GB | 数小时 | 略低于 LoRA |
| Prompt Tuning | 1×16GB | 数小时 | 一般 |

## LoRA（Low-Rank Adaptation）

只训练低秩矩阵，冻结原模型参数：

```python
from peft import LoraConfig, get_peft_model

config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
)

model = get_peft_model(base_model, config)
model.print_trainable_parameters()
# trainable params: 0.5%
```
