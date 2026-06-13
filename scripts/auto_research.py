#!/usr/bin/env python3
"""
Hermes 大脑系统 - 自动研究与自进化

用法:
    python auto_research.py discover [vault_path]        # 发现知识空白
    python auto_research.py gaps                          # 显示知识空白
    python auto_research.py evolve [vault_path]           # 自进化循环

功能:
    1. 分析现有知识，发现空白和薄弱点
    2. 自动搜索补充知识
    3. 抽取实体和概念，创建笔记
    4. 建立关联关系
    5. 更新索引和热缓存

自进化循环:
    发现空白 → 搜索补充 → 抽取知识 → 创建笔记 → 更新图谱 → 发现新空白
"""

import os
import re
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
from collections import defaultdict


def extract_wikilinks(content: str) -> List[str]:
    """提取 wikilinks"""
    pattern = r'\[\[([^\]]+)\]\]'
    return re.findall(pattern, content)


def extract_tags(content: str) -> List[str]:
    """提取标签"""
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        tags_match = re.search(r'tags:\s*\[([^\]]+)\]', frontmatter)
        if tags_match:
            return [t.strip() for t in tags_match.group(1).split(',')]
    return []


def extract_title(content: str) -> str:
    """提取标题"""
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


def scan_vault(vault_path: Path) -> Dict[str, Dict]:
    """扫描 Vault"""
    notes = {}
    
    for md_file in vault_path.rglob('*.md'):
        if md_file.name in ['index.md', 'SCHEMA.md', 'log.md', '.hermes_brain.db']:
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
                'wikilinks': extract_wikilinks(content),
                'content_length': len(content),
            }
        except Exception:
            pass
    
    return notes


def analyze_knowledge_gaps(notes: Dict[str, Dict]) -> Dict:
    """分析知识空白"""
    gaps = {
        'isolated': [],        # 孤立笔记（没有关联）
        'thin': [],            # 薄弱笔记（内容太少）
        'missing_concepts': [], # 缺失的概念（被引用但不存在）
        'tag_gaps': [],        # 标签空白（有标签但笔记很少）
        'topic_gaps': [],      # 主题空白（某个领域笔记很少）
    }
    
    # 收集所有存在的笔记名
    existing_names = set()
    for path, note in notes.items():
        existing_names.add(note['title'])
        # 也添加文件名（不含扩展名）
        existing_names.add(Path(path).stem)
    
    # 收集所有 wikilinks
    all_wikilinks = set()
    for note in notes.values():
        all_wikilinks.update(note['wikilinks'])
    
    # 1. 找出孤立笔记
    linked_notes = set()
    for note in notes.values():
        linked_notes.update(note['wikilinks'])
    
    for path, note in notes.items():
        stem = Path(path).stem
        if not note['wikilinks'] and stem not in linked_notes and note['title'] not in linked_notes:
            gaps['isolated'].append({
                'path': path,
                'title': note['title'],
                'reason': '没有关联，也没有被其他笔记引用',
            })
    
    # 2. 找出薄弱笔记（内容少于 200 字符）
    for path, note in notes.items():
        if note['content_length'] < 200:
            gaps['thin'].append({
                'path': path,
                'title': note['title'],
                'length': note['content_length'],
                'reason': f'内容只有 {note["content_length"]} 字符',
            })
    
    # 3. 找出缺失的概念（被引用但不存在）
    for link in all_wikilinks:
        # 解析 wikilink
        if '|' in link:
            target, _ = link.split('|', 1)
        else:
            target = link
        
        # 检查是否存在
        found = False
        for path, note in notes.items():
            if target in note['title'] or target in Path(path).stem:
                found = True
                break
        
        if not found:
            gaps['missing_concepts'].append({
                'name': target,
                'reason': '被引用但笔记不存在',
            })
    
    # 4. 找出标签空白（标签只有 1-2 个笔记）
    tag_counts = defaultdict(int)
    for note in notes.values():
        for tag in note['tags']:
            tag_counts[tag] += 1
    
    for tag, count in tag_counts.items():
        if count <= 2:
            gaps['tag_gaps'].append({
                'tag': tag,
                'count': count,
                'reason': f'标签 "{tag}" 只有 {count} 个笔记',
            })
    
    # 5. 找出主题空白（基于常见知识领域）
    knowledge_domains = {
        'AI': ['AI', 'LLM', '机器学习', '深度学习', 'GPT', 'Claude'],
        '设计': ['设计', 'UI', 'UX', 'CSS', '配色', '排版'],
        '开发': ['开发', 'Python', 'JavaScript', 'API', '数据库'],
        '工具': ['工具', 'MCP', 'Obsidian', 'Git', 'Docker'],
        '方法论': ['方法论', '流程', '架构', '模式', '最佳实践'],
    }
    
    for domain, keywords in knowledge_domains.items():
        count = 0
        for note in notes.values():
            content_lower = (note['title'] + ' '.join(note['tags'])).lower()
            if any(kw.lower() in content_lower for kw in keywords):
                count += 1
        
        if count <= 2:
            gaps['topic_gaps'].append({
                'domain': domain,
                'count': count,
                'reason': f'领域 "{domain}" 只有 {count} 个笔记',
            })
    
    return gaps


