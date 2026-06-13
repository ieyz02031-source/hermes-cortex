---
name: hermes-cortex
description: "Hermes 大脑系统 — 基于 Karpathy LLM Wiki 模式 + 知识图谱 + 语义检索的 Agent 记忆与知识管理系统"
trigger: "当需要管理知识、检索记忆、整理笔记、构建关联图谱、或进行知识驱动的决策时使用"
version: "1.3.0"
created: 2026-06-13
tags: [knowledge-management, memory, graph, obsidian, RAG, second-brain]
---

# Hermes 大脑系统

> 基于 Karpathy LLM Wiki 模式 + 知识图谱 + 语义检索的 Agent 记忆与知识管理系统

## 核心理念

**Karpathy LLM Wiki 模式**：别每次都去翻原始资料，而是让 LLM 一点点维护一个长期的 wiki。知识像复利一样累积。

**核心设计原则**：🧠 **"大脑"必须是自动的**。一个需要手动触发的"大脑"不是大脑，只是一堆脚本。所有知识管理操作（检索、学习、更新、维护）必须在后台自动运行，用户无感知。

**三大支柱**：
1. **记忆层** — 短期（热缓存）+ 中期（会话记忆）+ 长期（持久化知识）
2. **知识图谱** — 实体 + 概念 + 关联关系的网络
3. **检索层** — 语义搜索 + BM25 + 关联图遍历

**自动化三原则**：
1. **提问自动检索** — 用户问问题时，先检索知识库再回答
2. **学习自动记录** — 学到新知识时，自动创建笔记并更新索引
3. **对话结束自动维护** — 每次对话结束，自动更新热缓存和检查孤立笔记

---

## 架构设计

```
输入层（用户对话、外部资料、工具结果、系统事件）
    ↓
处理层（信息抽取、知识融合、图谱构建、索引更新）
    ↓
存储层（热缓存、索引、图谱、日志、笔记库）
    ↓
检索层（语义搜索、关键词搜索、图谱遍历、元数据过滤）
    ↓
输出层（回答、建议、洞察、行动）
```

---

## 笔记结构规范

### 实体笔记

描述具体的人、工具、项目、组织。

```markdown
---
title: [实体名称]
type: entity
created: YYYY-MM-DD
tags: [entity, 类别]
关联: [[相关笔记1]] | [[相关笔记2]]
---

# [实体名称]

## 概述
简要描述这个实体是什么。

## 属性
- **类型**: 人/工具/项目/组织
- **状态**: 活跃/归档/废弃

## 关联
- [[相关实体1]] — 关系描述
```

### 概念笔记

描述抽象的想法、方法论、设计模式。

```markdown
---
title: [概念名称]
type: concept
created: YYYY-MM-DD
tags: [concept, 领域]
关联: [[相关笔记1]] | [[相关笔记2]]
---

# [概念名称]

## 定义
清晰定义这个概念。

## 核心原则
1. 原则1
2. 原则2

## 相关概念
- [[相关概念1]] — 关系描述
```

### 探索笔记

描述研究过程、发现、分析。

```markdown
---
title: [探索主题]
type: exploration
created: YYYY-MM-DD
tags: [exploration, 主题]
关联: [[相关笔记1]] | [[相关笔记2]]
---

# [探索主题]

## 背景
为什么进行这次探索。

## 发现
详细描述。

## 行动项
- [ ] 行动1
- [ ] 行动2
```

### 日记笔记

记录日常任务、状态、思考。

```markdown
---
title: YYYY-MM-DD
type: daily
created: YYYY-MM-DD
tags: [daily]
---

# YYYY-MM-DD

## 任务
- [x] 完成的任务
- [ ] 未完成的任务
```

---

## 脚本工具

