# Python argparse 命令行参数

```python
import argparse

parser = argparse.ArgumentParser(description="RAG 文档管理工具")

parser.add_argument("--rebuild", action="store_true", help="重建索引")
parser.add_argument("--k", type=int, default=4, help="检索返回数")
parser.add_argument("--query", type=str, help="查询内容")

args = parser.parse_args()

if args.rebuild:
    rebuild_index()
elif args.query:
    result = query(args.query, k=args.k)
    print(result["answer"])
```

## 参数类型
- store_true: 布尔标志
- type=str: 字符串
- type=int: 整数
- default: 默认值
- required=True: 必填
