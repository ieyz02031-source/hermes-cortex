# Hermes Shell Hooks Integration Guide

## Overview

Hermes Agent has a native shell hooks system that fires shell scripts on lifecycle events. This is the primary mechanism for making Hermes Brain "automatic" — no user intervention needed.

## Architecture

```
Hermes Agent
    ├── on_session_start → hook_session_start.py → hot_cache.py
    ├── on_session_end   → hook_session_end.py   → hot_cache.py + maintain.py
    └── Daily cron       → Windows Task Scheduler → evolve.py + hot_cache.py + semantic_index.py
```

## Config Location

**CRITICAL**: Hermes reads config from `C:\Users\20716\AppData\Local\hermes\config.yaml`, NOT `~/.hermes/config.yaml`.

- `get_hermes_home()` returns `AppData/Local/hermes`
- `hermes config set` writes to the correct location
- `hermes hooks list` reads from the correct location
- Allowlist at `AppData/Local/hermes/shell-hooks-allowlist.json`

## Hook Config Format

```yaml
hooks:
  on_session_start:
    - command: "python D:/Hermes/skills/hermes-cortex/scripts/hook_session_start.py"
      timeout: 30
  on_session_end:
    - command: "python D:/Hermes/skills/hermes-cortex/scripts/hook_session_end.py"
      timeout: 60
hooks_auto_accept: true
```

**Key rules**:
- `command` is a SINGLE STRING (parsed by `shlex.split`), NOT separate `command` + `args`
- `matcher` is only for `pre_tool_call`/`post_tool_call` events
- `timeout` max 300s, default 60s
- Use `python` not `bash` on Windows (Unicode encoding issues)

## Allowlist Format

```json
{
  "approvals": [
    {
      "event": "on_session_start",
      "command": "python D:/Hermes/skills/hermes-cortex/scripts/hook_session_start.py",
      "approved_at": "2026-06-14T01:30:00Z",
      "script_mtime_at_approval": "2026-06-14T01:20:00Z"
    }
  ]
}
```

## Valid Hook Events

```
pre_tool_call, post_tool_call
transform_terminal_output, transform_tool_result, transform_llm_output
pre_llm_call, post_llm_call
pre_api_request, post_api_request, api_request_error
on_session_start, on_session_end, on_session_finalize, on_session_reset
subagent_start, subagent_stop
pre_gateway_dispatch
pre_approval_request, post_approval_response
```

## Pitfalls

### 1. `hermes config set` stores as JSON string

`hermes config set hooks '...'` stores the value as a quoted JSON string, not a YAML dict. The `_parse_hooks_block` function checks `isinstance(hooks_cfg, dict)` and returns empty.

**Fix**: Use Python `yaml.dump` to write directly:
```python
import yaml
from pathlib import Path
cfg = yaml.safe_load(Path(config_path).read_text())
cfg['hooks'] = {...}
Path(config_path).write_text(yaml.dump(cfg, ...))
```

### 2. bash on Windows has Unicode issues

Git Bash (MSYS) subprocess output in CP936 encoding causes `UnicodeDecodeError` when Hermes reads stdout with UTF-8.

**Fix**: Use Python wrapper scripts with `capture_output=True` + `CREATE_NO_WINDOW`.

### 3. allowlist path is in AppData, not ~/.hermes

`get_hermes_home()` returns `AppData/Local/hermes`, so the allowlist is at `AppData/Local/hermes/shell-hooks-allowlist.json`.

### 4. SOUL.md is at ~/.hermes/SOUL.md (different from config!)

SOUL.md is read from `~/.hermes/SOUL.md` which IS the home directory path. This is different from config.yaml which reads from AppData.

## Verification Commands

```bash
hermes hooks list          # Should show ✓ allowed
hermes hooks doctor        # Should show All healthy
hermes hooks test on_session_end    # Should show exit=0
hermes hooks test on_session_start  # Should show exit=0
```

## Windows Task Scheduler (Daily + Idle)

```powershell
# Create task with daily trigger at 9PM
$action = New-ScheduledTaskAction -Execute 'D:\Hermes\skills\hermes-cortex\scripts\cron_task.sh'
$trigger = New-ScheduledTaskTrigger -Daily -At '21:00'
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName 'Hermes Brain Auto Evolve' -Action $action -Trigger $trigger -Settings $settings -Force

# Add idle trigger (10 min idle)
$task = Get-ScheduledTask -TaskName 'Hermes Brain Auto Evolve'
$task.Settings.IdleSettings.IdleDuration = 'PT10M'
$task.Settings.IdleSettings.WaitTimeout = 'PT1H'
$task.Settings.IdleSettings.StopOnIdleEnd = $false
$task | Set-ScheduledTask
```

**Pitfall**: `New-ScheduledTaskTrigger -AtIdle` does NOT exist. Set `IdleSettings` on the task object instead.

## Auto Optimization System

`brain_hook.py` calls `auto_optimize.py` every 10 conversations (tracked via `D:\ObsidianVault\.hermes_brain_counter`).

**Thresholds** (in `auto_optimize.py`):
- note_count: 300 → archive old notes
- db_size_mb: 30MB → incremental index rebuild
- isolated_count: 20 → clean isolated notes
- orphan_links: 50 → clean broken links
- hot_cache_age_hours: 24 → refresh hot cache
