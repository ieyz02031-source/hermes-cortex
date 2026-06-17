# Agent Memory 研究发现 (2026-06-15)

## 研究来源

- Agent_Memory_Techniques (NirDiamant) — 30 种技术，Jupyter notebooks
- mem0-mcp (pinkpixel-dev) — Mem0 MCP 服务器实现
- herevault — 基于 Obsidian 的记忆系统
- Awesome-AI-Memory (IAAR-Shanghai) — AI 记忆知识库
- super-hippocampus — 三层知识库系统
- Letta (原 MemGPT) — 有状态 agent 框架

## 技术选型结论

| 方案 | 星数 | 特点 | 适合 Hermes | 决策 |
|------|------|------|-------------|------|
| **Mem0** | 28k+ | 通用记忆层，支持 MCP | ✅ Phase 2 候选 | 待集成 |
| **Letta** | 15k+ | 有状态 agent，自编辑记忆 | ❌ 太重 | 拒绝 |
| **Zep/Graphiti** | 5k+ | 时间感知知识图谱 | ✅ 适合 | 待集成 |
| **Agent_Memory_Techniques** | 教程 | 30 种技术，Jupyter notebooks | ✅ 学习用 | 已学习 |
| **engram** | 已集成 | 轻量级，18 个 MCP 工具 | ✅ 已在用 | 已集成 |
| **mem0-mcp** | npm 包 | Mem0 MCP 服务器 | ✅ Phase 2 候选 | 待集成 |

## 三层架构实现

### Hot Layer (memory)
- 每轮自动注入上下文
- 10,000 字符软限制
- 适合：核心规则、用户偏好、环境关键信息
- 当前：39 条规则，40% 使用率

### Warm Layer (engram)
- 按需 MCP 检索
- 无容量限制
- 适合：项目详情、历史决策、技术文档、详细工作流
- 当前：16 个记忆，18 个 MCP 工具
- 搜索：FTS5 全文搜索（非语义搜索）

### Cold Layer (Obsidian)
- 文档存储，持久化
- 无容量限制
- 适合：完整笔记、研究报告、探索日志、长期归档

## Mem0 v3 深度分析

### 核心特性
- **Single-pass ADD-only extraction** — 一次 LLM 调用，无 UPDATE/DELETE
- **Agent-generated facts are first-class** — agent 确认的动作同等权重存储
- **Entity linking** — 实体提取、嵌入、跨记忆链接
- **Multi-signal retrieval** — 语义、BM25 关键词、实体匹配并行评分融合
- **Temporal Reasoning** — 时间感知检索

### Benchmark 结果
| Benchmark | 旧版 | 新版 | Tokens | Latency p50 |
|-----------|------|------|--------|-------------|
| LoCoMo | 71.4 | **91.6** | 7.0K | 0.88s |
| LongMemEval | 67.8 | **94.8** | 6.8K | 1.09s |
| BEAM (1M) | — | **64.1** | 6.7K | 1.00s |
| BEAM (10M) | — | **48.6** | 6.9K | 1.05s |

### 集成方式
1. **pip install mem0ai** — Python 库
2. **npm install -g @pinkpixel/mem0-mcp** — MCP 服务器
3. **docker compose up** — 自托管服务器
4. **app.mem0.ai** — 云平台

### 存储模式
| 模式 | 优点 | 缺点 | 推荐场景 |
|------|------|------|----------|
| Cloud | 最简单，无需数据库 | 需要 API 密钥 | 生产环境 |
| Supabase | 免费，自托管 | 需要 Supabase 账号 | 自托管 |
| Local | 无需外部服务 | 数据不持久 | 开发测试 |

## 下一步

1. **Phase 2: 集成 mem0-mcp** — 语义搜索比 FTS5 更好
2. **Phase 3: 知识图谱增强** — Graphiti 时间感知知识图谱
3. **定期整理** — 每周清理过时记忆
