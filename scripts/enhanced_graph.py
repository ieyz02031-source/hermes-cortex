#!/usr/bin/env python3
"""
增强版知识图谱
从笔记中提取实体和关系，存储到数据库
"""

import os
import re
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# 配置
VAULT_DIR = Path("D:/ObsidianVault")
DB_PATH = VAULT_DIR / ".hermes_brain.db"

# 实体类型
ENTITY_TYPES = {
    "person": ["用户", "我", "Agent", "Hermes", "AI"],
    "tool": ["Python", "Git", "Docker", "Obsidian", "Hermes", "MCP"],
    "concept": ["知识图谱", "语义索引", "Harness", "Agent", "技能"],
    "project": ["hermes-cortex", "hermes-starter", "taste-critic"],
    "location": ["D:\\", "C:\\", "GitHub", "Obsidian"],
}

# 关系模式
RELATIONSHIP_PATTERNS = [
    (r"(.+?)是(.+?)的", "is_part_of"),
    (r"(.+?)使用(.+?)", "uses"),
    (r"(.+?)包含(.+?)", "contains"),
    (r"(.+?)依赖(.+?)", "depends_on"),
    (r"(.+?)创建了(.+?)", "created"),
    (r"(.+?)优化了(.+?)", "optimized"),
    (r"(.+?)整合了(.+?)", "integrates"),
]

def create_tables(conn):
    """创建实体和关系表"""
    cursor = conn.cursor()
    
    # 实体表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            note_path TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(name, type)
        )
    """)
    
    # 关系表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER,
            target_id INTEGER,
            relation_type TEXT NOT NULL,
            note_path TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_id) REFERENCES entities(id),
            FOREIGN KEY (target_id) REFERENCES entities(id),
            UNIQUE(source_id, target_id, relation_type)
        )
    """)
    
    conn.commit()

def extract_entities(text, note_path):
    """从文本中提取实体"""
    entities = []
    
    # 提取 [[wikilinks]] 中的实体
    wikilinks = re.findall(r'\[\[(.+?)\]\]', text)
    for link in wikilinks:
        # 清理链接
        name = link.split('|')[0].strip()
        if name:
            entities.append({
                "name": name,
                "type": "concept",
                "note_path": note_path
            })
    
    # 提取标题中的实体
    headers = re.findall(r'^#{1,3}\s+(.+)$', text, re.MULTILINE)
    for header in headers:
        name = header.strip()
        if len(name) > 2 and len(name) < 50:
            entities.append({
                "name": name,
                "type": "concept",
                "note_path": note_path
            })
    
    # 提取代码块中的工具
    code_blocks = re.findall(r'```(?:bash|python|shell)\n(.+?)```', text, re.DOTALL)
    for block in code_blocks:
        # 提取命令
        commands = re.findall(r'^(\w+)', block, re.MULTILINE)
        for cmd in commands:
            if cmd in ["python", "git", "docker", "pip", "curl", "npm"]:
                entities.append({
                    "name": cmd,
                    "type": "tool",
                    "note_path": note_path
                })
    
    return entities

def extract_relationships(text, note_path, entities):
    """从文本中提取关系"""
    relationships = []
    
    # 基于模式匹配
    for pattern, rel_type in RELATIONSHIP_PATTERNS:
        matches = re.findall(pattern, text)
        for match in matches:
            if len(match) == 2:
                source, target = match
                source = source.strip()
                target = target.strip()
                if source and target and len(source) < 30 and len(target) < 30:
                    relationships.append({
                        "source": source,
                        "target": target,
                        "relation_type": rel_type,
                        "note_path": note_path
                    })
    
    # 基于 co-occurrence
    entity_names = [e["name"] for e in entities]
    for i, name1 in enumerate(entity_names):
        for name2 in entity_names[i+1:]:
            if name1 != name2:
                relationships.append({
                    "source": name1,
                    "target": name2,
                    "relation_type": "related_to",
                    "note_path": note_path
                })
    
    return relationships

