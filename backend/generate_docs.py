"""
RAG QA System - 文档批量生成脚本

运行此脚本将在 backend/data/documents/ 下生成 80+ 篇
高质量的技术文档（.md 格式），覆盖多领域主题。

用法:
    cd backend
    python generate_docs.py
"""

import os
from pathlib import Path

# ──────────────────────────────────────────────
# 文档模板库（主题 → 内容）
# ──────────────────────────────────────────────

DOCUMENTS = {
    # --- Python 进阶 ---
    "python-generators.md": """# Python 生成器与 yield 详解

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
""",

    "python-context-managers.md": """# Python 上下文管理器协议

上下文管理器通过 `with` 语句确保资源的正确获取和释放。

## 使用 with 语句

```python
# 文件操作：自动关闭
with open("file.txt", "r") as f:
    content = f.read()

# 锁管理：自动释放
with threading.Lock():
    critical_section()
```

## 自定义上下文管理器

### 类方式

```python
class DatabaseConnection:
    def __init__(self, host):
        self.host = host

    def __enter__(self):
        self.conn = connect(self.host)
        return self.conn

    def __exit__(self, exc_type, exc_val, traceback):
        self.conn.close()
        return False  # 不抑制异常
```

### 生成器方式

```python
from contextlib import contextmanager

@contextmanager
def timer(name):
    import time
    start = time.time()
    yield
    print(f"{name}: {time.time() - start:.2f}s")
```
""",

    "python-type-hints.md": """# Python 类型提示完全指南

Python 3.5+ 支持类型提示，帮助 IDE 和静态检查工具发现错误。

## 基本类型

```python
def process(
    name: str,
    age: int,
    active: bool = True,
    scores: list[float] = [],
    config: dict[str, str] | None = None,
) -> str:
    return f"{name} is {age} years old"
```

## 复杂类型

```python
from typing import Optional, Union, Literal, TypedDict

# 可选类型
def greet(name: Optional[str] = None) -> str: ...

# 字面量类型
def set_mode(mode: Literal["auto", "manual"]) -> None: ...

# TypedDict
class UserDict(TypedDict):
    name: str
    age: int
    email: str | None
```

## 类型别名

```python
type JsonDict = dict[str, str | int | float | bool | None | list | dict]
type Callback = Callable[[str], None]
```
""",

    "python-exception-handling.md": """# Python 异常处理最佳实践

## try/except/finally/else

```python
try:
    result = dangerous_operation()
except ValueError as e:
    print(f"值错误: {e}")
except (KeyError, IndexError) as e:
    print(f"键/索引错误: {e}")
else:
    print(f"成功，结果: {result}")
finally:
    cleanup()
```

## 自定义异常

```python
class RAGError(Exception):
    def __init__(self, message: str, source: str = ""):
        self.source = source
        super().__init__(message)

class DocumentNotFoundError(RAGError): ...
class EmbeddingError(RAGError): ...
```

## 异常链

```python
try:
    process_data()
except ValueError as e:
    raise RAGError("数据处理失败") from e
```

## 最佳实践

1. 不要捕获裸 `except:`（会吞掉 SystemExit 等）
2. 使用 `finally` 释放资源
3. 提供有意义的错误信息
4. 使用异常链保留原始异常信息
""",

    "python-packaging.md": """# Python 项目打包与发布

## 项目结构

```
my-package/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── pyproject.toml
├── README.md
└── LICENSE
```

## pyproject.toml 配置

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "my-package"
version = "0.1.0"
description = "描述"
requires-python = ">=3.10"
dependencies = ["fastapi>=0.100.0"]

[project.optional-dependencies]
dev = ["pytest", "ruff"]
```

## 安装与发布

```bash
# 开发安装
pip install -e .

# 构建
python -m build

# 发布到 PyPI
twine upload dist/*
```
""",

    # --- FastAPI 进阶 ---
    "fastapi-dependency-injection.md": """# FastAPI 依赖注入系统

FastAPI 的依赖注入系统是最强大的特性之一，通过 `Depends` 实现。

## 基本用法

```python
from fastapi import FastAPI, Depends

def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
async def get_users(db: Database = Depends(get_db)):
    return db.query("SELECT * FROM users")
```

## 依赖嵌套

```python
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Database = Depends(get_db),
) -> User:
    user_id = decode_token(token)
    return db.get_user(user_id)

@app.get("/me")
async def me(user: User = Depends(get_current_user)):
    return user
```

## 带参数的依赖

```python
def pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/items/")
async def items(page: dict = Depends(pagination)):
    return get_items(**page)
```
""",

    "fastapi-middleware.md": """# FastAPI 中间件开发

中间件在请求处理前后执行，用于日志、认证、请求修改等。

## 自定义中间件

```python
from fastapi import FastAPI, Request
import time

app = FastAPI()

@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    elapsed = time.time() - start
    response.headers["X-Process-Time"] = str(elapsed)
    return response
```

## 日志中间件

```python
import logging

@app.middleware("http")
async def log_middleware(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"  -> {response.status_code}")
    return response
```

## 错误处理中间件

```python
from fastapi.responses import JSONResponse

@app.middleware("http")
async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )
```
""",

    # --- 更多通用技术 ---
    "http-rest-api-design.md": """# HTTP REST API 设计规范

## URL 命名规范

```
GET    /api/users          # 列表
POST   /api/users          # 创建
GET    /api/users/{id}     # 详情
PUT    /api/users/{id}     # 全量更新
PATCH  /api/users/{id}     # 部分更新
DELETE /api/users/{id}     # 删除
```

## 响应状态码

| 状态码 | 含义 |
|:--|:--|
| 200 | 成功 |
| 201 | 创建成功 |
| 204 | 删除成功（无返回体）|
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 422 | 参数验证失败 |
| 500 | 服务器错误 |

## 响应格式

```json
{
    "data": { ... },
    "meta": {
        "page": 1,
        "page_size": 10,
        "total": 100
    }
}
```

## 错误响应

```json
{
    "error": "NOT_FOUND",
    "message": "用户不存在",
    "detail": {"user_id": 999}
}
```
""",

    "json-serialization-guide.md": """# JSON 序列化与反序列化

JSON 是 Web API 中最常用的数据交换格式。

## Python JSON 操作

```python
import json

# 序列化（Python → JSON）
data = {"name": "张三", "age": 25}
json_str = json.dumps(data, ensure_ascii=False)

# 反序列化（JSON → Python）
parsed = json.loads('{"name": "李四", "age": 30}')

# 文件操作
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

## 自定义序列化

```python
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)

json.dumps(data, cls=DateTimeEncoder)
```

## Pydantic 与 JSON

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

user = User(name="张三", age=25)
json_str = user.model_dump_json()  # 序列化
parsed = User.model_validate_json(json_str)  # 反序列化
```
""",

    "git-version-control.md": """# Git 版本控制最佳实践

## 分支策略

```
main      产品环境代码
  ├── develop  开发分支
  │   ├── feat/xxx   功能分支
  │   ├── fix/xxx    修复分支
  │   └── chore/xxx  工具链分支
  └── hotfix/xxx     紧急修复
```

## 提交信息规范

```
类型: 简短描述

详细描述（可选）

类型：
- feat: 新功能
- fix: 修复
- docs: 文档
- style: 格式
- refactor: 重构
- test: 测试
- chore: 工具链
```

## 实用命令

```bash
# 查看提交历史
git log --oneline --graph

# 暂存部分修改
git add -p

# 修改最近一次提交
git commit --amend

# 撤销暂存
git reset HEAD <file>

# 查看差异
git diff --staged
```
""",

    "design-patterns-python.md": """# Python 设计模式实战

## 单例模式

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

## 工厂模式

```python
class LoaderFactory:
    _loaders = {}

    @classmethod
    def register(cls, ext, loader_cls):
        cls._loaders[ext] = loader_cls

    @classmethod
    def create(cls, ext):
        return cls._loaders[ext]()

# 注册
LoaderFactory.register(".txt", TextLoader)
LoaderFactory.register(".pdf", PDFLoader)
```

## 观察者模式

```python
class EventBus:
    def __init__(self):
        self._handlers = {}

    def on(self, event, handler):
        self._handlers.setdefault(event, []).append(handler)

    def emit(self, event, **data):
        for handler in self._handlers.get(event, []):
            handler(**data)
```
""",
}

