import csv
import json
import os
import re

snehasishroy_all = "/tmp/marcus-interview/coding/leetcode-google/snehasishroy/all.csv"
liquidslr_all = "/tmp/marcus-interview/coding/leetcode-google/liquidslr/5. All.csv"

# First, read snehasishroy for IDs and basic info
problems = {}

with open(snehasishroy_all, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        url = row.get('URL', '').strip()
        if not url:
            continue
        
        # Parse ID if possible
        try:
            pid = int(row.get('ID', 0))
        except ValueError:
            pid = 0
            
        freq_str = row.get('Frequency %', '0%').strip('%')
        try:
            freq = float(freq_str)
        except ValueError:
            freq = 0.0

        problems[url] = {
            "id": pid,
            "title": row.get('Title', ''),
            "url": url,
            "difficulty": row.get('Difficulty', '').capitalize(),
            "frequency": freq,
            "topics": [],
            "status": "todo",
            "date_solved": None,
            "notes": ""
        }

# Read liquidslr for Topics, update or add problems
with open(liquidslr_all, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        url = row.get('Link', '').strip()
        if not url:
            continue
            
        topics_str = row.get('Topics', '')
        topics = [t.strip() for t in topics_str.split(',') if t.strip()]
        
        freq_str = row.get('Frequency', '0')
        try:
            freq = float(freq_str)
        except ValueError:
            freq = 0.0
            
        diff = row.get('Difficulty', '').capitalize()
        title = row.get('Title', '')
            
        if url in problems:
            problems[url]['topics'] = topics
            if problems[url]['frequency'] == 0:
                problems[url]['frequency'] = freq
        else:
            # Add missing problem without ID
            problems[url] = {
                "id": None,
                "title": title,
                "url": url,
                "difficulty": diff,
                "frequency": freq,
                "topics": topics,
                "status": "todo",
                "date_solved": None,
                "notes": ""
            }

# Sort problems by frequency (descending) then by ID
problem_list = list(problems.values())
problem_list.sort(key=lambda x: (x['frequency'], (x['id'] or 0)), reverse=True)

# Generate list but fix None IDs if possible using url slug
for p in problem_list:
    if p['id'] is None:
        p['id'] = 0 # Fallback

output_path = "/Users/marcus/dev/workspaces/dsa/database.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(problem_list, f, indent=2)

print(f"Successfully generated {output_path} with {len(problem_list)} problems.")
