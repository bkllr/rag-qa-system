# RAG QA System — AI 技术文档智能问答系统

基于 **RAG（检索增强生成）** 架构的 AI 技术文档问答系统，支持流式对话、来源引用、Markdown 渲染。后端采用 FastAPI + LangChain + Chroma，前端采用 Vue 3 + Vite，LLM 使用 DeepSeek API。

> 📌 **Xiaomi Engineer Training Camp 简历项目** — 展示全栈交付能力与 AI Native 开发流程

---

## 📊 量化指标

| 指标 | 目标 | 状态 |
|:--|:--|:--|
| 索引文档数 | ≥100 篇 | ✅ 102 篇 |
| Git 提交数 | ≥30 次 | 🚧 22 次 |
| 检索准确率 | ≥80% | 待测试 |
| 响应时间 | <2s（含 LLM） | 待测试 |
| API 端点数 | 4 个 | ✅ 已完成 |
| 前端组件数 | 4 个 | ✅ 已完成 |

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

本项目全程使用 AI 辅助开发，践行 AI Native 开发范式：

### 1. 对话式架构设计

通过多轮 AI 对话完成技术选型：
- **LLM 选型**: DeepSeek API（性价比最优，OpenAI 兼容）
- **Embedding 选型**: text2vec-base-chinese（本地运行，中文效果最佳）
- **前端方案**: Vue 3 + Vite（轻量、响应式、SSE 友好）
- **文档生成策略**: 脚本批量生成（可控、可重复）

### 2. AI 辅助代码生成

| 模块 | 代码行数 | AI 参与度 | 关键亮点 |
|:--|:--|:--|:--|
| `config.py` | 102 | 95% | 单例工厂模式 |
| `document_loader.py` | 112 | 90% | 多格式支持 |
| `vector_store.py` | 225 | 85% | 持久化 + 索引重建 |
| `rag_engine.py` | 255 | 90% | LCEL 流式管道 + 防幻觉 Prompt |
| `main.py` | 222 | 90% | lifespan 自动构建索引 |
| `test_rag.py` | 142 | 95% | 20 个测试用例 |
| `generate_docs.py` | 1622 | 85% | 多主题模板生成 |
| 前端组件 | ~730 | 95% | SSE 流式 + Markdown 渲染 |

**总计**: AI 参与度约 **90%**，人工主要进行精度调优和 Prompt 优化。

### 3. RAG 防幻觉策略

在 Prompt 模板中强制约束 LLM 行为：

```
【回答规则】
1. 只基于参考资料中的信息回答，不要编造、不要猜测、不要使用外部知识。
2. 如果参考资料中没有相关信息，请明确回答："未在文档中找到相关内容"。
```

这是 AI Native 开发中的重要实践：**通过 Prompt Engineering 约束模型行为，而非过度依赖代码逻辑**。

### 4. 开发日志留痕

AI 对话截图保存在 `backend/ai-logs/` 目录，记录关键开发节点的 AI 对话内容。

### 5. AI 辅助调试与修复

在开发过程中遇到的关键 Bug：

| 问题 | AI 修复方案 | 经验教训 |
|:--|:--|:--|
| Python 三引号末尾逗号变元组 | 定位到 `topics["..."] = """...\n""",` 模式，编写精准修复脚本 | Python 字符串赋值时注意逗号 |
| Chroma L2 距离 → 相似度转换 | `1.0 / (1.0 + score)` 公式 | 向量数据库的距离度量需要正确映射 |
| PowerShell 变量符号与 Python `$` 冲突 | 将 Python 代码写入文件后执行 | 跨 shell 调用需注意转义 |

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

## 📝 项目方法论沉淀

### 为什么选择这个技术栈

1. **FastAPI > Flask**: 原生异步支持，对 SSE 流式输出更友好；自带交互式文档
2. **Chroma > FAISS**: 持久化更简单，无需额外转换；Python 原生集成更好
3. **text2vec-base-chinese > OpenAI Embedding**: 本地免费，中文效果更好；避免 API 调用延迟
4. **Vue 3 > React**: Composition API 对 SSE 的响应式绑定更简洁；学习曲线更平滑

### AI Native 开发的关键原则

1. **Prompt 即代码**: 防幻觉 Prompt 的价值不亚于业务逻辑
2. **流式优先**: SSE 流式输出极大提升用户体验（不需要等待完整回答）
3. **来源可追溯**: 每条回答附带来源引用，增强可信度
4. **可量化验证**: 通过 test_rag.py 客观评估检索质量

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