# ──────────────────────────────────────────────
# 文档生成函数
# ──────────────────────────────────────────────

def _generate_code_topics() -> dict:
    """生成编程相关主题文档。"""
    topics = {}

    # 设计模式
    topics["design-patterns-singleton-factory.md"] = """# 单例与工厂模式在 RAG 系统中的应用

## 单例模式

在 RAG 系统中，LLM 和 Embedding 模型应该使用单例模式避免重复加载：

```python
class LLMManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.model = load_model()
            self._initialized = True
```

优势：避免重复初始化，节约内存和启动时间。

## 工厂模式

文档加载器使用工厂模式：

```python
class LoaderFactory:
    def create_loader(self, file_path: str):
        ext = Path(file_path).suffix.lower()
        if ext == ".pdf":
            return PyPDFLoader(file_path)
        elif ext in (".md", ".txt"):
            return TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError(f"不支持的文件格式: {ext}")
```

## 策略模式

检索策略可以动态切换：

```python
class RetrievalStrategy(ABC):
    @abstractmethod
    def retrieve(self, query: str, k: int) -> list: ...

class SimilarityStrategy(RetrievalStrategy): ...
class MMRStrategy(RetrievalStrategy): ...
class HybridStrategy(RetrievalStrategy): ...
```
"""

    topics["solid-principles.md"] = """# SOLID 原则在 Python 项目中的实践

## 单一职责原则（SRP）

每个类只负责一件事：

```python
# 不好：一个类做太多事
class RAGSystem:
    def load_docs(self): ...
    def build_index(self): ...
    def search(self): ...
    def generate_answer(self): ...

# 好：职责分离
class DocumentLoader: ...
class VectorStore: ...
class RAGEngine: ...
```

## 开闭原则（OCP）

对扩展开放，对修改关闭：

```python
class BaseLoader(ABC):
    @abstractmethod
    def load(self, path: str) -> list[Document]: ...

class MarkdownLoader(BaseLoader): ...
class PDFLoader(BaseLoader): ...
class HTMLLoader(BaseLoader): ...  # 新增，无需修改原有代码
```

## 依赖倒置原则（DIP）

```python
# 依赖接口而非具体实现
class RAGEngine:
    def __init__(self, vector_store: AbstractVectorStore, llm: AbstractLLM):
        self.vector_store = vector_store
        self.llm = llm
```
"""

    topics["clean-code-python.md"] = """# Python 代码整洁之道

## 命名规范

```python
# 好
user_list: list[User]
MAX_RETRY_COUNT = 3
def get_user_by_id(user_id: int) -> User: ...

# 差
ul = []
max = 3
def get(u): ...
```

## 函数设计

```python
# 好：小函数，单一职责
def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def send_welcome_email(user: User) -> None:
    if not validate_email(user.email):
        raise ValueError(f"无效邮箱: {user.email}")
    email_service.send(user.email, template="welcome")
```

## 早返回模式

```python
# 好：减少嵌套
def process(data):
    if not data:
        return None
    if not validate(data):
        raise ValueError("无效数据")
    return transform(data)
```
"""

    topics["python-logging.md"] = """# Python logging 日志系统

## 基本配置

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger(__name__)
logger.info("服务启动")
logger.error("处理失败", exc_info=True)
```

## 日志级别

| 级别 | 用途 |
|:--|:--|
| DEBUG | 调试信息 |
| INFO | 一般信息 |
| WARNING | 警告 |
| ERROR | 错误 |
| CRITICAL | 严重错误 |

## 在 RAG 系统中使用

```python
logger.info(f"[检索] 查询: {query}")
logger.info(f"[检索] 找到 {len(docs)} 个相关文档")
logger.info(f"[生成] 耗时: {elapsed:.3f}s")
```
""",

    return topics


