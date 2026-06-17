#!/usr/bin/env python3
"""
Hermes Cortex 验证脚本
检查 Harness 的 5 个子系统是否正常工作
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

# 路径配置
SKILL_DIR = Path("D:/Hermes/skills/hermes-cortex")
VAULT_DIR = Path("D:/ObsidianVault")

def check_instructions():
    """检查 Instructions 子系统"""
    print("📋 检查 Instructions...")
    
    checks = []
    
    # 检查 SKILL.md
    skill_file = SKILL_DIR / "SKILL.md"
    if skill_file.exists():
        size = skill_file.stat().st_size
        checks.append(("SKILL.md", True, f"{size} bytes"))
    else:
        checks.append(("SKILL.md", False, "不存在"))
    
    # 检查 SOUL.md
    soul_file = Path.home() / ".hermes" / "SOUL.md"
    if soul_file.exists():
        checks.append(("SOUL.md", True, "存在"))
    else:
        checks.append(("SOUL.md", False, "不存在"))
    
    return checks

def check_state():
    """检查 State 子系统"""
    print("📊 检查 State...")
    
    checks = []
    
    # 检查 progress.md
    progress_file = SKILL_DIR / "progress.md"
    if progress_file.exists():
        checks.append(("progress.md", True, "存在"))
    else:
        checks.append(("progress.md", False, "不存在"))
    
    # 检查 feature_list.json
    feature_file = SKILL_DIR / "feature_list.json"
    if feature_file.exists():
        with open(feature_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        total = len(data.get('features', []))
        done = sum(1 for f in data.get('features', []) if f.get('status') == 'done')
        checks.append(("feature_list.json", True, f"{done}/{total} 完成"))
    else:
        checks.append(("feature_list.json", False, "不存在"))
    
    # 检查热缓存
    index_file = VAULT_DIR / "index.md"
    if index_file.exists():
        checks.append(("热缓存", True, "存在"))
    else:
        checks.append(("热缓存", False, "不存在"))
    
    # 检查数据库
    db_file = VAULT_DIR / ".hermes_brain.db"
    if db_file.exists():
        size = db_file.stat().st_size
        checks.append(("语义索引", True, f"{size/1024:.1f} KB"))
    else:
        checks.append(("语义索引", False, "不存在"))
    
    return checks

def check_verification():
    """检查 Verification 子系统"""
    print("✅ 检查 Verification...")
    
    checks = []
    
    # 检查 auto_optimize.py
    optimize_file = SKILL_DIR / "scripts" / "auto_optimize.py"
    if optimize_file.exists():
        checks.append(("auto_optimize.py", True, "存在"))
    else:
        checks.append(("auto_optimize.py", False, "不存在"))
    
    # 检查 maintain.py
    maintain_file = SKILL_DIR / "scripts" / "maintain.py"
    if maintain_file.exists():
        checks.append(("maintain.py", True, "存在"))
    else:
        checks.append(("maintain.py", False, "不存在"))
    
    return checks

def check_scope():
    """检查 Scope 子系统"""
    print("🎯 检查 Scope...")
    
    checks = []
    
    # 检查 feature_list.json 中的范围定义
    feature_file = SKILL_DIR / "feature_list.json"
    if feature_file.exists():
        with open(feature_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查是否有未完成的功能
        in_progress = [f for f in data.get('features', []) if f.get('status') == 'in_progress']
        if in_progress:
            checks.append(("范围控制", True, f"{len(in_progress)} 个进行中"))
        else:
            checks.append(("范围控制", True, "全部完成"))
    else:
        checks.append(("范围控制", False, "feature_list.json 不存在"))
    
    return checks

def check_lifecycle():
    """检查 Session Lifecycle 子系统"""
    print("🔄 检查 Session Lifecycle...")
    
    checks = []
    
    # 检查 init.sh
    init_file = SKILL_DIR / "init.sh"
    if init_file.exists():
        checks.append(("init.sh", True, "存在"))
    else:
        checks.append(("init.sh", False, "不存在"))
    
    # 检查 Shell Hooks
    hook_start = SKILL_DIR / "scripts" / "hook_session_start.py"
    hook_end = SKILL_DIR / "scripts" / "hook_session_end.py"
    if hook_start.exists() and hook_end.exists():
        checks.append(("Shell Hooks", True, "存在"))
    else:
        checks.append(("Shell Hooks", False, "不完整"))
    
    return checks

def run_verification():
    """运行完整验证"""
    print("=" * 60)
    print("🧠 Hermes Cortex Harness 验证")
    print("=" * 60)
    print()
    
    all_checks = []
    
    # 运行所有检查
    all_checks.extend(check_instructions())
    all_checks.extend(check_state())
    all_checks.extend(check_verification())
    all_checks.extend(check_scope())
    all_checks.extend(check_lifecycle())
    
    # 统计结果
    passed = sum(1 for _, ok, _ in all_checks if ok)
    failed = sum(1 for _, ok, _ in all_checks if not ok)
    total = len(all_checks)
    
    # 输出结果
    print()
    for name, ok, detail in all_checks:
        status = "✅" if ok else "❌"
        print(f"  {status} {name}: {detail}")
    
    print()
    print("=" * 60)
    print(f"📊 结果: {passed}/{total} 通过")
    
    if failed > 0:
        print(f"⚠️ {failed} 项未通过")
        return False
    else:
        print("✅ 全部通过！Harness 正常工作")
        return True

if __name__ == "__main__":
    success = run_verification()
    exit(0 if success else 1)
