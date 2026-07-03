# LangChain 对话记忆机制

## ConversationBufferMemory

保存完整对话历史：

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
memory.chat_memory.add_user_message("你好")
memory.chat_memory.add_ai_message("你好！有什么可以帮助你的？")

# 获取历史消息（用于 Prompt）
history = memory.buffer_as_str
```

## ConversationSummaryMemory

对长对话做摘要：

```python
from langchain.memory import ConversationSummaryMemory

memory = ConversationSummaryMemory(llm=llm)
# 自动对历史对话生成摘要
```

## 在 RAG 中的选择

RAG 问答系统通常不需要对话记忆，因为：
1. 每次查询独立检索文档
2. 用户问的是文档相关问题
3. 记忆可能引入上下文污染

推荐：无状态 RAG + 每次查询独立检索。
