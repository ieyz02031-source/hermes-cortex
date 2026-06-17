# Memory 优化工作流

## 概述

当 memory 接近 10,000 字符上限时，执行详细→索引迁移。核心思路：详细内容存 engram，memory 只保留一句话索引。

## 完整流程

### Phase 1：识别可迁移条目

扫描 memory 中的条目，识别含详细描述（>100字符）的条目：

```
可迁移特征：
- 包含 "详见"、"参考"、"步骤" 等详细描述
- 包含路径、配置、命令等技术细节
- 包含列表、表格等结构化内容
- 超过 100 字符的条目
```

### Phase 2：存入 engram

逐个用 `mem_save` 保存详细内容到 engram：

```bash
cd D:/Hermes/skills/hermes-cortex && echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"mem_save","arguments":{"title":"My Title","content":"**What**: ...\\n**Why**: ...\\n**Where**: ...\\n**Learned**: ...","type":"learning","topic_key":"my_key"}},"id":1}' | D:/Hermes/tools/engram/engram.exe mcp --tools=agent
```

**关键点**：
- 必须 `cd` 到 git repo 目录（engram 通过 git remote 自动识别 project）
- content 中的换行必须用 `\\n`（JSON 转义），不能用真实换行
- 逐个保存，不要批量——每次 terminal 调用一个 mem_save
- Python subprocess 在 Windows 上有 UTF-8 编码问题，必须用 terminal 工具

### Phase 3：压缩 memory 条目

用 `memory(action='replace')` 替换为一句话索引：

```python
# 用条目开头几个词作为 old_text，足够唯一即可
memory(action='replace', 
       old_text='SKILL_CLEANUP_DONE (2026-06-14)', 
       new_text='SKILL_CLEANUP_DONE: 详见engram搜索"skill cleanup"或Obsidian D:\\Hermes\\skills\\hermes-skill-audit\\')
```

**old_text 技巧**：
- 用条目开头几个词，足够唯一即可
- 整段文字含转义字符容易匹配失败
- 如果匹配失败，缩短 old_text 再试

### Phase 4：验证

```bash
# 检查 memory 使用率
memory(action='add', target='memory', content='TEST: 验证')  # 查看 usage
memory(action='remove', target='memory', old_text='TEST: 验证')

# 检查 engram 记忆数
cd D:/Hermes/skills/hermes-cortex && echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"mem_context","arguments":{"scope":"all"}},"id":1}' | D:/Hermes/tools/engram/engram.exe mcp --tools=agent

# 测试 engram 搜索
cd D:/Hermes/skills/hermes-cortex && echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"mem_search","arguments":{"query":"关键词","limit":5}},"id":1}' | D:/Hermes/tools/engram/engram.exe mcp --tools=agent
```

### Phase 5：记忆系统自动化（2026-06-15 新增）

完成三层迁移后，部署自动化脚本持续维护：

```bash
# 自动整理：去重、压缩、淘汰低优先级条目
python D:/Hermes/skills/hermes-cortex/scripts/memory_auto_cleanup.py

# 记忆衰减：基于访问频率和时间衰减记忆权重
python D:/Hermes/skills/hermes-cortex/scripts/memory_decay.py

# 跨层同步：扫描 memory 条目在 engram 中的存在性，检测不同步
python D:/Hermes/skills/hermes-cortex/scripts/memory_sync.py
```

**记忆衰减等级**：
| 等级 | 时间窗口 | 权重 | 处理 |
|------|---------|------|------|
| High | 7天内活跃 | 100% | 保持 |
| Medium | 30天内活跃 | 70% | 标记衰减 |
| Low | 90天内活跃 | 30% | 建议归档 |
| Stale | 90天+不活跃 | 10% | 建议删除 |

**三层同步检查逻辑**：
- memory↔engram：每条 memory 条目检查 engram 中是否有详细版本
- memory↔Obsidian：每条 memory 条目检查 Obsidian 中是否有对应文档
- 输出不同步报告，建议操作

## 实测效果

### 第一轮迁移（2026-06-15）
- 迁移 15 个详细条目到 engram
- memory 使用率：68% → 46%（-22%）
- 释放 ~2,200 字符

### 第二轮深度优化（2026-06-15）
- 进一步压缩剩余详细条目
- memory 使用率：46% → 38%（-8%）
- 总释放 ~3,000 字符
- engram 记忆数：2 → 16（+700%）

### 自动化部署（2026-06-15）
- 新增 3 个自动化脚本
- memory_auto_cleanup.py：去重 + 淘汰低优先级
- memory_decay.py：4 级衰减（High/Medium/Low/Stale）
- memory_sync.py：跨层同步检查

## 系统完整性验证（2026-06-15 最终）

