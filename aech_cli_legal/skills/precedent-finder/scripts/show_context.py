#!/usr/bin/env python3
"""
Show full context for a matched clause.

Uses: aech-cli-legal (future: clauses get-context)
"""
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="Show full context for a clause")
    parser.add_argument("--clause-id", required=True, help="Clause ID from search results")
    parser.add_argument("--context-lines", type=int, default=20, help="Lines of context")
    args = parser.parse_args()

    # TODO: Implement when aech-cli-legal has clause context retrieval
    print(json.dumps({
        "status": "stub",
        "action": "show_context",
        "clause_id": args.clause_id,
        "context_lines": args.context_lines,
        "message": "Will retrieve full clause context from database"
    }))


if __name__ == "__main__":
    main()
