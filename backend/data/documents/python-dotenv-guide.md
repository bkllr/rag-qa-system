# python-dotenv 配置管理

python-dotenv 是一个从 `.env` 文件加载环境变量的 Python 库，广泛用于管理应用的敏感配置。

## 安装

```bash
pip install python-dotenv
```

## .env 文件格式

```bash
# 注释行
API_KEY=sk-1234567890abcdef
DATABASE_URL=postgresql://user:pass@localhost:5432/db
DEBUG=True
PORT=8000
```

## 基本用法

```python
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 读取环境变量
api_key = os.getenv("API_KEY")
debug = os.getenv("DEBUG", "False").lower() == "true"
port = int(os.getenv("PORT", "8000"))
```

## 指定 .env 文件路径

```python
from pathlib import Path
from dotenv import load_dotenv

# 基于 __file__ 的绝对路径
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# 也可以指定其他路径
load_dotenv("/path/to/custom.env")
```

## 带默认值的读取

```python
import os

# 方式1: os.getenv（推荐）
api_key = os.getenv("API_KEY", "default_key")
port = int(os.getenv("PORT", "8000"))

# 方式2: os.environ.get
api_key = os.environ.get("API_KEY", "default_key")
```

## 最佳实践

### 1. 不要提交 .env 文件

```gitignore
# .gitignore
.env
.env.local
.env.production
```

### 2. 提供 .env.example

```bash
# .env.example
API_KEY=your_api_key_here
DATABASE_URL=your_database_url_here
DEBUG=False
```

### 3. 类型转换

```python
import os

# 字符串
api_key = os.getenv("API_KEY")

# 整数
port = int(os.getenv("PORT", "8000"))

# 布尔值
debug = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

# 列表（逗号分隔）
allowed_hosts = os.getenv("ALLOWED_HOSTS", "").split(",")
```

### 4. 配置校验

```python
def check_config():
    missing = []
    if not os.getenv("API_KEY"):
        missing.append("API_KEY")
    if not os.getenv("DATABASE_URL"):
        missing.append("DATABASE_URL")
    if missing:
        raise EnvironmentError(f"缺失配置: {', '.join(missing)}")
```

## 在 FastAPI 项目中的使用

```python
# config.py
from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "deepseek-chat")
```
