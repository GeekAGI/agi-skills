---
name: git-feature-branch
description: |
  基于项目版本管理规范，从 release 分支自动创建 feature 分支。
  分支命名格式为 feature/YYYYMMDD/{变更描述英文}。
  当用户需要创建新功能分支、开始新功能开发、或提到从 release 切分支时使用此 skill。
  适用于 Git 版本控制的项目，特别是使用 feature branch 工作流的团队。
---

# git-feature-branch

## Overview

此 skill 帮助用户基于 release 分支快速创建符合命名规范的 feature 分支。

分支命名规范：`feature/YYYYMMDD/{变更描述英文}`
- 日期部分使用版本上线日期（YYYYMMDD 格式），默认为当天日期
- 变更描述使用英文，单词间用短横线连接

## Using this Skill

当用户需要创建 feature 分支时：

1. 询问用户变更描述（可以是中文或英文）
2. 询问版本上线日期（可选，默认为当天）
3. 如果是中文描述，先将其翻译为英文
4. 将英文描述转换为短横线连接格式（kebab-case）
5. 执行脚本创建分支

### 工作流程

1. 确认当前在 git 仓库中
2. 检查并切换到 release 分支
3. 拉取最新的 release 分支代码
4. 基于 release 创建 feature 分支
5. 推送到远程仓库

### 示例用法

用户说：
- "帮我创建一个分支，用于新增巡检功能，版本 20260305 上线"
- "从 release 切一个分支，修复内存泄漏问题"
- "我要开始开发用户管理模块，3月5号上线"

执行步骤：
1. 提取变更描述："新增巡检功能" / "fix memory leak" / "user management module"
2. 提取版本上线日期：20260305 / 当天 / 20260305
3. 如果是中文，翻译为英文："add inspection feature"
4. 转换为 kebab-case："add-inspection-feature"
5. 生成分支名："feature/20260305/add-inspection-feature"
6. 执行脚本创建分支

脚本用法：
```bash
# 使用当天日期
python create_feature_branch.py "add inspection feature"

# 使用指定版本上线日期
python create_feature_branch.py "add inspection feature" 20260305
```

## Resources

- `scripts/create_feature_branch.py`: 创建 feature 分支的脚本，接收变更描述作为参数

## Implementation Notes

- 脚本会自动处理 release 分支的检出和更新
- 如果本地没有 release 分支，会从远程拉取
- 创建的分支会自动推送到远程
- 中文描述需要由 AI 翻译为英文后再处理
