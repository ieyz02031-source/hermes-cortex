#!/usr/bin/env python3
"""
智能记忆检索系统
结合知识图谱和记忆系统，支持推理和预知
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 导入知识图谱
sys.path.insert(0, str(Path(__file__).parent))
from knowledge_graph import KnowledgeGraph

# 记忆数据库（模拟）
MEMORY_DB = [
    {
        "id": 1,
        "title": "VIBE_CODING_WORKFLOW",
        "content": "Vibe Coding工作流：AWWWWARDS研究→designprompts.dev选风格→CSS变量→写代码",
        "tags": ["design", "workflow", "vibe"],
        "entities": ["vibe_coding", "luxury_design"]
    },
    {
        "id": 2,
        "title": "Taste Critic Rules",
        "content": "taste_critic.py 36条反模式规则，暗色主题默认用暖色",
        "tags": ["design", "rules", "quality"],
        "entities": ["no_ai_flavor"]
    },
    {
        "id": 3,
        "title": "Luxury vs Tech Design Patterns",
        "content": "高端设计两种模式：奢侈品极简和暖灰企业沉浸式",
        "tags": ["design", "luxury", "patterns"],
        "entities": ["luxury_design", "warm_enterprise", "cartier"]
    },
    {
        "id": 4,
        "title": "WeChat Integration",
        "content": "微信已对接Hermes，发送消息：hermes send --to weixin",
        "tags": ["tool", "integration", "wechat"],
        "entities": ["hermes"]
    },
    {
        "id": 5,
        "title": "Skill Cleanup Completed",
        "content": "技能清理完成，从117个清理到44个",
        "tags": ["system", "cleanup"],
        "entities": ["hermes"]
    }
]

class SmartMemoryRetrieval:
    """智能记忆检索"""
    
    def __init__(self):
        self.kg = KnowledgeGraph()
        self.memories = MEMORY_DB
    
    def search_by_entity(self, entity_id):
        """通过实体搜索记忆"""
        results = []
        for mem in self.memories:
            if entity_id in mem["entities"]:
                results.append(mem)
        return results
    
    def search_by_relation(self, entity_id, relation_type=None):
        """通过关系搜索记忆"""
        # 获取相关实体
        related = self.kg.find_related(entity_id, relation_type)
        
        # 搜索包含这些实体的记忆
        results = []
        for rel in related:
            memories = self.search_by_entity(rel["id"])
            for mem in memories:
                if mem not in results:
                    results.append(mem)
        
        return results
    
    def intelligent_search(self, query):
        """智能搜索"""
        print(f"智能搜索: \"{query}\"")
        
        # 1. 预测需求
        predictions = self.kg.predict_needs(query)
        print(f"   预测需求: {len(predictions)}个")
        
        # 2. 根据预测搜索记忆
        results = []
        for pred in predictions:
            for entity_id in pred["entities"]:
                memories = self.search_by_entity(entity_id)
                for mem in memories:
                    if mem not in results:
                        results.append(mem)
        
        # 3. 如果没有预测结果，使用关键词搜索
        if not results:
            print("   使用关键词搜索...")
            query_lower = query.lower()
            for mem in self.memories:
                if (query_lower in mem["title"].lower() or 
                    query_lower in mem["content"].lower()):
                    results.append(mem)
        
        return results
    
    def get_context(self, entity_id):
        """获取实体上下文"""
        entity = self.kg.get_entity(entity_id)
        if not entity:
            return None
        
        # 获取相关实体
        related = self.kg.find_related(entity_id)
        
        # 获取相关记忆
        memories = self.search_by_entity(entity_id)
        
        return {
            "entity": entity,
            "related": related,
            "memories": memories
        }
    
    def generate_report(self):
        """生成报告"""
        report = f"""
=== 智能记忆检索报告 ===
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

知识图谱:
- 实体数: {len(self.kg.entities)}
- 关系数: {len(self.kg.relations)}

记忆库:
- 记忆数: {len(self.memories)}

智能搜索示例:
"""
        
        # 示例1
        print("\n示例1: 我想做一个高端网站")
        results = self.intelligent_search("我想做一个高端网站")
        report += f"\n查询: \"我想做一个高端网站\"\n"
        report += f"结果: {len(results)}个记忆\n"
        for r in results:
            report += f"  - {r['title']}\n"
        
        # 示例2
        print("\n示例2: 设计参考什么品牌")
        results = self.intelligent_search("设计参考什么品牌")
        report += f"\n查询: \"设计参考什么品牌\"\n"
        report += f"结果: {len(results)}个记忆\n"
        for r in results:
            report += f"  - {r['title']}\n"
        
        # 示例3
        print("\n示例3: 用户偏好是什么")
        context = self.get_context("user")
        report += f"\n查询: \"用户偏好是什么\"\n"
        if context:
            report += f"实体: {context['entity']['name']}\n"
            report += f"相关实体: {len(context['related'])}个\n"
            for rel in context['related']:
                report += f"  - {rel['entity']['name']} (深度: {rel['depth']})\n"
            report += f"相关记忆: {len(context['memories'])}个\n"
            for mem in context['memories']:
                report += f"  - {mem['title']}\n"
        
        return report

def main():
    print("=== 智能记忆检索系统 ===")
    print(f"开始时间: {datetime.now()}")
    print()
    
    # 1. 初始化
    print("1. 初始化智能检索系统...")
    smr = SmartMemoryRetrieval()
    print(f"   - 知识图谱: {len(smr.kg.entities)}个实体, {len(smr.kg.relations)}个关系")
    print(f"   - 记忆库: {len(smr.memories)}个记忆")
    print()
    
    # 2. 测试智能搜索
    print("2. 测试智能搜索...")
    
    test_queries = [
        "我想做一个高端网站",
        "设计参考什么品牌",
        "用户偏好是什么",
        "Vibe Coding怎么用",
        "怎么拒绝AI味"
    ]
    
    for query in test_queries:
        print(f"\n   查询: \"{query}\"")
        results = smr.intelligent_search(query)
        print(f"   结果: {len(results)}个记忆")
        for r in results:
            print(f"     - {r['title']}")
    
    print()
    
    # 3. 生成报告
    print("3. 生成报告...")
    report = smr.generate_report()
    print(report)
    
    # 4. 保存报告
    report_path = Path("D:/Hermes/skills/hermes-cortex/reports")
    report_path.mkdir(exist_ok=True)
    report_file = report_path / f"smart_retrieval_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"报告已保存: {report_file}")

if __name__ == "__main__":
    main()
