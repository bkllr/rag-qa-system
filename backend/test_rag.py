"""
RAG QA System - 自动测试脚本

预定义 20 个测试问题 + 期望答案特征，
对每个问题调用 rag_engine.query()，
输出 PASS/FAIL 报告和准确率。
"""

import time
from rag_engine import query
from vector_store import get_vector_store


# ──────────────────────────────────────────────
# 测试用例定义
# ──────────────────────────────────────────────

TEST_CASES = [
    # (问题, 期望答案中应包含的关键词列表)
    ("什么是RAG？", ["检索增强生成", "Retrieval-Augmented Generation"]),
    ("FastAPI 支持哪些类型的流式响应？", ["StreamingResponse", "SSE"]),
    ("LangChain 的 LCEL 语法使用什么符号连接组件？", ["管道", "|", "pipe"]),
    ("Chroma 向量数据库的持久化模式怎么配置？", ["persist_directory", "持久化"]),
    ("text2vec-base-chinese 模型的维度是多少？", ["768"]),
    ("小米 MACE 框架主要用于什么场景？", ["移动端", "深度学习", "推理"]),
    ("RAG 系统如何防止 LLM 幻觉？", ["编造", "约束", "prompt"]),
    ("Python 装饰器的本质是什么？", ["高阶函数", "函数"]),
    ("FastAPI 如何配置 CORS？", ["CORSMiddleware", "allow_origins"]),
    ("什么是 SSE？", ["Server-Sent Events", "事件"]),
    ("DeepSeek API 的 base_url 是什么？", ["api.deepseek.com"]),
    ("Python 的 async def 定义的是什么？", ["协程", "coroutine"]),
    ("RecursiveCharacterTextSplitter 的 chunk_size 推荐值是多少？", ["500"]),
    ("小米 Open-Falcon 是什么？", ["监控", "monitoring"]),
    ("Vue 3 的组合式 API 使用什么函数定义？", ["setup", "ref", "computed"]),
    ("Chroma 数据库的 score 是什么意思？", ["距离", "越小", "L2"]),
    ("小米 Pegasus 底层的存储引擎是什么？", ["RocksDB"]),
    ("Vite 如何配置开发代理？", ["proxy", "target"]),
    ("RAG Prompt 中必须加入什么约束？", ["编造", "如实", "找不到"]),
    ("Python dotenv 库的作用是什么？", [".env", "环境变量"]),
]


def evaluate_answer(answer: str, expected_keywords: list[str]) -> bool:
    """检查回答是否包含期望的关键词（至少匹配 1 个）。"""
    answer_lower = answer.lower()
    for keyword in expected_keywords:
        if keyword.lower() in answer_lower:
            return True
    return False


def run_tests() -> dict:
    """
    运行所有测试用例。
    
    Returns:
        {"passed": int, "failed": int, "total": int, "accuracy": float, "details": list}
    """
    # 确保索引存在
    store = get_vector_store()
    if not store.has_index():
        print("[错误] 索引未构建，请先启动后端或运行 rebuild")
        return {"passed": 0, "failed": len(TEST_CASES), "total": len(TEST_CASES), "accuracy": 0.0, "details": []}

    passed = 0
    failed = 0
    details = []
    total_time = 0.0

    print("=" * 70)
    print("  RAG QA System - 测试脚本")
    print("=" * 70)
    print(f"  测试用例数: {len(TEST_CASES)}")
    print("-" * 70)

    for i, (question, keywords) in enumerate(TEST_CASES, 1):
        print(f"\n[{i:02d}] 问题: {question}")
        print(f"    期望关键词: {keywords}")

        try:
            result = query(question, k=4)
            answer = result["answer"]
            elapsed = result.get("elapsed", 0)
            total_time += elapsed

            is_pass = evaluate_answer(answer, keywords)
            status = "PASS" if is_pass else "FAIL"

            print(f"    回答: {answer[:100]}...")
            print(f"    耗时: {elapsed:.3f}s")
            print(f"    结果: {status}")

            if is_pass:
                passed += 1
            else:
                failed += 1
                print(f"    [未匹配] 回答中未找到期望关键词")

            details.append({
                "question": question,
                "keywords": keywords,
                "answer_preview": answer[:200],
                "elapsed": elapsed,
                "passed": is_pass,
            })

        except Exception as e:
            print(f"    [错误] {e}")
            failed += 1
            details.append({
                "question": question,
                "keywords": keywords,
                "answer_preview": f"ERROR: {str(e)}",
                "elapsed": 0,
                "passed": False,
            })

    accuracy = passed / len(TEST_CASES) * 100 if TEST_CASES else 0

    print("\n" + "=" * 70)
    print(f"  测试完成")
    print(f"  PASS: {passed}  |  FAIL: {failed}  |  准确率: {accuracy:.1f}%")
    print(f"  总耗时: {total_time:.3f}s  |  平均耗时: {total_time/len(TEST_CASES):.3f}s")
    print("=" * 70)

    return {
        "passed": passed,
        "failed": failed,
        "total": len(TEST_CASES),
        "accuracy": round(accuracy, 1),
        "avg_elapsed": round(total_time / len(TEST_CASES), 3) if TEST_CASES else 0,
        "details": details,
    }


if __name__ == "__main__":
    results = run_tests()

    # 输出供 README 使用的指标
    print(f"\n[量化指标]")
    print(f"  检索准确率: {results['accuracy']}%")
    print(f"  平均响应时间: {results['avg_elapsed']}s")
