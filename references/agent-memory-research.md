# Agent Memory 技术研究

> 2026-06-15 研究。来源：GitHub 搜索 + Agent_Memory_Techniques 项目分析。

## 主流方案对比

| 方案 | GitHub 星数 | 特点 | 资源消耗 | 适合 Hermes |
|------|------------|------|----------|-------------|
| **Mem0** | 28k+ | 通用 AI 记忆层，支持 MCP，自动提取用户偏好 | 中（Python + 向量DB） | ✅ Phase 2 候选 |
| **Letta (MemGPT)** | 15k+ | 有状态 agent，自编辑记忆，内/外独白架构 | 重（Python server） | ❌ 太重 |
| **Zep** | 商业 | 对话分类、实体提取、时间感知图谱 | 中 | ⚠️ 需 API |
| **Graphiti** | Zep 开源 | 时间感知知识图谱，episodic→semantic 提取 | 中（Neo4j） | ✅ 适合 |
| **engram** | 已集成 | 轻量级，SQLite + FTS5，18 个 MCP 工具 | 轻（7MB Go 二进制） | ✅ 已在用 |
| **Agent_Memory_Techniques** | 教程 | 30 种技术的 Jupyter notebooks | N/A | ✅ 学习用 |

## Agent_Memory_Techniques（30 种技术分类）

来源：`github.com/NirDiamant/Agent_Memory_Techniques`

| 分类 | 编号 | 技术 | 说明 |
|------|------|------|------|
| **短期记忆** | 01-05 | 对话缓冲、滑动窗口、摘要、摘要缓冲、Token 缓冲 | 管理单次对话内的上下文 |
| **长期记忆** | 06-11 | 向量存储、实体记忆、知识图谱、情景记忆、语义记忆、程序性记忆 | 跨会话持久化 |
| **认知架构** | 12-19 | 工作记忆、分层记忆、整合、压缩、自我反思、路由、时间记忆、遗忘衰减 | 人类记忆启发 |
| **检索与多 Agent** | 20-23 | 检索模式、跨会话记忆、多 Agent 共享、记忆工具 | 查找和共享 |
| **框架** | 24-27 | Graphiti、Mem0、Letta/MemGPT、Zep | 生产就绪 |
| **评估与生产** | 28-30 | 记忆评估、基准测试（LoCoMo）、生产模式 | 测量和部署 |

## 三层记忆架构（Hermes Cortex 已实现）

```
┌─────────────────────────────────────────────────────────┐
│  🔴 Hot Layer (每轮注入)                                  │
│  - memory 系统：核心规则，10K 字符软限制                    │
│  - 特点：自动注入上下文，无需查询                           │
├─────────────────────────────────────────────────────────┤
│  🟡 Warm Layer (按需检索)                                 │
│  - engram：18 个 MCP 工具，SQLite + FTS5                  │
│  - 特点：语义搜索，按需加载                                │
├─────────────────────────────────────────────────────────┤
│  🟢 Cold Layer (文档存储)                                 │
│  - Obsidian：Markdown 笔记库                              │
│  - 特点：持久化，可浏览，可搜索                             │
└─────────────────────────────────────────────────────────┘
```

## 记忆迁移工作流

当 Hot Layer 接近上限时：

1. 识别 `>100` 字符的详细条目
2. 用 `mem_save`（What/Why/Where/Learned 格式）存入 engram
3. memory 条目替换为一句话索引
4. 验证 usage 下降

**实测**：15 个条目迁移后，68% → 46%（-22%）。

## Phase 2 候选：Mem0

**Mem0** 是最成熟的通用记忆层：
- 自动从对话中提取用户偏好
- 语义搜索记忆
- 支持 MCP 协议
- 本地部署（OpenMemory）
- Docker 一键部署（mem0-aio 项目）

**集成评估**：
- ✅ 支持 MCP — 可直接注册到 Hermes
- ✅ 自动提取 — 减少手动维护
- ⚠️ 需要向量数据库（Qdrant）— 增加资源消耗
- ⚠️ Python 依赖 — 需要 Python 3.12 环境

## 参考链接

- Agent_Memory_Techniques: https://github.com/NirDiamant/Agent_Memory_Techniques
- Mem0: https://github.com/mem0ai/mem0
- Letta: https://github.com/letta-ai/letta
- Graphiti: https://github.com/getzep/graphiti
- Awesome-AI-Memory: https://github.com/IAAR-Shanghai/Awesome-AI-Memory
