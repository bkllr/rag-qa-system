# Prompt 工程进阶

## Few-Shot Prompting

```python
prompt = """
按要求分类：

Q: 今天天气真好
A: 日常

Q: Python 是解释型语言
A: 编程

Q: {input}
A:"""
```

## Chain of Thought

```python
prompt = """
请一步步思考：

问题：小明有 5 个苹果，吃了 2 个，又买了 3 个，还剩几个？
思路：5 - 2 = 3, 3 + 3 = 6
答案：6 个
"""
```

## 防幻觉技巧

1. 明确要求引用原文
2. 设置 "I don't know" 选项
3. 强制来源标注
4. 温度设为较低值（0.1-0.3）
5. 限制回答范围

## RAG 专属 Prompt 技巧

- 上下文放在前面
- 用分隔符隔离
- 明确优先级规则
- 提供反例（不要做什么）
