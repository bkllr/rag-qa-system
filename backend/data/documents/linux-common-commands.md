# Linux 常用命令

## 文件操作

```bash
ls -la           # 列出文件
cd /path         # 切换目录
cp src dst       # 复制
mv src dst       # 移动/重命名
rm -rf dir       # 删除
find . -name "*.py"  # 查找文件
```

## 文本处理

```bash
grep "pattern" file.txt     # 搜索
wc -l file.txt              # 行数
head -n 10 file.txt         # 前 10 行
tail -f file.txt            # 实时跟踪
```

## 进程管理

```bash
ps aux          # 查看进程
kill -9 PID     # 终止进程
htop            # 交互式进程查看
nohup cmd &     # 后台运行
```
