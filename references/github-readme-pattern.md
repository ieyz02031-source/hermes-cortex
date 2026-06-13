# GitHub README 专业格式指南

> 基于 headroom (20KB)、claude-obsidian (37KB)、swarmvault (48KB) 的分析

## 核心原则

1. **信息密度 > 字数** — 每句话都要有信息量
2. **数据说话** — 用具体数字而不是模糊描述
3. **折叠详细内容** — 用 `<details>` 隐藏长内容
4. **像说明书** — 用户看一遍就知道怎么用

## 必备章节

### 1. 开头（前 50 行决定第一印象）

```markdown
# 🧠 Project Name

<div align="center">
<pre>
ASCII art logo
</pre>
</div>

<p align="center">
  <strong>一句话介绍</strong>
</p>

<p align="center">
  快速导航链接（Install | Features | Proof | Comparison | FAQ）
</p>

徽章（License | Python | Stars | CI）
```

### 2. What it does（功能列表，不是长段落）

```markdown
## What it does

| Feature | Description |
|---------|-------------|
| Feature 1 | 具体描述，不要"支持XX"这种废话 |
| Feature 2 | 用数据说话："42 notes, 138 edges" |
```

### 3. How it works（架构图，30秒看懂）

```markdown
## How it works (30 seconds)

输入 → 处理 → 存储 → 检索 → 输出

用 ASCII 或 Mermaid 图，不要长段落
```

### 4. Get started（3步搞定）

```markdown
## Get started (30 seconds)

Step 1: Install
Step 2: Configure
Step 3: Run

每步一个命令，不要废话
```

### 5. Proof（数据证明）

```markdown
## Proof

| Metric | Value |
|--------|-------|
| Notes | 42 |
| Edges | 138 |
| Avg degree | 6.57 |
| Health score | 79.5% |
```

### 6. Compared to（竞品对比）

```markdown
## Compared to

| Feature | Us | Competitor A | Competitor B |
|---------|-----|-------------|-------------|
| Feature 1 | ✅ | ✅ | ❌ |
| Feature 2 | ✅ | ❌ | ✅ |
```

### 7. Scripts（详细文档，用折叠）

```markdown
## Scripts

<details>
<summary>Script 1 — short description</summary>

Usage, parameters, examples

</details>
```

### 8. Requirements（环境要求表格）

```markdown
## Requirements

| Component | Minimum | Recommended | Notes |
|-----------|---------|-------------|-------|
| OS | Windows 10+ | Windows 10/11 | Tested |
| Python | 3.12+ | 3.12.x | sentence-transformers |
| Disk | 100MB | 500MB | Index + notes |
| RAM | 2GB | 4GB | Embedding model |
```

### 9. FAQ（8-12个常见问题）

```markdown
## FAQ

**Q: 问题1？**
A: 回答1

**Q: 问题2？**
A: 回答2
```

### 10. When to use / When to skip

```markdown
## When to use · When to skip

✅ Use when:
- Scenario 1
- Scenario 2

❌ Skip when:
- Scenario 1
- Scenario 2
```

### 11. Troubleshooting（常见问题解决方案）

```markdown
## Troubleshooting

| Problem | Solution |
|---------|----------|
| Error 1 | Fix 1 |
| Error 2 | Fix 2 |
```

### 12. Roadmap（路线图）

```markdown
## Roadmap

### v1.2.0 (Planned)
- Feature 1
- Feature 2

### v2.0.0 (Future)
- Feature 3
```

### 13. 结尾（Contributing, License, Acknowledgments）

```markdown
## Contributing
PRs welcome!

## License
MIT

## Acknowledgments
- Project 1
- Project 2
```

## 反模式

❌ 不要：
- 长段落介绍（用表格）
- 模糊描述（用具体数字）
- 不折叠的长内容（用 `<details>`）
- 缺少环境要求
- 缺少竞品对比
- 缺少 FAQ
- 缺少 Troubleshooting

## 参考项目

| 项目 | Stars | README 大小 | 特点 |
|------|-------|------------|------|
| headroom | 2k | 20KB | 信息密度高，ASCII logo |
| claude-obsidian | 6.6k | 37KB | 完整的徽章和目录 |
| swarmvault | 556 | 48KB | 详细的脚本文档 |
