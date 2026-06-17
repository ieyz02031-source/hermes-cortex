# AHE 可观测性驱动 — 研究方法论与实现

> 基于 learn-harness-engineering (8,427⭐) 和 awesome-harness-engineering (3,175⭐) 的深度研究

## 核心洞察

**可观测性不是"加日志"，而是两层架构：**

```
┌─────────────────────────────────────────────┐
│  Layer 2: 过程可观测性 (Process Observability) │
│  - Sprint 合同：任务前协商"完成"的定义          │
│  - 评估者评分表：量化质量评估                    │
│  - 验收标准：明确的通过/失败条件                │
├─────────────────────────────────────────────┤
│  Layer 1: 运行时可观测性 (Runtime Observability)│
│  - 日志、追踪、健康检查                        │
│  - 系统级信号收集                              │
│  - 资源使用监控                                │
└─────────────────────────────────────────────┘
```

## Anthropic 三角色架构实验数据

**同一任务（"构建浏览器 DAW"），三种架构：**

| 架构 | 时间 | 成本 | 效果 |
|------|------|------|------|
| 无 Harness | 20 分钟 | $9 | 不能用 |
| 完整 Harness | 6 小时 | $200 | 能玩游戏 |
| 三角色架构 | 3 小时 50 分 | $124.70 | 高质量 |

**三角色架构细节：**

| 角色 | 时间 | 成本 | 职责 |
|------|------|------|------|
| Planner | 4.7 分钟 | $0.46 | 需求 → 产品规格 |
| Generator | 2 小时 7 分 | $71.08 | 按 Sprint 合同实现 |
| Evaluator | 8.8 分钟 | $3.24 | 用 Playwright 测试 |

**关键发现**：3x 效率差异，唯一变量是可观测性。

## Sprint 合同机制

**核心思想**：任务前协商"完成"的定义，避免"感觉完成了"但实际没完成。

**模板**：
```markdown
# Sprint 合同：暗黑模式支持

## 范围
- 修改主题切换组件
- 更新全局 CSS 变量
- 添加暗黑模式测试

## 验证标准
- 每个组件的视觉回归测试通过
- 主流程端到端测试通过
- 无无样式内容闪烁 (FOUC)

## 排除项
- 不处理打印样式
- 不处理第三方组件暗黑模式
```

**使用**：
```bash
python scripts/sprint_contract.py create "任务标题" "范围" "验证标准" "排除项"
python scripts/sprint_contract.py list
python scripts/sprint_contract.py show <contract_id>
```

## 评估者评分表机制

**核心思想**：将"好不好"转化为可量化评分，避免主观判断。

**默认维度**：
| 维度 | A (4分) | B (3分) | C (2分) | D (1分) |
|------|---------|---------|---------|---------|
| 代码正确性 | 所有测试通过 | 主流程通过 | 部分通过 | 构建失败 |
| 架构合规性 | 完全合规 | 轻微偏差 | 明显偏差 | 严重违规 |
| 测试覆盖 | 主流程+边界 | 仅主流程 | 仅骨架 | 无测试 |
| 性能 | 超出预期 | 符合预期 | 略低于预期 | 严重不足 |
| 安全性 | 无安全漏洞 | 低风险漏洞 | 中等风险漏洞 | 高风险漏洞 |

**使用**：
```bash
python scripts/evaluator_rubric.py create "评分表标题"
python scripts/evaluator_rubric.py evaluate <rubric_id> <task_id> "维度:评分" "维度:证据"
python scripts/evaluator_rubric.py summary <rubric_id>
```

## 消融实验机制

**核心思想**：逐个移除组件，识别哪个组件真正重要。

**Harness 组件**：
| 组件 | 名称 | 描述 |
|------|------|------|
| instructions | 指令 | SKILL.md 指令集 |
| state | 状态 | 进度追踪和状态持久化 |
| verification | 验证 | 自动验证和质量检查 |
| scope | 范围 | 功能边界控制 |
| lifecycle | 生命周期 | 会话初始化和清理 |
| sprint_contract | Sprint 合同 | 任务前协商完成定义 |
| evaluator_rubric | 评估者评分表 | 量化质量评估 |
| observability | 可观测性 | 运行时信号收集 |

**使用**：
```bash
python scripts/ablation_experiment.py create "实验标题"
python scripts/ablation_experiment.py run <experiment_id> <test_script> "指标1,指标2"
python scripts/ablation_experiment.py report <experiment_id>
```

## 预期效果

| 指标 | 预期提升 |
|------|----------|
| 任务完成效率 | +30% |
| 代码质量 | +40% |
| 系统可观测性 | +50% |

## 参考资源

- [learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering) — 12 讲座 + 6 项目
- [awesome-harness-engineering](https://github.com/walkinglabs/awesome-harness-engineering) — 186KB 资源列表
- [Anthropic: Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [OpenAI: Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)

## 安全实现原则

用户明确要求"确保不会对自身影响"。实现 AHE 组件时遵循：

1. **先备份** — `cp -r skill_dir skill_dir.backup.$(timestamp)`
2. **验证现有** — `verify_harness.py` 确认 11/11 通过
3. **实现新功能** — 新脚本独立，不修改现有脚本逻辑
4. **再次验证** — 新旧功能都正常
5. **更新追踪** — feature_list.json + progress.md

关键：新脚本是增量添加，不是替换。不影响现有 44 个技能、Shell Hooks、SOUL.md。

## L11 可观测性核心教训

来自 learn-harness-engineering 第 11 讲：

1. **没有可观测性时**：Agent 在不确定性下决策，重试变成盲目摸索，评估变成主观判断
2. **有可观测性时**：3x 效率差异，唯一变量是可观测性
3. **Sprint 合同**：任务前协商"完成"的定义，Generator 和 Evaluator 用同一份合同
4. **评估者评分表**：将"感觉不对"转化为具体证据（如"按钮对比度不足 WCAG AA 4.5:1，实测 2.1:1"）
5. **Evaluator 调优**：读评估者日志，找到判断偏差，更新 QA prompt 针对具体问题