| 组件 | 状态 | 指标 |
|------|------|------|
| memory 系统 | ✅ 正常 | 38 条目，39% 使用率 |
| engram 系统 | ✅ 正常 | 16 个记忆，语义搜索正常 |
| Obsidian 系统 | ✅ 正常 | 文档存储正常 |
| 知识图谱 | ✅ 正常 | 11 实体，11 关系 |
| 智能检索 | ✅ 正常 | 预测需求、关系遍历、路径查找 |
| 自动化脚本 | ✅ 正常 | 9 个脚本全部运行成功 |

## Memory 自管理工作流（2026-06-15 新增）

用户说"集合你的记忆自己打理好"时，执行完整的自管理流程：

### Phase 6：去重扫描

扫描所有 memory 条目，识别重复和冗余：

```
去重信号：
- 同一关键词出现在 3+ 条目中（如 THINK_BEFORE_ACT 出现 3 次）
- 多个 MEMORY_SYSTEM_* 变体（MEMORY_SYSTEM_COMPLETE, MEMORY_SYSTEM_UPGRADE_* 等）
- 含义相同但措辞不同的条目
- 同一规则的多个版本（如 USER_PREF_EXPLAIN_FLOW_FIRST 有 2 个版本）
```

### Phase 7：合并压缩

1. **合并同主题条目** — 多个变体只保留一条最完整的
2. **删除过时条目** — 已被新条目覆盖的旧版本
3. **压缩详细描述** — 详细内容已有 engram 版本的，memory 只留索引

### Phase 8：验证

```bash
# 检查 memory 使用率
memory(action='add', target='memory', content='TEST: 验证')  # 查看 usage
memory(action='remove', target='memory', old_text='TEST: 验证')

# 对比前后
# 去重前：44 条目，49% 使用率
# 去重后：38 条目，39% 使用率
```

### 实测效果

| 指标 | 去重前 | 去重后 | 变化 |
|------|--------|--------|------|
| 条目数 | 44 | 38 | -6（-14%） |
| 使用率 | 49% | 39% | -10% |
| 冗余条目 | 6 | 0 | -6 |
| 相似条目 | 2 | 0 | -2 |

**搜索测试**：
- "vibe coding" → 1 个记忆 ✅
- "luxury design" → 1 个记忆 ✅
- "memory system" → 1 个记忆 ✅
- "taste critic" → 3 个记忆 ✅
- "wechat" → 1 个记忆 ✅
- "skill cleanup" → 1 个记忆 ✅

## Pitfall 清单

### 必须知道
1. **engram 必须 cd 到 git repo 目录**：engram 通过 git remote 自动识别 project，不在 repo 目录会报 ambiguous_project
2. **Python subprocess UTF-8 问题**：Windows 上 Python 调用 engram 有编码错误，必须用 terminal 工具逐个调用
3. **batch_save.sh 不支持 JSON 数组**：必须逐行 JSON（NDJSON 格式），不能传 `[{...},{...}]`
4. **old_text 匹配失败**：缩短 old_text，用条目开头几个词即可。整段文字含转义字符容易匹配失败

### 高级技巧
5. **mem_update 用于重命名**：编辑/重命名已有记忆比删除+重建更安全（保留 context 和 timestamps）
6. **mem_stats 仅 MCP 可用**：`mem_stats` 仅通过 MCP STDIO 可用，直接终端调用可能返回 "tool not found"（engram 会话上下文问题）
7. **engram 搜索是 project-scoped**：必须 `cd` 到正确的 git repo 目录再调用，否则搜索返回空结果
8. **topic_key 用简洁可搜索关键词**：FTS5 全文搜索需要关键词近似匹配，topic_key 和 title 用简洁词

## 常见问题

### Q: old_text 匹配失败怎么办？
A: 缩短 old_text，用条目开头几个词即可。整段文字含转义字符容易匹配失败。

### Q: engram 保存报 ambiguous_project 怎么办？
A: 必须 `cd` 到 git repo 目录再调用。engram 通过 git remote 自动识别 project。

### Q: Python subprocess 调用 engram 失败怎么办？
A: Windows 上有 UTF-8 编码问题，必须用 terminal 工具逐个调用。

### Q: 搜索找不到记忆怎么办？
A: engram 使用 FTS5 全文搜索，需要关键词近似匹配。搜 "taste critic" 能找到 "Taste Critic Rules"，但搜 "design taste critic" 可能找不到。建议 topic_key 和 title 使用简洁可搜索的关键词。

### Q: mem_stats 返回 "tool not found" 怎么办？
A: engram 会话上下文问题。通过 MCP STDIO 调用（cd 到 repo 目录 + pipe JSON），不要直接终端调用。
