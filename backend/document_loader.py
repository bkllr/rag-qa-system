"""
RAG QA System - 文档加载与文本切片模块

支持 .txt、.md、.pdf 三种文档格式，
使用 LangChain 的文档加载器加载原始文档，
再用 RecursiveCharacterTextSplitter 进行递归切片，
切片时保留元数据（文件名、来源路径）。
"""

import os
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 切片参数
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def _load_single_file(file_path: str) -> List[Document]:
    """根据文件扩展名选择对应的加载器，加载单个文件。"""
    ext = Path(file_path).suffix.lower()

    if ext in (".txt", ".md"):
        from langchain_community.document_loaders import TextLoader

        loader = TextLoader(file_path, encoding="utf-8")
        return loader.load()

    elif ext == ".pdf":
        from langchain_community.document_loaders import PyPDFLoader

        loader = PyPDFLoader(file_path)
        return loader.load()

    else:
        print(f"  [跳过] 不支持的文件格式: {file_path}")
        return []


def load_documents(directory_path: str) -> List[Document]:
    """
    加载指定目录下的所有文档并进行切片。

    Args:
        directory_path: 文档目录路径

    Returns:
        切片后的 Document 列表，每个 Document 的 metadata 包含 source 字段

    流程:
        1. 遍历目录，加载所有 .txt/.md/.pdf 文件
        2. 将每个文档的 metadata.source 设置为文件名（不含路径）
        3. 使用 RecursiveCharacterTextSplitter 统一切片
        4. 返回切片后的 Document 列表
    """
    directory = Path(directory_path)

    if not directory.exists():
        print(f"[错误] 文档目录不存在: {directory_path}")
        return []

    # Step 1: 加载所有原始文档
    raw_documents: List[Document] = []
    supported_exts = {".txt", ".md", ".pdf"}

    for file_path in sorted(directory.rglob("*")):
        if file_path.is_file() and file_path.suffix.lower() in supported_exts:
            print(f"  [加载] {file_path.name}")
            docs = _load_single_file(str(file_path))
            # 规范化元数据：用文件名作为 source
            for doc in docs:
                doc.metadata["source"] = file_path.name
                doc.metadata["filename"] = file_path.name
            raw_documents.extend(docs)

    if not raw_documents:
        print(f"[警告] 目录中没有找到支持的文档: {directory_path}")
        return []

    print(f"  共加载 {len(raw_documents)} 个原始文档")

    # Step 2: 递归切片
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],
        length_function=len,
    )

    split_documents = text_splitter.split_documents(raw_documents)
    print(f"  切片完成，共 {len(split_documents)} 个片段")

    return split_documents


if __name__ == "__main__":
    # 独立运行时，测试文档加载功能
    from config import DOCUMENTS_PATH

    print(f"文档目录: {DOCUMENTS_PATH}")
    print("=" * 50)
    documents = load_documents(DOCUMENTS_PATH)
    print("=" * 50)
    print(f"总计: {len(documents)} 个切片")

    if documents:
        print(f"\n示例片段（第 1 个）:")
        print(f"  metadata: {documents[0].metadata}")
        print(f"  content (前 100 字): {documents[0].page_content[:100]}...")
