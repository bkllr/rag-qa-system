"""
RAG QA System - Chroma 向量数据库管理模块

使用 Chroma 持久化模式存储文档向量，
提供构建索引、语义检索、集合信息查询等功能。
"""

import os
from typing import List, Optional, Tuple
from pathlib import Path

from langchain_core.documents import Document
from langchain_chroma import Chroma

from config import CHROMA_PATH, get_embeddings


class VectorStore:
    """
    Chroma 向量数据库管理器。
    封装了文档索引构建、语义检索、集合信息查询等功能。
    使用单例模式确保全局只有一个实例。
    """

    _instance: Optional["VectorStore"] = None

    def __new__(cls) -> "VectorStore":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # 获取 Embedding 实例
        self._embeddings = get_embeddings()

        # 初始化 Chroma（持久化模式）
        self._vectorstore = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=self._embeddings,
            collection_name="rag_documents",
        )

    # ──────────────────────────────────────────────
    # 索引构建
    # ──────────────────────────────────────────────

    def build_index(self, documents: List[Document]) -> int:
        """
        将文档列表向量化后存入 Chroma。

        Args:
            documents: LangChain Document 列表

        Returns:
            存入的文档片段总数
        """
        if not documents:
            print("[警告] 文档列表为空，跳过索引构建")
            return 0

        # 先清空已有索引（如果有）
        self._clear_index()

        print(f"[索引] 正在构建向量索引，共 {len(documents)} 个片段...")
        # 批量添加文档
        ids = self._vectorstore.add_documents(documents)
        print(f"[索引] 构建完成，已存入 {len(ids)} 个片段")

        return len(ids)

    def _clear_index(self):
        """清空已有索引（用于重建）。"""
        try:
            collection = self._vectorstore._collection
            count = collection.count()
            if count > 0:
                # 获取所有 ID 并删除
                ids = collection.get()["ids"]
                if ids:
                    collection.delete(ids=ids)
                print(f"[索引] 已清空 {count} 条旧索引")
        except Exception as e:
            print(f"[警告] 清空索引时出错: {e}")

    # ──────────────────────────────────────────────
    # 语义检索
    # ──────────────────────────────────────────────

    def search(self, query: str, k: int = 4) -> List[Tuple[Document, float]]:
        """
        语义检索：返回最相关的 k 个文档片段及其相似度分数。

        Args:
            query: 查询文本
            k: 返回结果数

        Returns:
            [(Document, score), ...] 列表
            score 是 Chroma 的距离值，越小表示越相似。
        """
        if not query or not query.strip():
            return []

        results = self._vectorstore.similarity_search_with_score(query, k=k)

        return results

    # ──────────────────────────────────────────────
    # 集合信息
    # ──────────────────────────────────────────────

    def has_index(self) -> bool:
        """检查是否已有索引数据。"""
        try:
            count = self._vectorstore._collection.count()
            return count > 0
        except Exception:
            return False

    def get_collection_info(self) -> dict:
        """
        获取集合信息：已索引的文档数和片段数。

        Returns:
            {"document_count": int, "chunk_count": int}
        """
        try:
            collection = self._vectorstore._collection
            count = collection.count()

            # 获取所有唯一 source（文件数）
            all_data = collection.get()
            sources = set()
            if all_data["metadatas"]:
                for meta in all_data["metadatas"]:
                    if meta and "source" in meta:
                        sources.add(meta["source"])

            return {
                "document_count": len(sources),
                "chunk_count": count,
            }
        except Exception as e:
            print(f"[错误] 获取集合信息失败: {e}")
            return {"document_count": 0, "chunk_count": 0}

    # ──────────────────────────────────────────────
    # 索引重建
    # ──────────────────────────────────────────────

    def rebuild_from_directory(self, documents_path: str) -> int:
        """
        从文档目录重建索引。
        加载目录中的所有文档，切片，然后重新构建向量索引。

        Args:
            documents_path: 文档目录路径

        Returns:
            文档片段总数
        """
        from document_loader import load_documents

        print(f"[重建] 从目录加载文档: {documents_path}")
        documents = load_documents(documents_path)

        if not documents:
            print("[重建] 未找到文档")
            return 0

        return self.build_index(documents)

    def delete_collection(self):
        """删除整个集合（慎用）。"""
        try:
            self._vectorstore.delete_collection()
            print("[索引] 集合已删除")
            # 重新初始化
            self._vectorstore = Chroma(
                persist_directory=CHROMA_PATH,
                embedding_function=self._embeddings,
                collection_name="rag_documents",
            )
        except Exception as e:
            print(f"[错误] 删除集合失败: {e}")


# ──────────────────────────────────────────────
# 便捷函数（供其他模块使用）
# ──────────────────────────────────────────────

def get_vector_store() -> VectorStore:
    """获取 VectorStore 单例实例。"""
    return VectorStore()


if __name__ == "__main__":
    # 独立运行测试
    from config import DOCUMENTS_PATH

    store = get_vector_store()
    print(f"Chroma 持久化目录: {CHROMA_PATH}")
    print(f"索引状态: {'已存在' if store.has_index() else '未构建'}")

    info = store.get_collection_info()
    print(f"文档数: {info['document_count']}, 片段数: {info['chunk_count']}")

    if not store.has_index():
        print(f"\n开始从 {DOCUMENTS_PATH} 构建索引...")
        count = store.rebuild_from_directory(DOCUMENTS_PATH)
        print(f"构建完成，共 {count} 个片段")

        info = store.get_collection_info()
        print(f"文档数: {info['document_count']}, 片段数: {info['chunk_count']}")

        print("\n测试检索: '什么是RAG?'")
        results = store.search("什么是RAG?", k=3)
        for i, (doc, score) in enumerate(results, 1):
            print(f"\n  [{i}] score={score:.4f}, source={doc.metadata.get('source', '?')}")
            print(f"      {doc.page_content[:80]}...")
