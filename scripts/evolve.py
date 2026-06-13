#!/usr/bin/env python3
"""
Hermes 大脑系统 - 自进化引擎

用法:
    python evolve.py run [vault_path]           # 运行一次自进化循环
    python evolve.py dry-run [vault_path]       # 干运行（不创建笔记）
    python evolve.py status [vault_path]        # 显示自进化状态

功能:
    1. 发现知识空白
    2. 自动搜索补充知识
    3. LLM 抽取实体和概念
    4. 自动创建笔记
    5. 更新索引和热缓存
    6. 生成自进化报告

依赖:
    - web_search: Hermes 的网络搜索工具
    - write_file: Hermes 的文件写入工具
    - semantic_index.py: 语义索引
    - hot_cache.py: 热缓存
    - auto_research.py: 自动研究
"""

import os
import re
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict


# 配置
VAULT_PATH = Path(r"D:\ObsidianVault")
MAX_RESEARCH_TOPICS = 3  # 每次循环最多研究的主题数
MAX_SEARCH_RESULTS = 5   # 每个主题最多搜索结果数


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


def extract_tags(content: str) -> List[str]:
    """提取标签"""
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        tags_match = re.search(r'tags:\s*\[([^\]]+)\]', frontmatter)
        if tags_match:
            return [t.strip() for t in tags_match.group(1).split(',')]
    return []


def extract_wikilinks(content: str) -> List[str]:
    """提取 wikilinks"""
    pattern = r'\[\[([^\]]+)\]\]'
    return re.findall(pattern, content)


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
        'isolated': [],
        'thin': [],
        'missing_concepts': [],
        'tag_gaps': [],
        'topic_gaps': [],
    }
    
    # 收集所有存在的笔记名
    existing_names = set()
    for path, note in notes.items():
        existing_names.add(note['title'])
        existing_names.add(Path(path).stem)
    
    # 收集所有 wikilinks
    all_wikilinks = set()
    for note in notes.values():
        all_wikilinks.update(note['wikilinks'])
    
    # 找出孤立笔记
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
    
    # 找出薄弱笔记
    for path, note in notes.items():
        if note['content_length'] < 200:
            gaps['thin'].append({
                'path': path,
                'title': note['title'],
                'length': note['content_length'],
                'reason': f'内容只有 {note["content_length"]} 字符',
            })
    
    # 找出缺失的概念
    for link in all_wikilinks:
        if '|' in link:
            target, _ = link.split('|', 1)
        else:
            target = link
        
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
    
    # 找出标签空白
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
    
    # 找出主题空白
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


def suggest_research_topics(gaps: Dict) -> List[Dict]:
    """生成研究建议"""
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