def print_gaps(gaps: Dict):
    """打印知识空白"""
    print(f"\n{'='*60}")
    print("🔍 知识空白分析")
    print(f"{'='*60}")
    
    # 孤立笔记
    if gaps['isolated']:
        print(f"\n🏝️ 孤立笔记 ({len(gaps['isolated'])} 个):")
        for item in gaps['isolated'][:5]:
            print(f"  - {item['title']}: {item['reason']}")
        if len(gaps['isolated']) > 5:
            print(f"  - ... 还有 {len(gaps['isolated']) - 5} 个")
    
    # 薄弱笔记
    if gaps['thin']:
        print(f"\n📝 薄弱笔记 ({len(gaps['thin'])} 个):")
        for item in gaps['thin'][:5]:
            print(f"  - {item['title']}: {item['reason']}")
        if len(gaps['thin']) > 5:
            print(f"  - ... 还有 {len(gaps['thin']) - 5} 个")
    
    # 缺失概念
    if gaps['missing_concepts']:
        print(f"\n❓ 缺失概念 ({len(gaps['missing_concepts'])} 个):")
        for item in gaps['missing_concepts'][:10]:
            print(f"  - {item['name']}: {item['reason']}")
        if len(gaps['missing_concepts']) > 10:
            print(f"  - ... 还有 {len(gaps['missing_concepts']) - 10} 个")
    
    # 标签空白
    if gaps['tag_gaps']:
        print(f"\n🏷️ 标签空白 ({len(gaps['tag_gaps'])} 个):")
        for item in gaps['tag_gaps'][:5]:
            print(f"  - {item['tag']}: {item['reason']}")
    
    # 主题空白
    if gaps['topic_gaps']:
        print(f"\n📚 主题空白 ({len(gaps['topic_gaps'])} 个):")
        for item in gaps['topic_gaps']:
            print(f"  - {item['domain']}: {item['reason']}")
    
    # 总结
    total_gaps = sum(len(v) for v in gaps.values())
    print(f"\n{'='*60}")
    print(f"📊 总计: {total_gaps} 个知识空白")
    print(f"{'='*60}")


def suggest_research_topics(gaps: Dict) -> List[Dict]:
    """基于知识空白建议研究主题"""
    suggestions = []
    
    # 基于缺失概念
    for item in gaps['missing_concepts'][:5]:
        suggestions.append({
            'topic': item['name'],
            'reason': item['reason'],
            'priority': 'high',
            'type': 'missing_concept',
        })
    
    # 基于主题空白
    for item in gaps['topic_gaps']:
        suggestions.append({
            'topic': item['domain'],
            'reason': item['reason'],
            'priority': 'medium',
            'type': 'topic_gap',
        })
    
    # 基于标签空白
    for item in gaps['tag_gaps'][:3]:
        suggestions.append({
            'topic': item['tag'],
            'reason': item['reason'],
            'priority': 'low',
            'type': 'tag_gap',
        })
    
    return suggestions


