# GitHub README 写作规范

> 参考 headroom (20KB) / claude-obsidian (37KB) / swarmvault (48KB) 的专业格式

## 必须包含的元素

| 元素 | 说明 | 示例 |
|------|------|------|
| ASCII art logo | 专业感，用 `<pre>` 标签 | headroom 风格 |
| 一句话介绍 | 精炼，不超过两行 | "Turns conversations into knowledge graph" |
| 徽章 | License、Python、Framework、Docs | 用 shields.io |
| 快速导航 | Install、Features、Proof、Comparison、Scripts、FAQ | 用锚点链接 |
| What it does | 功能列表，每项一句话 | 用 `-` 列表 |
| How it works | ASCII 架构图，30 秒理解 | 用代码块 |
| Get started | 60 秒内跑通 | 用代码块 |
| Proof | 具体数据证明 | 用表格 |
| Compared to | 与竞品的清晰对比 | 用表格 |
| When to use / When to skip | 使用场景 | 用列表 |
| 折叠部分 | 详细内容隐藏 | 用 `<details>` |
| FAQ | 至少 5 个常见问题 | 用问答格式 |
| Contributing | 贡献指南 | 用代码块 |
| Related Projects | 相关项目 | 用链接列表 |
| License | 许可证 | 用徽章 |

## 禁止的写法

- ❌ 长篇大论的段落描述
- ❌ 重复内容（同一信息出现多次）
- ❌ "下一步建议"、"待实现"、"计划中"等字眼
- ❌ 没有数据支撑的功能描述
- ❌ 过于技术性的术语（除非有解释）

## 必须的写法

- ✅ 数据说话（具体数字、统计、输出示例）
- ✅ 对比表格（与竞品的清晰对比）
- ✅ 代码示例（可直接复制运行）
- ✅ 折叠隐藏（详细内容用 `<details>` 折叠）
- ✅ 使用场景（什么时候用、什么时候不用）

## 参考项目

| 项目 | 大小 | 特点 |
|------|------|------|
| headroom | 20KB | 信息密度最高，ASCII art + 数据 + 折叠 |
| claude-obsidian | 37KB | 最完整，徽章 + 目录 + FAQ + 竞品对比 |
| swarmvault | 48KB | 最详细，多语言 + 工作示例 + 平台支持 |

## 写作流程

1. **研究参考** — 先看 3 个热门项目的 README，提取结构
2. **写框架** — 按照上面的元素列表，先写框架
3. **填充内容** — 每个部分用数据支撑
4. **折叠细节** — 详细内容用 `<details>` 折叠
5. **检查重复** — 确保没有重复内容
6. **检查字数** — 目标 15-25KB，不超过 30KB

## 常见错误

| 错误 | 正确做法 |
|------|---------|
| 写了 33KB 但信息密度低 | 参考 headroom，17KB 信息密度更高 |
| 没有数据支撑 | 用具体数字、统计、输出示例 |
| 没有对比表格 | 与竞品做清晰对比 |
| 没有折叠部分 | 详细内容用 `<details>` 折叠 |
| 有重复内容 | 删除重复，合并相似内容 |
| 写了"下一步" | 删除，一次做完 |
