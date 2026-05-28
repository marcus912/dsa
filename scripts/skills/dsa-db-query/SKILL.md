---
name: dsa-db-query
description: Efficiently query and update the LeetCode problem database for Google DSA practice. Use this skill when Gemini CLI needs to find specific problems, filter by difficulty/status/topic, or update the solved status of a problem without reading the entire database.json file into context.
---

# DSA Database Query Skill

This skill provides a programmatic way to interact with the `database.json` file. This is highly recommended to save context tokens.

## Workflows

### 1. Querying Problems
Use the `scripts/query_db.py` script to find problems.

```bash
uv run scripts/skills/dsa-db-query/scripts/query_db.py query "{'difficulty': 'medium', 'status': 'todo', 'limit': 5}"
```

**Supported parameters:**
- `id`: Filter by specific LeetCode ID.
- `difficulty`: 'easy', 'medium', or 'hard'.
- `status`: 'todo' or 'solved'.
- `title_search`: Partial string match on the title.
- `limit`: Number of results to return (default 10).

### 2. Updating Problem Status
Use the same script to mark a problem as solved.

```bash
uv run scripts/skills/dsa-db-query/scripts/query_db.py update "{'id': 1, 'status': 'solved'}"
```

## Best Practices
- **Always query before updating:** Verify the problem exists and check its current state.
- **Limit results:** Avoid returning hundreds of problems to keep your context lean.
- **Prefer IDs:** When updating, always use the numeric ID for precision.
