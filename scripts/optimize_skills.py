#!/usr/bin/env python3
"""
技能自进化脚本（简化版）
优化技能描述，使其更清晰、更简洁
"""

import os
import re
from pathlib import Path

# 技能目录
SKILLS_DIR = Path.home() / ".hermes" / "skills"

# 优化规则
OPTIMIZATIONS = {
    # 去掉冗余前缀
    "Configure, extend, or contribute to": "配置、扩展、贡献",
    "Design one-off HTML artifacts": "快速做 HTML 页面原型",
    "Throwaway HTML mockups": "快速画 HTML 模型稿",
    "Generate project ideas via creative constraints": "用创意约束生成项目点子",
    "Humanize text: strip AI-isms and add real voice": "去 AI 味——把机器文字改成像人写的",
    "54 real design systems": "54 个真实设计系统参考",
    "Taste-as-Code system with design vibe switching": "设计质量评分 + 风格切换",
    "Deep audit before GitHub push": "推送前深度审计",
    "Systematically finds and fixes bugs": "系统化找 bug",
    "Builds production-ready REST API endpoints": "构建生产级 REST API",
    "Generate or edit images through Hermes Web UI": "通过 Web UI 生成图片",
    "Audit local AI coding-agent sessions": "审计 Agent 会话",
    "Create rich diagrams, data visualizations": "创建图表和数据可视化",
    "Full-cycle AI coding skill": "全流程编码",
    "Animate a local image into a short mp4 video": "图片转短视频",
    "Create AI videos with HyperFrames": "用 HTML/CSS/JS 做 AI 视频",
    "Create editable AI video projects": "用 React 做 AI 视频",
    "Vibe Coding 工作流": "Vibe Coding 编码工作流",
    "Decomposition playbook + anti-temptation rules": "看板调度——拆任务分配",
    "Pitfalls, examples, and edge cases": "看板工人——执行任务",
    "Webhook subscriptions: event-driven agent runs": "Webhook 事件触发 Agent",
    "Hermes Agent 数据管理与记忆优化规范": "D 盘数据管理、记忆自清洁",
    "Managing D: drive data policy": "D 盘数据组织策略",
    "IMAP/SMTP email from terminal": "终端收发邮件",
    "Clone/create/fork repos; manage remotes, releases": "克隆/创建/fork 仓库",
    "Review PRs: diffs, inline comments": "审查 PR——看 diff、写评论",
    "GitHub PR lifecycle: branch, commit, open, CI, merge": "PR 全流程",
    "Create, triage, label, assign GitHub issues": "管理 Issue",
    "GitHub auth setup: HTTPS tokens, SSH keys": "GitHub 认证配置",
    "Inspect codebases w/ pygount: LOC, languages, ratios": "扫描代码库统计",
    "MCP client: connect servers, register tools": "MCP 客户端",
    "Search/download GIFs from Tenor": "搜索下载 GIF",
    "HeartMuLa: Suno-like song generation": "AI 写歌",
    "Spotify: play, search, queue, manage playlists": "控制 Spotify",
    "YouTube transcripts to summaries, threads, blogs": "YouTube 字幕转摘要",
    "Audio spectrograms/features": "音频频谱分析",
    "llama.cpp local GGUF inference": "本地跑 GGUF 模型",
    "HuggingFace hf CLI: search/download/upload models": "HuggingFace 模型下载",
    "Read, search, create, and edit notes": "操作 Obsidian 笔记",
    "Gmail, Calendar, Drive, Docs, Sheets": "Google 全家桶",
    "Create, read, edit .pptx decks": "做 PPT",
    "Extract text from PDFs/scans": "PDF 提取文字",
    "Search arXiv papers by keyword, author, category": "搜索 arXiv 论文",
    "Karpathy's LLM Wiki: build/query interlinked markdown KB": "Karpathy 知识库",
    "Execute plans via delegate_task subagents": "子 Agent 执行计划",
    "4-phase root cause debugging": "4 阶段根因调试",
    "TDD: enforce RED-GREEN-REFACTOR": "TDD 红绿重构",
    "Throwaway experiments to validate an idea": "一次性实验验证想法",
    "Pre-commit review: security scan, quality gates": "提交前代码审查",
    "Debug Hermes TUI slash commands": "调试 Hermes TUI",
    "Author in-repo SKILL.md: frontmatter, validator": "写 SKILL.md",
    "Write implementation plans: bite-sized tasks": "写实施计划",
    "Plan mode: write markdown plan": "计划模式——只写不执行",
    "Iterative Python via live Jupyter kernel": "Jupyter 交互式 Python",
    "Debug Node.js via --inspect + Chrome DevTools": "Node.js 调试",
    "Debug Python: pdb REPL + debugpy remote": "Python 调试",
    "Modify, debug, or extend the s6-overlay supervision tree": "Docker s6 进程管理",
}

def optimize_skill_description(skill_path: Path):
    """优化单个技能的描述"""
    try:
        content = skill_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  ❌ 读取失败: {e}")
        return False
    
    # 提取 frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        print(f"  ❌ 无 frontmatter")
        return False
    
    frontmatter = match.group(1)
    body = content[match.end():]
    
    # 提取 description
    desc_match = re.search(r'description:\s*["\']?(.*?)["\']?\s*$', frontmatter, re.MULTILINE)
    if not desc_match:
        print(f"  ❌ 无 description")
        return False
    
    original_desc = desc_match.group(1).strip()
    
    # 应用优化规则
    optimized_desc = original_desc
    for old, new in OPTIMIZATIONS.items():
        if old in optimized_desc:
            optimized_desc = optimized_desc.replace(old, new)
            break
    
    # 如果没有变化，跳过
    if optimized_desc == original_desc:
        print(f"  ⏭️  无需优化")
        return False
    
    # 替换 description
    new_frontmatter = frontmatter.replace(
        f'description: "{original_desc}"',
        f'description: "{optimized_desc}"'
    )
    
    # 写入文件
    new_content = f"---\n{new_frontmatter}\n---{body}"
    skill_path.write_text(new_content, encoding='utf-8')
    
    print(f"  ✅ 优化完成")
    print(f"     原始: {original_desc[:50]}...")
    print(f"     优化: {optimized_desc[:50]}...")
    return True

def main():
    print("=" * 60)
    print("  技能自进化（简化版）")
    print("=" * 60)
    print()
    
    optimized_count = 0
    total_count = 0
    
    # 遍历所有技能
    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        total_count += 1
        skill_name = skill_md.parent.name
        
        print(f"📁 {skill_name}")
        
        if optimize_skill_description(skill_md):
            optimized_count += 1
    
    print()
    print("=" * 60)
    print(f"  优化完成: {optimized_count}/{total_count} 个技能")
    print("=" * 60)

if __name__ == "__main__":
    main()