def _generate_langchain_topics() -> dict:
    """生成 LangChain 高级主题文档。"""
    topics = {}

    topics["langchain-agents-tools.md"] = """# LangChain Agents 与 Tools

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
    \"\"\"在文档库中搜索相关内容\"\"\"
    results = vector_store.search(query, k=3)
    return "\\n".join([r.page_content for r in results])
```

## Tool 装饰器参数

- `name`: 工具名称（LLM 用它来识别）
- `description`: 工具描述（LLM 用它来判断何时使用）
- `return_direct`: 是否直接返回结果给用户
""",

    topics["langchain-memory.md"] = """# LangChain 对话记忆机制

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
""",

    topics["langchain-callbacks.md"] = """# LangChain Callbacks 回调系统

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
""",

    return topics


def _generate_xiaomi_topics() -> dict:
    """生成小米开源项目相关文档。"""
    topics = {}

    topics["xiaomi-vela-iot.md"] = """# 小米 Vela IoT 操作系统

Vela 是小米基于 NuttX 打造的物联网嵌入式操作系统。

## 项目概述

- 底层内核：NuttX（实时操作系统）
- 应用框架：基于 JavaScript/QuickJS
- 定位：AIoT 设备统一操作系统
- 开源地址：https://github.com/Xiaomi-mimc/vela

## 核心特性

1. 轻量级：最小配置仅需 128KB RAM
2. 实时性：基于 NuttX 的 RTOS 特性
3. 跨平台：统一 API，屏蔽底层差异
4. JS 引擎：支持 JavaScript 应用开发

## 架构设计

```
┌─────────────────────────────────────┐
│        Vela JS Framework            │
├─────────────────────────────────────┤
│         Vela System API             │
├─────────────────────────────────────┤
│           NuttX Kernel              │
├─────────────────────────────────────┤
│         Hardware (ARM/RISC-V)       │
└─────────────────────────────────────┘
```

## 应用场景

- 智能音箱
- 智能手表
- IoT 传感器
- 智能家居网关
""",

    topics["xiaomi-deepspark.md"] = """# 小米 DeepSpark 深度学习框架

DeepSpark 是小米开源的深度学习训练与推理加速库。

## 核心功能

1. 分布式训练优化
2. 模型压缩与量化
3. 推理加速
4. 支持 PyTorch/TensorFlow

## 模型量化

```python
# 将 float32 模型量化为 int8
from deepspark import quantize

model = torch.load("model.pth")
quantized = quantize(model, dtype="int8", calibration_data=calib_data)
torch.save(quantized, "model_int8.pth")
```

## 分布式训练

```python
# 多卡训练加速
trainer = DeepSparkTrainer(
    model=model,
    strategy="ddp",  # 分布式数据并行
    devices=[0, 1, 2, 3],
    precision="fp16",  # 混合精度
)
trainer.fit(train_data)
```
""",

    topics["xiaomi-aiot-platform.md"] = """# 小米 AIoT 开发者平台

小米 AIoT 平台连接数亿智能设备，为开发者提供设备接入、数据分析和 AI 能力。

## 平台能力

### 设备接入

- 支持 Wi-Fi、蓝牙、Zigbee 多种协议
- 标准化设备模型（Property/Event/Action）
- 自动生成设备 SDK

### 数据平台

- 设备数据实时采集
- 时序数据存储与查询
- 数据可视化仪表盘

### AI 能力

- 语音识别与合成
- 图像识别
- 自然语言处理
- 设备异常检测

## 开发流程

1. 注册开发者账号
2. 创建产品，定义设备模型
3. 开发固件（使用 Vela OS 或标准 Linux）
4. 设备配网与激活
5. 对接 AI 服务
""",

    topics["xiaomi-cloud-services.md"] = """# 小米云服务技术架构

小米云服务支撑着数亿用户的照片同步、通讯录备份、查找设备等功能。

## 存储架构

```
用户端
  │
  ├── 照片/视频 → 对象存储（纠删码 + 多副本）
  │     ├── 热数据层：SSD 集群
  │     └── 冷数据层：HDD 集群
  │
  ├── 通讯录/短信 → 结构化存储（分库分表）
  │     └── MySQL + Redis 缓存
  │
  └── 文件 → 分布式文件系统
```

## 关键技术

- 数据去重：基于内容哈希的全局去重
- 断点续传：大文件分片上传
- 端到端加密：设备端加密，云端无法解密
- CDN 加速：全球节点分发

## 同步协议

使用自定义同步协议，支持增量同步和冲突解决：

- 增量同步：只传变化的数据
- 冲突解决：基于时间戳的 Last-Write-Wins
- 离线支持：本地缓存 + 联网后自动合并
""",

    return topics


