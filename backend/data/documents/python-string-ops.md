# Python 字符串操作

## 基本方法

```python
s = "hello world"
s.upper()          # HELLO WORLD
s.lower()          # hello world
s.title()          # Hello World
s.split()          # ["hello", "world"]
s.replace("h","H") # Hello world
s.strip()          # 去两端空白
```

## f-string 格式化 (推荐)

```python
name = "张三"
f"你好 {name}"           # 你好 张三
f"价格 {price:.2f}"      # 价格 99.00
```

## 常用判断

- `isdigit()`: 是否纯数字
- `isalpha()`: 是否纯字母
- `startswith(prefix)`: 前缀判断
- `endswith(suffix)`: 后缀判断
- `join(list)`: 列表拼字符串
