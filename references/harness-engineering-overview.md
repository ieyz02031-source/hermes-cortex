# Harness Engineering 综合研究

## 核心定义

**Harness Engineering** = 设计 AI Agent 周围的脚手架（上下文传递、工具接口、规划制品、验证循环、记忆系统、沙箱），决定 Agent 在真实任务上是成功还是失败。

**关键洞察**：Harness 不是更好的 Prompt，而是设计 Agent 操作的系统。主要问题不再是答案质量，而是**行为后果**。

## 演进路径

```
Prompt Engineering → Context Engineering → Harness Engineering
     ↓                    ↓                      ↓
  单次指令            动态信息管理            系统级运行空间
```

## 5 个子系统

| 子系统 | 作用 | 典型文件 |
|--------|------|----------|
| **Instructions** | 告诉 Agent 做什么、按什么顺序 | AGENTS.md、CLAUDE.md |
| **State** | 跟踪已完成、进行中、下一步 | progress.md、feature_list.json |
| **Verification** | 只有通过测试才算完成 | tests、lint、type-check |
| **Scope** | 一次只做一个功能 | feature_list.json、definition of done |
| **Session Lifecycle** | 开始初始化，结束清理 | init.sh、clean-state checklist |

## 核心设计哲学

### 来自《御舆：解码 Agent Harness》(42万字, 3,654⭐)

- 对话循环为**辕**，工具系统为**辐**，权限管线为**軎辖**
- 139 张架构图，50+ 个设计决策分析
- 覆盖工具系统、权限管线、上下文压缩、记忆系统、钩子系统、子智能体调度

### 来自 harness-books (2,464⭐)

- 两本书聚焦同一个工程问题：一旦代码编写模型被放入终端、仓库、权限系统和团队工作流中，什么能让整个系统有界、连续且对后果负责？
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

## Agent 会话生命周期

```
START → 读 progress.md + feature_list.json
    ↓
SELECT → 选择一个 in_progress 功能
    ↓
EXECUTE → 实现功能 + 验证
    ↓
WRAP UP → 更新进度 + 热缓存 + 知识图谱
```

## 核心项目

| 项目 | 星数 | 内容 |
|------|------|------|
| **learn-harness-engineering** | 8,386 | 12 讲 + 6 个项目课程 |
| **claude-code-book** | 3,654 | 《御舆：解码 Agent Harness》42万字 |
| **harness-books** | 2,464 | 两本书：Claude Code 设计指南 + Claude Code vs Codex |
| **awesome-harness-engineering** | 1,814 | 资源列表 |
| **awesome-agent-harness** | 1,192 | 另一个资源列表 |
| **agentic-harness-engineering** | 556 | 可观测性驱动的自动进化 |
| **AutoHarness** | 323 | 自动化 Harness Engineering |
| **hermes-agent-self-evolution** | 4,081 | 技能自进化（DSPy + GEPA） |
| **hermes-optimization-guide** | 437 | 优化指南（24 部分） |
| **self-harness** | 157 | Datawhale 中文教程 |
| **Practical-Guide-to-Context-Engineering** | 694 | 上下文工程实践指南 |

## 与 Hermes Cortex 的对应

| Harness 子系统 | Hermes Cortex |
|----------------|---------------|
| Instructions | SKILL.md、SOUL.md |
| State | 知识图谱、语义索引、热缓存 |
| Verification | auto_optimize.py 警戒线监控 |
| Scope | 自进化循环的任务分解 |
| Session Lifecycle | Shell Hooks |

## 保存的笔记

- `2026-06-14-harness-engineering-deep-dive.md` — 深度研究（9.6KB）
- `2026-06-15-harness-engineering-comprehensive.md` — 综合研究（12.8KB）

## 参考资源

### 权威来源

- OpenAI: https://openai.com/index/harness-engineering/
- Anthropic: https://www.anthropic.com/engineering/claude-code-harness
- LangChain: https://blog.langchain.dev/context-engineering-for-agents/
- Martin Fowler: https://martinfowler.com/articles/building-info-radiator-for-coding-agent.html

### 中文资源

- Datawhale self-harness: https://github.com/datawhalechina/self-harness
- 清华 Agentic Harness Engineering: https://github.com/china-qijizhifeng/agentic-harness-engineering
- 鱼皮 Harness Engineering Guide: https://github.com/nexu-io/harness-engineering-guide
