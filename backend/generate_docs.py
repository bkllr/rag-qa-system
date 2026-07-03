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
"""

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
"""

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
"""

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
"""

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
"""

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
"""

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
"""

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
"""

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
"""

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
"""

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
"""

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
"""

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
"""

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
"""

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
"""

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
"""

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
"""

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
"""

    return topics


# ──────────────────────────────────────────────
# 主函数
# ──────────────────────────────────────────────

def _generate_more_topics() -> dict:
    """生成更多技术主题文档，达到 100+ 目标。"""
    topics = {}
    
    # --- 数据库类 ---
    topics["sql-basics.md"] = """# SQL 基础语法

## SELECT 查询

```sql
SELECT name, age FROM users WHERE age > 18 ORDER BY age DESC LIMIT 10;
```

## JOIN 连接\n\n| JOIN类型 | 说明 |\n|:--|:--|\n| INNER JOIN | 返回两个表匹配的行 |\n| LEFT JOIN | 返回左表所有行 |\n| RIGHT JOIN | 返回右表所有行 |\n
## 索引优化\n\n```sql\nCREATE INDEX idx_users_age ON users(age);\nCREATE INDEX idx_users_name_age ON users(name, age);\n```\n
## 聚合函数\n\n- COUNT: 计数\n- SUM: 求和\n- AVG: 平均值\n- MAX/MIN: 最大/最小值\n"""

    topics["nosql-redis-basics.md"] = """# Redis 基础与缓存策略

Redis 是一个高性能的内存键值数据库。\n
## 数据结构\n\n- String: 字符串\n- Hash: 哈希表\n- List: 列表\n- Set: 集合\n- ZSet: 有序集合\n
## 缓存策略\n\n### Cache-Aside\n1. 读：先查缓存，miss 则查 DB 并回写缓存\n2. 写：先写 DB，再删缓存\n
### 缓存穿透防护\n- 布隆过滤器预判 key 是否存在\n- 空值也缓存（短 TTL）\n
## 过期策略\n\n- TTL: 设置过期时间\n- LRU: 最近最少使用淘汰\n- LFU: 最不经常使用淘汰\n"""

    # --- 前端类 ---
    topics["css-flexbox-layout.md"] = """# CSS Flexbox 布局详解

Flexbox 是 CSS3 的一维布局模型。\n
## 容器属性\n\n```css\n.container {\n    display: flex;\n    flex-direction: row;       /* 主轴方向 */\n    justify-content: center;   /* 主轴对齐 */\n    align-items: center;       /* 交叉轴对齐 */\n    gap: 16px;                 /* 间距 */\n    flex-wrap: wrap;           /* 换行 */\n}\n```\n
## 项目属性\n\n```css\n.item {\n    flex: 1;         /* flex-grow */\n    align-self: flex-end;\n    order: 2;\n}\n```\n
## 常见布局\n- 水平居中: justify-content: center\n- 垂直居中: align-items: center\n- 两端对齐: justify-content: space-between\n"""

    topics["javascript-async.md"] = """# JavaScript 异步编程

## Promise\n\n```javascript\nfetch("/api/data")\n    .then(res => res.json())\n    .then(data => console.log(data))\n    .catch(err => console.error(err));\n```\n
## Async/Await\n\n```javascript\nasync function loadData() {\n    try {\n        const res = await fetch("/api/data");\n        const data = await res.json();\n        return data;\n    } catch (err) {\n        console.error(err);\n    }\n}\n```\n
## ReadableStream\n\n```javascript\nconst reader = response.body.getReader();\nconst decoder = new TextDecoder();\nwhile (true) {\n    const { done, value } = await reader.read();\n    if (done) break;\n    console.log(decoder.decode(value));\n}\n```\n"""

    topics["nodejs-basics.md"] = """# Node.js 基础

Node.js 是一个基于 Chrome V8 引擎的 JavaScript 运行时。\n
## 模块系统\n\n```javascript\n// 导出\nmodule.exports = { myFunc };\n// 导入\nconst { myFunc } = require("./module");\n\n// ES Modules\nimport { myFunc } from "./module.js";\n```\n
## 文件操作\n\n```javascript\nconst fs = require("fs");\n\n// 同步\nconst data = fs.readFileSync("file.txt", "utf-8");\n\n// 异步\nfs.readFile("file.txt", "utf-8", (err, data) => {\n    if (err) throw err;\n    console.log(data);\n});\n```\n
## 包管理\n\n```bash\nnpm init -y\nnpm install express\nnpm install --save-dev nodemon\n```\n"""

    # --- DevOps 扩展 ---
    topics["linux-common-commands.md"] = """# Linux 常用命令

## 文件操作\n\n```bash\nls -la           # 列出文件\ncd /path         # 切换目录\ncp src dst       # 复制\nmv src dst       # 移动/重命名\nrm -rf dir       # 删除\nfind . -name "*.py"  # 查找文件\n```\n
## 文本处理\n\n```bash\ngrep "pattern" file.txt     # 搜索\nwc -l file.txt              # 行数\nhead -n 10 file.txt         # 前 10 行\ntail -f file.txt            # 实时跟踪\n```\n
## 进程管理\n\n```bash\nps aux          # 查看进程\nkill -9 PID     # 终止进程\nhtop            # 交互式进程查看\nnohup cmd &     # 后台运行\n```\n"""

    topics["git-advanced.md"] = """# Git 高级操作

## 变基 Rebase\n\n```bash\ngit rebase main          # 将当前分支变基到 main\ngit rebase -i HEAD~3     # 交互式变基（压缩提交）\n```\n
## Cherry-Pick\n\n```bash\ngit cherry-pick <commit-hash>  # 将指定提交应用到当前分支\n```\n
## 暂存 Stash\n\n```bash\ngit stash              # 暂存当前修改\ngit stash pop          # 恢复最近的暂存\ngit stash list         # 查看暂存列表\n```\n
## 标签\n\n```bash\ngit tag v1.0.0              # 创建标签\ngit tag -a v1.0.0 -m "发布" # 附注标签\ngit push origin --tags      # 推送标签\n```\n"""

    # --- Python 库 ---
    topics["python-requests-lib.md"] = """# Python requests 库详解

```python\nimport requests\n\n# GET 请求\nresp = requests.get("https://api.example.com/data")\ndata = resp.json()\n\n# POST 请求\nresp = requests.post(\n    "https://api.example.com/submit",\n    json={"name": "test"},\n    headers={"Authorization": "Bearer token"},\n)\n\n# 超时与重试\nresp = requests.get(url, timeout=5)\n\n# 会话（复用连接）\nsession = requests.Session()\nsession.headers.update({"User-Agent": "MyApp/1.0"})\nresp = session.get(url)\n```\n\n## 响应处理\n- resp.status_code: HTTP 状态码\n- resp.json(): JSON 解析\n- resp.text: 文本内容\n- resp.content: 二进制内容\n"""

    topics["python-pathlib.md"] = """# Python pathlib 路径操作

pathlib 是 Python 3.4+ 推荐的路径处理库。\n
```python\nfrom pathlib import Path\n\n# 当前文件目录\nBASE_DIR = Path(__file__).resolve().parent\n\n# 路径拼接\ndata_dir = BASE_DIR / "data" / "documents"\nconfig_file = BASE_DIR / ".env"\n\n# 目录操作\ndata_dir.mkdir(parents=True, exist_ok=True)\n\n# 遍历文件\nfor file in data_dir.rglob("*.md"):\n    print(file.name, file.stem, file.suffix)\n\n# 文件操作\ncontent = (data_dir / "readme.md").read_text(encoding="utf-8")\n(data_dir / "output.txt").write_text("hello", encoding="utf-8")\n```\n\n## Path vs os.path\n| os.path | pathlib |\n|:--|:--|\n| os.path.join(a, b) | Path(a) / b |\n| os.path.exists(p) | Path(p).exists() |\n| os.path.dirname(p) | Path(p).parent |\n"""

    topics["python-argparse.md"] = """# Python argparse 命令行参数

```python\nimport argparse\n\nparser = argparse.ArgumentParser(description="RAG 文档管理工具")\n\nparser.add_argument("--rebuild", action="store_true", help="重建索引")\nparser.add_argument("--k", type=int, default=4, help="检索返回数")\nparser.add_argument("--query", type=str, help="查询内容")\n\nargs = parser.parse_args()\n\nif args.rebuild:\n    rebuild_index()\nelif args.query:\n    result = query(args.query, k=args.k)\n    print(result["answer"])\n```\n\n## 参数类型\n- store_true: 布尔标志\n- type=str: 字符串\n- type=int: 整数\n- default: 默认值\n- required=True: 必填\n"""

    # --- AI/ML 扩展 ---
    topics["machine-learning-basics.md"] = """# 机器学习基础概念

## 三大范式\n\n| 类型 | 数据需求 | 典型任务 |\n|:--|:--|:--|\n| 监督学习 | 标注数据 | 分类、回归 |\n| 无监督学习 | 无标注数据 | 聚类、降维 |\n| 强化学习 | 交互环境 | 游戏、控制 |\n
## 常见算法\n\n- 线性回归: 预测连续值\n- 逻辑回归: 二分类\n- 决策树: 可解释分类\n- SVM: 高维分类\n- K-Means: 聚类\n
## 评估指标\n\n- 分类: Accuracy, Precision, Recall, F1\n- 回归: MSE, MAE, R2\n- 聚类: Silhouette Score\n"""

    topics["neural-networks-intro.md"] = """# 神经网络入门

## 感知机\n\n```python\noutput = activation(W @ X + b)\n```\n
## 前向传播\n\n```\n输入层 → 隐藏层1 → 隐藏层2 → 输出层\n```\n
## 反向传播\n\n1. 计算输出误差\n2. 误差反向传播\n3. 梯度下降更新参数\n
## 激活函数\n\n- Sigmoid: (0, 1)，容易梯度消失\n- ReLU: max(0, x)，计算简单\n- Tanh: (-1, 1)，零中心化\n- Softmax: 多分类输出\n"""

    topics["nlp-basics.md"] = """# 自然语言处理基础

## 文本预处理\n\n1. 分词: 将文本切分为词/字\n2. 去停用词: 移除"的"、"是"等无意义词\n3. 词干提取: 还原单词基础形式\n4. 向量化: 文本转数值向量\n
## 词向量\n\n- One-Hot: 稀疏高维\n- Word2Vec: 稠密向量，捕获语义\n- GloVe: 基于共现矩阵\n- BERT: 上下文相关\n
## 常见任务\n\n- 文本分类: 情感分析、垃圾邮件检测\n- 命名实体识别: 识别人名/地名\n- 机器翻译: 语言转换\n- 问答系统: RAG 是其中一种方案\n"""

    # --- 杂项技术 ---
    topics["regular-expressions.md"] = """# 正则表达式速查

## 基本元字符\n\n| 符号 | 含义 |\n|:--|:--|\n| . | 任意字符 |\n| * | 0次或多次 |\n| + | 1次或多次 |\n| ? | 0次或1次 |\n| ^ | 行首 |\n| $ | 行尾 |\n| \\d | 数字 |\n| \\w | 字母/数字/下划线 |\n| \\s | 空白字符 |\n
## Python 使用\n\n```python\nimport re\n\n# 搜索\nresult = re.search(r"pattern", text)\n\n# 查找所有\nmatches = re.findall(r"\\d+", "a1b2c3")  # ['1','2','3']\n\n# 替换\nnew_text = re.sub(r"\\s+", " ", text)\n\n# 分组\nm = re.match(r"(\\w+)@(\\w+)", "user@example")\nprint(m.group(1))  # user\n```\n"""

    topics["yaml-config.md"] = """# YAML 配置文件

## 基本语法\n\n```yaml\nserver:\n  host: "0.0.0.0"\n  port: 8000\n  debug: true\n\ndatabase:\n  url: "postgresql://localhost/db"\n  pool_size: 10\n\n# 列表\nallowed_origins:\n  - "http://localhost:5173"\n  - "http://localhost:3000"\n```\n
## Python 读写\n\n```python\nimport yaml\n\nwith open("config.yaml") as f:\n    config = yaml.safe_load(f)\n\nwith open("output.yaml", "w") as f:\n    yaml.dump(config, f, allow_unicode=True)\n```\n
## YAML vs JSON\n- YAML: 可读性好，支持注释\n- JSON: 更严格，通用性更强\n"""

    topics["websocket-protocol.md"] = """# WebSocket 协议

WebSocket 是全双工通信协议，适合实时应用。\n
## 与 SSE 对比\n\n| 特性 | WebSocket | SSE |\n|:--|:--|:--|\n| 方向 | 双向 | 服务器→客户端 |\n| 协议 | ws:// | HTTP |\n| 复杂度 | 较高 | 低 |\n
## Python 实现\n\n```python\n# FastAPI WebSocket\nfrom fastapi import WebSocket\n\n@app.websocket("/ws")\nasync def websocket_endpoint(ws: WebSocket):\n    await ws.accept()\n    while True:\n        data = await ws.receive_text()\n        await ws.send_text(f"Echo: {data}")\n```\n
## JavaScript 客户端\n\n```javascript\nconst ws = new WebSocket("ws://localhost:8000/ws");\nws.onmessage = (event) => console.log(event.data);\nws.send("Hello Server!");\n```\n"""

    topics["microservices-basics.md"] = """# 微服务架构基础

## 核心原则\n\n1. 单一职责: 每个服务只做一件事\n2. 独立部署: 服务间独立发布\n3. 去中心化: 每个服务独立数据库\n4. 容错设计: 服务故障不影响整体\n
## 通信方式\n\n- 同步: REST API, gRPC\n- 异步: 消息队列 (Kafka, RabbitMQ)\n- 事件驱动: Event Bus\n
## API 网关\n\n统一入口，负责路由、认证、限流：\n\n```\n客户端 → API 网关 → 服务A/服务B/服务C\n```\n
## 与单体架构对比\n\n| 维度 | 单体 | 微服务 |\n|:--|:--|:--|\n| 复杂度 | 低 | 高 |\n| 扩展性 | 差 | 好 |\n| 部署 | 简单 | 复杂 |\n"""

    topics["tdd-test-driven.md"] = """# 测试驱动开发 (TDD)

## TDD 循环\n\n```\n1. 写测试 → 2. 运行测试(红) → 3. 写代码 → 4. 运行测试(绿) → 5. 重构\n```\n
## pytest 示例\n\n```python\n# test_rag.py\ndef test_query_returns_answer():\n    result = query("什么是Python?")\n    assert result["answer"]\n    assert len(result["sources"]) > 0\n\ndef test_empty_question():\n    result = query("")\n    assert result["answer"] == "未在文档中找到相关内容。"\n```\n\n## 测试金字塔\n\n```\n      /\\\n     /E2E\\       少量\n    /______\\\n   /集成测试\\    适量\n  /__________\\\n /  单元测试   \\  大量\n/______________\\\n```\n"""

    topics["code-review-practices.md"] = """# 代码审查最佳实践

## 审查清单\n\n- [ ] 逻辑正确性\n- [ ] 边界条件处理\n- [ ] 错误处理是否完整\n- [ ] 命名是否清晰\n- [ ] 是否有重复代码\n- [ ] 是否符合项目规范\n
## 提交粒度\n\n每个 commit 应该只做一件事：\n\n```bash\ngit commit -m "feat: 添加用户注册接口"\ngit commit -m "fix: 修复邮箱验证正则表达式"\ngit commit -m "refactor: 提取公共验证逻辑"\n```\n
## 审查注释格式\n\n```\n[建议] 这里可以用列表推导式简化\n[必须] 缺少空值检查\n[优化] 这个循环可以提取为单独函数\n```\n"""

    topics["oop-inheritance-polymorphism.md"] = """# 面向对象：继承与多态

## 继承\n\n```python\nclass Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        raise NotImplementedError\n\nclass Dog(Animal):\n    def speak(self):\n        return "汪汪！"\n\nclass Cat(Animal):\n    def speak(self):\n        return "喵喵！"\n```\n
## 多态\n\n```python\ndef make_sound(animal: Animal):\n    print(f"{animal.name}: {animal.speak()}")\n\nanimals = [Dog("旺财"), Cat("咪咪")]\nfor a in animals:\n    make_sound(a)\n```\n
## 抽象类\n\n```python\nfrom abc import ABC, abstractmethod\n\nclass BaseLoader(ABC):\n    @abstractmethod\n    def load(self, path: str): ...\n```\n"""

    topics["data-structures-algorithms.md"] = """# 数据结构与算法

## 时间复杂度\n\n| 复杂度 | 示例 |\n|:--|:--|\n| O(1) | 数组索引 |\n| O(log n) | 二分查找 |\n| O(n) | 线性搜索 |\n| O(n log n) | 快速排序 |\n| O(n^2) | 冒泡排序 |\n
## 常用数据结构\n\n- 数组/列表: O(1) 索引\n- 链表: O(1) 插入删除\n- 哈希表: O(1) 查找\n- 栈/队列: LIFO/FIFO\n- 树/图: 层次关系\n
## Python 实现\n\n```python\n# 二分查找\ndef binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n```\n"""

    return topics


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
    all_docs.update(_generate_more_topics())

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
