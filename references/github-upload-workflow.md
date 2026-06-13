# GitHub 上传工作流

> 当 git push 因网络问题（代理、防火墙）失败时的替代方案

## 问题

```
fatal: unable to access 'https://github.com/...': Failed to connect to github.com port 443
```

## 解决方案

用 `mcp_github_create_or_update_file` 逐个上传文件。

## 流程

### 1. 创建仓库

```python
mcp_github_create_repository(
    name="repo-name",
    description="项目描述",
    private=False,
    autoInit=False
)
```

### 2. 逐个上传文件

```python
# 根目录文件先上传
mcp_github_create_or_update_file(
    owner="username",
    repo="repo-name",
    path="README.md",
    content="文件内容",
    message="Add README.md",
    branch="main"
)

# 然后上传子目录文件
mcp_github_create_or_update_file(
    owner="username",
    repo="repo-name",
    path="scripts/build_graph.py",
    content="文件内容",
    message="Add scripts/build_graph.py",
    branch="main"
)
```

### 3. 检查上传状态

```bash
# 检查根目录
curl -s "https://api.github.com/repos/{owner}/{repo}/contents" | python -c "
import sys, json
items = json.load(sys.stdin)
for item in items:
    print(f\"  {item['type']:4} {item['name']}\")
"

# 检查子目录
curl -s "https://api.github.com/repos/{owner}/{repo}/contents/scripts" | python -c "
import sys, json
items = json.load(sys.stdin)
for item in items:
    print(f\"  {item['type']:4} {item['name']}\")
"
```

## 注意事项

1. **每个文件单独上传** — 不要用 `push_files`（会报空仓库错误）
2. **文件内容直接传** — 不需要 base64 编码
3. **每次上传自动 commit** — GitHub API 会自动创建 commit
4. **上传顺序** — 根目录文件 → 子目录文件
5. **大文件** — 如果文件太大，可能需要分段上传

## 示例：上传整个项目

```python
# 1. 创建仓库
mcp_github_create_repository(name="my-project", description="...")

# 2. 上传根目录文件
for file in [".gitignore", "README.md", "LICENSE", "CHANGELOG.md"]:
    content = read_file(file)
    mcp_github_create_or_update_file(
        owner="username",
        repo="my-project",
        path=file,
        content=content,
        message=f"Add {file}",
        branch="main"
    )

# 3. 上传子目录文件
for file in ["scripts/build_graph.py", "scripts/maintain.py", ...]:
    content = read_file(file)
    mcp_github_create_or_update_file(
        owner="username",
        repo="my-project",
        path=file,
        content=content,
        message=f"Add {file}",
        branch="main"
    )

# 4. 检查状态
curl -s "https://api.github.com/repos/username/my-project/contents"
```

## 验证

上传完成后，访问 `https://github.com/{owner}/{repo}` 确认：
- 所有文件都已上传
- 目录结构正确
- README 渲染正常
