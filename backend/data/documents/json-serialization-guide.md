# JSON 序列化与反序列化

JSON 是 Web API 中最常用的数据交换格式。

## Python JSON 操作

```python
import json

# 序列化（Python → JSON）
data = {"name": "张三", "age": 25}
json_str = json.dumps(data, ensure_ascii=False)

# 反序列化（JSON → Python）
parsed = json.loads('{"name": "李四", "age": 30}')

# 文件操作
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

## 自定义序列化

```python
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)

json.dumps(data, cls=DateTimeEncoder)
```

## Pydantic 与 JSON

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

user = User(name="张三", age=25)
json_str = user.model_dump_json()  # 序列化
parsed = User.model_validate_json(json_str)  # 反序列化
```
