#!/usr/bin/env python3
"""
Update project checklist / working memory.

Uses: aech-cli-inbox-assistant (or direct file manipulation)
"""
import argparse
import json
from datetime import datetime
from pathlib import Path


# Default checklist location
CHECKLIST_PATH = Path.home() / ".aech" / "project_checklist.json"


def load_checklist() -> dict:
    """Load checklist from file."""
    if CHECKLIST_PATH.exists():
        return json.loads(CHECKLIST_PATH.read_text())
    return {"items": [], "updated_at": None}


def save_checklist(checklist: dict):
    """Save checklist to file."""
    CHECKLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    checklist["updated_at"] = datetime.now().isoformat()
    CHECKLIST_PATH.write_text(json.dumps(checklist, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Update project checklist")
    parser.add_argument("--add", help="Add item to checklist")
    parser.add_argument("--complete", help="Mark item as complete")
    parser.add_argument("--remove", help="Remove item from checklist")
    parser.add_argument("--list", action="store_true", help="List all items")
    parser.add_argument("--output-format", choices=["json", "text"], default="text")
    args = parser.parse_args()

    checklist = load_checklist()

    if args.add:
        checklist["items"].append({
            "text": args.add,
            "status": "pending",
            "added_at": datetime.now().isoformat()
        })
        save_checklist(checklist)
        print(f"Added: {args.add}")

    elif args.complete:
        for item in checklist["items"]:
            if args.complete.lower() in item["text"].lower():
                item["status"] = "complete"
                item["completed_at"] = datetime.now().isoformat()
                save_checklist(checklist)
                print(f"Completed: {item['text']}")
                break
        else:
            print(f"Item not found: {args.complete}")

    elif args.remove:
        original_count = len(checklist["items"])
        checklist["items"] = [
            i for i in checklist["items"]
            if args.remove.lower() not in i["text"].lower()
        ]
        if len(checklist["items"]) < original_count:
            save_checklist(checklist)
            print(f"Removed items matching: {args.remove}")
        else:
            print(f"No items found matching: {args.remove}")

    elif args.list:
        if args.output_format == "json":
            print(json.dumps(checklist, indent=2))
        else:
            pending = [i for i in checklist["items"] if i["status"] == "pending"]
            complete = [i for i in checklist["items"] if i["status"] == "complete"]

            print("=== Project Checklist ===\n")
            print("Pending:")
            for item in pending:
                print(f"  [ ] {item['text']}")

            print("\nCompleted:")
            for item in complete:
                print(f"  [x] {item['text']}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
