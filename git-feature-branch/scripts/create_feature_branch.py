#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建 feature 分支的脚本

用法:
    python create_feature_branch.py <变更描述> [日期]

示例:
    python create_feature_branch.py "新增巡检功能"
    python create_feature_branch.py "新增巡检功能" 20260305
    python create_feature_branch.py "fix memory leak" 20260305
"""

import subprocess
import sys
from datetime import datetime


def run_command(cmd, check=True):
    """运行 shell 命令并返回输出"""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        check=check
    )
    return result


def get_current_date():
    """获取当前日期，格式 YYYYMMDD"""
    return datetime.now().strftime('%Y%m%d')


def to_kebab_case(text):
    """
    将文本转换为短横线连接的小写格式
    如果是中文，需要调用 AI 翻译后再转换
    """
    # 简单处理：替换空格和特殊字符为短横线，转小写
    import re
    # 将非字母数字字符替换为短横线
    text = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]+', '-', text)
    # 移除首尾短横线
    text = text.strip('-')
    return text.lower()


def create_feature_branch(description, date_str=None):
    """创建 feature 分支"""
    if not date_str:
        date_str = get_current_date()
    
    # 转换描述为 kebab-case
    feature_name = to_kebab_case(description)
    
    # 构建分支名
    branch_name = f'feature/{date_str}/{feature_name}'
    
    print(f'准备创建分支: {branch_name}')
    
    # 检查当前是否在 git 仓库中
    result = run_command('git rev-parse --git-dir', check=False)
    if result.returncode != 0:
        print('错误: 当前目录不是 git 仓库')
        sys.exit(1)
    
    # 获取远程名称
    result = run_command('git remote', check=False)
    remotes = result.stdout.strip().split('\n') if result.stdout else []
    remote = remotes[0] if remotes else 'origin'
    
    # 检查 release 分支是否存在
    result = run_command('git branch -a', check=False)
    branches = result.stdout
    
    has_local_release = 'release' in branches
    has_remote_release = f'remotes/{remote}/release' in branches
    
    if not has_local_release and not has_remote_release:
        print('错误: 未找到 release 分支')
        sys.exit(1)
    
    # 确保本地 release 分支是最新的
    if has_local_release:
        print('切换到 release 分支...')
        run_command('git checkout release')
        if has_remote_release:
            print('拉取最新的 release 分支...')
            run_command(f'git pull {remote} release')
    else:
        print('从远程拉取 release 分支...')
        run_command(f'git checkout -b release {remote}/release')
    
    # 创建 feature 分支
    print(f'创建 feature 分支: {branch_name}')
    run_command(f'git checkout -b {branch_name}')
    
    # 推送到远程
    print(f'推送到远程: {remote}')
    run_command(f'git push -u {remote} {branch_name}')
    
    print(f'\n✅ 分支创建成功: {branch_name}')
    return branch_name


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python create_feature_branch.py <变更描述> [日期]')
        print('示例:')
        print('  python create_feature_branch.py "新增巡检功能"')
        print('  python create_feature_branch.py "新增巡检功能" 20260305')
        sys.exit(1)

    # 检查最后一个参数是否为日期格式（8位数字）
    date_str = None
    description_args = sys.argv[1:]

    if len(description_args) >= 2:
        last_arg = description_args[-1]
        # 检查是否为纯数字且长度为8（日期格式）
        if last_arg.isdigit() and len(last_arg) == 8:
            date_str = last_arg
            description = ' '.join(description_args[:-1])
        else:
            description = ' '.join(description_args)
    else:
        description = ' '.join(description_args)

    create_feature_branch(description, date_str)
