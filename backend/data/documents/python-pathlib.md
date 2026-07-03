# Python pathlib 路径操作

pathlib 是 Python 3.4+ 推荐的路径处理库。

```python
from pathlib import Path

# 当前文件目录
BASE_DIR = Path(__file__).resolve().parent

# 路径拼接
data_dir = BASE_DIR / "data" / "documents"
config_file = BASE_DIR / ".env"

# 目录操作
data_dir.mkdir(parents=True, exist_ok=True)

# 遍历文件
for file in data_dir.rglob("*.md"):
    print(file.name, file.stem, file.suffix)

# 文件操作
content = (data_dir / "readme.md").read_text(encoding="utf-8")
(data_dir / "output.txt").write_text("hello", encoding="utf-8")
```

## Path vs os.path
| os.path | pathlib |
|:--|:--|
| os.path.join(a, b) | Path(a) / b |
| os.path.exists(p) | Path(p).exists() |
| os.path.dirname(p) | Path(p).parent |
