# 技能清理工作流

## 使用工具

**hermes-skill-audit** — 安装位置：`D:\Hermes\skills\hermes-skill-audit\`

```bash
# 完整审计
python D:/Hermes/skills/hermes-skill-audit/scripts/audit.py

# 快速摘要
python D:/Hermes/skills/hermes-skill-audit/scripts/audit.py --summary

# 预览清理
python D:/Hermes/skills/hermes-skill-audit/scripts/audit.py --dry-run

# 执行清理
python D:/Hermes/skills/hermes-skill-audit/scripts/audit.py --fix
```

## 清理流程

### 1. 运行审计
```bash
python scripts/audit.py --summary
```

### 2. 分析结果
- 查看技能数量和 token 消耗
- 检查重复技能
- 检查过期技能

### 3. 列出所有技能（中文注释）
```python
import sys
sys.path.insert(0, 'scripts')
from audit import scan_skills, HERMES_SKILLS_DIR
from collections import defaultdict

skills = scan_skills(HERMES_SKILLS_DIR)
categories = defaultdict(list)
for s in skills:
    categories[s['category']].append(s)

for cat, cat_skills in sorted(categories.items()):
    print(f"\n📁 {cat.upper()} ({len(cat_skills)} 个, ~{sum(s['estimated_tokens'] for s in cat_skills):,} tokens)")
    print("| 技能 | tokens | 干嘛的 |")
    print("|------|--------|--------|")
    for s in sorted(cat_skills, key=lambda x: x['name']):
        desc = s['description'][:50] if s['description'] else '(无描述)'
        print(f"| {s['name']} | {s['estimated_tokens']:,} | {desc} |")
```

### 4. 标记删除/保留

**删除标准**：
- 用户场景不匹配（Windows 用户删 Apple/macOS、不搞音乐删 media、不用 Docker 删 s6）
- 从没用过且无明确场景的（gaming、gifs、libreoffice 等 Antigravity 装的）
- 大型项目模板（web/ 176MB，需要时再装）

**保留标准**：
- Agent 日常工作流（plan、bug-hunter、systematic-debugging、squirrel、hermes-agent-skill-authoring）
- 用户实际在用的核心技能（hermes-cortex、design、taste-critic、research、obsidian）

### 5. 用户确认
列出"建议删除"清单后，**必须问用户确认**，不能直接执行。

### 6. 执行清理
```bash
# 删除技能
rm -rf ~/.hermes/skills/category/skill-name

# 合并技能（如需要）
# 先读取两个技能内容，合并后删除一个
```

### 7. 验证结果
```bash
python scripts/audit.py --summary
```

## 关键 Pitfall

### 1. 不要过度删除 Agent 自身在用的技能
用户会问"你平时用不到吗？"——plan、bug-hunter、systematic-debugging、squirrel、hermes-agent-skill-authoring 等是 Agent 日常工作流的一部分，必须保留。

### 2. 两个目录都要清理
技能可能在两个地方：
- `~/.hermes/skills/` — Hermes 实际读取的位置
- `D:\Hermes\skills\` — 用户的工作目录

清理时必须两个都清理，否则审计结果不准确。

### 3. 检查子目录
技能可能在子目录中（如 `mlops/evaluation/xxx`），不要只检查顶层目录。

用 `find ~/.hermes/skills -name "SKILL.md"` 查找所有技能。

### 4. 优化后检查低质量描述
优化脚本可能把描述改得太短（<25 字符），导致审计工具标记为"low-quality"。

### 5. 执行前先讲清楚流程
用户说"讲清楚点，是什么流程"时，先用通俗语言解释整个流程，再问"要从哪一步开始？"，用户确认后才执行。

## 实际案例

### 2026-06-15 清理记录

**清理前**：117 个技能，~300,265 tokens/轮
**清理后**：44 个技能，~113,364 tokens/轮
**减少**：-62%

**删除的类别**：
- Apple (5) — Windows 用户不需要
- Gaming (2) — 跟场景无关
- Smart-Home (1) — 不用
- Social-Media (1) — 不用
- Red-Teaming (1) — 不用
- media (5) — 不搞音乐、不搜 GIF
- data-science (1) — 不做数据科学
- email (1) — 不用终端邮件
- Creative 大部分 (16) — 只保留 5 个有用的
- MLOps 大部分 (7) — 只保留 2 个
- Productivity 大部分 (6) — 只保留 3 个
- Research 部分 (3) — 删除大文件
- Autonomous-AI-Agents 大部分 (4) — 只保留 hermes-agent
- s6 调试工具 (3) — 不用 Docker/Node.js/Python 调试
- Root 视频工具 (3) — 不做视频
- agenttrace (1) — 不用

**合并**：
- devops/data-organization + devops/hermes-data-management → hermes-data-management
