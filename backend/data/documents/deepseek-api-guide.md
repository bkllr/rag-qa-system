# DeepSeek API 使用指南

DeepSeek 提供 OpenAI 兼容的 API 接口，支持对话补全和流式输出。

## API 信息

- **Base URL**: `https://api.deepseek.com`
- **模型**: `deepseek-chat`
- **接口兼容**: OpenAI API 格式
- **定价**: 按 token 计费，价格极低

## 获取 API Key

1. 访问 https://platform.deepseek.com/
2. 注册账号
3. 在 API Keys 页面创建密钥

## 基本调用

### Python（OpenAI SDK）

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.deepseek.com",
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个技术助手"},
        {"role": "user", "content": "什么是RAG?"},
    ],
    temperature=0.3,
    max_tokens=2048,
)

print(response.choices[0].message.content)
```

### 流式输出

```python
stream = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好"}],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## 在 LangChain 中使用

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    api_key="your-api-key",
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
    temperature=0.3,
    streaming=True,
)

# 同步调用
response = llm.invoke("什么是RAG?")
print(response.content)

# 流式调用
for chunk in llm.stream("什么是RAG?"):
    print(chunk.content, end="")
```

## 参数说明

| 参数 | 说明 | 推荐值 |
|:--|:--|:--|
| model | 模型名称 | deepseek-chat |
| temperature | 采样温度 | 0.3（稳定回答）|
| max_tokens | 最大输出长度 | 2048 |
| stream | 是否流式 | True |
| top_p | 核采样概率 | 0.95 |

## 错误处理

```python
try:
    response = llm.invoke("你好")
except Exception as e:
    print(f"API 调用失败: {e}")
    # 常见错误：
    # 401: API Key 无效
    # 429: 请求频率超限
    # 500: 服务器内部错误
```

## 优势

1. **价格极低**: 比 GPT-4 便宜约 100 倍
2. **中文能力强**: 对中文理解和生成效果好
3. **OpenAI 兼容**: 无需修改代码，替换 base_url 即可
4. **流式支持**: 原生支持流式输出
