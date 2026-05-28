# Google DSA Interview Practice 🎯

Welcome to your personalized Data Structures and Algorithms (DSA) preparation repository, specifically targeted for Google coding interviews.

This repository tracks the problems you should solve, the ones you have already solved, and your overall progress. The database is populated from a comprehensive list of Google LeetCode problems, sorted by frequency to help you focus on the highest-impact questions.

## Project Structure

- `database.json`: The core database containing all problems, their metadata, and your current status.
- `scripts/`: Utilities for interacting with the database.
  - `generate_db.py`: The script that was used to parse the initial CSV data and generate `database.json`.
  - `dsa.py`: The primary CLI tool to interact with your problem set.
- `solutions/`: A dedicated folder where you can save your actual code implementations.

## Getting Started

### The CLI Tool (`dsa.py`)

A command-line tool is provided to help you pick problems, mark them as solved, and view your progress.

**1. View your stats**

To see how many problems you have solved so far:

```bash
uv run scripts/dsa.py stats
```

**2. Pick a problem to solve**

Need a suggestion? The tool will pick a random unsolved problem from the top 50 most frequently asked questions. 

```bash
uv run scripts/dsa.py pick
```

You can also filter by difficulty or change the pool size:

```bash
# Pick from the top 20 most frequent 'Medium' problems
uv run scripts/dsa.py pick --difficulty medium --top 20
```

**3. Mark a problem as solved**

Once you have successfully solved a problem, log your victory using its ID or URL:

```bash
# Mark problem ID 1 as solved
uv run scripts/dsa.py solve 1
```

## Writing Solutions

It is recommended to save your code in the `solutions/` folder. Use a naming convention like `YYYY-MM-DD-ProblemName.py` or `ID-ProblemName.cpp` to keep things organized.

Happy coding and good luck with your interview preparation! 🚀
