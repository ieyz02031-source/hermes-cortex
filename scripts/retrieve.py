#!/usr/bin/env python3
"""
Hermes 大脑系统 - 知识检索脚本

用法:
    python retrieve.py [query] [vault_path]

功能:
    1. 接收用户查询
    2. 执行三层检索（热缓存、索引、图谱）
    3. 返回相关笔记
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import json


def extract_wikilinks(content: str) -> List[str]:
    """从内容中提取 wikilinks"""
    pattern = r'\[\[([^\]]+)\]\]'
    return re.findall(pattern, content)


def extract_tags(content: str) -> List[str]:
    """从内容中提取标签"""
    # 从 frontmatter 中提取
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        tags_match = re.search(r'tags:\s*\[([^\]]+)\]', frontmatter)
        if tags_match:
            return [tag.strip() for tag in tags_match.group(1).split(',')]
    
    # 从内容中提取 #tags
    pattern = r'#(\w+)'
    return re.findall(pattern, content)


def extract_title(content: str) -> str:
    """从内容中提取标题"""
    # 从 frontmatter 中提取
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        title_match = re.search(r'title:\s*(.+)', frontmatter)
        if title_match:
            return title_match.group(1).strip()
    
    # 从内容中提取 # 标题
    title_match = re.search(r'^#\s+(.+)$', content, re.DOTALL)
    if title_match:
        return title_match.group(1).strip()
    
    return "Untitled"


def extract_summary(content: str, max_length: int = 200) -> str:
    """从内容中提取摘要"""
    # 移除 frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    
    # 移除标题
    content = re.sub(r'^#\s+.+\n', '', content, flags=re.MULTILINE)
    
    # 移除空行
    content = re.sub(r'\n\s*\n', '\n', content)
    
    # 截取前 max_length 个字符
    if len(content) > max_length:
        content = content[:max_length] + '...'
    
    return content.strip()


def search_by_keywords(query: str, vault_path: Path) -> List[Dict]:
    """基于关键词搜索"""
    results = []
    query_lower = query.lower()
    
    for md_file in vault_path.rglob('*.md'):
        # 跳过隐藏文件和特殊目录
        if any(part.startswith('.') for part in md_file.parts):
            continue
        
        try:
            content = md_file.read_text(encoding='utf-8')
            content_lower = content.lower()
            
            # 计算相关度分数
            score = 0
            
            # 标题匹配（权重最高）
            title = extract_title(content)
            if query_lower in title.lower():
                score += 10
            
            # 标签匹配
            tags = extract_tags(content)
            for tag in tags:
                if query_lower in tag.lower():
                    score += 5
            
            # 内容匹配
            if query_lower in content_lower:
                # 计算匹配次数
                count = content_lower.count(query_lower)
                score += min(count, 5)  # 最多加5分
            
            if score > 0:
                relative_path = md_file.relative_to(vault_path)
                results.append({
                    'path': str(relative_path),
                    'title': title,
                    'score': score,
                    'summary': extract_summary(content),
                    'tags': tags,
                })
        except Exception as e:
            print(f"Error reading {md_file}: {e}")
    
    # 按分数排序
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return results


def search_by_wikilinks(query: str, vault_path: Path) -> List[Dict]:
    """基于 wikilinks 搜索（图谱遍历）"""
    results = []
    query_lower = query.lower()
    
    # 首先找到包含查询的笔记
    matching_notes = []
    for md_file in vault_path.rglob('*.md'):
        if any(part.startswith('.') for part in md_file.parts):
            continue
        
        try:
            content = md_file.read_text(encoding='utf-8')
            title = extract_title(content)
            
            if query_lower in title.lower() or query_lower in content.lower():
                matching_notes.append({
                    'path': str(md_file.relative_to(vault_path)),
                    'title': title,
                    'content': content,
                })
        except Exception as e:
            pass
    
    # 然后查找这些笔记的 wikilinks
    for note in matching_notes:
        wikilinks = extract_wikilinks(note['content'])
        
        for wikilink in wikilinks:
            # 解析 wikilink
            if '|' in wikilink:
                target, _ = wikilink.split('|', 1)
            else:
                target = wikilink
            
            # 查找目标笔记
            for md_file in vault_path.rglob('*.md'):
                if any(part.startswith('.') for part in md_file.parts):
                    continue
                
                try:
                    content = md_file.read_text(encoding='utf-8')
                    title = extract_title(content)
                    
                    if target.lower() in title.lower() or target.lower() in str(md_file).lower():
                        relative_path = md_file.relative_to(vault_path)
                        
                        # 避免重复
                        if not any(r['path'] == str(relative_path) for r in results):
                            results.append({
                                'path': str(relative_path),
                                'title': title,
                                'score': 3,  # 图谱遍历的分数
                                'summary': extract_summary(content),
                                'tags': extract_tags(content),
                                'source': note['title'],  # 来源笔记
                            })
                except Exception as e:
                    pass
    
    return results


def retrieve(query: str, vault_path: Path, max_results: int = 5) -> List[Dict]:
    """执行三层检索"""
    print(f"\n🔍 检索查询: {query}")
    print(f"📁 Vault 路径: {vault_path}")
    
    # 第1层: 关键词搜索
    print(f"\n📊 第1层: 关键词搜索...")
    keyword_results = search_by_keywords(query, vault_path)
    print(f"  找到 {len(keyword_results)} 个结果")
    
    # 第2层: 图谱遍历
    print(f"\n🔗 第2层: 图谱遍历...")
    graph_results = search_by_wikilinks(query, vault_path)
    print(f"  找到 {len(graph_results)} 个结果")
    
    # 合并结果
    all_results = []
    seen_paths = set()
    
    # 添加关键词搜索结果
    for result in keyword_results:
        if result['path'] not in seen_paths:
            all_results.append(result)
            seen_paths.add(result['path'])
    
    # 添加图谱遍历结果
    for result in graph_results:
        if result['path'] not in seen_paths:
            all_results.append(result)
            seen_paths.add(result['path'])
    
    # 按分数排序
    all_results.sort(key=lambda x: x['score'], reverse=True)
    
    # 截取前 max_results 个结果
    results = all_results[:max_results]
    
    print(f"\n✅ 检索完成，返回 {len(results)} 个结果")
    
    return results


def format_results(results: List[Dict]) -> str:
    """格式化检索结果"""
    if not results:
        return "未找到相关笔记。"
    
    output = []
    for i, result in enumerate(results, 1):
        output.append(f"\n{'='*60}")
        output.append(f"📄 {i}. {result['title']}")
        output.append(f"   路径: {result['path']}")
        output.append(f"   分数: {result['score']}")
        
        if 'source' in result:
            output.append(f"   来源: {result['source']}")
        
        if result['tags']:
            output.append(f"   标签: {', '.join(result['tags'])}")
        
        output.append(f"\n   摘要:")
        output.append(f"   {result['summary']}")
    
    return '\n'.join(output)


def main():
    """主函数"""
    # 获取查询和 Vault 路径
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = "Hermes"
    
    if len(sys.argv) > 2:
        vault_path = Path(sys.argv[2])
    else:
        vault_path = Path(r"D:\ObsidianVault")
    
    if not vault_path.exists():
        print(f"错误: Vault 路径不存在: {vault_path}")
        sys.exit(1)
    
    # 执行检索
    results = retrieve(query, vault_path)
    
    # 格式化输出
    print(format_results(results))
    
    # 输出 JSON 格式（便于程序处理）
    print(f"\n{'='*60}")
    print("📋 JSON 格式:")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
