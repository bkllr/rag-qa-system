# LangChain LCEL 表达式语法详解

LCEL（LangChain Expression Language）是 LangChain 0.1+ 引入的声明式链式语法，用管道符 `|` 连接 Runnable 组件。

## Runnable 协议

所有 LCEL 组件都实现 Runnable 接口，提供统一的调用方法：

```python
# 同步调用
result = runnable.invoke(input)

# 批量调用
results = runnable.batch([input1, input2])

# 流式调用
for chunk in runnable.stream(input):
    process(chunk)

# 异步调用
result = await runnable.ainvoke(input)
async for chunk in runnable.astream(input):
    process(chunk)
```

## 管道符链式调用

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template("告诉我关于{topic}的知识")
llm = ChatOpenAI(model="deepseek-chat")

# 链式组合
chain = prompt | llm | StrOutputParser()

# 调用
result = chain.invoke({"topic": "RAG"})
```

## RunnablePassthrough

`RunnablePassthrough` 用于在链中透传数据，常用于同时传递检索结果和原始问题：

```python
from langchain_core.runnables import RunnablePassthrough

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# question 会原样透传，context 由 retriever 填充
result = chain.invoke("什么是RAG?")
```

## RunnableLambda

将普通函数包装为 Runnable：

```python
from langchain_core.runnables import RunnableLambda

def format_sources(docs):
    return "\n".join([d.page_content for d in docs])

chain = retriever | RunnableLambda(format_sources) | prompt | llm
```

## 并行执行

使用 `RunnableParallel` 并行执行多个 Runnable：

```python
from langchain_core.runnables import RunnableParallel

chain = RunnableParallel(
    answer=rag_chain,
    sources=retriever,
)
```

## 自定义 Runnable

```python
from langchain_core.runnables import Runnable

class CustomRunnable(Runnable):
    def invoke(self, input, config=None):
        # 自定义处理逻辑
        return processed_result
```

## LCEL 的优势

1. **流式支持**: 所有 LCEL 链天然支持流式输出
2. **异步支持**: 自动支持 async/await
3. **批处理**: 自动支持批量调用
4. **可组合**: 组件之间自由组合
5. **可观测**: 内置 tracing 和 logging
