import json
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
while current_dir != '/' and not os.path.exists(os.path.join(current_dir, "database.json")):
    current_dir = os.path.dirname(current_dir)
DB_PATH = os.path.join(current_dir, "database.json")

def load_db():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        sys.exit(1)
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(db):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)

def query(args):
    db = load_db()
    results = db
    
    # Simple filtering
    if args.get("id"):
        results = [p for p in results if str(p.get("id")) == str(args["id"])]
    if args.get("difficulty"):
        results = [p for p in results if p.get("difficulty", "").lower() == args["difficulty"].lower()]
    if args.get("status"):
        results = [p for p in results if p.get("status", "").lower() == args["status"].lower()]
    if args.get("title_search"):
        search = args["title_search"].lower()
        results = [p for p in results if search in p.get("title", "").lower()]
    
    # Sort and Limit
    results.sort(key=lambda x: x.get("frequency", 0), reverse=True)
    limit = args.get("limit", 10)
    
    print(json.dumps(results[:limit], indent=2))

def update_status(args):
    db = load_db()
    target_id = str(args.get("id"))
    new_status = args.get("status")
    
    updated = False
    for p in db:
        if str(p.get("id")) == target_id:
            p["status"] = new_status
            if new_status == "solved":
                from datetime import datetime
                p["date_solved"] = datetime.now().strftime("%Y-%m-%d")
            updated = True
            break
    
    if updated:
        save_db(db)
        print(f"Successfully updated problem {target_id} to status {new_status}")
    else:
        print(f"Error: Problem {target_id} not found.")
        sys.exit(1)

if __name__ == "__main__":
    command = sys.argv[1]
    import ast
    params = ast.literal_eval(sys.argv[2])
    
    if command == "query":
        query(params)
    elif command == "update":
        update_status(params)
