# Memory Architecture Patterns for Hermes

## Current Architecture (2026-06-14)

### Four-Layer Model (v4.0)

| Layer | System | Capacity | Injection | Content |
|-------|--------|----------|-----------|---------|
| Hot | memory | 10K chars | Auto every turn | Core rules, prefs, env |
| Warm | engram | Unlimited | MCP search | Project details, decisions |
| Cold | Obsidian | Unlimited | Manual/script | Full docs, research |
| Graph | knowledge_graph.py | 11 entities, 11 relations | Intelligent retrieval | Entity relationships |

### Hot Layer Content (43 entries, 48% usage)

Categories:
- User preferences (8): NO_C_DRIVE, CHINESE_ANNOTATIONS, KEEP_USED_SKILLS, EXPLAIN_FLOW_FIRST, RESEARCH_FIRST, BATCH_READING, NO_NEXT_STEPS, EXPLAIN_BEFORE_EXECUTE
- Workflow rules (6): WORKFLOW_NO_BLIND_ACTION, THINK_BEFORE_ACT, GITHUB_SYNC_RULE, SKILL_USAGE_RULE, KNOWLEDGE_STORAGE_RULE, MEMORY_POLICY
- Environment (5): HERMES_PATHS, PYTHON_ENV_SPLIT, DATA_ON_D_DRIVE, MEMORY_SYSTEM_OPTIMIZATION, When reporting model specs
- Tool configs (4): VIBE_CODING_WORKFLOW, DESIGN_VISUAL_RESEARCH, LUXURY_VS_TECH, DESIGN_PROMPT_WEBSITES
- Design rules (3): PITFALL_AI_FLAVOR, TASTE_CRITIC_RULES, SKILL_CLEANUP_DONE
- Integrations (5): AHE+engram, open-websearch, SOUL.md, Impeccable, Taste-as-Code
- References (8): Professional README, NVIDIA NIM, MemOS, WeChat, DESIGN_REF, etc.
- System (4): MEMORY_SYSTEM, MEMORY_SELF_MANAGER, KNOWLEDGE_GRAPH_SYSTEM, MEMORY_SYSTEM_UPGRADE

### Warm Layer Content (16 memories)

All stored in engram with structured format (What/Why/Where/Learned).

### Knowledge Graph (11 entities, 11 relations)

**Entity Types:**
- person: user
- system: hermes
- tool: engram, obsidian
- concept: luxury_design, warm_enterprise
- workflow: vibe_coding
- brand: cartier, aesop
- preference: light_theme, no_ai_flavor

**Relation Types:**
- 偏好: user → light_theme, no_ai_flavor
- 集成: hermes → engram, obsidian
- 参考: luxury_design → cartier, aesop
- 包含: vibe_coding → luxury_design, warm_enterprise
- 使用: user → hermes, vibe_coding

### Intelligent Retrieval (smart_retrieval.py)

**Capabilities:**
- Predict user needs based on context
- Search by entity relationships
- Traverse relations to find related entities
- Find paths between entities

**Example:**
- Query: "我想做一个高端网站"
- Prediction: 奢侈品设计 (confidence: 0.9)
- Results: VIBE_CODING_WORKFLOW, Luxury vs Tech Design Patterns

### Self-Management (memory_self_manager.py)

**Health Check:**
- memory usage threshold: 80%
- engram min memories: 10
- stale days threshold: 30

**Auto Maintenance:**
- Cleanup: Remove stale memories
- Sync: Keep memory indexes aligned with engram
- Decay: Reduce weight of low-frequency memories

**Health Score:** 90/100

## Optimization Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Memory usage | 68% | 48% | -20% |
| engram memories | 2 | 16 | +14 |
| Knowledge graph | 0 | 11 entities | +11 |
| Intelligent retrieval | 0 | 1 system | +1 |
| Self-management | 0 | 1 system | +1 |
| Total scripts | 0 | 10 | +10 |
| Total features | 0 | 28 | +28 |

## Design Decisions

1. **Why not unified?** — memory needs auto-injection, engram needs search, Obsidian needs persistence
2. **Why engram over Mem0?** — engram is zero-dependency Go binary, Mem0 needs OpenAI API
3. **Why 10K char limit?** — balances context window usage with information density
4. **Why one-line indexes?** — preserves lookup ability while minimizing Hot layer usage
5. **Why knowledge graph?** — enables prediction, reasoning, and relationship traversal
6. **Why self-management?** — reduces manual maintenance, keeps system healthy

## Scripts

| Script | Purpose | Status |
|--------|---------|--------|
| memory_auto_cleanup.py | Auto cleanup stale memories | ✓ |
| memory_decay.py | Decay low-frequency memories | ✓ |
| memory_sync.py | Sync memory and engram | ✓ |
| semantic_search.py | Semantic search with embeddings | ✓ |
| memory_tags.py | Tag-based classification | ✓ |
| auto_learning.py | Extract memories from conversations | ✓ |
| memory_priority.py | Priority-based retrieval | ✓ |
| knowledge_graph.py | Entity-relationship graph | ✓ |
| smart_retrieval.py | Intelligent retrieval | ✓ |
| memory_self_manager.py | Self-management system | ✓ |

## Pitfalls

1. **FTS5 keyword matching** — engram uses FTS5, not semantic search. Chinese queries may not find English memories.
2. **engram requires correct working directory** — must cd to git repo directory before calling.
3. **web_search token expiry** — Firecrawl tokens expire, use open-websearch as fallback.
4. **memory replace needs short unique substring** — don't use full text with escape characters.
