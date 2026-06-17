# Hermes Cortex 5 阶段优化方案

## 概述

基于 GitHub 研究 + 社区资源 + 实践总结的优化方案。

## 第一阶段：上下文压缩（立即见效）

**目标**：每轮消耗从 113K 降到 80K tokens

| 优化项 | 当前 | 目标 | 方法 |
|--------|------|------|------|
| SOUL.md | 11.7KB | <1KB | 只保留核心人格规则 |
| 系统提示 | ~50KB | ~30KB | 压缩技能描述 |
| 技能描述 | 冗余 | 精简 | 去掉示例和细节 |

**效果**：每轮节省 ~30K tokens

**详见**：`references/soul-compression.md`

## 第二阶段：技能自进化（质量提升）

**来源**：[hermes-agent-self-evolution](https://github.com/NousResearch/hermes-agent-self-evolution) (4,081⭐)

**原理**：用 DSPy + GEPA 自动优化技能描述

```
读取当前技能 → 生成评估数据 → GEPA 优化器（理解为什么失败）
    → 候选变体 → 评估 → 约束门控 → 最优变体
```

**执行**：
```bash
# 安装
git clone https://github.com/NousResearch/hermes-agent-self-evolution.git
cd hermes-agent-self-evolution
pip install -e ".[dev]"

# 优化单个技能
python -m evolution.skills.evolve_skill \
    --skill hermes-cortex \
    --iterations 10 \
    --eval-source synthetic
```

**效果**：技能质量提升 30%+

## 第三阶段：知识图谱升级（检索提升）

**来源**：[LightRAG](https://github.com/HKUDS/LightRAG) (EMNLP 2025)

**对比**：

| 能力 | 当前（语义索引） | 升级后（LightRAG） |
|------|------------------|-------------------|
| 搜索方式 | 文本相似度 | 实体关系 + 文本相似度 |
| 回答质量 | "文档里说了X" | "X和Y的关系，谁决定了Z" |
| 扩展性 | 500+文档退化 | 文档越多越好 |

**执行**：
```bash
# 安装 LightRAG
mkdir -p ~/.hermes/lightrag
cd ~/.hermes/lightrag
git clone https://github.com/HKUDS/LightRAG.git
cd LightRAG
pip install -e ".[api]"

# 启动服务
lightrag-server --host 127.0.0.1 --port 9623

# 导入现有知识
for file in D:/ObsidianVault/raw/exploration/*.md; do
  curl -X POST http://localhost:9623/documents/upload -F "file=@$file"
done
```

**效果**：检索准确率提升 50%+

## 第四阶段：成本优化（省钱）

**来源**：[hermes-optimization-guide](https://github.com/OnlyTerp/hermes-optimization-guide) (437⭐)

**方案**：

| 任务类型 | 推荐模型 | 原因 |
|----------|----------|------|
| 简单问答 | Kimi K2.6 | 便宜、快 |
| 复杂推理 | Claude Sonnet 5 | 质量高 |
| 代码生成 | GPT-5.5 | 工具调用强 |
| 嵌入 | nomic-embed-text | 免费本地 |

**执行**：
```bash
# 配置模型路由
hermes config set model anthropic/claude-sonnet-5
hermes config set fallback_models '["openrouter/moonshotai/kimi-k2.6"]'

# 启用提示缓存
hermes config set prompt_caching.enabled true

# 启用上下文压缩
hermes config set context_compression.enabled true
```

**效果**：成本降低 40-60%

## 第五阶段：可观测性（看得见）

**来源**：hermes-optimization-guide Part 20

**功能**：
- 看到每轮消耗多少 token
- 哪些技能被加载了
- 哪些工具调用失败了
- 成本趋势

**执行**：
```bash
# 安装 Langfuse 插件
hermes plugins install langfuse

# 配置
hermes config set plugins.langfuse.enabled true
hermes config set plugins.langfuse.public_key "your-key"
hermes config set plugins.langfuse.secret_key "your-secret"
```

**效果**：全链路追踪，知道钱花在哪

## 执行时间表

| 天数 | 阶段 | 任务 | 预期效果 |
|------|------|------|----------|
| **第1天** | 第一阶段 | 压缩 SOUL.md + 系统提示 | 每轮 -30K tokens |
| **第2天** | 第二阶段 | 技能自进化 | 质量 +30% |
| **第3天** | 第三阶段 | 知识图谱升级 | 检索 +50% |
| **第4天** | 第四阶段 | 成本优化 | 成本 -50% |
| **第5天** | 第五阶段 | 可观测性 | 全链路追踪 |

## 风险控制

| 风险 | 应对 |
|------|------|
| 技能自进化失败 | 保留原版，只替换通过测试的 |
| 知识图谱导入慢 | 先导入核心 10 个笔记测试 |
| 模型路由配置错 | 保留 fallback 模型 |
| Langfuse 部署失败 | 先用本地日志替代 |

## 预期最终效果

| 指标 | 当前 | 优化后 | 提升 |
|------|------|--------|------|
| 每轮消耗 | 113K tokens | ~60K tokens | -47% |
| 技能质量 | 基础 | 自进化 | +30% |
| 检索准确率 | 69.8% | ~90% | +29% |
| 成本 | 基准 | 优化后 | -50% |
| 可观测性 | 无 | 全链路 | 从0到1 |
