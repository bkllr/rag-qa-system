# Python 文件 IO

## 基本读写

```python
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()

with open("output.txt", "w", encoding="utf-8") as f:
    f.write("hello")
```

## 文件模式
| 模式 | 说明 |
|:--|:--|
| r | 只读 |
| w | 写入（覆盖）|
| a | 追加 |
| rb/wb | 二进制模式 |