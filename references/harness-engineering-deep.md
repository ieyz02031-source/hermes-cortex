# Harness Engineering 深度参考

## 核心定义

**Harness Engineering** = 设计 AI Agent 周围的脚手架（上下文传递、工具接口、规划制品、验证循环、记忆系统、沙箱），决定 Agent 在真实任务上是成功还是失败。

## 权威来源

### OpenAI
- [Harness Engineering](https://openai.com/index/harness-engineering/)
- [Unrolling the Codex Agent Loop](https://openai.com/index/unrolling-the-codex-agent-loop/)
- [Run Long-Horizon Tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex/)

### Anthropic
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-effective-tools-for-agents)
- [Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

### LangChain
- [The Anatomy of an Agent Harness](https://blog.langchain.com/the-anatomy-of-an-agent-harness/)
- [Improving Deep Agents with Harness Engineering](https://blog.langchain.com/improving-deep-agents-with-harness-engineering/)

### Martin Fowler
- [Harness Engineering for Coding Agent Users](https://martinfowler.com/articles/harness-engineering.html)

## 5 个子系统

| 子系统 | 作用 | 典型文件 |
|--------|------|----------|
| **Instructions** | 告诉 Agent 做什么、按什么顺序 | AGENTS.md、CLAUDE.md、docs/ |
| **State** | 跟踪已完成、进行中、下一步 | progress.md、feature_list.json、git log |
| **Verification** | 只有通过测试才算完成 | tests、lint、type-check、smoke runs |
| **Scope** | 一次只做一个功能 | feature_list.json、definition of done |
| **Session Lifecycle** | 开始初始化，结束清理 | init.sh、clean-state checklist、handoff note |

## 与 Hermes Cortex 的关系

| Harness 子系统 | Hermes Cortex 对应 |
|----------------|-------------------|
| **Instructions** | SKILL.md、SOUL.md |
| **State** | 知识图谱、语义索引、热缓存 |
| **Verification** | auto_optimize.py 警戒线监控 |
| **Scope** | 自进化循环的任务分解 |
| **Session Lifecycle** | Shell Hooks (on_session_start/end) |

## 综合研究来源 (2026-06-14)

### 书籍

- [harness-books](https://github.com/wquguru/harness-books) (2,464⭐) — 两本书：Claude Code 设计指南 + Claude Code vs Codex
- 核心观点：真正的危险不是模型偶尔说错话，而是系统没有处理后果的结构

### 中文教程

- [claude-code-book](https://github.com/lintinghua/claude-code-book) (3,654⭐) — 《御舆：解码 Agent Harness》42万字
- 核心观点：对话循环为辕，工具系统为辐，权限管线为軎辖；139张架构图
- [self-harness](https://github.com/datawhalechina/self-harness) (157⭐) — Datawhale 中文教程
- [Practical-Guide-to-Context-Engineering](https://github.com/WakeUp-Jin/Practical-Guide-to-Context-Engineering) (694⭐) — 上下文工程实践指南

### 框架

- [AutoHarness](https://github.com/aiming-lab/AutoHarness) (323⭐) — 自动化 Harness Engineering
- 6 步治理管道：Parse & Validate → Risk Classify → Permission Check → Execute → Output Sanitize → Audit Log
- [agentic-harness-engineering](https://github.com/china-qijizhifeng/agentic-harness-engineering) (556⭐) — 可观测性驱动的自动进化
- 三层可观测性：组件可观测性、经验可观测性、决策可观测性

### 资源列表

- [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) (1,814⭐)
- [awesome-agent-harness](https://github.com/zhangjintw/awesome-agent-harness) (1,192⭐)

### 技能自进化

- [hermes-agent-self-evolution](https://github.com/NousResearch/hermes-agent-self-evolution) (4,081⭐)
- DSPy + GEPA 自动优化技能，~$2-10 每次优化
- 5 个阶段：技能文件 → 工具描述 → 系统提示 → 工具代码 → 持续改进

### 优化指南

- [hermes-optimization-guide](https://github.com/OnlyTerp/hermes-optimization-guide) (437⭐)
- 24 部分完整指南：安装、Telegram、LightRAG、模型路由、可观测性、安全

## 课程

- [learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering) — 12 讲 + 6 个项目
- [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) — 资源列表
