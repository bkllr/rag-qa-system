# Python 列表推导式

```python
squares = [x**2 for x in range(10)]
evens = [x for x in range(10) if x % 2 == 0]
d = {k:v for k,v in [('a',1),('b',2)]}
```

## 对比 map/filter
列表推导式比 map/filter 更直观易读，Python社区推荐使用。