所有脚本位于 `D:\Hermes\skills\hermes-cortex\scripts\`

### 1. 热缓存 (`hot_cache.py`)

自动扫描最近修改的笔记，更新 `index.md` 顶部的热缓存区域。

```bash
python scripts/hot_cache.py
```

### 2. 语义索引 (`semantic_index.py`)

用 `all-MiniLM-L6-v2` 模型生成笔记的向量嵌入，存储到 SQLite，支持语义相似度搜索。

```bash
python scripts/semantic_index.py index    # 构建索引
python scripts/semantic_index.py search "查询内容"  # 语义搜索
python scripts/semantic_index.py stats    # 显示统计
```

### 3. 自动研究 (`auto_research.py`)

分析现有知识，发现空白和薄弱点，生成研究建议。

```bash
python scripts/auto_research.py discover  # 发现知识空白
python scripts/auto_research.py report    # 自进化报告
python scripts/auto_research.py suggest   # 研究建议
```

### 4. 知识图谱 (`build_graph.py`)

从 Obsidian Vault 中抽取实体和关系，构建知识图谱。

```bash
python scripts/build_graph.py
```

### 5. 知识检索 (`retrieve.py`)

三层检索（热缓存、索引、图谱），返回相关笔记。

```bash
python scripts/retrieve.py "查询内容"
```

### 6. 知识维护 (`maintain.py`)

孤立检测、关联推荐、过期清理、统计报告、引用验证。

```bash
python scripts/maintain.py validate   # 验证引用
python scripts/maintain.py isolated   # 找出孤立笔记
python scripts/maintain.py stats      # 生成统计
```

### 7. 自进化引擎 (`evolve.py`)

完整的自进化循环：发现空白 → 搜索补充 → 创建笔记 → 更新索引 → 更新热缓存。

```bash
python scripts/evolve.py run      # 运行一次自进化循环
python scripts/evolve.py dry-run  # 干运行（不创建笔记）
python scripts/evolve.py status   # 显示自进化状态
```

### 8. Cron 任务 (`cron.py`)

每天自动运行自进化循环。

```bash
python scripts/cron.py setup    # 设置 cron 任务
python scripts/cron.py remove   # 移除 cron 任务
python scripts/cron.py status   # 查看 cron 状态
python scripts/cron.py run      # 手动运行一次
```

### 9. 自动化 Hook (`brain_hook.py`)

**这是让 Hermes Brain 成为真正"大脑"的关键脚本。**

在每次对话结束时自动运行，更新热缓存和索引。

```bash
python scripts/brain_hook.py
```

**自动化流程**：
1. 更新热缓存（hot_cache.py）
2. 检查语义索引是否过期（>24小时则更新）
3. 检查孤立笔记（maintain.py）
4. 每 10 次对话自动检查优化（auto_optimize.py）

**关键设计**：用户无感知，后台自动运行。

### 10. 自动优化 (`auto_optimize.py`)

**当知识库接近性能瓶颈时自动触发优化。**

```bash
python scripts/auto_optimize.py
```

**警戒线**：

| 指标 | 阈值 | 触发优化 |
|------|------|----------|
| 笔记数 | 300 | 归档 90 天未修改的笔记 |
| 索引大小 | 30MB | 增量索引优化 |
| 孤立笔记 | 20 | 清理孤立笔记 |
| 无效链接 | 50 | 清理无效链接 |
| 热缓存年龄 | 24h | 更新热缓存 |

**触发方式**：`brain_hook.py` 每 10 次对话自动调用一次。

---

## 自进化循环

```
discover（发现空白）
    ↓
suggest（生成建议）
    ↓
web_search（搜索补充）
    ↓
LLM 抽取（实体和概念）
    ↓
创建笔记（write_file）
    ↓
更新索引（semantic_index.py）
    ↓
更新热缓存（hot_cache.py）
    ↓
