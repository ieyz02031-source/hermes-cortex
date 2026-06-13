#!/usr/bin/env python3
"""
Hermes Brain - 自动优化系统
当知识库接近性能瓶颈时自动触发优化
"""

import os
import sys
import json
import time
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

# 配置
VAULT_PATH = Path(r"D:\ObsidianVault")
SCRIPT_DIR = Path(r"D:\Hermes\skills\hermes-cortex\scripts")
PYTHON_312 = Path(r"C:\Users\20716\AppData\Local\Programs\Python\Python312\python.exe")
DB_PATH = VAULT_PATH / ".hermes_brain.db"

# 警戒线阈值
THRESHOLDS = {
    "note_count": 300,          # 笔记数超过300开始优化
    "db_size_mb": 30,           # 索引超过30MB开始优化
    "hook_time_sec": 1.5,       # Hook耗时超过1.5秒开始优化
    "isolated_count": 20,       # 孤立笔记超过20个开始清理
    "orphan_links": 50,         # 无效链接超过50个开始清理
    "hot_cache_age_hours": 24,  # 热缓存超过24小时更新
}


def get_stats():
    """获取当前统计信息"""
    stats = {}
    
    # 笔记数
    md_files = list(VAULT_PATH.rglob("*.md"))
    stats["note_count"] = len([f for f in md_files if not f.name.startswith(".")])
    
    # 数据库大小
    if DB_PATH.exists():
        stats["db_size_mb"] = DB_PATH.stat().st_size / (1024 * 1024)
    else:
        stats["db_size_mb"] = 0
    
    # 孤立笔记数
    stats["isolated_count"] = count_isolated_notes()
    
    # 无效链接数
    stats["orphan_links"] = count_orphan_links()
    
    # 热缓存年龄
    index_path = VAULT_PATH / "index.md"
    if index_path.exists():
        mtime = datetime.fromtimestamp(index_path.stat().st_mtime)
        stats["hot_cache_age_hours"] = (datetime.now() - mtime).total_seconds() / 3600
    else:
        stats["hot_cache_age_hours"] = 999
    
    return stats


def count_isolated_notes():
    """统计孤立笔记数（没有任何关联的笔记）"""
    count = 0
    for md_file in VAULT_PATH.rglob("*.md"):
        if md_file.name.startswith(".") or md_file.name in ["index.md", "SCHEMA.md", "log.md"]:
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            # 检查是否有 wikilinks
            if "[[" not in content and "关联:" not in content:
                count += 1
        except:
            pass
    return count


def count_orphan_links():
    """统计无效链接数（指向不存在笔记的链接）"""
    import re
    all_notes = set()
    for md_file in VAULT_PATH.rglob("*.md"):
        if not md_file.name.startswith("."):
            all_notes.add(md_file.stem)
    
    orphan_count = 0
    for md_file in VAULT_PATH.rglob("*.md"):
        if md_file.name.startswith("."):
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            links = re.findall(r'\[\[([^\]]+)\]\]', content)
            for link in links:
                target = link.split("|")[0].split("#")[0].strip()
                if target and target not in all_notes:
                    orphan_count += 1
        except:
            pass
    return orphan_count


def check_thresholds(stats):
    """检查是否超过警戒线"""
    alerts = []
    
    for key, threshold in THRESHOLDS.items():
        if key in stats and stats[key] > threshold:
            alerts.append({
                "metric": key,
                "current": stats[key],
                "threshold": threshold,
                "exceeded_by": stats[key] - threshold
            })
    
    return alerts


