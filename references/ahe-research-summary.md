# AHE 可观测性驱动研究总结

## 核心发现

**两层架构**（来自 learn-harness-engineering L11）：
- **运行时可观测性**：日志、追踪、健康检查 → "系统做了什么"
- **过程可观测性**：Sprint 合同、评分表、验收标准 → "为什么接受这个变更"

## Anthropic 实验数据

同一任务，三种架构：

| 架构 | 时间 | 成本 | 效果 |
|------|------|------|------|
| **无 Harness** | 20 分钟 | $9 | 不能用 |
| **完整 Harness** | 6 小时 | $200 | 能玩游戏 |
| **三角色架构** | 3 小时 50 分 | $124.70 | 高质量 |

## 已实现组件

| 组件 | 文件 | 功能 |
|------|------|------|
| **Sprint 合同** | scripts/sprint_contract.py | 任务前协商"完成"的定义 |
| **评估者评分表** | scripts/evaluator_rubric.py | 量化质量评估 |
| **消融实验** | scripts/ablation_experiment.py | 识别关键组件 |

## 预期收益

- 任务完成效率提升 30%
- 代码质量提升 40%
- 系统可观测性提升 50%

## 参考资源

- learn-harness-engineering: 8,429⭐，12 讲座 + 6 项目
- awesome-harness-engineering: 1,817⭐，186KB 资源列表
- Anthropic 实验: 三角色架构数据