def process_note(conn, note_path):
    """处理单个笔记"""
    try:
        with open(note_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ❌ 读取失败: {e}")
        return 0, 0
    
    # 提取实体
    entities = extract_entities(content, note_path)
    
    # 提取关系
    relationships = extract_relationships(content, note_path, entities)
    
    # 存储实体
    cursor = conn.cursor()
    entity_count = 0
    for entity in entities:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO entities (name, type, note_path)
                VALUES (?, ?, ?)
            """, (entity["name"], entity["type"], entity["note_path"]))
            if cursor.rowcount > 0:
                entity_count += 1
        except Exception as e:
            pass
    
    # 存储关系
    rel_count = 0
    for rel in relationships:
        try:
            # 获取实体 ID
            cursor.execute("SELECT id FROM entities WHERE name = ?", (rel["source"],))
            source_row = cursor.fetchone()
            cursor.execute("SELECT id FROM entities WHERE name = ?", (rel["target"],))
            target_row = cursor.fetchone()
            
            if source_row and target_row:
                cursor.execute("""
                    INSERT OR IGNORE INTO relationships (source_id, target_id, relation_type, note_path)
                    VALUES (?, ?, ?, ?)
                """, (source_row[0], target_row[0], rel["relation_type"], rel["note_path"]))
                if cursor.rowcount > 0:
                    rel_count += 1
        except Exception as e:
            pass
    
    conn.commit()
    return entity_count, rel_count

def build_knowledge_graph():
    """构建知识图谱"""
    print("=" * 60)
    print("  构建增强版知识图谱")
    print("=" * 60)
    print()
    
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    
    # 统计
    total_entities = 0
    total_relationships = 0
    processed_notes = 0
    
    # 遍历所有笔记
    for note_path in VAULT_DIR.rglob("*.md"):
        # 跳过隐藏文件和特殊目录
        if any(part.startswith('.') for part in note_path.parts):
            continue
        if 'raw' in note_path.parts and 'exploration' in note_path.parts:
            # 探索笔记也要处理
            pass
        
        print(f"📁 {note_path.name}")
        entity_count, rel_count = process_note(conn, note_path)
        total_entities += entity_count
        total_relationships += rel_count
        processed_notes += 1
        
        if entity_count > 0 or rel_count > 0:
            print(f"  ✅ 实体: {entity_count}, 关系: {rel_count}")
    
    # 统计结果
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM entities")
    final_entities = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM relationships")
    final_relationships = cursor.fetchone()[0]
    
    print()
    print("=" * 60)
    print(f"  知识图谱构建完成!")
    print("=" * 60)
    print(f"  处理笔记: {processed_notes}")
    print(f"  实体总数: {final_entities}")
    print(f"  关系总数: {final_relationships}")
    print("=" * 60)
    
    conn.close()

def query_knowledge_graph(query, limit=10):
    """查询知识图谱"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 搜索实体
    cursor.execute("""
        SELECT name, type, note_path 
        FROM entities 
        WHERE name LIKE ? 
        LIMIT ?
    """, (f"%{query}%", limit))
    entities = cursor.fetchall()
    
    # 搜索关系
    cursor.execute("""
        SELECT e1.name, r.relation_type, e2.name, r.note_path
        FROM relationships r
        JOIN entities e1 ON r.source_id = e1.id
        JOIN entities e2 ON r.target_id = e2.id
        WHERE e1.name LIKE ? OR e2.name LIKE ?
        LIMIT ?
    """, (f"%{query}%", f"%{query}%", limit))
    relationships = cursor.fetchall()
    
    conn.close()
    
    return {
        "entities": [{"name": e[0], "type": e[1], "note_path": e[2]} for e in entities],
        "relationships": [{"source": r[0], "relation": r[1], "target": r[2], "note_path": r[3]} for r in relationships]
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "query":
        query = " ".join(sys.argv[2:])
        if query:
            print(f"🔍 查询: {query}")
            results = query_knowledge_graph(query)
            print(f"\n📦 实体 ({len(results['entities'])}):")
            for entity in results['entities']:
                print(f"  - {entity['name']} ({entity['type']})")
            print(f"\n🔗 关系 ({len(results['relationships'])}):")
            for rel in results['relationships']:
                print(f"  - {rel['source']} → {rel['relation']} → {rel['target']}")
    else:
        build_knowledge_graph()
