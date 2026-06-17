# Harness Engineering 综合研究

## 核心定义

**Harness Engineering** = 设计 AI Agent 周围的脚手架（上下文传递、工具接口、规划制品、验证循环、记忆系统、沙箱），决定 Agent 在真实任务上是成功还是失败。

## 演进路径

```
Prompt Engineering → Context Engineering → Harness Engineering
     ↓                    ↓                      ↓
  单次指令            动态信息管理            系统级运行空间
```

## 权威项目

| 项目 | 星数 | 描述 |
|------|------|------|
| **harness-books** | 2,464 | 两本书：Claude Code 设计指南 + Claude Code vs Codex |
| **claude-code-book** | 3,654 | 《御舆：解码 Agent Harness》42万字 |
| **learn-harness-engineering** | 8,386 | 12 讲 + 6 个项目课程 |
| **AutoHarness** | 323 | 自动化 Harness Engineering |
| **agentic-harness-engineering** | 556 | 可观测性驱动的自动进化 |
| **awesome-harness-engineering** | 1,814 | 资源列表 |
| **self-harness** | 157 | Datawhale 中文教程 |
| **Practical-Guide-to-Context-Engineering** | 694 | 上下文工程实践指南 |

## 核心设计哲学

来自《御舆：解码 Agent Harness》(42万字)：
- 对话循环为**辕**，工具系统为**辐**，权限管线为**軎辖**
- 139 张架构图，50+ 个设计决策分析

来自 harness-books (2,464⭐)：
- 真正的危险不是模型偶尔说错话，而是系统没有处理后果的结构

## AutoHarness 6 步治理管道

```
1. Parse & Validate → 2. Risk Classify → 3. Permission Check
4. Execute → 5. Output Sanitize → 6. Audit Log
```

## AHE 三层可观测性

- **组件可观测性** — 7 个正交、文件级组件
- **经验可观测性** — ~10M-token 原始轨迹蒸馏
- **决策可观测性** — 有证据支持的编辑

## 详细笔记

- Obsidian: `D:\ObsidianVault\raw\exploration\2026-06-15-harness-engineering-comprehensive.md` (12.8KB)
- Obsidian: `D:\ObsidianVault\raw\exploration\2026-06-14-harness-engineering-deep-dive.md` (9.6KB)
- Obsidian: `D:\ObsidianVault\raw\exploration\2026-06-14-harness-engineering-research.md` (7.5KB)
