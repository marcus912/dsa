#!/usr/bin/env python3
import json
import os
import argparse
import random
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database.json")

def load_db():
    if not os.path.exists(DB_PATH):
        console.print(f"[bold red]Error:[/] Database not found at {DB_PATH}")
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(db):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)

def show_stats(db):
    total = len(db)
    solved = sum(1 for p in db if p.get("status") == "solved")
    
    table = Table(title="📊 Algorithms Progress Statistics", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right")
    
    table.add_row("Total Problems", str(total))
    table.add_row("Solved", f"{solved} ({solved/total*100:.2f}%)")
    table.add_row("Remaining", str(total - solved))
    
    console.print(table)
    
    diff_stats = {"Easy": [0,0], "Medium": [0,0], "Hard": [0,0]}
    for p in db:
        diff = p.get("difficulty", "Unknown")
        if diff not in diff_stats:
            diff_stats[diff] = [0,0]
        diff_stats[diff][1] += 1
        if p.get("status") == "solved":
            diff_stats[diff][0] += 1
            
    diff_table = Table(title="--- By Difficulty ---", show_header=True, header_style="bold green")
    diff_table.add_column("Difficulty")
    diff_table.add_column("Solved", justify="right")
    diff_table.add_column("Total", justify="right")
    diff_table.add_column("%", justify="right")

    for diff in ["Easy", "Medium", "Hard"]:
        if diff in diff_stats:
            s, t = diff_stats[diff]
            if t > 0:
                color = "green" if diff == "Easy" else "yellow" if diff == "Medium" else "red"
                diff_table.add_row(f"[{color}]{diff}[/]", str(s), str(t), f"{s/t*100:.1f}%")
    
    console.print(diff_table)

def pick_problem(db, difficulty=None, top_n=50):
    candidates = [p for p in db if p.get("status") != "solved"]
    
    if difficulty:
        candidates = [p for p in candidates if p.get("difficulty", "").lower() == difficulty.lower()]
        
    if not candidates:
        console.print("[yellow]No unsolved problems found matching criteria![/]")
        return

    pool = candidates[:top_n]
    chosen = random.choice(pool)
    
    content = f"[bold]ID:[/] {chosen['id']}\n"
    content += f"[bold]Title:[/] {chosen['title']}\n"
    content += f"[bold]Difficulty:[/] {chosen['difficulty']}\n"
    content += f"[bold]Frequency:[/] {chosen['frequency']}%\n"
    if chosen.get('topics'):
        content += f"[bold]Topics:[/] {', '.join(chosen['topics'])}\n"
    content += f"[bold]URL:[/] [link={chosen['url']}]{chosen['url']}[/link]"

    console.print(Panel(content, title="🎯 Suggested Problem", expand=False, border_style="bold blue"))
    console.print(f"\nRun [bold green]uv run scripts/algo.py solve {chosen['id']}[/] to mark it as solved!")

def solve_problem(db, pid_or_url):
    target = None
    for p in db:
        if str(p["id"]) == str(pid_or_url) or p["url"] == pid_or_url:
            target = p
            break
            
    if not target:
        console.print(f"[bold red]Error:[/] Problem with ID or URL '{pid_or_url}' not found.")
        return
        
    if target.get("status") == "solved":
        console.print(f"[yellow]Problem '{target['title']}' is already marked as solved![/]")
        return
        
    target["status"] = "solved"
    target["date_solved"] = datetime.now().strftime("%Y-%m-%d")
    save_db(db)
    
    console.print(f"✅ [bold green]Awesome job![/] Marked '{target['title']}' as [bold]SOLVED[/].")

def main():
    parser = argparse.ArgumentParser(description="Algorithms Study Lab CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    subparsers.add_parser("stats", help="Show current progress statistics")
    
    pick_parser = subparsers.add_parser("pick", help="Pick a random unsolved problem")
    pick_parser.add_argument("-d", "--difficulty", choices=["easy", "medium", "hard"], help="Filter by difficulty")
    pick_parser.add_argument("-n", "--top", type=int, default=50, help="Pick from the top N most frequent")
    
    solve_parser = subparsers.add_parser("solve", help="Mark a problem as solved")
    solve_parser.add_argument("id", help="The ID or URL of the problem")
    
    args = parser.parse_args()
    db = load_db()
    
    if args.command == "stats":
        show_stats(db)
    elif args.command == "pick":
        pick_problem(db, args.difficulty, args.top)
    elif args.command == "solve":
        solve_problem(db, args.id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