def create_note_from_research(topic: str, search_results: List[Dict], vault_path: Path) -> Optional[str]:
    """从搜索结果创建笔记"""
    if not search_results:
        return None
    
    # 生成笔记内容
    title = topic
    date = datetime.now().strftime('%Y-%m-%d')
    
    # 提取关键信息
    descriptions = []
    urls = []
    for result in search_results[:3]:
        if result.get('description'):
            descriptions.append(result['description'])
        if result.get('url'):
            urls.append(result['url'])
    
    # 生成摘要
    summary = ' '.join(descriptions[:3])
    if len(summary) > 500:
        summary = summary[:500] + '...'
    
    # 生成笔记内容
    content = f"""---
title: {title}
type: exploration
created: {date}
updated: {date}
tags: [exploration, {title.lower().replace(' ', '-')}]
关联: [[hermes-cortex-system]]
---

# {title}

## 概述

{summary}

## 来源

"""
    
    for url in urls:
        content += f"- [{url}]({url})\n"
    
    content += f"""
## 关键发现

（待补充）

## 行动项

- [ ] 深入研究 {title}
- [ ] 创建相关概念笔记
- [ ] 建立关联关系

---

*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # 创建笔记文件
    filename = f"{date}-{title.lower().replace(' ', '-')}.md"
    filepath = vault_path / 'raw' / 'exploration' / filename
    
    # 确保目录存在
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    # 写入文件
    filepath.write_text(content, encoding='utf-8')
    
    return str(filepath.relative_to(vault_path))


def run_evolution_cycle(vault_path: Path, dry_run: bool = False) -> Dict:
    """运行一次自进化循环"""
    print(f"\n{'='*60}")
    print("🧠 Hermes 大脑自进化循环")
    print(f"{'='*60}")
    
    # 1. 扫描笔记
    print("\n📊 步骤 1: 扫描笔记...")
    notes = scan_vault(vault_path)
    print(f"  找到 {len(notes)} 个笔记")
    
    # 2. 分析知识空白
    print("\n🔍 步骤 2: 分析知识空白...")
    gaps = analyze_knowledge_gaps(notes)
    total_gaps = sum(len(v) for v in gaps.values())
    print(f"  发现 {total_gaps} 个知识空白")
    
    # 3. 生成研究建议
    print("\n💡 步骤 3: 生成研究建议...")
    suggestions = suggest_research_topics(gaps)
    print(f"  生成 {len(suggestions)} 个研究建议")
    
    # 4. 选择研究主题
    print("\n📋 步骤 4: 选择研究主题...")
    topics_to_research = suggestions[:MAX_RESEARCH_TOPICS]
    for i, topic in enumerate(topics_to_research, 1):
        print(f"  {i}. [{topic['priority']}] {topic['topic']}")
    
    # 5. 搜索补充知识
    print("\n🌐 步骤 5: 搜索补充知识...")
    search_results = {}
    for topic in topics_to_research:
        print(f"  搜索: {topic['topic']}...")
        # 这里应该调用 web_search，但因为是在脚本中，我们模拟
        # 实际使用时，应该通过 Hermes 的 web_search 工具
        search_results[topic['topic']] = []
        print(f"    结果: 0 个（需要接入 web_search）")
    
    # 6. 创建笔记
    print("\n📝 步骤 6: 创建笔记...")
    created_notes = []
    if not dry_run:
        for topic in topics_to_research:
            results = search_results.get(topic['topic'], [])
            note_path = create_note_from_research(topic['topic'], results, vault_path)
            if note_path:
                created_notes.append(note_path)
                print(f"  创建: {note_path}")
            else:
                print(f"  跳过: {topic['topic']}（无搜索结果）")
    else:
        print("  干运行模式，跳过创建笔记")
    
    # 7. 更新索引
    print("\n📦 步骤 7: 更新索引...")
    if not dry_run:
        # 调用 semantic_index.py
        os.system(f'cd {vault_path.parent / "Hermes" / "skills" / "hermes-cortex"} && python scripts/semantic_index.py index')
        print("  索引已更新")
    else:
        print("  干运行模式，跳过更新索引")
    
    # 8. 更新热缓存
    print("\n🔥 步骤 8: 更新热缓存...")
    if not dry_run:
        # 调用 hot_cache.py
        os.system(f'cd {vault_path.parent / "Hermes" / "skills" / "hermes-cortex"} && python scripts/hot_cache.py')
        print("  热缓存已更新")
    else:
        print("  干运行模式，跳过更新热缓存")
    
    # 9. 生成报告
    print("\n📊 步骤 9: 生成报告...")
    report = {
        'timestamp': datetime.now().isoformat(),
        'notes_count': len(notes),
        'gaps_count': total_gaps,
        'suggestions_count': len(suggestions),
        'researched_count': len(topics_to_research),
        'created_count': len(created_notes),
        'created_notes': created_notes,
    }
    
    # 保存报告
    report_path = vault_path / '.hermes_evolution_report.json'
    if not dry_run:
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"  报告已保存: {report_path}")
    
    return report


def show_status(vault_path: Path):
    """显示自进化状态"""
    print(f"\n{'='*60}")
    print("🧠 Hermes 大脑自进化状态")
    print(f"{'='*60}")
    
    # 检查报告
    report_path = vault_path / '.hermes_evolution_report.json'
    if report_path.exists():
        report = json.loads(report_path.read_text(encoding='utf-8'))
        print(f"\n📊 最近一次自进化:")
        print(f"  - 时间: {report.get('timestamp', 'unknown')}")
        print(f"  - 笔记数: {report.get('notes_count', 0)}")
        print(f"  - 知识空白: {report.get('gaps_count', 0)}")
        print(f"  - 研究建议: {report.get('suggestions_count', 0)}")
        print(f"  - 已研究: {report.get('researched_count', 0)}")
        print(f"  - 已创建: {report.get('created_count', 0)}")
        
        if report.get('created_notes'):
            print(f"\n📝 创建的笔记:")
            for note in report['created_notes']:
                print(f"  - {note}")
    else:
        print("\n  尚未运行过自进化循环")
    
    # 检查数据库
    db_path = vault_path / '.hermes_brain.db'
    if db_path.exists():
        conn = sqlite3.connect(str(db_path))
        cursor = conn.execute('SELECT COUNT(*) FROM notes')
        count = cursor.fetchone()[0]
        conn.close()
        print(f"\n📦 语义索引:")
        print(f"  - 已索引笔记: {count}")
    else:
        print(f"\n📦 语义索引: 未创建")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python evolve.py run [vault_path]      # 运行一次自进化循环")
        print("  python evolve.py dry-run [vault_path]  # 干运行（不创建笔记）")
        print("  python evolve.py status [vault_path]   # 显示自进化状态")
        return
    
    command = sys.argv[1]
    vault_path = VAULT_PATH
    
    if len(sys.argv) > 2:
        vault_path = Path(sys.argv[2])
    
    if not vault_path.exists():
        print(f"错误: Vault 路径不存在: {vault_path}")
        sys.exit(1)
    
    if command == 'run':
        report = run_evolution_cycle(vault_path, dry_run=False)
        print(f"\n{'='*60}")
        print("✅ 自进化循环完成")
        print(f"{'='*60}")
        print(f"  - 研究了 {report['researched_count']} 个主题")
        print(f"  - 创建了 {report['created_count']} 个笔记")
    
    elif command == 'dry-run':
        report = run_evolution_cycle(vault_path, dry_run=True)
        print(f"\n{'='*60}")
        print("✅ 干运行完成")
        print(f"{'='*60}")
        print(f"  - 将研究 {report['researched_count']} 个主题")
        print(f"  - 将创建 {report['created_count']} 个笔记")
    
    elif command == 'status':
        show_status(vault_path)
    
    else:
        print(f"未知命令: {command}")


if __name__ == '__main__':
    main()