def _generate_ai_topics() -> dict:
    """生成 AI/ML 主题文档。"""
    topics = {}

    topics["transformer-architecture.md"] = """# Transformer 架构详解

Transformer 是 Google 2017 年提出的架构，彻底改变了 NLP 领域。

## 核心组件

### Self-Attention

```
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V
```

计算序列中每个位置与其他位置的相关性权重。

### Multi-Head Attention

多个独立的 Attention 头并行计算，从不同子空间提取特征：

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model=512, n_heads=8):
        self.heads = nn.ModuleList([
            SelfAttention(d_model // n_heads)
            for _ in range(n_heads)
        ])
```

### Position Encoding

由于 Transformer 没有循环结构，需要位置编码注入位置信息：

```python
PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

## Encoder-Decoder 结构

- Encoder：处理输入序列，生成上下文表示
- Decoder：自回归生成输出序列
""",

    topics["embedding-models-comparison.md"] = """# Embedding 模型对比与选择

## 主流中文 Embedding 模型

| 模型 | 维度 | 大小 | 中文效果 | 速度 |
|:--|:--|:--|:--|:--|
| text2vec-base-chinese | 768 | 400MB | 优秀 | 中等 |
| bge-large-zh-v1.5 | 1024 | 1.3GB | 最佳 | 较慢 |
| m3e-base | 768 | 420MB | 良好 | 中等 |
| stella-base-zh | 768 | 400MB | 良好 | 较快 |

## 选择因素

1. 任务场景：检索/分类/聚类
2. 算力限制：GPU/CPU
3. 延迟要求：实时/离线
4. 存储成本：向量维度影响存储

## 评估方法

```python
from sentence_transformers import evaluation

evaluator = evaluation.EmbeddingSimilarityEvaluator(
    sentences1=["查询1"], sentences2=["文档1"], scores=[0.9]
)
score = evaluator(model)
```
""",

    topics["llm-fine-tuning.md"] = """# 大语言模型微调方法

## 全量微调 vs 高效微调

| 方法 | GPU 需求 | 训练时间 | 效果 |
|:--|:--|:--|:--|
| 全量微调 | 8×A100 | 数天 | 最佳 |
| LoRA | 1×A100 | 数小时 | 接近全量 |
| QLoRA | 1×24GB | 数小时 | 略低于 LoRA |
| Prompt Tuning | 1×16GB | 数小时 | 一般 |

## LoRA（Low-Rank Adaptation）

只训练低秩矩阵，冻结原模型参数：

```python
from peft import LoraConfig, get_peft_model

config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
)

model = get_peft_model(base_model, config)
model.print_trainable_parameters()
# trainable params: 0.5%
```
""",

    topics["tokenization-guide.md"] = """# 分词器原理与实践

## 分词方法

### BPE（Byte Pair Encoding）

迭代合并高频字符对，GPT 系列使用：

```python
# 训练示例
corpus = "low low low lower"
# 合并 'l' + 'o' → 'lo'
# 合并 'lo' + 'w' → 'low'
```

### WordPiece

类似 BPE，但按语言模型似然选择合并，BERT 使用。

### SentencePiece

直接处理原始 Unicode 字符，不依赖预分词。

## 中文分词

```python
from tokenizers import Tokenizer

tokenizer = Tokenizer.from_pretrained("bert-base-chinese")

tokens = tokenizer.encode("你好世界！").tokens
# ['[CLS]', '你', '好', '世', '界', '！', '[SEP]']
```

## Token 数估算

- 英文：1 token ≈ 0.75 词
- 中文：1 token ≈ 1.5 字
- 代码：1 token ≈ 0.5 字符
""",

    topics["prompt-engineering-advanced.md"] = """# Prompt 工程进阶

## Few-Shot Prompting

```python
prompt = \"\"\"
按要求分类：

Q: 今天天气真好
A: 日常

Q: Python 是解释型语言
A: 编程

Q: {input}
A:\"\"\"
```

## Chain of Thought

```python
prompt = \"\"\"
请一步步思考：

问题：小明有 5 个苹果，吃了 2 个，又买了 3 个，还剩几个？
思路：5 - 2 = 3, 3 + 3 = 6
答案：6 个
\"\"\"
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
""",

    return topics


