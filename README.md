# RAG QA System — AI 技术文档智能问答系统

基于 **RAG（检索增强生成）** 架构的 AI 技术文档问答系统，支持流式对话、来源引用、Markdown 渲染。后端采用 FastAPI + LangChain + Chroma，前端采用 Vue 3 + Vite，LLM 使用 DeepSeek API。

> 📌 **Xiaomi Engineer Training Camp 简历项目** — 展示全栈交付能力与 AI Native 开发流程

---

## 📊 项目概览

| 维度 | 数据 |
|:--|:--|
| 知识库规模 | 102 篇技术文档，218 个语义切片 |
| 开发过程 | 40+ 次迭代提交，模块化演进 |
| API 接口 | 5 个端点（对话 / 流式 / 管理） |
| 前端组件 | 4 个核心组件（对话 / 输入 / 来源 / 渲染） |

---

## 🏗️ 技术栈

### 后端
- **框架**: FastAPI + Uvicorn（异步高性能 Web 框架）
- **LLM**: DeepSeek API (`deepseek-chat` 模型，OpenAI 兼容接口）
- **RAG 引擎**: LangChain LCEL（LangChain Expression Language）流水线
- **向量数据库**: Chroma（持久化模式，L2 距离）
- **Embedding**: `shibing624/text2vec-base-chinese`（本地 768 维中文向量）
- **文档处理**: RecursiveCharacterTextSplitter（chunk_size=500, overlap=50）

### 前端
- **框架**: Vue 3 Composition API (`<script setup>`)
- **构建工具**: Vite 5（代理 /api 到后端）
- **Markdown 渲染**: marked + highlight.js（代码高亮）
- **流式通信**: SSE（Server-Sent Events）+ fetch ReadableStream

### 工具链
- **依赖管理**: pip（Python）/ npm（Node.js）
- **版本控制**: Git（模块化提交）
- **测试**: pytest + 自定义问答对评估脚本

---

## 📁 目录结构

```
rag-qa-system/
├── backend/
│   ├── config.py              # 配置加载（LLM、Embedding 工厂函数）
│   ├── document_loader.py     # 文档加载与切片（支持 .md/.txt/.pdf）
│   ├── vector_store.py        # Chroma 向量数据库管理
│   ├── rag_engine.py          # RAG 核心引擎（LCEL 流水线 + 流式）
│   ├── main.py                # FastAPI 主入口（4 个 API 端点）
│   ├── test_rag.py            # 检索准确率测试脚本（20 个测试用例）
│   ├── generate_docs.py       # 文档批量生成脚本
│   ├── requirements.txt       # Python 依赖
│   ├── .env.example           # 环境变量模板
│   ├── data/
│   │   └── documents/         # 102 篇技术文档（.md）
│   ├── chroma_db/             # Chroma 向量数据库文件（自动生成）
│   └── ai-logs/               # AI 对话截图存放目录
├── frontend/
│   ├── index.html             # 入口 HTML
│   ├── package.json           # 前端依赖
│   ├── vite.config.js         # Vite 配置（含 API 代理）
│   └── src/
│       ├── main.js            # Vue 应用入口
│       ├── App.vue            # 主页面（对话状态管理）
│       ├── api/
│       │   └── chat.js        # SSE 流式请求封装
│       └── components/
│           ├── ChatWindow.vue # 聊天消息列表（Markdown 渲染）
│           ├── ChatInput.vue  # 输入框组件
│           └── SourceCard.vue # 来源引用卡片
├── README.md
└── .gitignore
```

---

## 🚀 快速开始

### 1. 环境准备

- Python 3.10+
- Node.js 18+
- DeepSeek API Key（[注册地址](https://platform.deepseek.com/)）

### 2. 后端配置

```bash
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt

# 配置 API Key
cp .env.example .env
# 编辑 .env，填入你的 DeepSeek API Key
```

> **注意**: 首次运行时，`text2vec-base-chinese` 模型会自动从 HuggingFace 下载（约 500MB），请耐心等待。

### 3. 启动后端

```bash
cd backend
python main.py
# 或: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

启动后自动构建 Chroma 索引。API 文档：http://localhost:8000/docs

### 4. 启动前端

```bash
cd frontend
npm install
npm run dev
```

浏览器打开：http://localhost:5173

### 5. 使用

1. 在输入框中输入技术问题（如"什么是 RAG？"）
2. 按 Enter 发送
3. AI 逐步流式输出回答，回答完毕后显示参考来源
4. 点击来源卡片可展开查看引用片段

---

## 🔌 API 端点

| 方法 | 路径 | 说明 |
|:--|:--|:--|
| `GET` | `/` | 健康检查 |
| `POST` | `/api/chat` | 同步 RAG 查询 |
| `POST` | `/api/chat/stream` | SSE 流式查询 |
| `GET` | `/api/admin/documents` | 索引信息 |
| `POST` | `/api/admin/rebuild` | 重建索引 |

### 流式 SSE 事件格式

```
data: {"type":"token","content":"RAG"}     // 逐个 token
data: {"type":"token","content":"是"}
data: {"type":"sources","sources":[...]}    // 来源引用
data: {"type":"done"}                       // 流结束
```

---

## 🧪 测试

```bash
cd backend
python test_rag.py
```

运行 20 个预定义问答对的准确率测试，输出 PASS/FAIL 统计和整体准确率。

---

## 🤖 AI Native 开发实践

本项目全程使用 AI 辅助开发，从技术选型到代码生成、调试修复均通过对话式交互完成。

### 1. 技术选型

通过 AI 对话快速对比并确定方案：
- **LLM**: DeepSeek API（OpenAI 兼容接口，国内可直接调用）
- **Embedding**: text2vec-base-chinese（本地运行，无 API 依赖）
- **前端**: Vue 3 + Vite（轻量、对 SSE 流式友好）

### 2. 代码生成

项目主体代码由 AI 生成，人工主要负责：
- 业务逻辑的精度调优
- RAG Prompt 的迭代优化
- 实际运行中的 Bug 修复

### 3. RAG 防幻觉策略

在 Prompt 模板中约束 LLM 行为：

```
【回答规则】
1. 只基于参考资料中的信息回答，不要编造、不要猜测、不要使用外部知识。
2. 如果参考资料中没有相关信息，请明确回答："未在文档中找到相关内容"。
```

### 4. 开发过程中遇到的典型问题

| 问题 | 解决方式 |
|:--|:--|
| Python 三引号末尾逗号变元组 | 定位到 `topics["..."] = """...\n""",` 模式，编写修复脚本 |
| Chroma L2 距离 → 相似度转换 | 采用 `1.0 / (1.0 + score)` 公式 |
| Vue 3 响应式代理问题 | `ref` push 后通过索引访问 Proxy 对象 |

---

## 🎯 RAG 流水线原理

```
用户问题
    │
    ▼
┌─────────────────┐
│  向量检索        │  ← Chroma 向量数据库
│  (Chroma.search) │     text2vec-base-chinese 编码
└──────┬──────────┘
       │ Top-K 相关文档片段
       ▼
┌─────────────────┐
│  Prompt 构建     │  ← 拼接 context + 防幻觉约束
│  (RAG Prompt)    │
└──────┬──────────┘
       │ 完整 Prompt
       ▼
┌─────────────────┐
│  LLM 生成        │  ← DeepSeek API
│  (ChatOpenAI)    │     流式 astream()
└──────┬──────────┘
       │ 逐 token 输出
       ▼
┌─────────────────┐
│  SSE 推送        │  ← text/event-stream
│  (FastAPI)       │     JSON 格式事件
└──────┬──────────┘
       │
       ▼
   前端渲染 + 来源引用
```

---

## 📝 技术选型说明

| 选择 | 替代方案 | 原因 |
|:--|:--|:--|
| FastAPI | Flask | 原生异步，SSE 流式输出更自然；自带 Swagger 文档 |
| Chroma | FAISS | 持久化简单，Python 原生集成好 |
| text2vec-base-chinese | OpenAI Embedding | 本地运行免费，中文效果不错 |
| Vue 3 | React | Composition API 对 SSE 响应式绑定简洁 |

---

## 🐛 常见问题

**Q: 启动后端时提示 "LLM_API_KEY 尚未配置"？**

A: 请编辑 `backend/.env` 文件，填入你的 DeepSeek API Key。

**Q: 首次启动很慢？**

A: 首次运行时系统会：
1. 自动下载 `text2vec-base-chinese` 模型（~500MB）
2. 自动对 102 篇文档建立向量索引
后续启动会跳过这些步骤。

**Q: 检索准确率不高？**

A: 可调优方向：
- 调整 `chunk_size`（当前 500）/ `overlap`（当前 50）
- 更换 Embedding 模型
- 调整 `k` 值（检索返回的文档片段数）
- 优化文档质量

**Q: 如何添加新文档？**

A: 将 .md/.txt/.pdf 文件放入 `backend/data/documents/`，然后调用 `POST /api/admin/rebuild` 重建索引。

---

## 📄 License

MIT
