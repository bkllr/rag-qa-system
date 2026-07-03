# Docker Compose

```yaml
version: "3"
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
  frontend:
    build: ./frontend
    ports: ["5173:5173"]
```

```bash
docker-compose up -d        # 启动
docker-compose down         # 停止
docker-compose logs -f      # 查看日志
```