# Harness Engineering 研究笔记

> 2026-06-14 研究整理，来源：GitHub 搜索 + B站搜索

## 核心概念

Harness Engineering = 围绕 AI Agent 构建**可靠的工作环境**，而非写更好的 prompt。

> Anthropic 实验：同一模型（Opus 4.5），同一任务（"build a 2D retro game editor"）
> - **无 Harness**：$9，20 分钟，产出不可用
> - **有 Harness**：$200，6 小时，产出可玩
> - 模型没变，Harness 变了

## Harness 的 5 个子系统

```
1. Instructions — 告诉 Agent 做什么、按什么顺序、开始前读什么
2. State        — 跟踪已完成、进行中、下一步，持久化到磁盘
3. Verification — 测试、lint、类型检查、冒烟测试，只有通过才算完成
4. Scope        — 一次一个功能，不过度扩展，明确定义"完成"
5. Lifecycle    — 开始初始化，结束清理，留下干净的重启路径
```

## Top 项目（按价值排序）

| 项目 | ⭐ | 为什么值得深入 |
|------|-----|---------------|
| **ECC (affaan-m)** | 214k | 最大的 Agent Harness 优化系统（Skills/Instincts/Memory/Security） |
| **langchain** | 139k | 自我定位为 "The agent engineering platform" |
| **agent-skills (addyosmani)** | 58k | 生产级 AI 编码 Agent 工程技能 |
| **learn-harness-engineering** | 8.3k | 从0到1入门教程，12讲+6项目，含中文 |
| **nexent (ModelEngine-Group)** | 5k | 零代码平台，Harness Engineering 原则的落地实现 |
| **awesome-harness-engineering** | 1.8k | 资源大全 |
| **AutoHarness** | 322 | 自动化 Harness Engineering（前沿方向） |
| **AHE (china-qijizhifeng)** | 556 | 学术级成果：84.7% pass@1 on Terminal-Bench |

## Hermes Agent Starter Pack

**地址**: github.com/rblakemesser/hermes-starter-pack

核心理念：4 步手动操作 → Agent 自己配置自己（采访用户 → 自动配置一切）。

功能：持久化记忆(Honcho)、Telegram Bot、BrowserOS 浏览器控制、arch skill suite、自测试验证。

**关键设计**：`hermes -s hermes-bootstrap` 启动后，Agent 按照 SKILL.md runbook 自动完成配置。

## 核心参考文献

- OpenAI: [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
- Anthropic: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Anthropic: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- LangChain: [Improving Deep Agents with harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering)
- Cursor: [Continually improving our agent harness](https://cursor.com/blog/continually-improving-agent-harness)
- Martin Fowler: [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html)

## 对 Hermes Cortex 的启发

| Harness 概念 | Hermes Cortex 对应 | 可以改进 |
|--------------|-------------------|----------|
| Instructions | SOUL.md + SKILL.md | ✅ 已有 |
| State | .hermes_brain_counter | ⚠️ 太简单，可以加 progress.md |
| Verification | auto_optimize.py | ⚠️ 只检查阈值，没有自验证 |
| Scope | evolve.py 的 MAX_RESEARCH_TOPICS | ✅ 已有 |
| Session Lifecycle | Shell Hooks | ✅ 已有 |

## B站热门 Harness 视频

1. "Agent和Harness到底是什么？一个动画彻底搞懂！" — 轩辕的编程宇宙（13.8万播放）
2. "让Agent能力暴涨的Harness，到底是什么？" — 糊粥人儿（1.9万播放）
3. "7.2k Stars！Agent操控浏览器神器Browser Harness开源" — AI大白话007（1.3万播放）
4. "pi agent最佳实践 | Harness Agent定制全流程实战" — 程序员暮闲（5,730播放）
