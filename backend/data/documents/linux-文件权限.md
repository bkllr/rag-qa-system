# Linux 文件权限

```bash
ls -l
# -rwxr-xr-x owner group file
# [type][usr][grp][oth]
# r=4  w=2  x=1

chmod 755 script.sh   # rwxr-xr-x
chmod 644 file.txt    # rw-r--r--
chown user:group file
```

## 目录权限
- r: 可列出目录内容
- w: 可在目录中创建/删除文件
- x: 可进入目录