#!/usr/bin/env python3
"""
Hermes 大脑系统 - 热缓存自动更新

用法:
    python hot_cache.py [vault_path] [--recent N]

功能:
    1. 扫描最近修改的 N 个笔记
    2. 提取关键信息
    3. 生成热缓存摘要
    4. 更新 index.md 顶部的热缓存区域
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List


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
    return None


def extract_tags(content: str) -> List[str]:
    """从内容中提取标签"""
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        tags_match = re.search(r'tags:\s*\[([^\]]+)\]', frontmatter)
        if tags_match:
            return [t.strip() for t in tags_match.group(1).split(',')]
    return []


def extract_summary(content: str, max_sentences: int = 3) -> str:
    """提取摘要（前N句话）"""
    # 移除 frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    # 移除标题行
    content = re.sub(r'^#\s+.+\n', '', content, flags=re.MULTILINE)
    # 移除空行和引用
    content = re.sub(r'\n\s*\n', '\n', content)
    content = re.sub(r'^>\s+', '', content, flags=re.MULTILINE)
    
    # 按句号分割
    sentences = re.split(r'[。！？\.\!\?]', content)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    if not sentences:
        return ""
    
    summary = '。'.join(sentences[:max_sentences])
    if len(summary) > 200:
        summary = summary[:200] + '...'
    return summary


def get_recent_notes(vault_path: Path, limit: int = 10) -> List[Dict]:
    """获取最近修改的笔记"""
    notes = []
    
    for md_file in vault_path.rglob('*.md'):
        # 跳过特殊文件
        if md_file.name in ['index.md', 'SCHEMA.md', 'log.md']:
            continue
        if any(part.startswith('.') for part in md_file.parts):
            continue
        
        try:
            mtime = md_file.stat().st_mtime
            content = md_file.read_text(encoding='utf-8')
            title = extract_title(content)
            tags = extract_tags(content)
            summary = extract_summary(content)
            relative_path = md_file.relative_to(vault_path)
            
            notes.append({
                'path': str(relative_path),
                'title': title or str(relative_path),
                'tags': tags,
                'summary': summary,
                'mtime': mtime,
                'date': datetime.fromtimestamp(mtime).strftime('%Y-%m-%d'),
            })
        except Exception as e:
            pass
    
    # 按修改时间排序
    notes.sort(key=lambda x: x['mtime'], reverse=True)
    return notes[:limit]


def generate_hot_cache(notes: List[Dict]) -> str:
    """生成热缓存内容"""
    lines = []
    for note in notes:
        tag_str = ', '.join(note['tags'][:3]) if note['tags'] else ''
        summary_str = note['summary'][:80] + '...' if len(note['summary']) > 80 else note['summary']
        
        if tag_str:
            lines.append(f"- **{note['date']}**: [{note['title']}] — {tag_str}")
        else:
            lines.append(f"- **{note['date']}**: [{note['title']}]")
    
    return '\n'.join(lines)


def update_index_hot_cache(index_path: Path, hot_cache_content: str):
    """更新 index.md 中的热缓存区域"""
    content = index_path.read_text(encoding='utf-8')
    
    # 查找热缓存区域
    pattern = r'(## 热缓存 \(Hot Cache\)\s*\n\n最近上下文，每次会话更新：\s*\n\n)(.*?)(\n\n---)'
    
    match = re.search(pattern, content, re.DOTALL)
    if match:
        new_content = content[:match.start(1)] + match.group(1) + hot_cache_content + match.group(3) + content[match.end(3):]
    else:
        # 如果没找到热缓存区域，在开头添加
        new_content = f"## 热缓存 (Hot Cache)\n\n最近上下文，每次会话更新：\n\n{hot_cache_content}\n\n---\n\n" + content
    
    index_path.write_text(new_content, encoding='utf-8')


def main():
    """主函数"""
    # 解析参数
    vault_path = Path(r"D:\ObsidianVault")
    recent_limit = 10
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            print("用法: python hot_cache.py [vault_path] [--recent N]")
            print("  vault_path: Obsidian Vault 路径 (默认: D:\\ObsidianVault)")
            print("  --recent N: 最近 N 个笔记 (默认: 10)")
            return
        if not sys.argv[1].startswith('--'):
            vault_path = Path(sys.argv[1])
    
    if '--recent' in sys.argv:
        idx = sys.argv.index('--recent')
        if idx + 1 < len(sys.argv):
            recent_limit = int(sys.argv[idx + 1])
    
    if not vault_path.exists():
        print(f"错误: Vault 路径不存在: {vault_path}")
        sys.exit(1)
    
    print(f"🔥 更新热缓存: {vault_path}")
    print(f"  扫描最近 {recent_limit} 个笔记...")
    
    # 获取最近笔记
    notes = get_recent_notes(vault_path, recent_limit)
    print(f"  找到 {len(notes)} 个最近笔记")
    
    # 生成热缓存
    hot_cache = generate_hot_cache(notes)
    
    # 更新 index.md
    index_path = vault_path / 'index.md'
    if index_path.exists():
        update_index_hot_cache(index_path, hot_cache)
        print(f"  ✅ 已更新 {index_path}")
    else:
        print(f"  ⚠️ index.md 不存在，跳过更新")
    
    # 输出热缓存内容
    print(f"\n{'='*50}")
    print("热缓存内容:")
    print(f"{'='*50}")
    print(hot_cache)


if __name__ == '__main__':
    main()
