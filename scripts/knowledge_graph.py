#!/usr/bin/env python3
"""
知识图谱系统
构建实体和关系的网络，支持推理和预知
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# 实体定义
ENTITIES = {
    # 用户
    "user": {
        "type": "person",
        "name": "用户",
        "properties": {
            "language": "中文",
            "preference": "浅色主题",
            "rejection": "深色背景"
        }
    },
    
    # 系统
    "hermes": {
        "type": "system",
        "name": "Hermes",
        "properties": {
            "version": "v0.16.0",
            "memory_system": "三层架构"
        }
    },
    
    # 工具
    "engram": {
        "type": "tool",
        "name": "engram",
        "properties": {
            "version": "v1.16.3",
            "language": "Go",
            "features": ["持久化记忆", "FTS5搜索", "MCP工具"]
        }
    },
    
    "obsidian": {
        "type": "tool",
        "name": "Obsidian",
        "properties": {
            "location": "D:\\ObsidianVault",
            "purpose": "文档存储"
        }
    },
    
    # 设计概念
    "luxury_design": {
        "type": "concept",
        "name": "奢侈品极简设计",
        "properties": {
            "style": "Playfair衬线+浅灰白底",
            "references": ["Cartier", "Aesop", "Celine"]
        }
    },
    
    "warm_enterprise": {
        "type": "concept",
        "name": "暖灰企业沉浸式",
        "properties": {
            "style": "暖灰#f5f3f0+分屏布局",
            "references": ["Cartier", "Tresmares"]
        }
    },
    
    "vibe_coding": {
        "type": "workflow",
        "name": "Vibe Coding",
        "properties": {
            "steps": ["AWWWWARDS研究", "designprompts.dev选风格", "CSS变量", "写代码"],
            "depth": "七层视觉深度"
        }
    },
    
    # 设计参考
    "cartier": {
        "type": "brand",
        "name": "Cartier",
        "properties": {
            "style": "奢侈品极简",
            "features": ["粒子互动", "视频背景", "鼠标跟随"]
        }
    },
    
    "aesop": {
        "type": "brand",
        "name": "Aesop",
        "properties": {
            "style": "极简",
            "features": ["Playfair衬线", "大留白"]
        }
    },
    
    # 用户偏好
    "light_theme": {
        "type": "preference",
        "name": "浅色主题",
        "properties": {
            "colors": ["白色背景", "蓝色强调"],
            "rejection": "深色背景"
        }
    },
    
    "no_ai_flavor": {
        "type": "preference",
        "name": "拒绝AI味",
        "properties": {
            "rejection": ["紫色渐变", "粒子", "噪点", "网格", "光晕orb"]
        }
    }
}

# 关系定义
RELATIONS = [
    # 用户偏好
    {"from": "user", "to": "light_theme", "type": "偏好", "weight": 1.0},
    {"from": "user", "to": "no_ai_flavor", "type": "偏好", "weight": 1.0},
    
    # 系统集成
    {"from": "hermes", "to": "engram", "type": "集成", "weight": 1.0},
    {"from": "hermes", "to": "obsidian", "type": "集成", "weight": 1.0},
    
    # 设计关系
    {"from": "luxury_design", "to": "cartier", "type": "参考", "weight": 0.9},
    {"from": "luxury_design", "to": "aesop", "type": "参考", "weight": 0.8},
    {"from": "warm_enterprise", "to": "cartier", "type": "参考", "weight": 0.9},
    
    # 工作流关系
    {"from": "vibe_coding", "to": "luxury_design", "type": "包含", "weight": 0.7},
    {"from": "vibe_coding", "to": "warm_enterprise", "type": "包含", "weight": 0.7},
    
    # 用户使用
    {"from": "user", "to": "hermes", "type": "使用", "weight": 1.0},
    {"from": "user", "to": "vibe_coding", "type": "使用", "weight": 0.8}
]

class KnowledgeGraph:
    """知识图谱"""
    
    def __init__(self):
        self.entities = ENTITIES
        self.relations = RELATIONS
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """构建图谱"""
        graph = defaultdict(list)
        for rel in self.relations:
            graph[rel["from"]].append({
                "to": rel["to"],
                "type": rel["type"],
                "weight": rel["weight"]
            })
            # 反向关系
            graph[rel["to"]].append({
                "to": rel["from"],
                "type": f"被{rel['type']}",
                "weight": rel["weight"]
            })
        return graph
    
    def get_entity(self, entity_id):
        """获取实体"""
        return self.entities.get(entity_id)
    
    def get_relations(self, entity_id):
        """获取实体的所有关系"""
        return self.graph.get(entity_id, [])
    
    def find_path(self, from_id, to_id, max_depth=3):
        """查找两个实体之间的路径"""
        if from_id == to_id:
            return [from_id]
        
        visited = set()
        queue = [(from_id, [from_id])]
        
        while queue:
            current, path = queue.pop(0)
            
            if len(path) > max_depth:
                continue
            
            if current in visited:
                continue
            
            visited.add(current)
            
            for rel in self.graph.get(current, []):
                next_entity = rel["to"]
                
                if next_entity == to_id:
                    return path + [next_entity]
                
                if next_entity not in visited:
                    queue.append((next_entity, path + [next_entity]))
        
        return None
    
    def find_related(self, entity_id, relation_type=None, max_depth=2):
        """查找相关实体"""
        related = []
        visited = set()
        queue = [(entity_id, 0)]
        
        while queue:
            current, depth = queue.pop(0)
            
            if depth > max_depth:
                continue
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current != entity_id:
                entity = self.get_entity(current)
                if entity:
                    related.append({
                        "id": current,
                        "entity": entity,
                        "depth": depth
                    })
            
            for rel in self.graph.get(current, []):
                if relation_type is None or rel["type"] == relation_type:
                    queue.append((rel["to"], depth + 1))
        
        return related
    
    def predict_needs(self, context):
        """预测用户需求"""
        predictions = []
        
        # 根据上下文预测
        if "设计" in context or "design" in context.lower():
            predictions.append({
                "need": "设计参考",
                "entities": ["luxury_design", "warm_enterprise", "cartier"],
                "confidence": 0.8
            })
        
        if "高端" in context or "luxury" in context.lower():
            predictions.append({
                "need": "奢侈品设计",
                "entities": ["luxury_design", "cartier", "aesop"],
                "confidence": 0.9
            })
        
        if "工作流" in context or "workflow" in context.lower():
            predictions.append({
                "need": "Vibe Coding",
                "entities": ["vibe_coding"],
                "confidence": 0.7
            })
        
        return predictions
    
    def generate_report(self):
        """生成图谱报告"""
        report = f"""
