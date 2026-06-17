# 工具集成评估框架

## 评估标准

集成新工具前必须分析以下指标：

| 指标 | 阈值 | 说明 |
|------|------|------|
| **大小** | < 50MB | 仓库总大小 |
| **依赖** | < 10MB | 运行时依赖总大小 |
| **语言** | Go/Rust 优先 | 零依赖单二进制最优 |
| **运行时** | 无依赖优先 | Node.js/Python 次之 |
| **端口** | 不固定 | MCP stdio 优先 |
| **安装** | 简单 | 一条命令完成 |

## 已评估项目（2026-06-14 ~ 2026-06-15）

### ✅ 已集成

| 项目 | 大小 | 依赖 | 语言 | 状态 |
|------|------|------|------|------|
| **engram** | 7MB | 0 | Go | ✅ 已集成（MCP 服务器，20 个工具，FTS5 全文搜索） |
| **open-websearch** | 525KB | 13 | TypeScript | ✅ 已集成（MCP 服务器，多引擎搜索，MODE=stdio） |

### ❌ 已拒绝（资源消耗过高）

| 项目 | 大小 | 依赖 | 语言 | 拒绝原因 |
|------|------|------|------|----------|
| **MemOS** | 56MB | 20MB (transformers 9.5MB + better-sqlite3 10.4MB) | TypeScript | 依赖太大，需要 Node.js 20+，固定端口 18800 |
| **evolver** | 96MB | AWS SDK | JavaScript | 仓库太大（96MB），AWS SDK 依赖重 |
| **ACE** | - | faiss-cpu + sentence-transformers + scikit-learn | Python | 依赖太重（8个），需要 GPU 加速 |
| **pro-workflow** | 386KB | better-sqlite3 | JavaScript | 需要 Claude Code 环境，better-sqlite3 需重新编译 |
| **CORAL** | 75MB | - | Python | 太大（75MB） |
| **Memory-Plus** | 3.3MB | 12个（qdrant-client, langchain, scikit-learn） | Python | 依赖太多 |

### 🔍 已研究（轻量级替代方案）

| 项目 | 星数 | 大小 | 核心特性 | 状态 |
|------|------|------|----------|------|
| **nocturne_memory** | 1,198⭐ | 2.9MB | 图结构记忆，MCP 支持 | 可考虑 |
| **LycheeMem** | 358⭐ | 5MB | 轻量级长期记忆 | 可考虑 |
| **GenericAgent** | 12,851⭐ | 40MB | 自进化技能树，6x 更少 token | 较大但高星 |
| **open-webSearch** | 1,416⭐ | 525KB | 多引擎搜索，无需 API 密钥 | ✅ 已集成（MCP 服务器，MODE=stdio） |

### 📊 评估标准权重

| 优先级 | 指标 | 说明 |
|--------|------|------|
| 1 | **大小** | < 10MB 优先，> 50MB 拒绝 |
| 2 | **依赖数** | 0 优先，> 10 警惕 |
| 3 | **运行时** | 无依赖 > Go/Rust > Node.js > Python |
| 4 | **端口** | MCP stdio 优先，避免固定端口 |
| 5 | **安装** | 一条命令完成 |

## 评估流程

1. **检查大小**：`curl -s "https://api.github.com/repos/owner/repo" | python -c "import sys,json; print(json.load(sys.stdin)['size'])"`
2. **检查依赖**：查看 package.json / go.mod / Cargo.toml / pyproject.toml
3. **检查语言**：优先 Go/Rust（零依赖单二进制）
4. **检查运行时**：优先无依赖，Node.js/Python 次之
5. **检查端口**：MCP stdio 优先，避免固定端口
6. **检查安装**：一条命令完成优先
7. **检查 npm 包大小**：`curl -s "https://registry.npmjs.org/<pkg>" | python -c "..."` 获取 unpackedSize
8. **检查端口冲突**：确认 MCP 服务器是否需要固定端口，是否与现有服务冲突
9. **检查 MCP 启动模式**：STDIO only？还是同时启动 HTTP？需要 `env` 配置吗？

## 关键 Pitfall

### 3. open-websearch 需要 MODE=stdio 环境变量

open-websearch 默认同时启动 STDIO 和 HTTP 服务器。如果端口被占用（如 Hermes Web UI 的 8648），会报 `EADDRINUSE` 错误。

**解决方案**：在 MCP 配置中设置 `env: MODE: stdio`：

```yaml
mcp_servers:
  open-websearch:
    command: open-websearch
    args: []
    timeout: 30
    env:
      MODE: stdio
```

**原理**：`enableHttpServer` 的逻辑是 `process.env.MODE ? ['both', 'http'].includes(process.env.MODE) : true`，设为 `stdio` 会禁用 HTTP 服务器。

### 4. 必须先检查再集成（"检查好再干"）

用户明确要求：**集成任何工具前必须先检查资源消耗**。不要看到好项目就直接集成。

**正确流程**：
1. 搜索相关项目
2. 检查每个项目的大小、依赖、运行时要求
3. 列出对比表格
4. 排除资源消耗过高的项目
5. 只集成最轻量的方案

**错误流程**：
1. 看到好项目
2. 直接开始集成
3. 发现太重了
4. 用户说"会影响，拖累"

### 2. 用户拒绝信号

用户会说：
- "会影响，拖累" → 立即停止，分析原因
- "太重了" → 寻找轻量级替代
- "依赖太多" → 寻找零依赖方案
- "这个MemO会影响" → 用户在说 MemOS 会拖累系统

**不要争辩**，直接接受并寻找替代方案。

## 拒绝信号

用户会说：
- "会影响，拖累" → 立即停止，分析原因
- "太重了" → 寻找轻量级替代
- "依赖太多" → 寻找零依赖方案

## 决策原则

1. **轻量级优先**：Go/Rust 单二进制 > Node.js/Python
2. **零依赖优先**：无依赖 > 有依赖
3. **MCP stdio 优先**：避免固定端口
4. **简单安装优先**：一条命令 > 复杂配置
5. **已有方案优先**：engram 已足够，不需要 MemOS
