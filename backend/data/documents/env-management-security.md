# 环境变量与密钥管理

## .env 文件安全

```bash
# 永远不要提交到 Git
.env
.env.local
.env.production
```

## 密钥注入方式

```python
# 方式1: .env 文件（开发环境）
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")

# 方式2: 环境变量（生产环境）
api_key = os.environ["API_KEY"]

# 方式3: 密钥管理服务（推荐）
from vault_client import get_secret
api_key = get_secret("api/deepseek/key")
```

## 安全准则

1. 不在代码中硬编码密钥
2. 不同环境使用不同密钥
3. 定期轮换密钥
4. 限制密钥权限范围
5. 监控密钥使用情况
