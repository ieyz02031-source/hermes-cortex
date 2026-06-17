# 外部工具集成指南（Windows 环境）

## 概述

在 Windows 环境下集成外部工具（Go 二进制文件、Rust 工具等）到 Hermes 的标准流程。

## 标准流程

### 1. 查找发布版本

```bash
# 查看 GitHub releases
curl -s "https://api.github.com/repos/<owner>/<repo>/releases/latest" | python -c "
import sys,json
data=json.load(sys.stdin)
print(f\"版本: {data['tag_name']}\")
for asset in data['assets']:
    print(f\"  - {asset['name']}: {asset['browser_download_url']}\")
"
```

### 2. 下载 Windows 版本

```bash
# 创建工具目录
mkdir -p "D:\Hermes\tools\<tool-name>"

# 下载 zip 文件
curl -L "<release-url>" -o "D:\Hermes\tools\<tool-name>\<tool>.zip"

# 解压
cd "D:\Hermes\tools\<tool-name>"
unzip -o <tool>.zip
```

### 3. 验证安装

```bash
# 验证版本
"D:\Hermes\tools\<tool-name>\<tool>.exe" --version
```

### 4. 配置 MCP 服务器

```python
import yaml

config_path = 'C:/Users/20716/AppData/Local/hermes/config.yaml'
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

config['mcp_servers']['<tool-name>'] = {
    'command': 'D:/Hermes/tools/<tool-name>/<tool>.exe',
    'args': ['mcp', '--tools=agent'],
    'timeout': 30
}

with open(config_path, 'w', encoding='utf-8') as f:
    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
```

**⚠️ MCP 服务器 `env` 字段**：有些 MCP 服务器需要环境变量来控制行为（如禁用 HTTP 服务器、设置 API 密钥等）。Hermes config.yaml 支持 `env` 字段：

```yaml
mcp_servers:
  open-websearch:
    command: open-websearch
    args: []
    timeout: 30
    env:
      MODE: stdio          # 禁用 HTTP 服务器，只用 STDIO
  firecrawl:
    command: npx
    args: ['-y', 'firecrawl-mcp']
    env:
      FIRECRAWL_API_KEY: fc-xxx
```

**常见 `env` 配置**：
- `MODE: stdio` — 禁用 HTTP 服务器（open-websearch 需要）
- `API_KEY` — 设置 API 密钥（firecrawl、github 等需要）
- `USE_PROXY: true` + `PROXY_URL` — 启用代理

### 5. 验证 MCP 集成

```bash
# 测试 MCP 服务器
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | \
  "D:\Hermes\tools\<tool-name>\<tool>.exe" mcp --tools=agent

# 验证 Hermes 配置
python -c "
import yaml
config = yaml.safe_load(open('C:/Users/20716/AppData/Local/hermes/config.yaml'))
print('<tool-name>' in config.get('mcp_servers', {}))
"
```

## 实际案例

### engram（持久化记忆系统）

- **仓库**: Gentleman-Programming/engram
- **版本**: v1.16.3
- **安装位置**: `D:\Hermes\tools\engram\engram.exe`
- **MCP 配置**: `args: ['mcp', '--tools=agent']`
- **工具数**: 20 个 MCP 工具

### open-websearch（全网搜索）

- **仓库**: Aas-ee/open-webSearch
- **版本**: v2.1.11
- **安装方式**: `npm install -g open-websearch`（全局 npm 安装）
- **MCP 配置**: `command: open-websearch, args: [], env: {MODE: stdio}`
- **工具数**: 5 个 MCP 工具（search, fetchWebContent, fetchGithubReadme, fetchCsdn, fetchJuejin）
- **关键 Pitfall**: 必须设置 `MODE: stdio` 环境变量，否则会尝试启动 HTTP 服务器并报端口冲突错误

### 集成检查清单

- [ ] 下载正确架构的版本（amd64 vs arm64）
- [ ] 验证 `--version` 输出
- [ ] 测试 MCP 服务器启动
- [ ] 更新 Hermes config.yaml
- [ ] 更新 feature_list.json
- [ ] 更新 SKILL.md
- [ ] 更新 progress.md
- [ ] 运行 verify_harness.py 确认不影响现有功能

## 注意事项

1. **brew 不可用** — Windows 环境没有 brew，必须手动下载
2. **路径格式** — YAML 配置中用正斜杠 `D:/Hermes/tools/...`
3. **MCP args 格式** — 用数组 `['mcp', '--tools=agent']`
4. **超时设置** — 默认 30 秒，复杂操作可设 60 秒
