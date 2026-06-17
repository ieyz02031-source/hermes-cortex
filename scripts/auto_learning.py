#!/usr/bin/env python3
"""
自动学习系统
从对话中自动提取记忆
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 对话示例
SAMPLE_CONVERSATIONS = [
    {
        "id": 1,
        "user": "我喜欢浅色主题，白底+蓝色强调",
        "assistant": "好的，我会记住你的设计偏好",
        "extracted_memories": [
            {
                "key": "USER_PREF_LIGHT_THEME",
                "content": "用户偏好浅色主题：白底+蓝色强调",
                "type": "preference"
            }
        ]
    },
    {
        "id": 2,
        "user": "不要用深色背景，太丑了",
        "assistant": "明白，我会避免使用深色背景",
        "extracted_memories": [
            {
                "key": "USER_PREF_NO_DARK_BG",
                "content": "用户拒绝深色背景",
                "type": "preference"
            }
        ]
    },
    {
        "id": 3,
        "user": "参考Cartier的风格做高端网站",
        "assistant": "好的，我会参考Cartier的设计风格",
        "extracted_memories": [
            {
                "key": "DESIGN_REF_CARTIER",
                "content": "高端网站设计参考Cartier风格",
                "type": "design"
            }
        ]
    }
]

def extract_memories_from_conversation(conversation):
    """从对话中提取记忆"""
    memories = []
    
    # 提取用户偏好
    user_text = conversation["user"].lower()
    
    # 检测偏好关键词
    preference_keywords = {
        "喜欢": "preference",
        "偏好": "preference",
        "不要": "rejection",
        "拒绝": "rejection",
        "参考": "reference",
        "用": "usage"
    }
    
    for keyword, memory_type in preference_keywords.items():
        if keyword in user_text:
            # 提取关键词后的内容
            idx = user_text.find(keyword)
            content = conversation["user"][idx:]
            
            memories.append({
                "key": f"AUTO_{memory_type.upper()}_{conversation['id']}",
                "content": content,
                "type": memory_type,
                "source": "auto_extract"
            })
    
    return memories

def save_memory_to_engram(memory):
    """保存记忆到engram"""
    try:
        # 构建engram请求
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "mem_save",
                "arguments": {
                    "title": memory["key"],
                    "content": f"**What**: {memory['content']}\n**Why**: 自动提取的用户偏好\n**Where**: 对话记录\n**Learned**: {memory['content']}",
                    "type": memory["type"],
                    "topic_key": memory["key"].lower()
                }
            },
            "id": 1
        }
        
        # 调用engram
        result = subprocess.run(
            ["D:/Hermes/tools/engram/engram.exe", "mcp", "--tools=agent"],
            input=json.dumps(request),
            capture_output=True,
            text=True,
            timeout=10,
            cwd="D:/Hermes/skills/hermes-cortex"
        )
        
        if result.returncode == 0 and result.stdout:
            response = json.loads(result.stdout)
            if "result" in response and not response.get("error"):
                return True
        
        return False
    except Exception as e:
        print(f"Error saving to engram: {e}")
        return False

def generate_learning_report(conversations, extracted_memories):
    """生成学习报告"""
    report = f"""
=== 自动学习报告 ===
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

对话分析:
"""
    
    for conv in conversations:
        report += f"\n对话 {conv['id']}:\n"
        report += f"  用户: {conv['user']}\n"
        report += f"  助手: {conv['assistant']}\n"
        
        memories = extract_memories_from_conversation(conv)
        if memories:
            report += f"  提取的记忆:\n"
            for mem in memories:
                report += f"    - {mem['key']}: {mem['content']}\n"
        else:
            report += f"  未提取到记忆\n"
    
    report += f"\n提取统计:\n"
    report += f"  - 总对话数: {len(conversations)}\n"
    report += f"  - 提取记忆数: {len(extracted_memories)}\n"
    
    return report

def main():
    print("=== 自动学习系统 ===")
    print(f"开始时间: {datetime.now()}")
    print()
    
    # 1. 分析对话
    print("1. 分析对话...")
    all_memories = []
    for conv in SAMPLE_CONVERSATIONS:
        memories = extract_memories_from_conversation(conv)
        all_memories.extend(memories)
        print(f"  - 对话 {conv['id']}: 提取了 {len(memories)} 个记忆")
    print()
    
    # 2. 保存记忆
    print("2. 保存记忆到engram...")
    saved_count = 0
    for mem in all_memories:
        if save_memory_to_engram(mem):
            print(f"  ✓ 保存成功: {mem['key']}")
            saved_count += 1
        else:
            print(f"  ✗ 保存失败: {mem['key']}")
    print()
    
    # 3. 生成报告
    print("3. 生成学习报告...")
    report = generate_learning_report(SAMPLE_CONVERSATIONS, all_memories)
    print(report)
    
    # 4. 保存报告
    report_path = Path("D:/Hermes/skills/hermes-cortex/reports")
    report_path.mkdir(exist_ok=True)
    report_file = report_path / f"auto_learning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"报告已保存: {report_file}")

if __name__ == "__main__":
    main()
