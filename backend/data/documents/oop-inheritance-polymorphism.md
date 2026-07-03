# 面向对象：继承与多态

## 继承

```python
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        raise NotImplementedError

class Dog(Animal):
    def speak(self):
        return "汪汪！"

class Cat(Animal):
    def speak(self):
        return "喵喵！"
```

## 多态

```python
def make_sound(animal: Animal):
    print(f"{animal.name}: {animal.speak()}")

animals = [Dog("旺财"), Cat("咪咪")]
for a in animals:
    make_sound(a)
```

## 抽象类

```python
from abc import ABC, abstractmethod

class BaseLoader(ABC):
    @abstractmethod
    def load(self, path: str): ...
```