回到 discover
```

---

## 工具集成

### Obsidian 集成

笔记存储位置：`D:\ObsidianVault\`

```
D:\ObsidianVault\
├── index.md              # 主索引
├── SCHEMA.md             # 结构规范
├── log.md                # 操作日志
├── concepts/             # 概念笔记
├── entities/             # 实体笔记
├── raw/                  # 原始笔记
│   ├── exploration/      # 探索笔记
│   ├── research/         # 研究笔记
│   └── heartbeat/        # 心跳笔记
├── daily/                # 日记
└── hermes/               # Hermes 相关
```

### 记忆工具集成

```bash
memory(action='add', target='memory', content='...')
memory(action='replace', target='memory', old_text='...', new_text='...')
memory(action='remove', target='memory', old_text='...')
```

### 检索工具集成

```bash
search_files(pattern='...', target='content', path='D:\\ObsidianVault')
read_file(path='D:\\ObsidianVault\\index.md')
write_file(path='D:\\ObsidianVault\\new-note.md', content='...')
```

### Phoenix 集成

Phoenix（不死鸟）桌面控制工具可以用于：
- **桌面截图** — 捕获桌面状态
- **文件操作** — 读写文件
- **代码执行** — 运行 Python/shell
- **浏览器控制** — 执行 JS 和扫描网页

---

## 最佳实践

### 笔记命名规范

- **实体笔记**: `tool-name.md`, `person-name.md`, `project-name.md`
- **概念笔记**: `concept-name.md`, `methodology-name.md`
- **探索笔记**: `YYYY-MM-DD-exploration-topic.md`
- **日记**: `YYYY-MM-DD.md`

### 标签使用规范

- 每个笔记最多 3 个标签
- 标签按用途分类，不是按主题
- 新标签必须在 SCHEMA.md 中注册

### 关联维护规范

- 每个笔记至少有 1 个关联
- 关联关系要有描述（不只是链接）
- 定期检查关联的有效性

### 热缓存更新规范

- 每次会话后更新热缓存
- 热缓存只保留最近 500 字
- 热缓存是最近上下文的摘要

---

## ⚠️ 关键 Pitfall

### 0. 一口气做完，不留"下一步"

用户明确拒绝任何形式的"待实现"、"下一步"、"计划中"。必须一次性完成所有功能，不留 TODO。
- ❌ "下一步建议：可以添加 X 功能"
- ❌ "待实现：Y 功能"
- ❌ "计划中：Z 优化"
- ❌ "还有建议或者下一步打算" — 用户说这句话时，意思是"把能做的都做完"

## 关键陷阱

### 0. 彻底融合 Hermes（非外挂模式）

Hermes Brain 不是"外挂脚本"，而是 Hermes 的"大脑"。必须通过以下机制融合：

**Shell Hooks**（自动生命周期）：
```yaml
# 在 AppData/Local/hermes/config.yaml 的 hooks: 下配置
hooks:
  on_session_start:
    - command: "python D:/Hermes/skills/hermes-cortex/scripts/hook_session_start.py"
      timeout: 30
  on_session_end:
    - command: "python D:/Hermes/skills/hermes-cortex/scripts/hook_session_end.py"
      timeout: 60
hooks_auto_accept: true
```

**allowlist**（首次安全确认）：
```json
// AppData/Local/hermes/shell-hooks-allowlist.json
{"approvals": [{"event":"on_session_start","command":"python D:/Hermes/skills/hermes-cortex/scripts/hook_session_start.py","approved_at":"..."}]}
```

**SOUL.md**（注入到 system prompt）：
在 `~/.hermes/SOUL.md` 中添加"大脑系统"章节，让 Agent 知道它有 brain 并主动使用。

**验证**：`hermes hooks list` 应显示 ✓ allowed，`hermes hooks doctor` 应显示 All healthy。

详见 `references/hermes-hooks-integration.md`。

### 1. 不要用 C 盘路径

用户明确拒绝 C 盘存储。所有文件必须放在 D 盘：
- **Skill 目录**: `D:\Hermes\skills\hermes-cortex\`
- **笔记库**: `D:\ObsidianVault\`
- **项目目录**: `D:\Hermes\`

### 2. Python 3.12 vs 3.13 环境

语义索引需要 Python 3.12 环境，因为 `sentence-transformers` 装在 Python 3.12 中：

```bash
# 语义索引用 Python 3.12
/c/Users/20716/AppData/Local/Programs/Python/Python312/python.exe scripts/semantic_index.py index

