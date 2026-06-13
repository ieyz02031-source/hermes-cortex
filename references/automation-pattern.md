# 自动化设计模式

> 关键教训：用户说"这个skill不是大脑吗，还要特定使用吗？"

## 问题

最初版本的 Hermes Brain 是一堆需要手动运行的脚本：
```bash
python scripts/evolve.py run      # 需要手动触发
python scripts/hot_cache.py       # 需要手动触发
python scripts/semantic_index.py index  # 需要手动触发
```

用户反馈：**"大脑"应该是自动工作的，不需要人去按按钮。**

## 解决方案

### 设计原则

**"Brain" 类 skill 必须是自动的**：
1. 提问时自动检索
2. 学习时自动记录
3. 对话结束时自动维护

### 实现方式

#### 1. brain_hook.py — 对话结束自动运行

```python
#!/usr/bin/env python3
"""
Hermes Brain 自动化 Hook
在每次对话结束时自动运行，更新热缓存和索引
"""
import subprocess
from pathlib import Path

SKILL_DIR = Path(r"D:\Hermes\skills\hermes-cortex")
SCRIPTS_DIR = SKILL_DIR / "scripts"
PYTHON_312 = Path(r"C:\Users\20716\AppData\Local\Programs\Python\Python312\python.exe")

def run_script(script_name, args=None):
    cmd = [str(PYTHON_312), str(SCRIPTS_DIR / script_name)]
    if args:
        cmd.extend(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.returncode == 0
    except:
        return False

def main():
    # 1. 更新热缓存
    run_script("hot_cache.py")
    
    # 2. 更新语义索引（每天只运行一次）
    index_file = Path(r"D:\ObsidianVault") / ".hermes_brain.db"
    if index_file.exists():
        import time
        hours_since_update = (time.time() - index_file.stat().st_mtime) / 3600
        if hours_since_update > 24:
            run_script("semantic_index.py", ["index"])
    
    # 3. 检查孤立笔记
    run_script("maintain.py", ["isolated"])

if __name__ == "__main__":
    main()
```

#### 2. 对话中自动检索

在回答问题前，自动检索知识库：
```bash
python scripts/retrieve.py "用户的问题"
```

#### 3. 学习后自动创建笔记

学到新知识后，自动运行自进化循环：
```bash
python scripts/evolve.py run
```

### Windows 计划任务

每天晚上 9 点自动运行自进化循环：
```powershell
# PowerShell 注册计划任务
$action = New-ScheduledTaskAction -Execute 'D:\Hermes\skills\hermes-cortex\scripts\cron_task.sh'
$trigger = New-ScheduledTaskTrigger -Daily -At '21:00'
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName 'Hermes Brain Auto Evolve' -Action $action -Trigger $trigger -Settings $settings -Force

# 更新已有任务
Unregister-ScheduledTask -TaskName 'Hermes Brain Auto Evolve' -Confirm:$false
Register-ScheduledTask -TaskName 'Hermes Brain Auto Evolve' -Action $action -Trigger $trigger -Settings $settings -Force
```

**⚠️ 更新计划任务时**：必须先 `Unregister-ScheduledTask` 再 `Register-ScheduledTask`，不能直接覆盖。

### 空闲时自动运行

```powershell
# 添加空闲触发器（电脑空闲 10 分钟后运行）
$task = Get-ScheduledTask -TaskName 'Hermes Brain Auto Evolve'
$task.Settings.IdleSettings.IdleDuration = 'PT10M'
$task.Settings.IdleSettings.WaitTimeout = 'PT1H'
$task.Settings.IdleSettings.StopOnIdleEnd = $false
$task | Set-ScheduledTask
```

**⚠️ Pitfall**: `New-ScheduledTaskTrigger -AtIdle` 参数不存在。必须设置 `$task.Settings.IdleSettings` 属性。

### 自动优化（防臃肿）

`brain_hook.py` 每 10 次对话自动调用 `auto_optimize.py`，检查：
- 笔记数 > 300 → 归档旧笔记
- 索引 > 30MB → 增量优化
- 孤立笔记 > 20 → 清理
- 无效链接 > 50 → 清理
- 热缓存 > 24h → 更新

计数器文件：`D:\ObsidianVault\.hermes_brain_counter`

## 反模式

### ❌ 需要手动触发的"大脑"

```bash
# 这不是大脑，只是一堆脚本
python scripts/evolve.py run
python scripts/hot_cache.py
python scripts/semantic_index.py index
```

### ✅ 真正自动的大脑

```python
# 用户无感知，后台自动运行
import subprocess
subprocess.run(["python", "brain_hook.py"])
```

## 总结

**设计 "Brain" 类 skill 时，必须问自己**：
1. 用户需要手动触发吗？→ 如果是，设计失败
2. 用户需要知道内部实现吗？→ 如果是，设计失败
3. 用户需要分步操作吗？→ 如果是，设计失败

**正确答案**：所有操作在后台自动运行，用户只管提问和学习。
