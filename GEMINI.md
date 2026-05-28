# Google DSA Interview Practice 🎯

This workspace is a specialized environment for preparing for Google's Data Structures and Algorithms (DSA) coding interviews. It manages a large database of LeetCode problems, tracks progress, and provides a CLI for interaction.

## Project Overview

- **Core Tech:** Python 3.13+, `uv` (dependency management), `rich` (CLI formatting).
- **Architecture:** 
  - `database.json`: Central state for 2,200+ problems, tracking status, frequency, and metadata.
  - `scripts/dsa.py`: Primary user-facing CLI.
  - `solutions/`: Local folder for saving problem implementations.
  - `.gemini/skills/dsa-db-query`: Custom agent skill for efficient database manipulation.

## Environment & Tooling

### Dependency Management (uv)
The project uses `uv`. Avoid using `pip` directly.
- **Install dependencies:** `uv sync`
- **Add a package:** `uv add <package>`
- **Run the CLI:** `uv run scripts/dsa.py <command>`

### Key Commands
- **Show Stats:** `uv run scripts/dsa.py stats`
- **Pick a Problem:** `uv run scripts/dsa.py pick [-d {easy,medium,hard}]`
- **Mark Solved:** `uv run scripts/dsa.py solve <ID>`

## Agent Instructions & Conventions

### Database Management
- **Token Efficiency:** NEVER read `database.json` in its entirety. It contains over 2,000 items and will exhaust the context window.
- **Query Skill:** ALWAYS use the `dsa-db-query` skill to search, filter, or update problem statuses.
- **Problem Statuses:** Only two statuses are supported: `todo` and `solved`.

### Solution Patterns
- When helping the user solve a problem, suggest saving the solution in `solutions/` with a descriptive name (e.g., `solutions/121-best-time-to-buy-and-sell-stock.py`).
- Prefer clean, idiomatic Python solutions with time and space complexity analysis in the docstring.

### Development Conventions
- Use `rich` for any CLI-based output to maintain visual consistency.
- Maintain the sorted order of `database.json` (primarily by frequency) when performing updates if the entire file is ever regenerated.
