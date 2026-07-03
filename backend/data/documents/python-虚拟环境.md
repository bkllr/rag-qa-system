# Python 虚拟环境

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate    # Windows
pip freeze > requirements.txt
pip install -r requirements.txt
deactivate
```

## 最佳实践
1. 每个项目独立虚拟环境
2. requirements.txt 锁定版本号
3. .gitignore 忽略 venv 目录