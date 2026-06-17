# Harness Engineering 研究

> 2026-06-14 调研整理，涵盖 GitHub 项目、B站视频、权威文章

## 核心概念

**Harness = 马具/缰绳** — 控制 AI Agent 的方向和行为

```
马 = AI Agent（强大但需要引导）
骑手 = 人类（知道要去哪）
缰绳 = Harness（控制系统）
```

**Harness 的 5 个子系统**：
1. **Instructions** — AGENTS.md，告诉 Agent 做什么
2. **State** — progress.md，跟踪进度
3. **Verification** — tests/lint，验证结果
4. **Scope** — feature_list.json，限制范围
5. **Session Lifecycle** — init.sh，初始化和清理

## 关键实验数据

**Anthropic 实验**：同一模型（Opus 4.5），同一任务

| 条件 | 成本 | 时间 | 结果 |
|------|------|------|------|
| 无 Harness | $9 | 20 分钟 | 产出不可用 |
| 有 Harness | $200 | 6 小时 | 产出可玩 |

## Top Harness Engineering 项目

| 项目 | ⭐ | 亮点 |
|------|-----|------|
| langchain-ai/langchain | 139,204 | "The agent engineering platform" |
| affaan-m/ECC | 214,810 | 最大的 Agent Harness 优化系统 |
| walkinglabs/learn-harness-engineering | 8,370 | 从0到1入门教程，12讲+6项目 |
| ModelEngine-Group/nexent | 5,043 | 零代码 Harness 平台 |
| wquguru/harness-books | 2,461 | 两本 Harness Engineering 书籍 |

## 权威参考文章

- OpenAI: Harness engineering: leveraging Codex in an agent-first world
- Anthropic: Effective harnesses for long-running agents
- Anthropic: Harness design for long-running application development
- LangChain: Improving Deep Agents with harness engineering
- Cursor: Continually improving our agent harness
- Martin Fowler: Harness engineering for coding agent users

## Hermes Starter 项目

### rblakemesser/hermes-starter-pack
- Agent 自配置 Runbook
- 8 个配置阶段（Preflight → Interview → Config → Memory → Skills → Telegram → Browser → Self-test）
- 关键设计：Agent 自己干活，只在需要人的时候才问

### S3YED/appie-kit
- 510 个生产级技能，9 大类别
- 从真实 Web 设计公司（Weblyfe）提取
- 技术栈：MiniMax M2.7 + Hermes Agent + Telegram + n8n

## 详见

Obsidian: D:\ObsidianVault\raw\exploration\2026-06-14-harness-engineering-research.md
