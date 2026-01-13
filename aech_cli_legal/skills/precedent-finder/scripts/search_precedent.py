#!/usr/bin/env python3
"""
Search for precedent clauses in the clause database.

Uses: aech-cli-legal clauses search
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Search for precedent clauses")
    parser.add_argument("query", nargs="?", help="Clause text or type to search for")
    parser.add_argument("--clause-type", help="Search by clause type (e.g., indemnification)")
    parser.add_argument("--file", help="Read clause text from file")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results")
    parser.add_argument("--output-format", choices=["json", "table"], default="table")
    args = parser.parse_args()

    # Determine query text
    if args.file:
        query = Path(args.file).read_text().strip()
    elif args.clause_type:
        query = args.clause_type
    elif args.query:
        query = args.query
    else:
        print(json.dumps({"error": "Must provide query, --clause-type, or --file"}))
        sys.exit(1)

    # Call aech-cli-legal clauses search
    cmd = ["aech-cli-legal", "clauses", "search", query, "--top-k", str(args.top_k)]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        if args.output_format == "json":
            print(json.dumps(data, indent=2))
        else:
            # Format as table for human readability
            results = data.get("results", [])
            if not results:
                print("No matching clauses found.")
                return

            print(f"\nFound {len(results)} matching clauses:\n")
            print("| # | Deal | Date | Similarity | Preview |")
            print("|---|------|------|------------|---------|")
            for i, r in enumerate(results, 1):
                preview = r.get("text", "")[:50] + "..."
                print(f"| {i} | {r.get('deal_name', 'N/A')} | {r.get('deal_date', 'N/A')} | {r.get('similarity', 'N/A')} | {preview} |")

    except subprocess.CalledProcessError as e:
        print(json.dumps({"error": f"CLI failed: {e.stderr}"}))
        sys.exit(1)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON from CLI", "raw": result.stdout}))
        sys.exit(1)


if __name__ == "__main__":
    main()
