# LangChain Agents 与 Tools

## Agent 概念

Agent 使用 LLM 决定执行哪些操作、以什么顺序执行。

```python
from langchain.agents import create_react_agent
from langchain.tools import Tool

tools = [
    Tool(name="search", func=search_docs, description="搜索文档"),
    Tool(name="calculator", func=calculate, description="数学计算"),
]

agent = create_react_agent(llm, tools, prompt)
result = agent.invoke({"input": "查找RAG相关文档并统计数量"})
```

## 自定义 Tool

```python
from langchain.tools import tool

@tool
def search_docs(query: str) -> str:
    """在文档库中搜索相关内容"""
    results = vector_store.search(query, k=3)
    return "\n".join([r.page_content for r in results])
```

## Tool 装饰器参数

- `name`: 工具名称（LLM 用它来识别）
- `description`: 工具描述（LLM 用它来判断何时使用）
- `return_direct`: 是否直接返回结果给用户
