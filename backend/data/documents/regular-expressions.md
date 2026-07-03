# 正则表达式速查

## 基本元字符

| 符号 | 含义 |
|:--|:--|
| . | 任意字符 |
| * | 0次或多次 |
| + | 1次或多次 |
| ? | 0次或1次 |
| ^ | 行首 |
| $ | 行尾 |
| \d | 数字 |
| \w | 字母/数字/下划线 |
| \s | 空白字符 |

## Python 使用

```python
import re

# 搜索
result = re.search(r"pattern", text)

# 查找所有
matches = re.findall(r"\d+", "a1b2c3")  # ['1','2','3']

# 替换
new_text = re.sub(r"\s+", " ", text)

# 分组
m = re.match(r"(\w+)@(\w+)", "user@example")
print(m.group(1))  # user
```