# 其他脚本用默认 python
python scripts/hot_cache.py
python scripts/auto_research.py
```

### 3. f-string 中不要有真实换行

Python f-string 不能有真实换行，必须用 `\n`：
```python
# ❌ 错误
print(f"
{text}")

# ✅ 正确
print(f"\n{text}")
```

### 4. GitHub README 质量要求

上传 GitHub 前必须参考热门项目的 README 格式（headroom 20KB、claude-obsidian 37KB、swarmvault 48KB）。README 必须像"说明书"，包含：
- 环境要求表格
- 分平台安装指南
- 故障排除
- FAQ
- 竞品对比
- 路线图

详见 `references/github-readme-pattern.md`。

### 5. 不要留"下一步"

用户明确拒绝"下一步建议"、"待实现"、"计划中"等字眼。所有功能一次性做完，不留 TODO。

### 6. 一口气做完，不要分步确认

用户偏好批量处理，不要问"继续吗"、"下一步"、"要我做吗"。一次性完成所有操作，不留"待实现"或"下一步"。

### 5. 不要创建 Web UI / Dashboard

用户明确拒绝 Web UI 仪表板，不要创建 dashboard.py 或类似的可视化工具。

### 6. Skill 自检流程

打包前必须自检：
- 用 `grep "^##"` 检查 SKILL.md 是否有重复章节
- 删除冗余文件（COMPLETION_REPORT.md、README.md 在 skill 目录中不需要）
- `rm -rf scripts/__pycache__` 清理缓存
- 确认所有路径指向 D 盘
- `python -m py_compile scripts/*.py` 语法检查

### 7. GitHub README 格式要求

用户对 README 质量要求很高。参考 headroom (20KB) 和 claude-obsidian (37KB) 的格式：
- ASCII art logo 开头
- 一句话介绍 + 快速导航链接
- 数据说话（具体数字、统计）
- 用 `<details>` 折叠详细内容
- 竞品对比表格
- "When to use · When to skip" 章节
- Requirements 表格（最低/推荐配置）
- 不要写废话，信息密度要高

详见 `references/github-readme-pattern.md`。

### 8. GitHub 上传工作流

当 `git push` 因网络问题（代理、防火墙）失败时，用 `mcp_github_create_or_update_file` 逐个上传：

```python
# 流程：
# 1. 创建仓库：mcp_github_create_repository
# 2. 逐个文件上传：mcp_github_create_or_update_file
# 3. 检查状态：curl -s "https://api.github.com/repos/{owner}/{repo}/contents"
```

**⚠️ 关键陷阱：更新已有文件必须传 sha 参数**

GitHub API 的 `PUT /contents/{path}` 接口：
- **创建新文件**：不需要 `sha` 参数
- **更新已有文件**：**必须**传入当前文件的 `sha` 参数，否则 GitHub 拒绝更新

```python
# ❌ 错误：更新文件不传 sha → GitHub 返回 422 或静默失败
mcp_github_create_or_update_file(
    path="README.md",
    content=new_content,
    message="Update README"
)

# ✅ 正确：先获取 sha，再更新
# Step 1: 获取当前文件的 sha
result = mcp_github_get_file_contents(owner=owner, repo=repo, path="README.md")
current_sha = result['sha']

# Step 2: 用 sha 更新
mcp_github_create_or_update_file(
    path="README.md",
    content=new_content,
    message="Update README",
    sha=current_sha  # ← 这个是关键
)
```

**工作流顺序（避免重复工作）**：
1. 先在本地写好完整内容
2. 验证内容质量（大小、章节、格式）
3. 一次性上传到 GitHub
4. 上传后验证文件大小是否匹配

**不要**：先上传简化版 → 再更新完整版（浪费时间，容易出错）

**上传顺序**：
- 根目录文件 → 子目录文件
- 每个文件单独上传，不要用 push_files（会报空仓库错误）
- 文件内容直接传，不需要 base64 编码
- 每次上传会自动 commit

详见 `references/github-upload-workflow.md`。

### 9. Skill 打包前自检清单

打包/上传前必须完成：

```bash
# 1. 检查重复章节
grep "^##" SKILL.md | sort | uniq -d

# 2. 语法检查
python -m py_compile scripts/*.py

# 3. 清理缓存
rm -rf scripts/__pycache__

# 4. 检查路径
grep -r "C:\\\\" . && echo "❌ 发现 C 盘路径" || echo "✅ 全部 D 盘"

# 5. 检查文件完整性
find . -type f | wc -l  # 确认文件数量

# 6. 删除冗余文件
rm -f COMPLETION_REPORT.md README.md  # skill 目录中不需要
```

---

## GitHub 热榜对比

详见 `references/github-comparison.md` — 包含 20+ 个项目的详细对比分析、功能矩阵、优先级路线图。

## GitHub README 格式

详见 `references/github-readme-format.md` — 参考 claude-obsidian (6.6k⭐) 的专业 README 格式。

---

## 参考资源

### 设计模式

详见 `references/automation-pattern.md` — **"Brain" 类 skill 必须是自动的**，不要让用户手动触发。

### GitHub 项目

| 项目 | 描述 | 链接 |
|------|------|------|
| **claude-obsidian** | 自组织 AI 第二大脑 | https://github.com/AgriciDaniel/claude-obsidian |
| **swarmvault** | 本地优先 LLM Wiki | https://github.com/swarmclawai/swarmvault |
| **kajet** | Obsidian 语义搜索 MCP | https://github.com/jpalczewski/kajet |
| **Karpathy-wiki-graph** | 企业级知识图谱 Agent | https://github.com/LCccode/Karpathy-wiki-graph |
| **graph-memory-mcp** | 语义持久化知识图谱记忆 | https://github.com/river-ai-lab/graph-memory-mcp |
| **hermes-cortex** | Hermes 配置、技能、记忆层 | https://github.com/lukemcqueen/hermes-cortex |
| **PRISM** | Agent 无关的编排系统 | https://github.com/racar/PRISM |

### 中文资源

| 资源 | 描述 | 链接 |
|------|------|------|
| **AI Agent 记忆机制综述** | 知乎专栏 | https://zhuanlan.zhihu.com/p/1995813479794353043 |
| **2026年Agent记忆系统方案横评** | 腾讯云 | https://cloud.tencent.com/developer/article/2665379 |
| **AI Agent 记忆技术演进全解析** | CSDN | https://tianqi.csdn.net/69f58bda0a2f6a37c5a756ea.html |
| **Agent Memory 技术演进** | GitHub Blog | https://github.com/kejun/blogpost/blob/main/agent-memory-evolution-2026.md |

### GitHub README 格式

详见 `references/github-readme-format.md` — 基于 claude-obsidian (6.6k⭐) 的专业 README 结构模板。

### Karpathy LLM Wiki 原文

https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

---

## 总结

Hermes 大脑系统是一个基于 Karpathy LLM Wiki 模式的知识管理系统，它通过：

1. **结构化存储** — 实体、概念、探索、日记四种笔记类型
2. **知识图谱** — 实体 + 关系的网络结构
3. **三层检索** — 热缓存 + 索引 + 图谱的检索架构
4. **自动维护** — 孤立检测、关联推荐、过期清理、引用验证
5. **自进化循环** — discover → suggest → search → extract → create → update

实现了知识的持续累积和智能检索，让 Hermes 真正拥有一个"大脑"。

---

## Hermes 原生融合（Shell Hooks）

Hermes 有原生 Shell Hooks 系统，可以让 brain 真正融入 Hermes 生命周期。

**配置方式**（在 `~/.hermes/config.yaml`）：

```yaml
hooks:
  on_session_end:
    - command: "C:/Users/20716/AppData/Local/Programs/Python/Python312/python.exe"
      args: ["D:/Hermes/skills/hermes-cortex/scripts/brain_hook.py"]
      timeout: 60
  on_session_start:
    - command: "C:/Users/20716/AppData/Local/Programs/Python/Python312/python.exe"
      args: ["D:/Hermes/skills/hermes-cortex/scripts/hot_cache.py"]
      timeout: 30
```

**可用事件**：`on_session_start`, `on_session_end`, `on_session_finalize`, `post_tool_call`, `pre_llm_call`, `post_llm_call`, `subagent_start`, `subagent_stop`

**验证**：`hermes hooks list` / `hermes hooks test <event>` / `hermes hooks doctor`

详见 `references/hermes-hooks-integration.md`。

---

## 自动化工作流

```
用户提问
    ↓
自动检索（retrieve.py）
    ↓
回答问题
    ↓
学习新知识
    ↓
自动创建笔记（evolve.py）
    ↓
更新索引（semantic_index.py）
    ↓
更新热缓存（hot_cache.py）
    ↓
等待下一次提问
```

---

## ⚠️ 关键 Pitfall（续）

### 10. "大脑"必须是全自动的

用户明确指出："这个skill不是大脑吗，还要特定使用吗"。**一个需要手动触发的"大脑"不是大脑，只是一堆脚本。**

- ❌ 提供 `python scripts/xxx.py` 命令让用户手动跑
- ❌ 问用户"要我运行这个吗"
- ✅ 配置 Shell Hooks，会话结束自动运行
- ✅ 配置 Windows 计划任务，每天自动运行自进化循环
- ✅ 所有操作后台执行，用户无感知

### 11. 更新 cron 时间要改 3 个地方

当用户要求改变 cron 时间时，需要同时更新：
1. `scripts/cron.py` — Python 脚本中的 crontab 命令
2. `scripts/cron_task.sh` — Shell 脚本中的注释
3. GitHub — 上传更新后的文件

### 12. Windows 计划任务用 PowerShell cmdlet

创建 Windows 计划任务时，用 PowerShell cmdlet 而不是 XML：

```powershell
# ✅ 正确：用 cmdlet
$action = New-ScheduledTaskAction -Execute 'path\to\script'
$trigger = New-ScheduledTaskTrigger -Daily -At '21:00'
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName 'Task Name' -Action $action -Trigger $trigger -Settings $settings

# ❌ 错误：用 XML（编码问题导致失败）
Register-ScheduledTask -TaskName 'Task Name' -Xml 'path\to\xml'
```

---

## 日志

自动化日志保存在：`D:\ObsidianVault\.hermes_logs\`
