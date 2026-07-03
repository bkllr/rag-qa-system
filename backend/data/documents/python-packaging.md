# Python 项目打包与发布

## 项目结构

```
my-package/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── pyproject.toml
├── README.md
└── LICENSE
```

## pyproject.toml 配置

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "my-package"
version = "0.1.0"
description = "描述"
requires-python = ">=3.10"
dependencies = ["fastapi>=0.100.0"]

[project.optional-dependencies]
dev = ["pytest", "ruff"]
```

## 安装与发布

```bash
# 开发安装
pip install -e .

# 构建
python -m build

# 发布到 PyPI
twine upload dist/*
```