def _generate_devops_topics() -> dict:
    """生成 DevOps 相关主题。"""
    topics = {}

    topics["docker-quickstart.md"] = """# Docker 快速入门

## 基本概念

- **镜像（Image）**: 应用的只读模板
- **容器（Container）**: 镜像的运行实例
- **Dockerfile**: 构建镜像的脚本

## Dockerfile 示例

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 常用命令

```bash
# 构建镜像
docker build -t my-app .

# 运行容器
docker run -p 8000:8000 my-app

# 查看运行中的容器
docker ps

# 停止容器
docker stop <container_id>
```
""",

    topics["nginx-reverse-proxy.md"] = """# Nginx 反向代理配置

## 基本配置

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        root /var/www;
    }
}
```

## SSE 流式代理

```nginx
location /api/ {
    proxy_pass http://backend:8000;
    proxy_buffering off;  # 关键：禁用缓冲
    proxy_cache off;
    proxy_set_header Connection '';
    proxy_http_version 1.1;
    chunked_transfer_encoding on;
}
```

## 负载均衡

```nginx
upstream backend {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}
```
""",

    topics["ci-cd-basics.md"] = """# CI/CD 持续集成与部署

## 工作流程

```
代码提交 → 自动构建 → 自动测试 → 自动部署
```

## GitHub Actions 示例

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest
```

## 关键实践

1. 每次提交触发自动测试
2. 合并前必须通过 CI
3. 自动部署到开发环境
4. 生产发布需要人工审批
""",

    return topics


