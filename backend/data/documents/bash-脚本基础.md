# Bash 脚本基础

```bash
#!/bin/bash

# 变量
NAME="world"
echo "Hello, $NAME"

# 条件判断
if [ -f "file.txt" ]; then
    echo "文件存在"
fi

# 循环
for i in {1..5}; do
    echo $i
done

# 函数
function greet() {
    echo "Hello $1"
}
greet "World"
```