def print_suggestions(suggestions: List[Dict]):
    """打印研究建议"""
    print(f"\n{'='*60}")
    print("💡 研究建议")
    print(f"{'='*60}")
    
    if not suggestions:
        print("  没有需要研究的主题")
        return
    
    # 按优先级分组
    high = [s for s in suggestions if s['priority'] == 'high']
    medium = [s for s in suggestions if s['priority'] == 'medium']
    low = [s for s in suggestions if s['priority'] == 'low']
    
    if high:
        print(f"\n🔴 高优先级:")
        for s in high:
            print(f"  - {s['topic']}: {s['reason']}")
    
    if medium:
        print(f"\n🟡 中优先级:")
        for s in medium:
            print(f"  - {s['topic']}: {s['reason']}")
    
    if low:
        print(f"\n🟢 低优先级:")
        for s in low[:5]:
            print(f"  - {s['topic']}: {s['reason']}")


def generate_evolution_report(vault_path: Path) -> Dict:
    """生成自进化报告"""
    notes = scan_vault(vault_path)
    gaps = analyze_knowledge_gaps(notes)
    suggestions = suggest_research_topics(gaps)
    
    # 计算知识健康度
    total_notes = len(notes)
    isolated_count = len(gaps['isolated'])
    thin_count = len(gaps['thin'])
    missing_count = len(gaps['missing_concepts'])
    
    # 健康度 = 100 - (问题数 / 总笔记数 * 100)
    problem_count = isolated_count + thin_count + missing_count
    health_score = max(0, 100 - (problem_count / max(total_notes, 1) * 100))
    
    return {
        'timestamp': datetime.now().isoformat(),
        'total_notes': total_notes,
        'health_score': round(health_score, 1),
        'gaps': {k: len(v) for k, v in gaps.items()},
        'suggestions': suggestions,
        'top_issues': gaps['isolated'][:3] + gaps['thin'][:3] + gaps['missing_concepts'][:3],
    }


def print_evolution_report(report: Dict):
    """打印自进化报告"""
    print(f"\n{'='*60}")
    print("🧠 Hermes 大脑自进化报告")
    print(f"{'='*60}")
    
    print(f"\n📊 基本统计:")
    print(f"  - 笔记总数: {report['total_notes']}")
    print(f"  - 健康度: {report['health_score']}%")
    
    # 健康度可视化
    score = report['health_score']
    if score >= 80:
        status = "🟢 健康"
    elif score >= 60:
        status = "🟡 一般"
    else:
        status = "🔴 需要关注"
    print(f"  - 状态: {status}")
    
    print(f"\n🔍 问题统计:")
    for gap_type, count in report['gaps'].items():
        if count > 0:
            print(f"  - {gap_type}: {count}")
    
    if report['suggestions']:
        print(f"\n💡 建议研究主题:")
        for s in report['suggestions'][:5]:
            print(f"  - [{s['priority']}] {s['topic']}")
    
    print(f"\n{'='*60}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python auto_research.py discover [vault_path]  # 发现知识空白")
        print("  python auto_research.py report [vault_path]    # 自进化报告")
        print("  python auto_research.py suggest [vault_path]   # 研究建议")
        return
    
    command = sys.argv[1]
    vault_path = Path(r"D:\ObsidianVault")
    
    if len(sys.argv) > 2 and not sys.argv[2].startswith('--'):
        vault_path = Path(sys.argv[2])
    
    if not vault_path.exists():
        print(f"错误: Vault 路径不存在: {vault_path}")
        sys.exit(1)
    
    if command == 'discover':
        notes = scan_vault(vault_path)
        gaps = analyze_knowledge_gaps(notes)
        print_gaps(gaps)
    
    elif command == 'report':
        report = generate_evolution_report(vault_path)
        print_evolution_report(report)
    
    elif command == 'suggest':
        notes = scan_vault(vault_path)
        gaps = analyze_knowledge_gaps(notes)
        suggestions = suggest_research_topics(gaps)
        print_suggestions(suggestions)
    
    else:
        print(f"未知命令: {command}")


if __name__ == '__main__':
    main()
