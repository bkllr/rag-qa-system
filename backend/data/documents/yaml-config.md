# YAML 配置文件

## 基本语法

```yaml
server:
  host: "0.0.0.0"
  port: 8000
  debug: true

database:
  url: "postgresql://localhost/db"
  pool_size: 10

# 列表
allowed_origins:
  - "http://localhost:5173"
  - "http://localhost:3000"
```

## Python 读写

```python
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

with open("output.yaml", "w") as f:
    yaml.dump(config, f, allow_unicode=True)
```

## YAML vs JSON
- YAML: 可读性好，支持注释
- JSON: 更严格，通用性更强
