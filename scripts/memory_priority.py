#!/usr/bin/env python3
"""
记忆优先级系统
给记忆设置优先级，重要记忆优先显示
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 优先级定义
PRIORITY_LEVELS = {
    "high": {
        "name": "高",
        "description": "核心规则、用户偏好",
        "weight": 1.0,
        "auto_inject": True
    },
    "medium": {
        "name": "中",
        "description": "项目详情、技术文档",
        "weight": 0.7,
        "auto_inject": False
    },
    "low": {
        "name": "低",
        "description": "历史记录、临时信息",
        "weight": 0.3,
        "auto_inject": False
    }
}

# 记忆数据库（模拟）
MEMORY_DB = [
    {
        "id": 1,
        "title": "WORKFLOW_NO_BLIND_ACTION",
        "content": "干活遇到不会不要盲目干别瞎编",
        "priority": "high",
        "tags": ["system", "workflow"]
    },
    {
        "id": 2,
        "title": "VIBE_CODING_WORKFLOW",
        "content": "Vibe Coding工作流",
        "priority": "high",
        "tags": ["design", "workflow"]
    },
    {
        "id": 3,
        "title": "Taste Critic Rules",
        "content": "taste_critic.py 36条反模式规则",
        "priority": "high",
        "tags": ["design", "quality"]
    },
    {
        "id": 4,
        "title": "WeChat Integration",
        "content": "微信已对接Hermes",
        "priority": "medium",
        "tags": ["tool", "integration"]
    },
    {
        "id": 5,
        "title": "Skill Cleanup Completed",
        "content": "技能清理完成",
        "priority": "medium",
        "tags": ["system", "cleanup"]
    },
    {
        "id": 6,
        "title": "Test Save",
        "content": "测试记忆",
        "priority": "low",
        "tags": ["test"]
    }
]

def search_by_priority(priority, memories):
    """按优先级搜索记忆"""
    results = []
    for mem in memories:
        if mem["priority"] == priority:
            results.append(mem)
    return results

def get_auto_inject_memories(memories):
    """获取自动注入的记忆（高优先级）"""
    results = []
    for mem in memories:
        if mem["priority"] == "high":
            results.append(mem)
    return results

def calculate_priority_score(memory):
    """计算优先级分数"""
    priority_info = PRIORITY_LEVELS.get(memory["priority"], PRIORITY_LEVELS["medium"])
    return priority_info["weight"]

def generate_priority_report(memories):
    """生成优先级报告"""
    report = f"""
=== 记忆优先级报告 ===
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

优先级定义:
"""
    
    for priority, info in PRIORITY_LEVELS.items():
        report += f"  - {priority}: {info['name']} ({info['description']})\n"
        report += f"    权重: {info['weight']}, 自动注入: {info['auto_inject']}\n"
    
    report += f"\n记忆优先级:\n"
    
    for mem in memories:
        priority_info = PRIORITY_LEVELS.get(mem["priority"], PRIORITY_LEVELS["medium"])
        report += f"  - {mem['title']}: {priority_info['name']} (权重: {priority_info['weight']})\n"
    
    report += f"\n按优先级统计:\n"
    
    priority_counts = {}
    for mem in memories:
        priority_counts[mem["priority"]] = priority_counts.get(mem["priority"], 0) + 1
    
    for priority, count in sorted(priority_counts.items()):
        priority_info = PRIORITY_LEVELS.get(priority, PRIORITY_LEVELS["medium"])
        report += f"  - {priority_info['name']}: {count}个记忆\n"
    
    report += f"\n自动注入的记忆（高优先级）:\n"
    
    auto_inject = get_auto_inject_memories(memories)
    for mem in auto_inject:
        report += f"  - {mem['title']}\n"
    
    return report

def main():
    print("=== 记忆优先级系统 ===")
    print(f"开始时间: {datetime.now()}")
    print()
    
    # 1. 按优先级搜索
    print("1. 按优先级搜索...")
    for priority in ["high", "medium", "low"]:
        results = search_by_priority(priority, MEMORY_DB)
        print(f"  - {priority}: {len(results)}个记忆")
        for r in results:
            print(f"    * {r['title']}")
    print()
    
    # 2. 获取自动注入的记忆
    print("2. 获取自动注入的记忆...")
    auto_inject = get_auto_inject_memories(MEMORY_DB)
    print(f"  - 自动注入: {len(auto_inject)}个记忆")
    for mem in auto_inject:
        print(f"    * {mem['title']}")
    print()
    
    # 3. 计算优先级分数
    print("3. 计算优先级分数...")
    for mem in MEMORY_DB:
        score = calculate_priority_score(mem)
        print(f"  - {mem['title']}: {score}")
    print()
    
    # 4. 生成报告
    print("4. 生成优先级报告...")
    report = generate_priority_report(MEMORY_DB)
    print(report)
    
    # 5. 保存报告
    report_path = Path("D:/Hermes/skills/hermes-cortex/reports")
    report_path.mkdir(exist_ok=True)
    report_file = report_path / f"memory_priority_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"报告已保存: {report_file}")

if __name__ == "__main__":
    main()
