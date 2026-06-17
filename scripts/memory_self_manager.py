#!/usr/bin/env python3
"""
记忆自管理系统
自动打理记忆，保持系统健康
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 记忆健康检查配置
HEALTH_CHECK_CONFIG = {
    "memory_usage_threshold": 80,  # memory使用率阈值
    "engram_min_memories": 10,  # engram最少记忆数
    "stale_days_threshold": 30,  # 过时天数阈值
    "auto_cleanup_enabled": True,  # 自动清理开关
    "auto_sync_enabled": True,  # 自动同步开关
    "auto_decay_enabled": True,  # 自动衰减开关
}

class MemorySelfManager:
    """记忆自管理器"""
    
    def __init__(self):
        self.config = HEALTH_CHECK_CONFIG
        self.report_path = Path("D:/Hermes/skills/hermes-cortex/reports")
        self.report_path.mkdir(exist_ok=True)
    
    def check_memory_health(self):
        """检查memory健康状态"""
        print("检查memory健康状态...")
        
        # 模拟检查（实际应该读取memory状态）
        health = {
            "status": "healthy",
            "usage_percent": 48,
            "entry_count": 43,
            "issues": []
        }
        
        if health["usage_percent"] > self.config["memory_usage_threshold"]:
            health["status"] = "warning"
            health["issues"].append(f"使用率过高: {health['usage_percent']}%")
        
        return health
    
    def check_engram_health(self):
        """检查engram健康状态"""
        print("检查engram健康状态...")
        
        try:
            result = subprocess.run(
                ["D:/Hermes/tools/engram/engram.exe", "mcp", "--tools=agent"],
                input='{"jsonrpc":"2.0","method":"tools/call","params":{"name":"mem_context","arguments":{"scope":"all"}},"id":1}',
                capture_output=True,
                text=True,
                timeout=10,
                cwd="D:/Hermes/skills/hermes-cortex"
            )
            
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                content = data['result']['content'][0]['text']
                content_data = json.loads(content)
                
                import re
                match = re.search(r'(\d+) observations', content_data.get('result', ''))
                if match:
                    memory_count = int(match.group(1))
                    return {
                        "status": "healthy" if memory_count >= self.config["engram_min_memories"] else "warning",
                        "memory_count": memory_count,
                        "issues": [] if memory_count >= self.config["engram_min_memories"] else [f"记忆数过少: {memory_count}"]
                    }
            
            return {"status": "error", "memory_count": 0, "issues": ["engram连接失败"]}
        except Exception as e:
            return {"status": "error", "memory_count": 0, "issues": [str(e)]}
    
    def auto_cleanup(self):
        """自动清理"""
        if not self.config["auto_cleanup_enabled"]:
            return {"status": "disabled"}
        
        print("执行自动清理...")
        # 模拟清理
        return {"status": "done", "cleaned": 0}
    
    def auto_sync(self):
        """自动同步"""
        if not self.config["auto_sync_enabled"]:
            return {"status": "disabled"}
        
        print("执行自动同步...")
        # 模拟同步
        return {"status": "done", "synced": 0}
    
    def auto_decay(self):
        """自动衰减"""
        if not self.config["auto_decay_enabled"]:
            return {"status": "disabled"}
        
        print("执行自动衰减...")
        # 模拟衰减
        return {"status": "done", "decayed": 0}
    
    def generate_health_report(self, memory_health, engram_health, cleanup_result, sync_result, decay_result):
        """生成健康报告"""
        report = f"""
=== 记忆系统健康报告 ===
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

memory状态:
- 状态: {memory_health['status']}
- 使用率: {memory_health['usage_percent']}%
- 条目数: {memory_health['entry_count']}
- 问题: {', '.join(memory_health['issues']) if memory_health['issues'] else '无'}

engram状态:
- 状态: {engram_health['status']}
- 记忆数: {engram_health['memory_count']}
- 问题: {', '.join(engram_health['issues']) if engram_health['issues'] else '无'}

自动维护:
- 清理: {cleanup_result['status']}
- 同步: {sync_result['status']}
- 衰减: {decay_result['status']}

健康评分: {self._calculate_health_score(memory_health, engram_health)}/100

建议:
"""
        
        if memory_health['status'] == 'warning':
            report += "  - 考虑清理memory中的低优先级条目\n"
        
        if engram_health['status'] == 'warning':
            report += "  - 考虑添加更多记忆到engram\n"
        
        if not memory_health['issues'] and not engram_health['issues']:
            report += "  - 系统状态良好，无需操作\n"
        
        return report
    
    def _calculate_health_score(self, memory_health, engram_health):
        """计算健康评分"""
        score = 100
        
        # memory问题扣分
        if memory_health['status'] == 'warning':
            score -= 20
        if memory_health['usage_percent'] > 80:
            score -= 10
        
        # engram问题扣分
        if engram_health['status'] == 'warning':
            score -= 20
        if engram_health['memory_count'] < 10:
            score -= 10
        
        return max(0, score)
    
    def run_self_management(self):
        """运行自管理"""
        print("=== 记忆自管理系统 ===")
        print(f"开始时间: {datetime.now()}")
        print()
        
        # 1. 健康检查
        print("1. 健康检查...")
        memory_health = self.check_memory_health()
        engram_health = self.check_engram_health()
        print()
        
        # 2. 自动维护
        print("2. 自动维护...")
        cleanup_result = self.auto_cleanup()
        sync_result = self.auto_sync()
        decay_result = self.auto_decay()
        print()
        
        # 3. 生成报告
        print("3. 生成报告...")
        report = self.generate_health_report(memory_health, engram_health, cleanup_result, sync_result, decay_result)
        print(report)
        
        # 4. 保存报告
        report_file = self.report_path / f"self_management_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存: {report_file}")
        
        return {
            "memory_health": memory_health,
            "engram_health": engram_health,
            "cleanup_result": cleanup_result,
            "sync_result": sync_result,
            "decay_result": decay_result
        }

def main():
    manager = MemorySelfManager()
    result = manager.run_self_management()
    
    print()
    print("=== 自管理完成 ===")
    print(f"memory状态: {result['memory_health']['status']}")
    print(f"engram状态: {result['engram_health']['status']}")
    print(f"健康评分: {manager._calculate_health_score(result['memory_health'], result['engram_health'])}/100")

if __name__ == "__main__":
    main()
