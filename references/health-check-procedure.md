# Hermes Cortex 全面体检流程

当用户说"体检"、"检查状态"、"系统状态"时，运行以下检查。

## 检查清单

### 1. 文件结构
```bash
cd "D:\Hermes\skills\hermes-cortex"
find . -type f | wc -l          # 总文件数
du -sh .                         # 目录大小
ls -la scripts/*.py | wc -l     # Python 脚本数
ls -la references/*.md | wc -l  # 参考文档数
ls -la templates/*.md | wc -l   # 模板文件数
```

### 2. 脚本语法检查
```bash
for f in scripts/*.py; do python -m py_compile "$f" 2>&1 && echo "✅ $f" || echo "❌ $f"; done
```

### 3. Harness 验证
```bash
python scripts/verify_harness.py
```

### 4. 知识库状态
```bash
python scripts/auto_optimize.py      # 警戒线检查
python scripts/hot_cache.py          # 热缓存更新
python scripts/semantic_index.py stats  # 语义索引统计
python scripts/build_graph.py        # 知识图谱构建
python scripts/auto_research.py report  # 自进化报告
python scripts/retrieve.py "测试查询"  # 知识检索测试
```

### 5. 自动化系统
```bash
# Shell Hooks
cat scripts/hook_session_start.py | head -5

# 计划任务
powershell -Command "Get-ScheduledTask -TaskName 'Hermes Cortex Auto Evolve' | Select-Object TaskName, State, NextRunTime"

# 配置文件
python -c "import yaml; config=yaml.safe_load(open('C:/Users/20716/AppData/Local/hermes/config.yaml')); print('hooks:', 'on_session_start' in config.get('hooks', {})); print('hooks_auto_accept:', config.get('hooks_auto_accept', False))"
```

### 6. 资源使用
```bash
ls -la "D:\ObsidianVault\.hermes_brain.db"  # 数据库大小
du -sh "D:\ObsidianVault"                   # Vault 大小
```

## 健康度评分标准

| 项目 | 满分 | 评分标准 |
|------|------|----------|
| 文件完整性 | 20 | 所有文件存在且格式正确 |
| 脚本运行 | 20 | 所有脚本语法检查通过 |
| Harness 系统 | 20 | verify_harness.py 全部通过 |
| 知识库 | 20 | 健康度 > 80%，孤立笔记 < 10 |
| 自动化 | 10 | Shell Hooks + 计划任务正常 |
| 资源使用 | 10 | 磁盘空间充足，内存使用正常 |

## 输出格式

```
## ✅ Hermes Cortex 全面体检完成

### 系统状态总览
| 指标 | 状态 | 详情 |
|------|------|------|
| 文件结构 | ✅ | X 个文件，XKB |
| Python 脚本 | ✅ | X 个，全部语法检查通过 |
| ...

### 详细检查结果
...

### 系统健康度
总体评分：X/100
```
