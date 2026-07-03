# Python 类型提示完全指南

Python 3.5+ 支持类型提示，帮助 IDE 和静态检查工具发现错误。

## 基本类型

```python
def process(
    name: str,
    age: int,
    active: bool = True,
    scores: list[float] = [],
    config: dict[str, str] | None = None,
) -> str:
    return f"{name} is {age} years old"
```

## 复杂类型

```python
from typing import Optional, Union, Literal, TypedDict

# 可选类型
def greet(name: Optional[str] = None) -> str: ...

# 字面量类型
def set_mode(mode: Literal["auto", "manual"]) -> None: ...

# TypedDict
class UserDict(TypedDict):
    name: str
    age: int
    email: str | None
```

## 类型别名

```python
type JsonDict = dict[str, str | int | float | bool | None | list | dict]
type Callback = Callable[[str], None]
```
