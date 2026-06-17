# 技能审计工作流

## 工具

**hermes-skill-audit** — 审计和清理 Hermes Agent 技能

**安装位置**：`D:\Hermes\skills\hermes-skill-audit\`

## 使用方法

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

## 审计指标

| 指标 | 说明 | 警戒线 |
|------|------|--------|
| 技能数 | 总技能数量 | >50 个需要清理 |
| 每轮消耗 | 每条消息加载的 tokens | >200K 需要优化 |
| 重复技能 | 内容相似的技能 | >0 组需要合并 |
| 使用次数 | 技能被加载的次数 | 0 次的需要评估 |

## 清理标准

### 删除

- **用户场景不匹配**：Windows 用户删 Apple/macOS、不搞音乐删 media、不用 Docker 删 s6
- **从没用过且无明确场景**：gaming、gifs、libreoffice 等 Antigravity 装的
- **大型项目模板**：web/ 176MB，需要时再装
- **重复技能**：codex/opencode/claude-code 等内容重叠的

### 保留

- **Agent 日常工作流**：plan、bug-hunter、systematic-debugging、squirrel、hermes-agent-skill-authoring
- **用户实际在用的核心技能**：hermes-cortex、design、taste-critic、research、obsidian
- **设计相关**：humanizer、claude-design、popular-web-designs、sketch、ideation

## 实际案例

### 案例 1：117 → 44 技能（2026-06-14）

| 指标 | 清理前 | 清理后 | 减少 |
|------|--------|--------|------|
| 技能数 | 117 | 44 | -62% |
| 每轮消耗 | ~300,265 tokens | ~113,586 tokens | -62% |

**删除的类别**：
- Apple(5) — Windows 用户不需要
- Gaming(2) — 跟场景无关
- Smart-Home(1) — 不用
- Social-Media(1) — 不用
- Red-Teaming(1) — 不用
- media(5) — 不搞音乐、不搜 GIF
- data-science(1) — 不做数据科学
- email(1) — 不用终端邮件
- Creative 大部分(16) — 只保留 5 个有用的
- MLOps 大部分(7) — 只保留 2 个
- Productivity 大部分(6) — 只保留 3 个
- Research 部分(3) — 删除大文件
- Autonomous-AI-Agents 大部分(4) — 只保留 hermes-agent
- s6 调试工具(3) — 不用 Docker/Node.js/Python 调试
- Root 视频工具(3) — 不做视频
- agenttrace(1) — 不用会话审计

**合并**：
- devops/data-organization + devops/hermes-data-management → hermes-data-management

## 关键教训

### 1. 不要过度删除

**用户会问"你平时用不到吗？"** — plan、bug-hunter、systematic-debugging 等是 Agent 日常工作流的一部分，必须保留。

**删除前先问自己**：
- 这个技能我用过吗？
- 这个技能有明确的使用场景吗？
- 这个技能是 Agent 日常工作流的一部分吗？

如果任何一个是"是"，就保留。

### 2. 两个目录都要清理

技能可能在两个地方：
- `~/.hermes/skills/` — Hermes 实际读取的
- `D:\Hermes\skills\` — 你工作的目录

清理时要同时清理两个目录。

### 3. 用户确认再删

永远不要自动删除，先展示分析再问用户。

**正确流程**：
1. 运行审计，生成报告
2. 展示给用户，标注建议删除/保留
3. 用户确认后执行清理
4. 验证清理结果

### 4. 清理后验证

```bash
# 检查技能数
ls ~/.hermes/skills/ | wc -l

# 检查每轮消耗
python D:/Hermes/skills/hermes-skill-audit/scripts/audit.py --summary

# 检查是否有重复
python D:/Hermes/skills/hermes-skill-audit/scripts/audit.py | grep -i "duplicate"
```
