# Python 日期时间处理

## 基本操作

```python
from datetime import datetime, timedelta
import time

# 当前时间
now = datetime.now()
print(now.isoformat())   # 2024-01-01T12:00:00

# 时间差计算
delta = timedelta(days=7, hours=2)
future = now + delta
past = now - delta

# 格式化
now.strftime("%Y-%m-%d %H:%M:%S")
datetime.strptime("2024-01-01", "%Y-%m-%d")

# 时间戳
ts = time.time()                     # 秒级
dt = datetime.fromtimestamp(ts)
```

## 常用场景

- 记录API请求耗时: `elapsed = time.time() - start`
- 缓存过期时间: `expire_at = now + timedelta(hours=1)`
- 日志时间戳: `now.isoformat()`
