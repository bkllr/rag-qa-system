"""
RAG QA System - 配置加载模块

使用 python-dotenv 读取 .env 文件中的配置项，
提供 get_llm() 和 get_embeddings() 工厂函数，
其他模块通过调用这两个函数获取 LLM 和 Embedding 实例。
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ──────────────────────────────────────────────
# 路径常量（基于 __file__ 的绝对路径，避免相对路径问题）
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent  # backend/
CHROMA_PATH = str(BASE_DIR / "chroma_db")  # Chroma 持久化目录
DOCUMENTS_PATH = str(BASE_DIR / "data" / "documents")  # 原始文档目录
AI_LOGS_PATH = str(BASE_DIR / "ai-logs")  # AI 对话截图目录

# ──────────────────────────────────────────────
# 加载 .env 配置
# ──────────────────────────────────────────────
load_dotenv(BASE_DIR / ".env")

# LLM 配置
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "deepseek-chat")

# Embedding 配置
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "shibing624/text2vec-base-chinese")


# ──────────────────────────────────────────────
# 工厂函数
# ──────────────────────────────────────────────

# 缓存实例，避免重复加载
_llm_instance = None
_embeddings_instance = None


def get_llm():
    """
    获取 LLM 实例（DeepSeek API，兼容 OpenAI 接口）。
    使用单例模式，避免重复初始化。
    """
    global _llm_instance
    if _llm_instance is None:
        from langchain_openai import ChatOpenAI

        _llm_instance = ChatOpenAI(
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL,
            model=LLM_MODEL_NAME,
            temperature=0.3,  # 低温度保证回答稳定
            max_tokens=2048,
            streaming=True,  # 支持流式输出
        )
    return _llm_instance


def get_embeddings():
    """
    获取 Embedding 模型实例（本地 HuggingFace 模型）。
    使用单例模式，避免重复加载模型。
    首次调用时会自动下载模型（约 500MB）。
    """
    global _embeddings_instance
    if _embeddings_instance is None:
        from langchain_huggingface import HuggingFaceEmbeddings

        _embeddings_instance = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},  # CPU 推理，兼容性最好
            encode_kwargs={"normalize_embeddings": True},
        )
    return _embeddings_instance


def check_config():
    """检查必要配置是否已填写，返回缺失项列表。"""
    missing = []
    if not LLM_API_KEY or LLM_API_KEY == "your_deepseek_api_key_here":
        missing.append("LLM_API_KEY")
    return missing


if __name__ == "__main__":
    print(f"BASE_DIR:       {BASE_DIR}")
    print(f"CHROMA_PATH:    {CHROMA_PATH}")
    print(f"DOCUMENTS_PATH: {DOCUMENTS_PATH}")
    print(f"LLM_BASE_URL:   {LLM_BASE_URL}")
    print(f"LLM_MODEL_NAME: {LLM_MODEL_NAME}")
    print(f"EMBEDDING_MODEL: {EMBEDDING_MODEL}")
    missing = check_config()
    if missing:
        print(f"\n[警告] 缺失配置项: {', '.join(missing)}")
        print("请在 backend/.env 中填写正确的值")
    else:
        print("\n[OK] 配置完整")
