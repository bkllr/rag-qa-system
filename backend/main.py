"""
RAG QA System - FastAPI 主入口

提供以下 API 端点：
- POST /api/chat           同步 RAG 查询
- POST /api/chat/stream    SSE 流式输出
- GET  /api/admin/documents  获取索引信息
- POST /api/admin/rebuild   重建索引

启动时自动检查并构建 Chroma 索引。
"""

import json
import sys
import time
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# 确保 backend 目录在 import 路径中
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import DOCUMENTS_PATH, check_config
from vector_store import get_vector_store
from rag_engine import query, astream


# ──────────────────────────────────────────────
# Pydantic 模型
# ──────────────────────────────────────────────

class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list
    elapsed: float


class DocumentsInfo(BaseModel):
    document_count: int
    chunk_count: int


class RebuildResponse(BaseModel):
    status: str
    chunk_count: int
    document_count: int


class ErrorResponse(BaseModel):
    error: str
    detail: str = ""


# ──────────────────────────────────────────────
# 应用生命周期管理
# ──────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """启动时自动检查并构建索引。"""
    print("=" * 50)
    print("  RAG QA System 启动中...")
    print("=" * 50)

    # 检查配置
    missing = check_config()
    if missing:
        print(f"  [警告] 缺失配置项: {', '.join(missing)}")
        print(f"  请在 {Path(__file__).parent / '.env'} 中填写正确的值")
        print(f"  首次运行前需要注册 DeepSeek API Key")
    else:
        print("  [OK] 配置完整")

    # 检查并构建索引
    store = get_vector_store()
    if store.has_index():
        info = store.get_collection_info()
        print(f"  [OK] 索引已存在: {info['document_count']} 个文档, {info['chunk_count']} 个片段")
    else:
        print(f"  [索引] 未找到索引，正在从 {DOCUMENTS_PATH} 自动构建...")
        count = store.rebuild_from_directory(DOCUMENTS_PATH)
        info = store.get_collection_info()
        print(f"  [OK] 索引构建完成: {info['document_count']} 个文档, {info['chunk_count']} 个片段")

    print(f"  API 文档: http://localhost:8000/docs")
    print("=" * 50)

    yield  # 应用运行中

    # 关闭时清理（Chroma 自动持久化，无需额外操作）
    print("RAG QA System 关闭")


# ──────────────────────────────────────────────
# FastAPI 应用
# ──────────────────────────────────────────────

app = FastAPI(
    title="RAG QA System",
    description="AI 技术文档智能问答系统 - 基于 RAG 架构",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 配置（允许前端跨域，开发阶段允许所有来源）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应改为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────
# 请求日志中间件
# ──────────────────────────────────────────────

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录每个请求的方法、路径和耗时。"""
    start = time.time()
    response = await call_next(request)
    elapsed = time.time() - start
    # 跳过静态资源和健康检查
    if not request.url.path.startswith("/api"):
        return response
    print(f"  [{request.method}] {request.url.path} → {response.status_code} ({elapsed:.3f}s)")
    return response


# ──────────────────────────────────────────────
# API 端点
# ──────────────────────────────────────────────

@app.get("/")
async def root():
    """健康检查。"""
    return {
        "message": "RAG QA System API is running",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.post("/api/chat", response_model=ChatResponse)
async def api_chat(request: ChatRequest):
    """
    同步 RAG 查询。
    
    请求体: {"question": "什么是RAG?"}
    返回: 回答文本 + 来源引用 + 耗时
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=422, detail="问题不能为空")

    try:
        result = query(request.question.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG 查询失败: {str(e)}")
    return ChatResponse(**result)


@app.post("/api/chat/stream")
async def api_chat_stream(request: ChatRequest):
    """
    SSE 流式 RAG 查询。
    
    请求体: {"question": "什么是RAG?"}
    响应: text/event-stream 流
    
    事件类型:
        data: {"type":"token","content":"..."}   单个文本 token
        data: {"type":"sources","sources":[...]}  来源引用列表
        data: {"type":"done"}                     流结束
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=422, detail="问题不能为空")

    async def event_generator():
        try:
            async for event_type, data in astream(request.question.strip()):
                if event_type == "token":
                    yield f"data: {json.dumps({'type': 'token', 'content': data}, ensure_ascii=False)}\n\n"
                elif event_type == "sources":
                    yield f"data: {json.dumps({'type': 'sources', 'sources': data}, ensure_ascii=False)}\n\n"
                elif event_type == "done":
                    yield f"data: {json.dumps({'type': 'done'})}\n\n"
                elif event_type == "error":
                    yield f"data: {json.dumps({'type': 'error', 'content': data}, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'content': f'流式输出异常: {str(e)}'}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 禁用 nginx 缓冲
        },
    )


@app.get("/api/admin/documents", response_model=DocumentsInfo)
async def api_get_documents_info():
    """获取索引信息。"""
    store = get_vector_store()
    info = store.get_collection_info()
    return DocumentsInfo(**info)


@app.post("/api/admin/rebuild", response_model=RebuildResponse)
async def api_rebuild_index():
    """重建索引（重新加载文档并构建向量索引）。"""
    store = get_vector_store()
    try:
        chunk_count = store.rebuild_from_directory(DOCUMENTS_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"索引重建失败: {str(e)}")
    info = store.get_collection_info()

    return RebuildResponse(
        status="ok",
        chunk_count=chunk_count,
        document_count=info["document_count"],
    )


# ──────────────────────────────────────────────
# 启动入口
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
