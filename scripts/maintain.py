#!/usr/bin/env python3
"""
Hermes 大脑系统 - 知识维护脚本

用法:
    python maintain.py [vault_path]

功能:
    1. 孤立检测 - 找出没有关联的笔记
    2. 关联推荐 - 基于内容推荐关联
    3. 过期检测 - 找出过期的笔记
    4. 统计报告 - 生成统计报告
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
from datetime import datetime, timedelta


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


def extract_created_date(content: str) -> str:
    """从内容中提取创建日期"""
    # 从 frontmatter 中提取
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        date_match = re.search(r'created:\s*(\d{4}-\d{2}-\d{2})', frontmatter)
        if date_match:
            return date_match.group(1)
    
    return None


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
                'tags': extract_tags(content),
                'wikilinks': extract_wikilinks(content),
                'created': extract_created_date(content),
                'content_length': len(content),
            }
        except Exception as e:
            print(f"Error reading {md_file}: {e}")
    
    return notes


def find_isolated_notes(notes: Dict[str, Dict]) -> List[str]:
    """找出孤立的笔记（没有被其他笔记链接，也没有链接到其他笔记）"""
    # 收集所有被链接的笔记
    linked_notes = set()
    for note_data in notes.values():
        for wikilink in note_data['wikilinks']:
            # 解析 wikilink
            if '|' in wikilink:
                target, _ = wikilink.split('|', 1)
            else:
                target = wikilink
            
            # 查找目标笔记
            for path in notes.keys():
                if target in path or path.endswith(f'{target}.md'):
                    linked_notes.add(path)
                    break
    
    # 找出孤立的笔记
    isolated = []
    for path, note_data in notes.items():
        # 如果笔记没有链接到其他笔记，也没有被其他笔记链接
        if not note_data['wikilinks'] and path not in linked_notes:
            isolated.append(path)
    
    return isolated


def find_outdated_notes(notes: Dict[str, Dict], days_threshold: int = 30) -> List[str]:
    """找出过期的笔记（超过指定天数未更新）"""
    outdated = []
    threshold_date = datetime.now() - timedelta(days=days_threshold)
    
    for path, note_data in notes.items():
        if note_data['created']:
            try:
                created_date = datetime.strptime(note_data['created'], '%Y-%m-%d')
                if created_date < threshold_date:
                    outdated.append(path)
            except ValueError:
                pass
    
    return outdated


def recommend_links(notes: Dict[str, Dict], note_path: str) -> List[str]:
    """为笔记推荐关联"""
    note_data = notes.get(note_path)
    if not note_data:
        return []
    
    # 基于标签推荐
    recommendations = []
    note_tags = set(note_data['tags'])
    
    for path, other_data in notes.items():
        if path == note_path:
            continue
        
        # 计算标签相似度
        other_tags = set(other_data['tags'])
        common_tags = note_tags & other_tags
        
        if common_tags:
            recommendations.append({
                'path': path,
                'title': other_data['title'],
                'common_tags': list(common_tags),
                'score': len(common_tags),
            })
    
    # 按分数排序
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    return recommendations[:5]  # 返回前5个推荐


def generate_statistics(notes: Dict[str, Dict]) -> Dict:
    """生成统计信息"""
    # 统计笔记类型
    type_counts = defaultdict(int)
    for note_data in notes.values():
        # 从路径推断类型
        if 'entities' in note_data['path']:
            type_counts['entity'] += 1
        elif 'concepts' in note_data['path']:
            type_counts['concept'] += 1
        elif 'exploration' in note_data['path']:
            type_counts['exploration'] += 1
        elif 'daily' in note_data['path']:
            type_counts['daily'] += 1
        else:
            type_counts['other'] += 1
    
    # 统计标签使用
    tag_counts = defaultdict(int)
    for note_data in notes.values():
        for tag in note_data['tags']:
            tag_counts[tag] += 1
    
    # 统计链接数量
    link_counts = defaultdict(int)
    for note_data in notes.values():
        for wikilink in note_data['wikilinks']:
            link_counts[wikilink] += 1
    
    return {
        'total_notes': len(notes),
        'type_counts': dict(type_counts),
        'tag_counts': dict(tag_counts),
        'link_counts': dict(link_counts),
        'average_links': sum(len(n['wikilinks']) for n in notes.values()) / len(notes) if notes else 0,
    }


def print_statistics(stats: Dict):
    """打印统计信息"""
    print("\n" + "="*60)
    print("Hermes 大脑系统 - 知识维护报告")
    print("="*60)
    
    print(f"\n📊 基本统计:")
    print(f"  - 总笔记数: {stats['total_notes']}")
    print(f"  - 平均链接数: {stats['average_links']:.2f}")
    
    print(f"\n📁 笔记类型分布:")
    for type_name, count in stats['type_counts'].items():
        print(f"  - {type_name}: {count}")
    
    print(f"\n🏷️ 热门标签 (Top 10):")
    sorted_tags = sorted(stats['tag_counts'].items(), key=lambda x: x[1], reverse=True)[:10]
    for tag, count in sorted_tags:
        print(f"  - {tag}: {count}")
    
    print(f"\n🔗 热门链接 (Top 10):")
    sorted_links = sorted(stats['link_counts'].items(), key=lambda x: x[1], reverse=True)[:10]
    for link, count in sorted_links:
        print(f"  - {link}: {count}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python maintain.py scan [vault_path]      # 扫描笔记")
        print("  python maintain.py isolated [vault_path]   # 找出孤立笔记")
        print("  python maintain.py outdated [vault_path]   # 找出过期笔记")
        print("  python maintain.py recommend [vault_path]  # 推荐关联")
        print("  python maintain.py validate [vault_path]   # 验证引用")
        print("  python maintain.py stats [vault_path]      # 生成统计")
        return
    
    command = sys.argv[1]
    vault_path = Path(r"D:\ObsidianVault")
    
    if len(sys.argv) > 2:
        vault_path = Path(sys.argv[2])
    
    if not vault_path.exists():
        print(f"错误: Vault 路径不存在: {vault_path}")
        sys.exit(1)
    
    if command == 'scan':
        notes = scan_vault(vault_path)
        print(f"扫描完成，找到 {len(notes)} 个笔记")
    
    elif command == 'isolated':
        notes = scan_vault(vault_path)
        isolated = find_isolated_notes(notes)
        print(f"找到 {len(isolated)} 个孤立笔记")
        for path in isolated[:10]:
            print(f"  - {path}")
    
    elif command == 'outdated':
        notes = scan_vault(vault_path)
        outdated = find_outdated_notes(notes)
        print(f"找到 {len(outdated)} 个过期笔记")
        for path in outdated[:10]:
            print(f"  - {path}")
    
    elif command == 'recommend':
        notes = scan_vault(vault_path)
        for path in list(notes.keys())[:5]:
            recommendations = recommend_links(notes, path)
            if recommendations:
                print(f"\n{path}:")
                for rec in recommendations:
                    print(f"  - {rec['title']} (共同标签: {', '.join(rec['common_tags'])})")
    
    elif command == 'validate':
        issues = validate_references(vault_path)
        print_reference_issues(issues)
    
    elif command == 'stats':
        notes = scan_vault(vault_path)
        stats = generate_statistics(notes)
        print_statistics(stats)
    
    else:
        print(f"未知命令: {command}")


def validate_references(vault_path: Path) -> Dict:
    """验证引用有效性"""
    import re
    
    notes = scan_vault(vault_path)
    issues = {
        'broken_links': [],      # 断开的链接
        'orphan_notes': [],      # 孤立笔记
        'duplicate_titles': [],  # 重复标题
    }
    
    # 收集所有存在的笔记名
    existing_names = set()
    title_to_paths = defaultdict(list)
    
    for path, note in notes.items():
        existing_names.add(note['title'])
        existing_names.add(Path(path).stem)
        title_to_paths[note['title']].append(path)
    
    # 检查重复标题
    for title, paths in title_to_paths.items():
        if len(paths) > 1:
            issues['duplicate_titles'].append({
                'title': title,
                'paths': paths,
                'reason': f'标题 "{title}" 在 {len(paths)} 个文件中出现',
            })
    
    # 检查断开的链接
    for path, note in notes.items():
        for wikilink in note.get('wikilinks', []):
            # 解析 wikilink
            if '|' in wikilink:
                target, _ = wikilink.split('|', 1)
            else:
                target = wikilink
            
            # 检查是否存在
            found = False
            for other_path, other_note in notes.items():
                if target in other_note['title'] or target in Path(other_path).stem:
                    found = True
                    break
            
            if not found:
                issues['broken_links'].append({
                    'source': path,
                    'target': target,
                    'reason': f'链接 [[{target}]] 不存在',
                })
    
    # 检查孤立笔记
    linked_notes = set()
    for note in notes.values():
        for wikilink in note.get('wikilinks', []):
            if '|' in wikilink:
                target, _ = wikilink.split('|', 1)
            else:
                target = wikilink
            linked_notes.add(target)
    
    for path, note in notes.items():
        stem = Path(path).stem
        if not note.get('wikilinks') and stem not in linked_notes and note['title'] not in linked_notes:
            issues['orphan_notes'].append({
                'path': path,
                'title': note['title'],
                'reason': '没有关联，也没有被其他笔记引用',
            })
    
    return issues


def print_reference_issues(issues: Dict):
    """打印引用问题"""
    print(f"\n{'='*60}")
    print("🔗 引用验证报告")
    print(f"{'='*60}")
    
    # 断开的链接
    if issues['broken_links']:
        print(f"\n❌ 断开的链接 ({len(issues['broken_links'])} 个):")
        for item in issues['broken_links'][:10]:
            print(f"  - {item['source']}: {item['reason']}")
        if len(issues['broken_links']) > 10:
            print(f"  - ... 还有 {len(issues['broken_links']) - 10} 个")
    else:
        print(f"\n✅ 没有断开的链接")
    
    # 孤立笔记
    if issues['orphan_notes']:
        print(f"\n🏝️ 孤立笔记 ({len(issues['orphan_notes'])} 个):")
        for item in issues['orphan_notes'][:10]:
            print(f"  - {item['title']}: {item['reason']}")
        if len(issues['orphan_notes']) > 10:
            print(f"  - ... 还有 {len(issues['orphan_notes']) - 10} 个")
    else:
        print(f"\n✅ 没有孤立笔记")
    
    # 重复标题
    if issues['duplicate_titles']:
        print(f"\n⚠️ 重复标题 ({len(issues['duplicate_titles'])} 个):")
        for item in issues['duplicate_titles'][:5]:
            print(f"  - {item['title']}: {item['reason']}")
    else:
        print(f"\n✅ 没有重复标题")
    
    # 总结
    total_issues = sum(len(v) for v in issues.values())
    print(f"\n{'='*60}")
    print(f"📊 总计: {total_issues} 个引用问题")
    print(f"{'='*60}")