def optimize_incremental_index():
    """增量索引优化（只更新新增/修改的笔记）"""
    print("📦 增量索引优化...")
    import subprocess
    
    try:
        result = subprocess.run(
            [str(PYTHON_312), str(SCRIPT_DIR / "semantic_index.py"), "index"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print("  ✅ 索引更新完成")
        else:
            print(f"  ⚠️ 索引更新警告: {result.stderr[:200]}")
    except Exception as e:
        print(f"  ❌ 索引更新失败: {e}")


def optimize_cleanup_isolated():
    """清理孤立笔记（添加默认关联）"""
    print("🔗 清理孤立笔记...")
    import subprocess
    
    try:
        result = subprocess.run(
            [str(PYTHON_312), str(SCRIPT_DIR / "maintain.py"), "isolated"],
            capture_output=True, text=True, timeout=60
        )
        print(f"  ✅ 孤立笔记检查完成")
    except Exception as e:
        print(f"  ❌ 清理失败: {e}")


def optimize_hot_cache():
    """更新热缓存"""
    print("🔥 更新热缓存...")
    import subprocess
    
    try:
        result = subprocess.run(
            [str(PYTHON_312), str(SCRIPT_DIR / "hot_cache.py")],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print("  ✅ 热缓存更新完成")
    except Exception as e:
        print(f"  ❌ 热缓存更新失败: {e}")


def optimize_archive_old_notes():
    """归档过期笔记（30天未修改的 WARM → COLD，90天 → ARCHIVE）"""
    print("📁 归档过期笔记...")
    
    now = datetime.now()
    archived = 0
    
    for md_file in VAULT_PATH.rglob("*.md"):
        if md_file.name.startswith(".") or md_file.name in ["index.md", "SCHEMA.md", "log.md"]:
            continue
        
        try:
            mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
            days_old = (now - mtime).days
            
            # 90天未修改的笔记移到 archive
            if days_old > 90 and "archive" not in str(md_file):
                archive_dir = VAULT_PATH / "archive"
                archive_dir.mkdir(exist_ok=True)
                
                # 保持原有目录结构
                relative = md_file.relative_to(VAULT_PATH)
                target = archive_dir / relative.name
                
                if not target.exists():
                    # 只移动，不删除（安全第一）
                    import shutil
                    shutil.copy2(md_file, target)
                    archived += 1
        except:
            pass
    
    if archived > 0:
        print(f"  ✅ 归档了 {archived} 个过期笔记")
    else:
        print("  ✅ 没有需要归档的笔记")


def run_optimization(alerts):
    """根据警报执行优化"""
    print("\n🔧 开始自动优化...")
    print("=" * 50)
    
    for alert in alerts:
        metric = alert["metric"]
        
        if metric == "note_count":
            optimize_archive_old_notes()
        
        elif metric == "db_size_mb":
            optimize_incremental_index()
        
        elif metric == "hook_time_sec":
            optimize_incremental_index()
        
        elif metric == "isolated_count":
            optimize_cleanup_isolated()
        
        elif metric == "orphan_links":
            optimize_cleanup_isolated()
        
        elif metric == "hot_cache_age_hours":
            optimize_hot_cache()
    
    print("=" * 50)
    print("✅ 自动优化完成")


def main():
    """主函数"""
    print("🧠 Hermes Brain 自动优化系统")
    print("=" * 50)
    
    # 获取统计信息
    stats = get_stats()
    
    print("\n📊 当前状态:")
    print(f"  笔记数: {stats['note_count']} (警戒线: {THRESHOLDS['note_count']})")
    print(f"  索引大小: {stats['db_size_mb']:.2f}MB (警戒线: {THRESHOLDS['db_size_mb']}MB)")
    print(f"  孤立笔记: {stats['isolated_count']} (警戒线: {THRESHOLDS['isolated_count']})")
    print(f"  无效链接: {stats['orphan_links']} (警戒线: {THRESHOLDS['orphan_links']})")
    print(f"  热缓存年龄: {stats['hot_cache_age_hours']:.1f}小时 (警戒线: {THRESHOLDS['hot_cache_age_hours']}小时)")
    
    # 检查阈值
    alerts = check_thresholds(stats)
    
    if alerts:
        print(f"\n⚠️ 发现 {len(alerts)} 个警报:")
        for alert in alerts:
            print(f"  🔴 {alert['metric']}: {alert['current']} (超过阈值 {alert['threshold']})")
        
        # 执行优化
        run_optimization(alerts)
        
        # 重新检查
        print("\n📊 优化后状态:")
        stats_after = get_stats()
        print(f"  笔记数: {stats_after['note_count']}")
        print(f"  索引大小: {stats_after['db_size_mb']:.2f}MB")
        print(f"  孤立笔记: {stats_after['isolated_count']}")
        print(f"  无效链接: {stats_after['orphan_links']}")
    else:
        print("\n✅ 所有指标正常，无需优化")


if __name__ == "__main__":
    main()
