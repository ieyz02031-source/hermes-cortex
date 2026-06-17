#!/usr/bin/env python3
"""
记忆衰减系统
基于访问频率和时间衰减记忆权重
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 衰减配置
DECAY_CONFIG = {
    "high_frequency": {"days": 7, "weight": 1.0},    # 高频：7天内访问，权重100%
    "medium_frequency": {"days": 30, "weight": 0.7},  # 中频：30天内访问，权重70%
    "low_frequency": {"days": 90, "weight": 0.3},     # 低频：90天内访问，权重30%
    "stale": {"days": 90, "weight": 0.1}              # 过时：超过90天，权重10%
}

def get_memory_access_stats():
    """获取记忆访问统计"""
    # 这里应该从engram获取记忆的访问时间
    # 简化版本：返回模拟数据
    return [
        {"id": 1, "title": "VIBE_CODING_WORKFLOW", "last_accessed": "2026-06-14", "access_count": 15},
        {"id": 2, "title": "Taste Critic Rules", "last_accessed": "2026-06-14", "access_count": 10},
        {"id": 3, "title": "Skill Cleanup Completed", "last_accessed": "2026-06-10", "access_count": 5},
        {"id": 4, "title": "SOUL.md Compression", "last_accessed": "2026-06-12", "access_count": 3},
        {"id": 5, "title": "NVIDIA NIM API", "last_accessed": "2026-06-01", "access_count": 1},
    ]

def calculate_decay_weight(last_accessed_str):
    """计算衰减权重"""
    try:
        last_accessed = datetime.strptime(last_accessed_str, "%Y-%m-%d")
        days_since = (datetime.now() - last_accessed).days
        
        if days_since <= DECAY_CONFIG["high_frequency"]["days"]:
            return DECAY_CONFIG["high_frequency"]["weight"]
        elif days_since <= DECAY_CONFIG["medium_frequency"]["days"]:
            return DECAY_CONFIG["medium_frequency"]["weight"]
        elif days_since <= DECAY_CONFIG["low_frequency"]["days"]:
            return DECAY_CONFIG["low_frequency"]["weight"]
        else:
            return DECAY_CONFIG["stale"]["weight"]
    except:
        return 0.5  # 默认权重

def apply_decay_to_memories():
    """应用衰减到记忆"""
    memories = get_memory_access_stats()
    decayed_memories = []
    
    for mem in memories:
        weight = calculate_decay_weight(mem["last_accessed"])
        decayed_memories.append({
            **mem,
            "decay_weight": weight,
            "status": "active" if weight > 0.3 else "stale"
        })
    
    return decayed_memories

def generate_decay_report(decayed_memories):
    """生成衰减报告"""
    report = f"""
=== 记忆衰减报告 ===
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

衰减配置:
- 高频 (7天内): 权重 100%
- 中频 (30天内): 权重 70%
- 低频 (90天内): 权重 30%
- 过时 (90天+): 权重 10%

记忆状态:
"""
    
    active_count = 0
    stale_count = 0
    
    for mem in decayed_memories:
        status_icon = "✓" if mem["status"] == "active" else "⚠"
        report += f"  {status_icon} {mem['title']}: 权重 {mem['decay_weight']:.1%} ({mem['status']})\n"
        
        if mem["status"] == "active":
            active_count += 1
        else:
            stale_count += 1
    
    report += f"""
统计:
- 活跃记忆: {active_count}
- 过时记忆: {stale_count}
- 总计: {len(decayed_memories)}

建议:
- 活跃记忆: 保持在memory中
- 过时记忆: 考虑迁移到engram或Obsidian
"""
    
    return report

def main():
    print("=== 记忆衰减系统 ===")
    print(f"开始时间: {datetime.now()}")
    print()
    
    # 1. 应用衰减
    print("1. 计算记忆衰减权重...")
    decayed_memories = apply_decay_to_memories()
    print(f"   处理了 {len(decayed_memories)} 个记忆")
    print()
    
    # 2. 生成报告
    print("2. 生成衰减报告...")
    report = generate_decay_report(decayed_memories)
    print(report)
    
    # 3. 保存报告
    report_path = Path("D:/Hermes/skills/hermes-cortex/reports")
    report_path.mkdir(exist_ok=True)
    report_file = report_path / f"memory_decay_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"报告已保存: {report_file}")

if __name__ == "__main__":
    main()
