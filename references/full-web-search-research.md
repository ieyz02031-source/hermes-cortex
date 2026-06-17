# 全网搜索研究

## 研究背景

用户要求扩大搜索范围到全网，不限于 GitHub。

## 已研究项目

### 全网搜索 MCP 服务器

| 项目 | 星数 | 大小 | 依赖 | 核心特性 | 风险 |
|------|------|------|------|----------|------|
| **open-webSearch** | 1,416⭐ | 525KB | 13 | 多引擎搜索，无需 API 密钥 | 低 |
| **firecrawl-mcp-server** | 6,567⭐ | - | - | 官方 Firecrawl MCP | 需 API 密钥 |
| **exa-mcp-server** | 4,574⭐ | - | - | Exa 搜索 | 需 API 密钥 |
| **duckduckgo-mcp-server** | 1,238⭐ | - | - | DuckDuckGo 搜索 | 有限 |
| **mcp-searxng** | 898⭐ | - | - | SearXNG 私有搜索 | 需自建 |
| **web-search-mcp** | 946⭐ | - | - | 简单 Web 搜索 | 有限 |

### 全网搜索框架

| 项目 | 星数 | 大小 | 核心特性 |
|------|------|------|----------|
| **deep-research** | 19,118⭐ | - | AI 驱动深度研究助手 |
| **MindSearch** | 6,871⭐ | 4.3MB | LLM 多代理搜索框架（依赖重） |
| **ddgs** | 2,721⭐ | - | 多引擎聚合搜索库 |

## 最佳候选：open-webSearch

**核心特性**：
- 多引擎搜索：bing, baidu, duckduckgo, exa, brave, startpage, sogou, csdn, juejin
- 无需 API 密钥
- MCP 服务器支持
- CLI 和本地守护进程
- 支持代理配置
- 返回结构化结果（标题、URL、描述）
- 支持获取文章内容（csdn, github README, 通用 HTTP 页面）

**依赖（13个）**：
- @modelcontextprotocol/sdk: MCP 协议
- axios: HTTP 客户端
- cheerio: HTML 解析
- express: HTTP 服务器
- jsdom: DOM 模拟
- zod: 数据验证
- 等

**安装方式**：
```bash
npm install -g open-websearch
```

**MCP 配置**：
```yaml
mcp_servers:
  open-websearch:
    command: npx
    args: ['open-websearch', 'mcp']
    timeout: 30
```

**与 engram 的关系**：互补
- engram：持久化记忆（跨会话）
- open-webSearch：全网搜索（实时信息）

## 决策

当前 engram 已满足记忆需求。open-webSearch 可作为后续增强，待用户确认后集成。

## 搜索工具总结

| 工具 | 覆盖范围 | API 密钥 | 状态 |
|------|----------|----------|------|
| **GitHub API** | GitHub 仓库 | 需要（已有） | ✅ 在用 |
| **web_search (Firecrawl)** | 全球网页 | 需要（已有） | ⚠️ Token 过期 |
| **web_extract** | 特定 URL | 不需要 | ✅ 在用 |
| **curl** | 特定 API | 不需要 | ✅ 在用 |
| **open-webSearch** | 全网多引擎 | 不需要 | 🔍 待集成 |
