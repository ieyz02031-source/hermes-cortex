#!/usr/bin/env python3
"""
记忆分类标签系统
给记忆打标签，按主题分类
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 记忆标签定义
MEMORY_TAGS = {
    # 设计相关
    "design": {
        "name": "设计",
        "description": "设计相关知识",
        "keywords": ["design", "vibe", "taste", "luxury", "style", "ui", "ux"]
    },
    "workflow": {
        "name": "工作流",
        "description": "工作流程和方法",
        "keywords": ["workflow", "process", "method", "pipeline"]
    },
    "tool": {
        "name": "工具",
        "description": "工具和集成",
        "keywords": ["tool", "integration", "mcp", "engram", "wechat"]
    },
    "system": {
        "name": "系统",
        "description": "系统配置和优化",
        "keywords": ["system", "config", "optimization", "cleanup"]
    },
    "memory": {
        "name": "记忆",
        "description": "记忆系统相关",
        "keywords": ["memory", "engram", "search", "storage"]
    }
}

# 记忆数据库（模拟）
MEMORY_DB = [
    {
        "id": 1,
        "title": "VIBE_CODING_WORKFLOW",
        "content": "Vibe Coding工作流：AWWWWARDS研究→designprompts.dev选风格→CSS变量→写代码",
        "tags": ["design", "workflow"],
        "priority": "high"
    },
    {
        "id": 2,
        "title": "Taste Critic Rules",
        "content": "taste_critic.py 36条反模式规则，暗色主题默认用暖色",
        "tags": ["design", "quality"],
        "priority": "high"
    },
    {
        "id": 3,
        "title": "Luxury vs Tech Design Patterns",
        "content": "高端设计两种模式：奢侈品极简和暖灰企业沉浸式",
        "tags": ["design", "luxury"],
        "priority": "high"
    },
    {
        "id": 4,
        "title": "WeChat Integration",
        "content": "微信已对接Hermes，发送消息：hermes send --to weixin",
        "tags": ["tool", "integration"],
        "priority": "medium"
    },
    {
        "id": 5,
        "title": "Skill Cleanup Completed",
        "content": "技能清理完成，从117个清理到44个",
        "tags": ["system", "cleanup"],
        "priority": "medium"
    },
    {
        "id": 6,
        "title": "Memory System Optimization Complete",
        "content": "三层记忆架构优化完成：Hot(memory) + Warm(engram) + Cold(Obsidian)",
        "tags": ["memory", "system"],
        "priority": "high"
    }
]

def classify_memory(memory):
    """自动分类记忆"""
    content_lower = memory["content"].lower()
    title_lower = memory["title"].lower()
    
    matched_tags = []
    for tag, tag_info in MEMORY_TAGS.items():
        for keyword in tag_info["keywords"]:
            if keyword in content_lower or keyword in title_lower:
                if tag not in matched_tags:
                    matched_tags.append(tag)
                break
    
    return matched_tags

def search_by_tag(tag, memories):
    """按标签搜索记忆"""
    results = []
    for mem in memories:
        if tag in mem["tags"]:
            results.append(mem)
    return results

def search_by_priority(priority, memories):
    """按优先级搜索记忆"""
    results = []
    for mem in memories:
        if mem["priority"] == priority:
            results.append(mem)
    return results

def generate_tag_report(memories):
    """生成标签报告"""
    report = f"""
=== 记忆分类标签报告 ===
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

标签定义:
"""
    
    for tag, tag_info in MEMORY_TAGS.items():
        report += f"  - {tag}: {tag_info['name']} ({tag_info['description']})\n"
    
    report += f"\n记忆分类:\n"
    
    for mem in memories:
        report += f"  - {mem['title']}: {', '.join(mem['tags'])} (优先级: {mem['priority']})\n"
    
    report += f"\n按标签统计:\n"
    
    tag_counts = {}
    for mem in memories:
        for tag in mem["tags"]:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    for tag, count in sorted(tag_counts.items()):
        report += f"  - {tag}: {count}个记忆\n"
    
    report += f"\n按优先级统计:\n"
    
    priority_counts = {}
    for mem in memories:
        priority_counts[mem["priority"]] = priority_counts.get(mem["priority"], 0) + 1
    
    for priority, count in sorted(priority_counts.items()):
        report += f"  - {priority}: {count}个记忆\n"
    
    return report

def main():
    print("=== 记忆分类标签系统 ===")
    print(f"开始时间: {datetime.now()}")
    print()
    
    # 1. 自动分类
    print("1. 自动分类记忆...")
    for mem in MEMORY_DB:
        auto_tags = classify_memory(mem)
        print(f"  - {mem['title']}: {auto_tags}")
    print()
    
    # 2. 按标签搜索
    print("2. 按标签搜索...")
    for tag in ["design", "tool", "system", "memory"]:
        results = search_by_tag(tag, MEMORY_DB)
        print(f"  - {tag}: {len(results)}个记忆")
        for r in results:
            print(f"    * {r['title']}")
    print()
    
    # 3. 按优先级搜索
    print("3. 按优先级搜索...")
    for priority in ["high", "medium", "low"]:
        results = search_by_priority(priority, MEMORY_DB)
        print(f"  - {priority}: {len(results)}个记忆")
        for r in results:
            print(f"    * {r['title']}")
    print()
    
    # 4. 生成报告
    print("4. 生成标签报告...")
    report = generate_tag_report(MEMORY_DB)
    print(report)
    
    # 5. 保存报告
    report_path = Path("D:/Hermes/skills/hermes-cortex/reports")
    report_path.mkdir(exist_ok=True)
    report_file = report_path / f"memory_tags_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"报告已保存: {report_file}")

if __name__ == "__main__":
    main()
