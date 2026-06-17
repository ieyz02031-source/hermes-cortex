#!/usr/bin/env python3
"""
语义搜索系统
用embedding模型理解语义，找到相似内容
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 检查sentence-transformers是否可用
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not available, using fallback")

# 记忆数据库（模拟）
MEMORY_DB = [
    {
        "id": 1,
        "title": "VIBE_CODING_WORKFLOW",
        "content": "Vibe Coding工作流：AWWWWARDS研究→designprompts.dev选风格→CSS变量→写代码",
        "tags": ["design", "workflow", "vibe"],
        "embedding": None
    },
    {
        "id": 2,
        "title": "Taste Critic Rules",
        "content": "taste_critic.py 36条反模式规则，暗色主题默认用暖色",
        "tags": ["design", "rules", "quality"],
        "embedding": None
    },
    {
        "id": 3,
        "title": "Luxury vs Tech Design Patterns",
        "content": "高端设计两种模式：奢侈品极简和暖灰企业沉浸式",
        "tags": ["design", "luxury", "patterns"],
        "embedding": None
    },
    {
        "id": 4,
        "title": "WeChat Integration",
        "content": "微信已对接Hermes，发送消息：hermes send --to weixin",
        "tags": ["tool", "integration", "wechat"],
        "embedding": None
    },
    {
        "id": 5,
        "title": "Skill Cleanup Completed",
        "content": "技能清理完成，从117个清理到44个",
        "tags": ["system", "cleanup", "optimization"],
        "embedding": None
    }
]

def load_model():
    """加载embedding模型"""
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        return None
    
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ 模型加载成功")
        return model
    except Exception as e:
        print(f"✗ 模型加载失败: {e}")
        return None

def generate_embeddings(model, memories):
    """生成记忆的embedding"""
    if model is None:
        return memories
    
    print("生成记忆embedding...")
    for mem in memories:
        if mem["embedding"] is None:
            # 组合标题和内容生成embedding
            text = f"{mem['title']} {mem['content']}"
            mem["embedding"] = model.encode(text).tolist()
    
    print(f"✓ 生成了 {len(memories)} 个记忆的embedding")
    return memories

def semantic_search(model, query, memories, top_k=3):
    """语义搜索"""
    if model is None:
        # 回退到关键词搜索
        return keyword_search(query, memories, top_k)
    
    print(f"语义搜索: \"{query}\"")
    
    # 生成查询的embedding
    query_embedding = model.encode(query)
    
    # 计算相似度
    results = []
    for mem in memories:
        if mem["embedding"] is not None:
            # 计算余弦相似度
            similarity = np.dot(query_embedding, mem["embedding"]) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(mem["embedding"])
            )
            results.append({
                "id": mem["id"],
                "title": mem["title"],
                "content": mem["content"],
                "tags": mem["tags"],
                "similarity": float(similarity)
            })
    
    # 按相似度排序
    results.sort(key=lambda x: x["similarity"], reverse=True)
    
    return results[:top_k]

def keyword_search(query, memories, top_k=3):
    """关键词搜索（回退方案）"""
    print(f"关键词搜索: \"{query}\"")
    
    query_lower = query.lower()
    results = []
    
    for mem in memories:
        # 检查标题和内容是否包含查询词
        title_lower = mem["title"].lower()
        content_lower = mem["content"].lower()
        tags_lower = [t.lower() for t in mem["tags"]]
        
        # 计算匹配分数
        score = 0
        if query_lower in title_lower:
            score += 3
        if query_lower in content_lower:
            score += 2
        if any(query_lower in t for t in tags_lower):
            score += 1
        
        if score > 0:
            results.append({
                "id": mem["id"],
                "title": mem["title"],
                "content": mem["content"],
                "tags": mem["tags"],
                "similarity": score / 6  # 归一化到0-1
            })
    
    # 按分数排序
    results.sort(key=lambda x: x["similarity"], reverse=True)
    
    return results[:top_k]

def main():
    print("=== 语义搜索系统 ===")
    print(f"开始时间: {datetime.now()}")
    print()
    
    # 1. 加载模型
    print("1. 加载embedding模型...")
    model = load_model()
    print()
    
    # 2. 生成embedding
    print("2. 生成记忆embedding...")
    memories = generate_embeddings(model, MEMORY_DB)
    print()
    
    # 3. 测试搜索
    test_queries = [
        "高端设计",
        "怎么设计网站",
        "类似Cartier的风格",
        "vibe coding",
        "微信集成",
        "技能清理"
    ]
    
    print("3. 测试语义搜索...")
    for query in test_queries:
        print(f"\n查询: \"{query}\"")
        results = semantic_search(model, query, memories, top_k=2)
        
        if results:
            for i, r in enumerate(results, 1):
                print(f"  {i}. {r['title']} (相似度: {r['similarity']:.2%})")
        else:
            print("  未找到相关记忆")
    
    print()
    print("=== 测试完成 ===")

if __name__ == "__main__":
    main()
