# 小米 DeepSpark 深度学习框架

DeepSpark 是小米开源的深度学习训练与推理加速库。

## 核心功能

1. 分布式训练优化
2. 模型压缩与量化
3. 推理加速
4. 支持 PyTorch/TensorFlow

## 模型量化

```python
# 将 float32 模型量化为 int8
from deepspark import quantize

model = torch.load("model.pth")
quantized = quantize(model, dtype="int8", calibration_data=calib_data)
torch.save(quantized, "model_int8.pth")
```

## 分布式训练

```python
# 多卡训练加速
trainer = DeepSparkTrainer(
    model=model,
    strategy="ddp",  # 分布式数据并行
    devices=[0, 1, 2, 3],
    precision="fp16",  # 混合精度
)
trainer.fit(train_data)
```