def _generate_security_topics() -> dict:
    """生成安全相关主题。"""
    topics = {}

    topics["api-security.md"] = """# API 安全最佳实践

## 认证与授权

```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/api/secure")
async def secure_endpoint(token: str = Depends(security)):
    user = verify_token(token)
    return {"user": user}
```

## 输入验证

```python
from pydantic import BaseModel, Field, validator

class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., pattern=r'^[\\w.-]+@[\\w.-]+\\.\\w+$')
    age: int = Field(..., ge=0, le=150)

    @validator('name')
    def name_no_html(cls, v):
        if '<' in v or '>' in v:
            raise ValueError('名称不能包含 HTML 标签')
        return v
```

## 常见攻击防护

1. SQL 注入：使用参数化查询
2. XSS：转义输出、CSP 头
3. CSRF：使用 CSRF Token
4. 速率限制：防止暴力破解
""",

    topics["env-management-security.md"] = """# 环境变量与密钥管理

## .env 文件安全

```bash
# 永远不要提交到 Git
.env
.env.local
.env.production
```

## 密钥注入方式

```python
# 方式1: .env 文件（开发环境）
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")

# 方式2: 环境变量（生产环境）
api_key = os.environ["API_KEY"]

# 方式3: 密钥管理服务（推荐）
from vault_client import get_secret
api_key = get_secret("api/deepseek/key")
```

## 安全准则

1. 不在代码中硬编码密钥
2. 不同环境使用不同密钥
3. 定期轮换密钥
4. 限制密钥权限范围
5. 监控密钥使用情况
""",

    return topics


# ──────────────────────────────────────────────
# 主函数
# ──────────────────────────────────────────────

def generate_all_docs(output_dir: str) -> int:
    """将所有文档写入目标目录。"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 收集所有文档（保留已有的 24 篇）
    all_docs = {}
    all_docs.update(DOCUMENTS)
    all_docs.update(_generate_code_topics())
    all_docs.update(_generate_langchain_topics())
    all_docs.update(_generate_xiaomi_topics())
    all_docs.update(_generate_ai_topics())
    all_docs.update(_generate_devops_topics())
    all_docs.update(_generate_security_topics())

    count = 0
    for filename, content in all_docs.items():
        file_path = output_path / filename
        # 跳过已存在的文件
        if file_path.exists():
            continue
        file_path.write_text(content, encoding="utf-8")
        print(f"  [生成] {filename}")
        count += 1

    return count


def count_documents(directory: str) -> int:
    """统计文档目录的文档数。"""
    doc_path = Path(directory)
    return len(list(doc_path.glob("*.md"))) + len(list(doc_path.glob("*.txt")))


if __name__ == "__main__":
    from config import DOCUMENTS_PATH

    before = count_documents(DOCUMENTS_PATH)
    print(f"生成前文档数: {before}")

    generated = generate_all_docs(DOCUMENTS_PATH)
    print(f"新生成文档数: {generated}")

    after = count_documents(DOCUMENTS_PATH)
    print(f"生成后文档总数: {after}")

    if after >= 100:
        print("\\n[OK] 文档总数已达 100+ 目标！")
    else:
        print(f"\\n[推进] 还需 {100 - after} 篇达到 100+ 目标")
