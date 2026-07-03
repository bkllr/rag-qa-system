# Python 生成器与 yield 详解

生成器是 Python 中一种特殊的迭代器，使用 `yield` 关键字产生值。

## 基本语法

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for num in countdown(5):
    print(num)  # 5, 4, 3, 2, 1
```

## 生成器表达式

类似于列表推导式，但使用圆括号：

```python
# 列表（一次性创建）
squares_list = [x**2 for x in range(1000)]

# 生成器（惰性求值，节省内存）
squares_gen = (x**2 for x in range(1000))
```

## 无限生成器

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
```

## 生成器的优势

1. 内存效率：按需生成值，不一次性加载
2. 延迟计算：只在需要时才执行
3. 可组合：多个生成器可以串联处理数据流
