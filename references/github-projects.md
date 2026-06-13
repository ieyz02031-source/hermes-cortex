# GitHub 知识管理项目汇总

> 更新时间: 2026-06-13

## 核心项目

### 1. claude-obsidian — 自组织 AI 第二大脑

- **GitHub**: https://github.com/AgriciDaniel/claude-obsidian
- **Stars**: 活跃增长中
- **功能**: 
  - 15 个 Claude Code 技能
  - 自动研究循环（`/autoresearch`）
  - 知识图谱可视化
  - 混合检索（BM25 + 余弦重排序）
  - 热缓存（`hot.md`）+ 索引（`index.md`）+ 日志（`log.md`）
  - 方法论模式（LYT/PARA/Zettelkasten）
- **适合 Hermes**: 架构设计可以借鉴
- **安装**: 需要 Claude Code 环境

### 2. swarmvault — 本地优先 LLM Wiki

- **GitHub**: https://github.com/swarmclawai/swarmvault
- **功能**:
  - 本地优先的知识图谱构建器
  - RAG 知识库
  - Agent 记忆存储
  - 基于 Karpathy 的 LLM Wiki 模式
- **适合 Hermes**: 作为知识库后端

### 3. kajet — Obsidian 语义搜索 MCP 服务器

- **GitHub**: https://github.com/jpalczewski/kajet
- **功能**:
  - 12 个 MCP 工具（语义搜索、笔记编辑、vault 探索）
  - 本地嵌入（AllMiniLM-L6-v2），Metal GPU 加速
  - 增量索引，只重新嵌入变化的文件
  - Web 仪表板，实时 MCP 事件流
  - 单一二进制文件，零运行时依赖
- **适合 Hermes**: 直接作为 MCP 服务器接入
- **安装**: 需要从源码编译（Rust + Deno）

### 4. Karpathy-wiki-graph — 企业级知识图谱 Agent

- **GitHub**: https://github.com/LCccode/Karpathy-wiki-graph
- **功能**:
  - CLI-atomic，可插入的技能
  - 支持 Word/PDF/Excel/PPT
  - 三层 wiki：文章 + 概念 + vis-network 图
  - ~10% RAG token 成本
  - 智能增量训练
- **适合 Hermes**: 作为知识图谱构建工具

### 5. graph-memory-mcp — 语义持久化知识图谱记忆

- **GitHub**: https://github.com/river-ai-lab/graph-memory-mcp
- **功能**:
  - 语义、持久化的知识图谱记忆
  - 基于 MCP 协议
  - 支持多 Agent 系统
- **适合 Hermes**: 作为记忆层 MCP 服务器

### 6. hermes-cortex — Hermes 配置、技能、记忆层

- **GitHub**: https://github.com/lukemcqueen/hermes-cortex
- **功能**:
  - 配置管理
  - 技能系统
  - 持久化知识库
  - ClawMetry 仪表板
  - 自改进工作流系统
- **适合 Hermes**: 直接参考其架构设计

### 7. PRISM — Agent 无关的编排系统

- **GitHub**: https://github.com/racar/PRISM
- **功能**:
  - 跨项目技能记忆
  - 持久化知识库
  - 技能、gotchas、决策记录
  - 确保正确的上下文到达正确的 Agent
- **适合 Hermes**: 作为编排层参考

## 辅助项目

### 8. llm_knowledge_bases_karpathy — 端到端 Python 实现

- **GitHub**: https://github.com/chirindaopensource/llm_knowledge_bases_karpathy
- **功能**:
  - Karpathy LLM Wiki 架构的完整 Python 实现
  - 增量编译异构源到结构化 Markdown wiki 图
  - BM25 检索
  - 引用强制问答
  - LoRA 微调
  - 全面评估
- **适合 Hermes**: 作为实现参考

### 9. memory-wiki-graph-stack — 自维护个人 wiki

- **GitHub**: https://github.com/nardovibecoding/memory-wiki-graph-stack
- **功能**:
  - 混合搜索
  - 知识图谱
  - 完整性审计
  - 生命周期 + 提升链
  - Claude Code 技能
- **适合 Hermes**: 作为维护策略参考

### 10. memwiki — AI 编码 Agent 的持久化记忆协议

- **GitHub**: https://github.com/hereisSwapnil/memwiki
- **功能**:
  - 基于 Markdown 的知识系统
  - 保存上下文、决策、模式、进度
  - 跨会话持久化
- **适合 Hermes**: 作为记忆协议参考

## 中文资源

### 1. AI Agent 记忆机制综述

- **来源**: 知乎专栏
- **链接**: https://zhuanlan.zhihu.com/p/1995813479794353043
- **内容**: 
  - Zep [2025/02]：基于时序知识图谱的智能体记忆架构
  - EverMemOS [2026/01]：自组织记忆操作系统

### 2. 2026年Agent记忆系统方案横评与选型指南

- **来源**: 腾讯云
- **链接**: https://cloud.tencent.com/developer/article/2665379
- **内容**: 
  - 2026年AI Agent记忆系统方案对比
  - 记忆将升维为AI人格与第三大核心组件

### 3. AI Agent 记忆技术演进全解析

- **来源**: CSDN
- **链接**: https://tianqi.csdn.net/69f58bda0a2f6a37c5a756ea.html
- **内容**: 
  - 第一代向量记忆（如 LangChain Memory）
  - 第二代结构化记忆（如 MemGPT/Letta 和 Graphiti）
  - 2026年主流的第三代记忆系统

### 4. Agent Memory 技术演进

- **来源**: GitHub Blog
- **链接**: https://github.com/kejun/blogpost/blob/main/agent-memory-evolution-2026.md
- **内容**: 
  - 从检索到记忆的本质
  - MongoDB 与 The New Stack 的最新行业洞察
  - 2026 年 AI Agent 记忆系统的三大主流范式

## 技术趋势

### 1. 三代记忆系统演进

| 代数 | 技术 | 代表项目 | 特点 |
|------|------|---------|------|
| 第一代 | 向量记忆 | LangChain Memory | 简单、易用 |
| 第二代 | 结构化记忆 | MemGPT/Letta, Graphiti | 结构化、可查询 |
| 第三代 | 知识图谱记忆 | Zep, EverMemOS | 语义、关联、时序 |

### 2. Karpathy LLM Wiki 模式

- **核心思想**: 别每次都去翻原始资料，而是让 LLM 一点点维护一个长期的 wiki
- **实现方式**: 增量更新 + 结构化存储 + 关联网络 + 检索增强
- **代表项目**: claude-obsidian, swarmvault, Karpathy-wiki-graph

### 3. MCP 协议标准化

- **趋势**: 越来越多的工具支持 MCP 协议
- **优势**: 标准化、可互操作、易于集成
- **代表项目**: kajet, graph-memory-mcp

## 选型建议

### 对于 Hermes

1. **短期**: 借鉴 claude-obsidian 的架构设计
2. **中期**: 安装 kajet 作为 MCP 服务器
3. **长期**: 构建完整的知识图谱系统

### 对于个人用户

1. **轻量级**: 使用 Obsidian + 手动整理
2. **中量级**: 使用 claude-obsidian 或 swarmvault
3. **重量级**: 使用 kajet + 自定义构建

### 对于团队

1. **小团队**: 使用 Obsidian Git 同步
2. **中团队**: 使用 swarmvault 或 PRISM
3. **大团队**: 自定义构建知识图谱系统
