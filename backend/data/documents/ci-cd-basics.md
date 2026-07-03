# CI/CD 持续集成与部署

## 工作流程

```
代码提交 → 自动构建 → 自动测试 → 自动部署
```

## GitHub Actions 示例

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest
```

## 关键实践

1. 每次提交触发自动测试
2. 合并前必须通过 CI
3. 自动部署到开发环境
4. 生产发布需要人工审批
