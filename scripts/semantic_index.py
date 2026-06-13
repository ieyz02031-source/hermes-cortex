#!/usr/bin/env python3
"""
Hermes 大脑系统 - 语义索引与检索

用法:
    python semantic_index.py index [vault_path]    # 构建索引
    python semantic_index.py search [query]        # 语义搜索
    python semantic_index.py rebuild               # 重建索引

功能:
    1. 用 sentence-transformers 生成笔记的向量嵌入
    2. 存储到 SQLite 数据库
    3. 支持语义相似度搜索
    4. 支持增量更新（只重新索引变化的笔记）
"""

import os
import re
import sys
import json
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# 嵌入模型配置
MODEL_NAME = 'all-MiniLM-L6-v2'
DB_NAME = '.hermes_brain.db'


def get_db_path(vault_path: Path) -> Path:
    """获取数据库路径"""
    return vault_path / DB_NAME


def extract_title(content: str) -> str:
    """从内容中提取标题"""
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        title_match = re.search(r'title:\s*(.+)', frontmatter)
        if title_match:
            return title_match.group(1).strip()
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    return "Untitled"


def extract_tags(content: str) -> List[str]:
    """从内容中提取标签"""
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        tags_match = re.search(r'tags:\s*\[([^\]]+)\]', frontmatter)
        if tags_match:
            return [t.strip() for t in tags_match.group(1).split(',')]
    return []


