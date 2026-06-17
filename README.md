# Hermes Cortex

> Hermes 大脑系统 — 基于 Karpathy LLM Wiki 模式 + 知识图谱 + 语义检索的 Agent 记忆与知识管理系统

[![Version](https://img.shields.io/badge/version-v2.9.0-blue.svg)](https://github.com/ieyz02031-source/hermes-cortex/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Hermes Agent](https://img.shields.io/badge/Hermes-Agent-green.svg)](https://hermes-agent.nousresearch.com)

## 核心理念

**Karpathy LLM Wiki 模式**：别每次都去翻原始资料，而是让 LLM 一点点维护一个长期的 wiki。知识像复利一样累积。

**核心设计原则**：🧠 **"大脑"必须是自动的**。一个需要手动触发的"大脑"不是大脑，只是一堆脚本。所有知识管理操作（检索、学习、更新、维护）必须在后台自动运行，用户无感知。

## 架构设计

```
输入层（用户对话、外部资料、工具结果、系统事件）
    ↓
处理层（信息抽取、知识融合、图谱构建、索引更新）
    ↓
存储层（热缓存、索引、图谱、日志、笔记库）
    ↓
检索层（语义搜索、关键词搜索、图谱遍历、元数据过滤）
    ↓
输出层（回答、建议、洞察、行动）
```

## 三大支柱

| 支柱 | 说明 |
|------|------|
| **记忆层** | 短期（热缓存）+ 中期（会话记忆）+ 长期（持久化知识） |
| **知识图谱** | 实体 + 概念 + 关联关系的网络 |
| **检索层** | 语义搜索 + BM25 + 关联图遍历 |

## 自动化三原则

1. **提问自动检索** — 用户问问题时，先检索知识库再回答
2. **学习自动记录** — 学到新知识时，自动创建笔记并更新索引
3. **对话结束自动维护** — 每次对话结束，自动更新热缓存和检查孤立笔记

## 功能特性

### 记忆系统

- **四层架构**：Hot（memory）+ Warm（engram）+ Cold（Obsidian）+ Graph（知识图谱）
- **智能检索**：语义搜索 + 关键词搜索 + 图谱遍历
- **自动维护**：健康检查、清理、同步、衰减

### 知识图谱

- **实体识别**：自动从对话中提取实体
- **关系构建**：自动建立实体间关系
- **路径查找**：支持多跳关系查询

### RAG 检索改进

- **章节树切块**：保留文档层级结构
- **三阶段检索**：向量 + BM25 + RRF 融合
- **自动查询扩展**：基于 Embedding 的同义词发现

### 计算机视觉

- **屏幕截图**：mss 库全屏截图
- **AI 分析**：NVIDIA Vision API 图片理解
- **UI Automation**：mcp-windows 专业级界面操控

## 目录结构

```
hermes-cortex/
├── SKILL.md                    # 核心文档
├── feature_list.json           # 功能列表
├── progress.md                 # 进度记录
├── scripts/                    # Python 脚本
│   ├── memory_auto_cleanup.py  # 记忆自动清理
│   ├── memory_decay.py         # 记忆衰减
│   ├── memory_sync.py          # 记忆同步
│   ├── knowledge_graph.py      # 知识图谱
│   ├── smart_retrieval.py      # 智能检索
│   └── ...
├── references/                 # 参考文档
│   ├── engram-integration.md   # engram 集成
│   ├── rag-search-improvements.md  # RAG 改进
│   └── ...
└── reports/                    # 运行报告
```

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/ieyz02031-source/hermes-cortex.git
cd hermes-cortex
```

### 2. 安装依赖

```bash
pip install -r requirements.txt  # 如果有
```

### 3. 配置 Hermes

确保 Hermes Agent 已安装并配置好：

```bash
hermes setup
```

### 4. 使用技能

在 Hermes 会话中，系统会自动加载 hermes-cortex 技能。触发关键词：

- "检索知识"
- "记忆管理"
- "知识图谱"
- "RAG 搜索"

## 技术栈

| 组件 | 技术 | 用途 |
|------|------|------|
| **记忆存储** | engram | 持久化记忆 |
| **知识库** | Obsidian | Markdown 笔记 |
| **知识图谱** | SQLite | 实体关系存储 |
| **语义搜索** | sentence-transformers | 向量检索 |
| **关键词搜索** | FTS5 | 全文检索 |
| **视觉分析** | NVIDIA Vision API | 图片理解 |
| **UI 自动化** | mcp-windows | 界面操控 |

## 相关项目

- [Hermes Agent](https://hermes-agent.nousresearch.com) — 随你成长的 AI 智能体
- [engram](https://github.com/mcp-engram) — 持久化记忆系统
- [Obsidian](https://obsidian.md) — 知识管理工具

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

- GitHub: [ieyz02031-source](https://github.com/ieyz02031-source)
- 项目地址: [hermes-cortex](https://github.com/ieyz02031-source/hermes-cortex)
