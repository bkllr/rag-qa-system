# Python logging 日志系统

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
