# Shell Hooks Integration — Hermes Cortex 完全融合指南

## 核心发现

Hermes 有原生 Shell Hooks 系统，支持在会话生命周期关键节点自动执行脚本。

## 支持的事件类型

```
on_session_start     — 会话开始时
on_session_end       — 会话结束时
on_session_finalize  — 会话最终化时
on_session_reset     — 会话重置时
pre_llm_call         — LLM 调用前
post_llm_call        — LLM 调用后
post_tool_call       — 工具调用后
transform_llm_output — 输出转换
transform_terminal_output — 终端输出转换
transform_tool_result — 工具结果转换
```

## 配置格式（关键陷阱！）

### ❌ 错误格式（hermes config set 会存成 JSON 字符串）
```yaml
hooks:
  on_session_start:
    - command: "bash"
      args:
        - "D:/Hermes/skills/hermes-cortex/scripts/hook_session_start.sh"
```

### ✅ 正确格式（command 是单个字符串，用 shlex.split() 解析）
```yaml
hooks:
  on_session_start:
    - command: "python D:/Hermes/skills/hermes-cortex/scripts/hook_session_start.py"
      timeout: 30
  on_session_end:
    - command: "python D:/Hermes/skills/hermes-cortex/scripts/hook_session_end.py"
      timeout: 60
```

## ⚠️ 关键陷阱：两个 config.yaml

**Hermes 实际读取的配置文件是 `AppData/Local/hermes/config.yaml`，不是 `~/.hermes/config.yaml`！**

| 路径 | 用途 |
|------|------|
| `C:\Users\<user>\AppData\Local\hermes\config.yaml` | **Hermes 实际读取**（hooks、MCP、providers） |
| `~/.hermes/config.yaml` | SOUL.md、skills 等 |

修改 hooks 配置必须用 Python yaml.dump 直接写 AppData 文件：
```python
import yaml
from pathlib import Path

config_path = Path('C:/Users/<user>/AppData/Local/hermes/config.yaml')
with open(config_path, 'r') as f:
    cfg = yaml.safe_load(f)

cfg['hooks'] = {
    'on_session_start': [{'command': 'python ...', 'timeout': 30}],
    'on_session_end': [{'command': 'python ...', 'timeout': 60}]
}

with open(config_path, 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True)
```

## Allowlist 配置

Shell hooks 首次使用需要 approve。allowlist 文件位置：
```
C:\Users\<user>\AppData\Local\hermes\shell-hooks-allowlist.json
```

格式：
```json
{
  "approvals": [
    {"event": "on_session_start", "command": "python D:/Hermes/skills/hermes-cortex/scripts/hook_session_start.py"},
    {"event": "on_session_end", "command": "python D:/Hermes/skills/hermes-cortex/scripts/hook_session_end.py"}
  ]
}
```

## Windows 编码陷阱

**bash 脚本在 Windows 上会有编码错误**（Git Bash 输出非 UTF-8）。解决方案：
- 用 Python wrapper 脚本替代 bash 脚本
- Python 脚本内部调用 subprocess 运行实际逻辑
- 设置 `encoding='utf-8', errors='replace'`

## 验证命令

```bash
hermes hooks list          # 查看配置的 hooks
hermes hooks doctor        # 健康检查
hermes hooks test <event>  # 测试特定事件
```

## 参考文件

- 源码：`D:\Hermes\hermes-agent\agent\shell_hooks.py`
- CLI：`D:\Hermes\hermes-agent\hermes_cli\hooks.py`
- 事件定义：`D:\Hermes\hermes-agent\hermes_cli\plugins.py` (VALID_HOOKS)