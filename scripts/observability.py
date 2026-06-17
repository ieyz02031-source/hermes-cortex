#!/usr/bin/env python3
"""
简单可观测性脚本
分析 Hermes 日志，追踪成本和性能
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# 配置
LOGS_DIR = Path.home() / ".hermes" / "logs"
SESSIONS_DIR = Path.home() / ".hermes" / "sessions"

def analyze_session_logs():
    """分析 session 日志"""
    print("=" * 60)
    print("  Session 日志分析")
    print("=" * 60)
    print()
    
    if not SESSIONS_DIR.exists():
        print("❌ Session 目录不存在")
        return
    
    # 统计
    total_sessions = 0
    total_tokens = 0
    total_cost = 0
    model_usage = defaultdict(int)
    
    # 遍历 session 文件
    for session_file in SESSIONS_DIR.glob("*.json"):
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            total_sessions += 1
            
            # 提取 token 使用
            if 'usage' in data:
                usage = data['usage']
                total_tokens += usage.get('total_tokens', 0)
                total_cost += usage.get('total_cost', 0)
            
            # 提取模型使用
            if 'model' in data:
                model_usage[data['model']] += 1
                
        except Exception as e:
            pass
    
    print(f"📊 总览:")
    print(f"  - 总会话数: {total_sessions}")
    print(f"  - 总 token 数: {total_tokens:,}")
    print(f"  - 总成本: ${total_cost:.4f}")
    print()
    
    print(f"📈 模型使用:")
    for model, count in sorted(model_usage.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {model}: {count} 次")
    print()

def analyze_error_logs():
    """分析错误日志"""
    print("=" * 60)
    print("  错误日志分析")
    print("=" * 60)
    print()
    
    error_file = LOGS_DIR / "errors.log"
    if not error_file.exists():
        print("❌ 错误日志不存在")
        return
    
    # 统计错误类型
    error_types = defaultdict(int)
    total_errors = 0
    
    with open(error_file, 'r', encoding='utf-8') as f:
        for line in f:
            if 'ERROR' in line:
                total_errors += 1
                # 提取错误类型
                if 'ConnectionError' in line:
                    error_types['ConnectionError'] += 1
                elif 'TimeoutError' in line:
                    error_types['TimeoutError'] += 1
                elif 'APIError' in line:
                    error_types['APIError'] += 1
                else:
                    error_types['Other'] += 1
    
    print(f"📊 错误统计:")
    print(f"  - 总错误数: {total_errors}")
    print()
    
    print(f"📈 错误类型:")
    for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {error_type}: {count} 次")
    print()

def analyze_tool_usage():
    """分析工具使用"""
    print("=" * 60)
    print("  工具使用分析")
    print("=" * 60)
    print()
    
    # 遍历 session 文件
    tool_usage = defaultdict(int)
    total_tool_calls = 0
    
    for session_file in SESSIONS_DIR.glob("*.json"):
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 提取工具调用
            if 'messages' in data:
                for message in data['messages']:
                    if 'tool_calls' in message:
                        for tool_call in message['tool_calls']:
                            tool_name = tool_call.get('function', {}).get('name', 'unknown')
                            tool_usage[tool_name] += 1
                            total_tool_calls += 1
                            
        except Exception as e:
            pass
    
    print(f"📊 工具使用统计:")
    print(f"  - 总工具调用: {total_tool_calls}")
    print()
    
    print(f"📈 最常用工具:")
    for tool, count in sorted(tool_usage.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  - {tool}: {count} 次")
    print()

def generate_report():
    """生成报告"""
    print("=" * 60)
    print("  Hermes 可观测性报告")
    print(f"  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    analyze_session_logs()
    analyze_error_logs()
    analyze_tool_usage()
    
    print("=" * 60)
    print("  报告完成")
    print("=" * 60)

if __name__ == "__main__":
    generate_report()
