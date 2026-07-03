# LangChain Callbacks 回调系统

Callbacks 用于监控和记录 LangChain 链的执行过程。

## 自定义 Callback

```python
from langchain.callbacks.base import BaseCallbackHandler

class RAGCallback(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"LLM 调用开始，Prompt 长度: {len(prompts[0])}")

    def on_llm_end(self, response, **kwargs):
        print(f"LLM 调用结束")

    def on_llm_error(self, error, **kwargs):
        print(f"LLM 调用出错: {error}")

    def on_retriever_end(self, documents, **kwargs):
        print(f"检索完成，找到 {len(documents)} 个文档")
```

## 使用 Callback

```python
chain.invoke(
    {"question": "什么是RAG?"},
    config={"callbacks": [RAGCallback()]}
)
```

## 常见用途

- 记录每次 LLM 调用的耗时
- 监控 token 消耗
- 追踪检索质量
- 错误告警