=== 知识图谱报告 ===
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

实体统计:
- 总数: {len(self.entities)}
- 类型分布:
"""
        
        type_counts = defaultdict(int)
        for entity in self.entities.values():
            type_counts[entity["type"]] += 1
        
        for type_name, count in sorted(type_counts.items()):
            report += f"  - {type_name}: {count}\n"
        
        report += f"\n关系统计:\n"
        report += f"- 总数: {len(self.relations)}\n"
        
        relation_counts = defaultdict(int)
        for rel in self.relations:
            relation_counts[rel["type"]] += 1
        
        report += f"- 类型分布:\n"
        for type_name, count in sorted(relation_counts.items()):
            report += f"  - {type_name}: {count}\n"
        
        report += f"\n示例查询:\n"
        
        # 示例1：查找用户偏好
        user_prefs = self.find_related("user", "偏好")
        report += f"\n1. 用户偏好:\n"
        for pref in user_prefs:
            report += f"   - {pref['entity']['name']} (深度: {pref['depth']})\n"
        
        # 示例2：查找设计参考
        design_refs = self.find_related("luxury_design", "参考")
        report += f"\n2. 奢侈品设计参考:\n"
        for ref in design_refs:
            report += f"   - {ref['entity']['name']} (深度: {ref['depth']})\n"
        
        # 示例3：查找路径
        path = self.find_path("user", "cartier")
        report += f"\n3. 用户到Cartier的路径:\n"
        if path:
            report += f"   - {' → '.join(path)}\n"
        else:
            report += f"   - 未找到路径\n"
        
        # 示例4：预测需求
        predictions = self.predict_needs("我想做一个高端网站")
        report += f"\n4. 预测需求（上下文：我想做一个高端网站）:\n"
        for pred in predictions:
            report += f"   - {pred['need']} (置信度: {pred['confidence']})\n"
            report += f"     相关实体: {', '.join(pred['entities'])}\n"
        
        return report

def main():
    print("=== 知识图谱系统 ===")
    print(f"开始时间: {datetime.now()}")
    print()
    
    # 1. 构建图谱
    print("1. 构建知识图谱...")
    kg = KnowledgeGraph()
    print(f"   - 实体数: {len(kg.entities)}")
    print(f"   - 关系数: {len(kg.relations)}")
    print()
    
    # 2. 测试查询
    print("2. 测试查询...")
    
    # 查询用户偏好
    print("\n   查询：用户偏好")
    user_prefs = kg.find_related("user", "偏好")
    for pref in user_prefs:
        print(f"   - {pref['entity']['name']}")
    
    # 查询设计参考
    print("\n   查询：奢侈品设计参考")
    design_refs = kg.find_related("luxury_design", "参考")
    for ref in design_refs:
        print(f"   - {ref['entity']['name']}")
    
    # 查询路径
    print("\n   查询：用户到Cartier的路径")
    path = kg.find_path("user", "cartier")
    if path:
        print(f"   - {' → '.join(path)}")
    else:
        print(f"   - 未找到路径")
    
    # 预测需求
    print("\n   预测：我想做一个高端网站")
    predictions = kg.predict_needs("我想做一个高端网站")
    for pred in predictions:
        print(f"   - {pred['need']} (置信度: {pred['confidence']})")
    
    print()
    
    # 3. 生成报告
    print("3. 生成图谱报告...")
    report = kg.generate_report()
    print(report)
    
    # 4. 保存报告
    report_path = Path("D:/Hermes/skills/hermes-cortex/reports")
    report_path.mkdir(exist_ok=True)
    report_file = report_path / f"knowledge_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"报告已保存: {report_file}")

if __name__ == "__main__":
    main()
