# Memory System Upgrade - 2026-06-14

## Summary

Full upgrade of the three-layer memory system: optimization, automation, and intelligence.

## Phase 1: Memory Optimization

**Goal**: Reduce memory usage from 68% to <50%

**Method**: Migrate detailed entries to engram, keep only index in memory

**Steps**:
1. Identify entries with >100 chars of detail
2. Save detail to engram via `mem_save`
3. Replace memory entry with one-line index: `KEY: 详见engram搜索'keyword'`

**Result**: 68% → 44% usage, 15 entries migrated

**Pitfalls**:
- `memory(action='replace')` uses exact substring match. Use short prefix (first 3-5 words) as `old_text`, not the full entry. Transient escapes cause match failures.
- engram must be called from git repo directory: `cd D:/Hermes/skills/hermes-cortex && echo '...' | D:/Hermes/tools/engram/engram.exe mcp --tools=agent`
- Python subprocess has UTF-8 encoding issues on Windows. Use `terminal` tool instead.
- engram content must use `**What**: / **Why**: / **Where**: / **Learned**:` format

## Phase 2: Automation Scripts

| Script | Purpose | Location |
|--------|---------|----------|
| memory_auto_cleanup.py | Auto-cleanup stale memories, cross-layer sync, decay | scripts/ |
| memory_decay.py | Decay weights based on access frequency | scripts/ |
| memory_sync.py | Sync memory indexes ↔ engram content | scripts/ |
| semantic_search.py | Embedding-based semantic search (fallback to keyword) | scripts/ |
| memory_tags.py | Auto-classify memories by tags | scripts/ |
| auto_learning.py | Extract memories from conversations | scripts/ |
| memory_priority.py | Priority-based memory management | scripts/ |

## Decay Configuration

| Frequency | Time Range | Weight |
|-----------|------------|--------|
| High | 7 days | 100% |
| Medium | 30 days | 70% |
| Low | 90 days | 30% |
| Stale | 90+ days | 10% |

## Priority Levels

| Priority | Description | Weight | Auto-inject |
|----------|-------------|--------|-------------|
| High | Core rules, user preferences | 1.0 | Yes |
| Medium | Project details, technical docs | 0.7 | No |
| Low | History, temporary info | 0.3 | No |

## engram Calling Patterns

### Save Memory
```bash
cd D:/Hermes/skills/hermes-cortex && echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"mem_save","arguments":{"title":"Title","content":"**What**: ...\\n**Why**: ...\\n**Where**: ...\\n**Learned**: ...","type":"learning","topic_key":"my_key"}},"id":1}' | D:/Hermes/tools/engram/engram.exe mcp --tools=agent
```

### Search Memory
```bash
cd D:/Hermes/skills/hermes-cortex && echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"mem_search","arguments":{"query":"search term","limit":5}},"id":1}' | D:/Hermes/tools/engram/engram.exe mcp --tools=agent
```

### Update Memory
```bash
cd D:/Hermes/skills/hermes-cortex && echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"mem_update","arguments":{"id":2,"title":"New Title","content":"...","type":"learning","topic_key":"new_key"}},"id":1}' | D:/Hermes/tools/engram/engram.exe mcp --tools=agent
```

### Get Context
```bash
cd D:/Hermes/skills/hermes-cortex && echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"mem_context","arguments":{"scope":"all"}},"id":1}' | D:/Hermes/tools/engram/engram.exe mcp --tools=agent
```

## Key Pitfalls

1. **engram must be called from git repo directory** — engram uses git remote to identify project. Call from wrong directory → `ambiguous_project` error.

2. **No mem_delete** — engram has no delete tool. Use `mem_update` to overwrite, or `mem_review` to mark as reviewed.

3. **FTS5 keyword search** — engram uses FTS5 full-text search, not semantic search. "高端设计" won't find "luxury design". Use English keywords or topic_key.

4. **Python subprocess encoding** — Windows Python subprocess fails with `UnicodeDecodeError` when calling engram. Use `terminal` tool instead.

5. **Content format** — engram expects `**What**: / **Why**: / **Where**: / **Learned**:` format for mem_save content.

6. **Conflict detection** — engram auto-detects semantically similar memories and marks `judgment_required: true`. Use `mem_judge` to resolve.

7. **topic_key for upserts** — Same project+scope+topic_key overwrites previous memory. Use for updating existing entries.

## Feature List Updates

- F018: 记忆系统优化 (memory optimization)
- F019: 记忆自动整理 (auto cleanup)
- F020: 记忆衰减系统 (decay system)
- F021: 跨层同步系统 (cross-layer sync)
- F022: 语义搜索系统 (semantic search)
- F023: 记忆分类标签系统 (tag system)
- F024: 自动学习系统 (auto learning)
- F025: 记忆优先级系统 (priority system)
