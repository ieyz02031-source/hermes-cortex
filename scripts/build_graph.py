#!/usr/bin/env python3
"""
Hermes 大脑系统 - 知识图谱构建脚本

用法:
    python build_graph.py [vault_path]

功能:
    1. 扫描 Obsidian Vault 中的所有笔记
    2. 抽取实体和关系
    3. 构建知识图谱
    4. 输出图谱统计信息
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple


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
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    
    return "Untitled"


def extract_type(content: str) -> str:
    """从内容中提取笔记类型"""
    # 从 frontmatter 中提取
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        type_match = re.search(r'type:\s*(\w+)', frontmatter)
        if type_match:
            return type_match.group(1).strip()
    
    # 从目录推断
    return "unknown"


def scan_vault(vault_path: Path) -> Dict[str, Dict]:
    """扫描 Vault 中的所有笔记"""
    notes = {}
    
    for md_file in vault_path.rglob('*.md'):
        # 跳过隐藏文件和特殊目录
        if any(part.startswith('.') for part in md_file.parts):
            continue
        
        try:
            content = md_file.read_text(encoding='utf-8')
            relative_path = md_file.relative_to(vault_path)
            
            notes[str(relative_path)] = {
                'path': str(md_file),
                'title': extract_title(content),
                'type': extract_type(content),
                'tags': extract_tags(content),
                'wikilinks': extract_wikilinks(content),
                'content_length': len(content),
            }
        except Exception as e:
            print(f"Error reading {md_file}: {e}")
    
    return notes


def build_graph(notes: Dict[str, Dict]) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """构建知识图谱"""
    # 节点: {note_path: {properties}}
    nodes = {}
    # 边: {(source, target): {properties}}
    edges = defaultdict(set)
    
    for note_path, note_data in notes.items():
        # 添加节点
        nodes[note_path] = {
            'title': note_data['title'],
            'type': note_data['type'],
            'tags': note_data['tags'],
        }
        
        # 添加边（wikilinks）
        for wikilink in note_data['wikilinks']:
            # 解析 wikilink
            if '|' in wikilink:
                target, _ = wikilink.split('|', 1)
            else:
                target = wikilink
            
            # 查找目标笔记
            target_path = None
            for path in notes.keys():
                if target in path or path.endswith(f'{target}.md'):
                    target_path = path
                    break
            
            if target_path:
                edges[(note_path, target_path)].add('wikilink')
    
    return nodes, edges


def analyze_graph(nodes: Dict, edges: Dict) -> Dict:
    """分析图谱统计信息"""
    # 统计节点类型
    type_counts = defaultdict(int)
    for node_data in nodes.values():
        type_counts[node_data['type']] += 1
    
    # 统计边的数量
    edge_count = len(edges)
    
    # 统计每个节点的度数
    degree_counts = defaultdict(int)
    for (source, target) in edges:
        degree_counts[source] += 1
        degree_counts[target] += 1
    
    # 找出孤立节点
    isolated_nodes = [node for node in nodes if degree_counts[node] == 0]
    
    # 找出高连接度节点
    high_degree_nodes = sorted(degree_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        'total_nodes': len(nodes),
        'total_edges': edge_count,
        'type_counts': dict(type_counts),
        'isolated_nodes': isolated_nodes,
        'high_degree_nodes': high_degree_nodes,
        'average_degree': sum(degree_counts.values()) / len(degree_counts) if degree_counts else 0,
    }


def print_statistics(stats: Dict):
    """打印统计信息"""
    print("\n" + "="*60)
    print("Hermes 大脑系统 - 知识图谱统计")
    print("="*60)
    
    print(f"\n📊 基本统计:")
    print(f"  - 总节点数: {stats['total_nodes']}")
    print(f"  - 总边数: {stats['total_edges']}")
    print(f"  - 平均度数: {stats['average_degree']:.2f}")
    
    print(f"\n📁 节点类型分布:")
    for type_name, count in stats['type_counts'].items():
        print(f"  - {type_name}: {count}")
    
    print(f"\n🔗 高连接度节点 (Top 10):")
    for node, degree in stats['high_degree_nodes']:
        print(f"  - {node}: {degree} 连接")
    
    print(f"\n🏝️ 孤立节点 ({len(stats['isolated_nodes'])} 个):")
    for node in stats['isolated_nodes'][:10]:  # 只显示前10个
        print(f"  - {node}")
    if len(stats['isolated_nodes']) > 10:
        print(f"  - ... 还有 {len(stats['isolated_nodes']) - 10} 个")


def main():
    """主函数"""
    # 获取 Vault 路径
    if len(sys.argv) > 1:
        vault_path = Path(sys.argv[1])
    else:
        vault_path = Path(r"D:\ObsidianVault")
    
    if not vault_path.exists():
        print(f"错误: Vault 路径不存在: {vault_path}")
        sys.exit(1)
    
    print(f"🔍 扫描 Vault: {vault_path}")
    
    # 扫描笔记
    notes = scan_vault(vault_path)
    print(f"  找到 {len(notes)} 个笔记")
    
    # 构建图谱
    print(f"\n🔗 构建知识图谱...")
    nodes, edges = build_graph(notes)
    
    # 分析图谱
    print(f"\n📊 分析图谱...")
    stats = analyze_graph(nodes, edges)
    
    # 打印统计信息
    print_statistics(stats)
    
    print("\n" + "="*60)
    print("✅ 知识图谱构建完成!")
    print("="*60)


if __name__ == '__main__':
    main()
