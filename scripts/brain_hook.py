#!/usr/bin/env python3
"""
Hermes Brain - 自动化 Hook
在每次对话结束时自动运行，更新热缓存和索引
"""
import os
import sys
import subprocess
import time
from pathlib import Path

# 配置
SKILL_DIR = Path(r"D:\Hermes\skills\hermes-cortex")
SCRIPTS_DIR = SKILL_DIR / "scripts"
VAULT_DIR = Path(r"D:\ObsidianVault")
PYTHON_312 = Path(r"C:\Users\20716\AppData\Local\Programs\Python\Python312\python.exe")

# 优化检查频率（每 N 次对话检查一次）
OPTIMIZE_CHECK_INTERVAL = 10
COUNTER_FILE = VAULT_DIR / ".hermes_brain_counter"


def get_counter():
    """获取对话计数器"""
    try:
        if COUNTER_FILE.exists():
            return int(COUNTER_FILE.read_text().strip())
    except:
        pass
    return 0


def increment_counter():
    """递增计数器"""
    count = get_counter() + 1
    COUNTER_FILE.write_text(str(count))
    return count


def run_script(script_name, args=None, timeout=60):
    """运行脚本"""
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        return False
    
    cmd = [str(PYTHON_312), str(script_path)]
    if args:
        cmd.extend(args)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0
    except:
        return False


def main():
    """主函数：自动运行 Hermes Brain 的关键任务"""
    # 1. 更新热缓存
    run_script("hot_cache.py")
    
    # 2. 更新语义索引（每天只运行一次）
    index_file = VAULT_DIR / ".hermes_brain.db"
    if index_file.exists():
        last_modified = index_file.stat().st_mtime
        hours_since_update = (time.time() - last_modified) / 3600
        
        if hours_since_update > 24:
            run_script("semantic_index.py", ["index"], timeout=120)
    else:
        run_script("semantic_index.py", ["index"], timeout=120)
    
    # 3. 检查孤立笔记
    run_script("maintain.py", ["isolated"])
    
    # 4. 定期执行自动优化（每 10 次对话检查一次）
    count = increment_counter()
    if count % OPTIMIZE_CHECK_INTERVAL == 0:
        run_script("auto_optimize.py", timeout=180)


if __name__ == "__main__":
    main()
