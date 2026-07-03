# LangChain 框架核心概念

LangChain 是一个用于构建 LLM 应用的开源框架，提供模块化的组件来串联 LLM、提示词、检索器等。

## 核心组件

### 1. Chat Models（聊天模型）

LangChain 通过统一的接口对接各种 LLM：

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key="your-key",
    base_url="https://api.deepseek.com",
    temperature=0.3,
)

# 同步调用
response = llm.invoke("你好")
print(response.content)
```

### 2. Prompt Templates（提示词模板）

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "请根据以下上下文回答问题。\n上下文：{context}\n问题：{question}"
)

# 格式化
formatted = prompt.format(context="RAG是检索增强生成", question="什么是RAG?")
```

### 3. Output Parsers（输出解析器）

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
# 将 AIMessage 转为纯文本字符串
```

## LCEL 表达式语法

LangChain Expression Language (LCEL) 是 LangChain 的新版链式语法，使用管道符 `|` 连接组件：

```python
# 传统方式（旧版 Chain）
# from langchain.chains import LLMChain
# chain = LLMChain(llm=llm, prompt=prompt)

# LCEL 方式（推荐）
chain = prompt | llm | StrOutputParser()

# 调用
result = chain.invoke({"context": "...", "question": "..."})
```

## 流式输出

LCEL 原生支持流式输出：

```python
# 同步流式
for chunk in chain.stream({"question": "你好"}):
    print(chunk, end="", flush=True)

# 异步流式
async for chunk in chain.astream({"question": "你好"}):
    print(chunk, end="", flush=True)
```

## 模块化包结构

LangChain 0.3+ 采用模块化包结构：
- `langchain-core`: 核心抽象（Runnable, PromptTemplate 等）
- `langchain-openai`: OpenAI/兼容接口集成
- `langchain-community`: 社区集成（各种加载器、工具）
- `langchain-chroma`: Chroma 向量数据库集成
- `langchain-huggingface`: HuggingFace 模型集成
