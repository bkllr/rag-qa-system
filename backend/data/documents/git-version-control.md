# Git 版本控制最佳实践

## 分支策略

```
main      产品环境代码
  ├── develop  开发分支
  │   ├── feat/xxx   功能分支
  │   ├── fix/xxx    修复分支
  │   └── chore/xxx  工具链分支
  └── hotfix/xxx     紧急修复
```

## 提交信息规范

```
类型: 简短描述

详细描述（可选）

类型：
- feat: 新功能
- fix: 修复
- docs: 文档
- style: 格式
- refactor: 重构
- test: 测试
- chore: 工具链
```

## 实用命令

```bash
# 查看提交历史
git log --oneline --graph

# 暂存部分修改
git add -p

# 修改最近一次提交
git commit --amend

# 撤销暂存
git reset HEAD <file>

# 查看差异
git diff --staged
```
