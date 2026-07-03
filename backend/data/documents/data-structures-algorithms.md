# 数据结构与算法

## 时间复杂度

| 复杂度 | 示例 |
|:--|:--|
| O(1) | 数组索引 |
| O(log n) | 二分查找 |
| O(n) | 线性搜索 |
| O(n log n) | 快速排序 |
| O(n^2) | 冒泡排序 |

## 常用数据结构

- 数组/列表: O(1) 索引
- 链表: O(1) 插入删除
- 哈希表: O(1) 查找
- 栈/队列: LIFO/FIFO
- 树/图: 层次关系

## Python 实现

```python
# 二分查找
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```
