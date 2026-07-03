"""
RAG QA System - 核心 RAG 引擎模块

使用 LangChain LCEL 表达式语法构建检索增强生成流水线：
1. 向量检索 → 获取最相关文档片段
2. Prompt 构建 → 将检索结果拼接为上下文
3. LLM 生成 → 调用大模型生成回答
4. 组装返回 → 回答 + 来源引用

支持同步查询（query）和异步流式输出（astream）。
"""

from __future__ import annotations

import json
import time
import asyncio
from typing import AsyncGenerator, Dict, List, Tuple

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

from config import get_llm
from vector_store import get_vector_store


# ──────────────────────────────────────────────
# RAG Prompt 模板（关键：防幻觉约束）
# ──────────────────────────────────────────────

RAG_PROMPT_TEMPLATE = """你是一个专业的技术文档助手。
请严格根据以下参考资料回答用户的问题。

【回答规则】
1. 只基于参考资料中的信息回答，不要编造、不要猜测、不要使用外部知识。
2. 如果参考资料中没有相关信息，请明确回答："未在文档中找到相关内容"。
3. 回答要简洁准确，优先使用参考资料中的原话。
4. 如果参考资料中有代码示例，可以引用。

【参考资料】
{context}

【用户问题】
{question}

【回答】"""


def _build_context(docs_with_scores: List[Tuple[Document, float]]) -> str:
    """
    将检索结果拼接为 context 字符串。

    Args:
        docs_with_scores: [(Document, float), ...] 列表

    Returns:
        格式化的 context 字符串
    """
    parts = []
    for i, (doc, score) in enumerate(docs_with_scores, 1):
        source = doc.metadata.get("source", "未知文件")
        # 将 Chroma 的距离分数转换为相似度百分比
        # Chroma 使用 L2 距离，越小越相似
        similarity = max(0.0, min(1.0, 1.0 / (1.0 + score)))

        parts.append(
            f"【片段 {i} - 来源: {source} - 相似度: {similarity:.0%}】\n{doc.page_content}\n"
        )

    return "\n".join(parts)


def _format_sources(docs_with_scores: List[Tuple[Document, float]]) -> List[dict]:
    """
    格式化来源信息，供前端展示。

    Args:
        docs_with_scores: [(Document, float), ...]

    Returns:
        [{"content": str, "filename": str, "score": float}, ...]
    """
    sources = []
    for doc, score in docs_with_scores:
        similarity = max(0.0, min(1.0, 1.0 / (1.0 + score)))
        sources.append({
            "content": doc.page_content[:200],  # 截取前 200 字
            "filename": doc.metadata.get("source", "未知"),
            "score": round(similarity, 4),
        })
    return sources


# ──────────────────────────────────────────────
# 同步查询（非流式）
# ──────────────────────────────────────────────

def query(question: str, k: int = 4) -> Dict:
    """
    同步 RAG 查询：检索 → 生成 → 返回完整回答。

    Args:
        question: 用户问题
        k: 检索返回的文档数

    Returns:
        {
            "answer": str,         # LLM 生成的回答
            "sources": [...]       # 来源引用列表
            "elapsed": float,      # 耗时（秒）
        }
    """
    start_time = time.time()

    # Step 1: 向量检索
    store = get_vector_store()
    docs_with_scores = store.search(question, k=k)

    if not docs_with_scores:
        elapsed = time.time() - start_time
        return {
            "answer": "未在文档中找到相关内容。",
            "sources": [],
            "elapsed": round(elapsed, 3),
        }

    # Step 2: 构建 context
    context = _build_context(docs_with_scores)

    # Step 3: 构建 LCEL 链并生成
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    chain = prompt | llm | StrOutputParser()

    try:
        answer = chain.invoke({"context": context, "question": question})
    except Exception as e:
        answer = f"生成回答时出错: {str(e)}"

    # Step 4: 组装返回
    elapsed = time.time() - start_time
    sources = _format_sources(docs_with_scores)

    return {
        "answer": answer,
        "sources": sources,
        "elapsed": round(elapsed, 3),
    }


# ──────────────────────────────────────────────
# 异步流式查询
# ──────────────────────────────────────────────

async def astream(
    question: str, k: int = 4
) -> AsyncGenerator[Tuple[str, str | dict | None], None]:
    """
    异步流式 RAG 查询，逐个 token 返回。

    用法:
        async for event_type, data in rag_engine.astream("问题"):
            if event_type == "token":
                print(data, end="")  # 逐步打印 token
            elif event_type == "sources":
                # data 是来源列表
            elif event_type == "done":
                break

    Args:
        question: 用户问题
        k: 检索返回的文档数

    Yields:
        ("token", str)     - 单个文本 token
        ("sources", list)  - 来源引用列表
        ("done", None)     - 流结束
        ("error", str)     - 错误信息
    """
    start_time = time.time()

    # Step 1: 向量检索
    store = get_vector_store()
    docs_with_scores = store.search(question, k=k)

    if not docs_with_scores:
        yield ("token", "未在文档中找到相关内容。")
        yield ("sources", [])
        yield ("done", None)
        return

    # Step 2: 构建 context
    context = _build_context(docs_with_scores)

    # Step 3: 流式生成
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    chain = prompt | llm | StrOutputParser()

    try:
        async for chunk in chain.astream({"context": context, "question": question}):
            yield ("token", chunk)
    except Exception as e:
        yield ("error", f"生成回答时出错: {str(e)}")
        yield ("done", None)
        return

    # Step 4: 返回来源
    sources = _format_sources(docs_with_scores)
    yield ("sources", sources)

    # 记录耗时
    elapsed = time.time() - start_time
    print(f"[RAG] 流式查询完成，耗时 {elapsed:.3f}s")

    yield ("done", None)


# ──────────────────────────────────────────────
# 独立测试
# ──────────────────────────────────────────────

if __name__ == "__main__":
    test_question = "什么是RAG?"

    # 先确保索引存在
    store = get_vector_store()
    if not store.has_index():
        from config import DOCUMENTS_PATH
        print(f"索引不存在，正在从 {DOCUMENTS_PATH} 构建...")
        store.rebuild_from_directory(DOCUMENTS_PATH)

    print(f"\n问题: {test_question}")
    print("=" * 60)

    # 测试非流式查询
    print("\n[非流式查询]")
    result = query(test_question, k=4)
    print(f"回答: {result['answer'][:200]}...")
    print(f"来源数: {len(result['sources'])}")
    print(f"耗时: {result['elapsed']}s")

    # 测试流式查询
    print("\n[流式查询]")
    async def test_stream():
        async for event_type, data in astream(test_question, k=4):
            if event_type == "token":
                print(data, end="", flush=True)
            elif event_type == "sources":
                print(f"\n\n[来源: {len(data)} 个]")
                for s in data:
                    print(f"  - {s['filename']} (相似度: {s['score']:.2%})")
            elif event_type == "done":
                print("\n--- 流式输出结束 ---")

    asyncio.run(test_stream())