def extract_text_for_embedding(content: str) -> str:
    """提取用于生成嵌入的文本"""
    # 移除 frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    # 移除代码块
    content = re.sub(r'```[\s\S]*?```', '', content)
    # 移除 wikilinks 的括号部分，保留文字
    content = re.sub(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', r'\1', content)
    # 移除 markdown 格式
    content = re.sub(r'[#*_`\[\]()]', '', content)
    # 压缩空白
    content = re.sub(r'\s+', ' ', content).strip()
    
    # 截取前 500 字符（模型输入限制）
    return content[:500]


def compute_hash(content: str) -> str:
    """计算内容哈希"""
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def init_db(db_path: Path) -> sqlite3.Connection:
    """初始化数据库"""
    conn = sqlite3.connect(str(db_path))
    conn.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            path TEXT PRIMARY KEY,
            title TEXT,
            tags TEXT,
            content_hash TEXT,
            embedding BLOB,
            updated_at TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    conn.commit()
    return conn


def get_embedding_model():
    """获取嵌入模型（延迟加载）"""
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(MODEL_NAME)
        return model
    except ImportError:
        print("错误: 需要安装 sentence-transformers")
        print("运行: pip install sentence-transformers")
        sys.exit(1)


def scan_vault(vault_path: Path) -> Dict[str, Dict]:
    """扫描 Vault 中的所有笔记"""
    notes = {}
    
    for md_file in vault_path.rglob('*.md'):
        if md_file.name == DB_NAME:
            continue
        if any(part.startswith('.') for part in md_file.parts):
            continue
        
        try:
            content = md_file.read_text(encoding='utf-8')
            relative_path = str(md_file.relative_to(vault_path))
            
            notes[relative_path] = {
                'path': relative_path,
                'title': extract_title(content),
                'tags': extract_tags(content),
                'text': extract_text_for_embedding(content),
                'hash': compute_hash(content),
            }
        except Exception as e:
            pass
    
    return notes


def index_vault(vault_path: Path, force: bool = False):
    """为 Vault 建立语义索引"""
    db_path = get_db_path(vault_path)
    conn = init_db(db_path)
    
    print(f"📦 构建语义索引: {vault_path}")
    
    # 扫描笔记
    print("  扫描笔记...")
    notes = scan_vault(vault_path)
    print(f"  找到 {len(notes)} 个笔记")
    
    # 获取已索引的笔记
    existing = {}
    cursor = conn.execute('SELECT path, content_hash FROM notes')
    for row in cursor:
        existing[row[0]] = row[1]
    
    # 找出需要更新的笔记
    to_update = []
    for path, note in notes.items():
        if force or path not in existing or existing[path] != note['hash']:
            to_update.append(note)
    
    if not to_update:
        print("  ✅ 所有笔记已是最新，无需更新")
        return
    
    print(f"  需要更新 {len(to_update)} 个笔记")
    
    # 加载模型
    print("  加载嵌入模型...")
    model = get_embedding_model()
    
    # 批量生成嵌入
    print("  生成嵌入向量...")
    texts = [note['text'] for note in to_update]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
    
    # 存储到数据库
    print("  存储到数据库...")
    for note, embedding in zip(to_update, embeddings):
        conn.execute('''
            INSERT OR REPLACE INTO notes (path, title, tags, content_hash, embedding, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            note['path'],
            note['title'],
            json.dumps(note['tags'], ensure_ascii=False),
            note['hash'],
            embedding.tobytes(),
            datetime.now().isoformat(),
        ))
    
    # 更新元数据
    conn.execute('''
        INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)
    ''', ('last_indexed', datetime.now().isoformat()))
    conn.execute('''
        INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)
    ''', ('model_name', MODEL_NAME))
    conn.execute('''
        INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)
    ''', ('total_notes', str(len(notes))))
    
    conn.commit()
    conn.close()
    
    print(f"  ✅ 索引完成，共 {len(notes)} 个笔记")


def search_vault(query: str, vault_path: Path, top_k: int = 5) -> List[Dict]:
    """语义搜索 Vault"""
    db_path = get_db_path(vault_path)
    
    if not db_path.exists():
        print("错误: 索引不存在，请先运行: python semantic_index.py index")
        sys.exit(1)
    
    conn = sqlite3.connect(str(db_path))
    
    # 加载模型
    model = get_embedding_model()
    
    # 生成查询向量
    query_embedding = model.encode([query])[0]
    
    # 从数据库加载所有嵌入
    cursor = conn.execute('SELECT path, title, tags, embedding FROM notes')
    results = []
    
    for row in cursor:
        path, title, tags_json, embedding_bytes = row
        
        # 计算余弦相似度
        import numpy as np
        embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
        
        # 余弦相似度
        dot_product = np.dot(query_embedding, embedding)
        norm1 = np.linalg.norm(query_embedding)
        norm2 = np.linalg.norm(embedding)
        
        if norm1 > 0 and norm2 > 0:
            similarity = dot_product / (norm1 * norm2)
        else:
            similarity = 0.0
        
        tags = json.loads(tags_json) if tags_json else []
        
        results.append({
            'path': path,
            'title': title,
            'tags': tags,
            'score': float(similarity),
        })
    
    conn.close()
    
    # 按相似度排序
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return results[:top_k]


def print_results(results: List[Dict], query: str):
    """打印搜索结果"""
    print(f"\n{'='*60}")
    print(f"🔍 语义搜索: {query}")
    print(f"{'='*60}")
    
    if not results:
        print("  未找到相关笔记")
        return
    
    for i, result in enumerate(results, 1):
        tags_str = ', '.join(result['tags'][:3]) if result['tags'] else ''
        score_bar = '█' * int(result['score'] * 20)
        
        print(f"\n  {i}. {result['title']}")
        print(f"     路径: {result['path']}")
        print(f"     相似度: {result['score']:.3f} {score_bar}")
        if tags_str:
            print(f"     标签: {tags_str}")


def show_stats(vault_path: Path):
    """显示索引统计"""
    db_path = get_db_path(vault_path)
    
    if not db_path.exists():
        print("索引不存在")
        return
    
    conn = sqlite3.connect(str(db_path))
    
    # 获取元数据
    cursor = conn.execute('SELECT key, value FROM meta')
    meta = {}
    for row in cursor:
        meta[row[0]] = row[1]
    
    # 获取笔记数量
    cursor = conn.execute('SELECT COUNT(*) FROM notes')
    count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\n📊 索引统计:")
    print(f"  - 笔记数量: {count}")
    print(f"  - 嵌入模型: {meta.get('model_name', 'unknown')}")
    print(f"  - 最后索引: {meta.get('last_indexed', 'unknown')}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python semantic_index.py index [vault_path]    # 构建索引")
        print("  python semantic_index.py search [query]        # 语义搜索")
        print("  python semantic_index.py rebuild               # 重建索引")
        print("  python semantic_index.py stats                 # 显示统计")
        return
    
    command = sys.argv[1]
    vault_path = Path(r"D:\ObsidianVault")
    
    if command == 'index':
        if len(sys.argv) > 2 and not sys.argv[2].startswith('--'):
            vault_path = Path(sys.argv[2])
        index_vault(vault_path)
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("错误: 请提供搜索查询")
            return
        query = ' '.join(sys.argv[2:])
        results = search_vault(query, vault_path)
        print_results(results, query)
    
    elif command == 'rebuild':
        if len(sys.argv) > 2:
            vault_path = Path(sys.argv[2])
        index_vault(vault_path, force=True)
    
    elif command == 'stats':
        show_stats(vault_path)
    
    else:
        print(f"未知命令: {command}")


if __name__ == '__main__':
    main()
