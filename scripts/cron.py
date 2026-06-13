#!/usr/bin/env python3
"""
Hermes 大脑系统 - Cron 任务

用法:
    python cron.py setup                  # 设置 cron 任务
    python cron.py remove                 # 移除 cron 任务
    python cron.py status                 # 查看 cron 状态
    python cron.py run                    # 手动运行一次

功能:
    1. 设置每天自动运行自进化循环
    2. 自动生成自进化报告
    3. 自动更新索引和热缓存
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime


# 配置
SCRIPT_DIR = Path(r"D:\Hermes\skills\hermes-cortex\scripts")
VAULT_PATH = Path(r"D:\ObsidianVault")
LOG_DIR = VAULT_PATH / ".hermes_logs"


def setup_cron():
    """设置 cron 任务"""
    print("⏰ 设置 cron 任务...")
    
    # 确保日志目录存在
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # 创建 cron 脚本
    cron_script = SCRIPT_DIR / "cron_task.sh"
    cron_script.write_text(f"""#!/bin/bash
# Hermes 大脑系统 - 自动自进化任务
# 运行时间: 每天晚上 9:00

cd {SCRIPT_DIR.parent}
python scripts/evolve.py run >> {LOG_DIR}/evolution.log 2>&1
python scripts/hot_cache.py >> {LOG_DIR}/hot_cache.log 2>&1
python scripts/semantic_index.py index >> {LOG_DIR}/index.log 2>&1
""", encoding='utf-8')
    
    # 使脚本可执行
    os.chmod(str(cron_script), 0o755)
    
    print(f"  ✅ Cron 脚本已创建: {cron_script}")
    print(f"  📝 日志目录: {LOG_DIR}")
    print(f"\n  请手动添加到 crontab:")
    print(f"  0 21 * * * {cron_script}")


def remove_cron():
    """移除 cron 任务"""
    print("🗑️ 移除 cron 任务...")
    
    cron_script = SCRIPT_DIR / "cron_task.sh"
    if cron_script.exists():
        cron_script.unlink()
        print(f"  ✅ Cron 脚本已删除: {cron_script}")
    else:
        print(f"  ⚠️ Cron 脚本不存在: {cron_script}")
    
    print(f"\n  请手动从 crontab 中移除:")
    print(f"  0 21 * * * {cron_script}")


def show_status():
    """显示 cron 状态"""
    print("⏰ Cron 状态:")
    
    cron_script = SCRIPT_DIR / "cron_task.sh"
    if cron_script.exists():
        print(f"  ✅ Cron 脚本存在: {cron_script}")
        
        # 检查日志
        log_files = list(LOG_DIR.glob("*.log")) if LOG_DIR.exists() else []
        if log_files:
            print(f"\n  📝 日志文件:")
            for log_file in log_files:
                size = log_file.stat().st_size
                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                print(f"    - {log_file.name}: {size} bytes, 最后更新: {mtime}")
        else:
            print(f"\n  📝 日志文件: 无")
    else:
        print(f"  ❌ Cron 脚本不存在")


def run_once():
    """手动运行一次"""
    print("🚀 手动运行自进化循环...")
    
    # 运行自进化循环
    os.system(f'cd {SCRIPT_DIR.parent} && python scripts/evolve.py run')
    
    # 更新热缓存
    print("\n🔥 更新热缓存...")
    os.system(f'cd {SCRIPT_DIR.parent} && python scripts/hot_cache.py')
    
    # 更新索引
    print("\n📦 更新索引...")
    os.system(f'cd {SCRIPT_DIR.parent} && python scripts/semantic_index.py index')
    
    print("\n✅ 手动运行完成")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python cron.py setup    # 设置 cron 任务")
        print("  python cron.py remove   # 移除 cron 任务")
        print("  python cron.py status   # 查看 cron 状态")
        print("  python cron.py run      # 手动运行一次")
        return
    
    command = sys.argv[1]
    
    if command == 'setup':
        setup_cron()
    elif command == 'remove':
        remove_cron()
    elif command == 'status':
        show_status()
    elif command == 'run':
        run_once()
    else:
        print(f"未知命令: {command}")


if __name__ == '__main__':
    main()
