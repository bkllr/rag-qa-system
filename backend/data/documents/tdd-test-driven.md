# 测试驱动开发 (TDD)

## TDD 循环

```
1. 写测试 → 2. 运行测试(红) → 3. 写代码 → 4. 运行测试(绿) → 5. 重构
```

## pytest 示例

```python
# test_rag.py
def test_query_returns_answer():
    result = query("什么是Python?")
    assert result["answer"]
    assert len(result["sources"]) > 0

def test_empty_question():
    result = query("")
    assert result["answer"] == "未在文档中找到相关内容。"
```

## 测试金字塔

```
      /\
     /E2E\       少量
    /______\
   /集成测试\    适量
  /__________\
 /  单元测试   \  大量
/______________\
```
