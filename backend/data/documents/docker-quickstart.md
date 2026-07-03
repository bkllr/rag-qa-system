# Docker 快速入门

## 基本概念

- **镜像（Image）**: 应用的只读模板
- **容器（Container）**: 镜像的运行实例
- **Dockerfile**: 构建镜像的脚本

## Dockerfile 示例

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 常用命令

```bash
# 构建镜像
docker build -t my-app .

# 运行容器
docker run -p 8000:8000 my-app

# 查看运行中的容器
docker ps

# 停止容器
docker stop <container_id>
```
