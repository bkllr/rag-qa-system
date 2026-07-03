# Git 高级操作

## 变基 Rebase

```bash
git rebase main          # 将当前分支变基到 main
git rebase -i HEAD~3     # 交互式变基（压缩提交）
```

## Cherry-Pick

```bash
git cherry-pick <commit-hash>  # 将指定提交应用到当前分支
```

## 暂存 Stash

```bash
git stash              # 暂存当前修改
git stash pop          # 恢复最近的暂存
git stash list         # 查看暂存列表
```

## 标签

```bash
git tag v1.0.0              # 创建标签
git tag -a v1.0.0 -m "发布" # 附注标签
git push origin --tags      # 推送标签
```
