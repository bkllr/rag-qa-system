# Python 基础语法概览

Python 是一种高级、通用的编程语言，以其简洁的语法和强大的标准库而闻名。

## 数据类型

Python 内置了以下基本数据类型：

- **int**: 整数类型，如 `42`
- **float**: 浮点数类型，如 `3.14`
- **str**: 字符串类型，如 `"hello"`
- **bool**: 布尔类型，`True` 或 `False`
- **list**: 列表，有序可变序列，如 `[1, 2, 3]`
- **tuple**: 元组，有序不可变序列，如 `(1, 2, 3)`
- **dict**: 字典，键值对集合，如 `{"name": "Python"}`
- **set**: 集合，无序不重复元素集合，如 `{1, 2, 3}`

## 控制流

### 条件语句

```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"
```

### 循环

```python
# for 循环
for item in items:
    print(item)

# while 循环
while condition:
    do_something()
```

## 函数定义

Python 使用 `def` 关键字定义函数，支持默认参数、可变参数和关键字参数：

```python
def greet(name, greeting="你好"):
    return f"{greeting}, {name}!"

# 调用
greet("梁岚瑞")  # 你好, 梁岚瑞!
greet("World", greeting="Hello")  # Hello, World!
```

## 类与面向对象

Python 是一门面向对象的语言，所有数据类型都是对象：

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return f"{self.name}: 汪汪！"
```

## 模块与导入

Python 通过 `import` 语句导入模块：

```python
import os
from datetime import datetime
import numpy as np
```
