# engram Integration Reference

## Quick Reference

- **Binary**: `D:\Hermes\tools\engram\engram.exe` v1.16.3
- **Tools**: 18 MCP tools (not 20)
- **Project dir**: Must cd to `D:/Hermes/skills/hermes-cortex` before calling
- **No delete**: Use mem_update to overwrite

## Tools List (18)

| Tool | Purpose |
|------|---------|
| mem_save | Save new memory |
| mem_search | Semantic search |
| mem_context | Get recent context |
| mem_update | Update existing memory |
| mem_get_observation | Get specific memory by ID |
| mem_review | List/mark reviewed memories |
| mem_compare | Record semantic verdict |
| mem_judge | Resolve conflict reviews |
| mem_pin / mem_unpin | Pin/unpin memory |
| mem_current_project | Get current project |
| mem_session_start/end | Session tracking |
| mem_session_summary | Session summary |
| mem_suggest_topic_key | Suggest topic key |
| mem_save_prompt | Save prompt as memory |
| mem_capture_passive | Extract learnings |
| mem_doctor | Diagnostic check |

## Correct Call Format

```bash
cd D:/Hermes/skills/hermes-cortex && echo '{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "mem_save", "arguments": {"title": "Title", "content": "Content", "type": "learning", "topic_key": "topic"}}, "id": 1}' | D:/Hermes/tools/engram/engram.exe mcp --tools=agent 2>&1
```

## Pitfalls

1. Must cd to project dir first
2. Use terminal pipe, not Python subprocess (encoding issues)
3. No mem_delete — use mem_update
4. Conflict detection triggers on related memories
