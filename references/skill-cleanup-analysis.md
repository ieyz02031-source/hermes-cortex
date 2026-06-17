# 技能清理分析 (2026-06-15)

## 当前状态

- 总技能数：68 个
- 总磁盘占用：~190MB
- web/ 目录：176MB（占 93%）

## 分类统计

| 类别 | 数量 | 说明 |
|------|------|------|
| 核心技能 | 1 | hermes-cortex |
| 设计技能 | 9 | design, taste-critic, vibe-coding-workflow 等 |
| 开发技能 | 10 | software-development, claw-code-harness 等 |
| 自动化技能 | 7 | agency-agents, autonomous 等 |
| 知识管理 | 2 | note-taking, research |
| 工具技能 | 3 | cli-anything-hermes, terminal-ops, tmux |
| 其他 | 40 | Antigravity 装的，来历不明 |

## 问题

1. **web/ 目录 176MB**：16 个项目模板（next-saas、tailadmin、ecommerce 等），用户大概率没用过
2. **40 个"其他"技能**：apple、hono、squirrel、unship、sendblue、gaming、gifs、libreoffice 等，跟用户场景完全不搭
3. **功能重叠**：设计相关 6 个，代码审计 4 个，Agent 相关 5 个

## 清理建议

### 删除（用户没用过、跟场景无关）
- gaming、gifs、libreoffice、sendblue、apple、hono、squirrel、unship
- web/ 下的 16 个项目模板（176MB，需要时再装）

### 保留（用户实际在用）
- hermes-cortex、design、taste-critic、research、note-taking
- agency-agents、mcp、superpowers-zh、software-development
- vibe-coding-workflow、design-vibe、awesome-design-md

## 影响

**运行不受影响**——Hermes 只在触发时加载 skill，不会全部预加载。但：
1. 上下文污染：68 个 skill 的描述会挤占系统提示
2. 选择困难：同类 skill 多了，Hermes 可能选错
3. 磁盘浪费：176MB 的 web 模板用户根本不用
