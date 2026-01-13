#!/usr/bin/env python3
"""
Conduct legal research on a question.

Uses: aech-cli-legal research cases, aech-cli-legal research statutes
"""
import argparse
import json
import subprocess
from pathlib import Path


def search_cases(query: str, jurisdiction: str = None) -> dict:
    """Search case law database."""
    cmd = ["aech-cli-legal", "research", "cases", query]
    if jurisdiction:
        cmd.extend(["--jurisdiction", jurisdiction])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return {"status": "stub", "query": query, "results": []}


def search_statutes(query: str, jurisdiction: str = None) -> dict:
    """Search statute database."""
    cmd = ["aech-cli-legal", "research", "statutes", query]
    if jurisdiction:
        cmd.extend(["--jurisdiction", jurisdiction])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return {"status": "stub", "query": query, "results": []}


def main():
    parser = argparse.ArgumentParser(description="Conduct legal research")
    parser.add_argument("question", nargs="?", help="Research question")
    parser.add_argument("--question-file", help="Read question from file")
    parser.add_argument("--jurisdiction", help="Jurisdiction to focus on")
    parser.add_argument("--output", help="Output file for research memo")
    args = parser.parse_args()

    if args.question_file:
        question = Path(args.question_file).read_text().strip()
    elif args.question:
        question = args.question
    else:
        print(json.dumps({"error": "No question provided"}))
        return

    # Conduct research
    case_results = search_cases(question, args.jurisdiction)
    statute_results = search_statutes(question, args.jurisdiction)

    research = {
        "question": question,
        "jurisdiction": args.jurisdiction,
        "cases": case_results.get("results", []),
        "statutes": statute_results.get("results", []),
        "summary": "Research conducted - see results above"
    }

    # Format as memo if output specified
    if args.output:
        memo = f"""# Research Memo

## Question
{question}

## Jurisdiction
{args.jurisdiction or "Not specified"}

## Case Law
{json.dumps(case_results.get("results", []), indent=2)}

## Statutes
{json.dumps(statute_results.get("results", []), indent=2)}

## Summary
Further analysis required. The above results provide starting points for deeper research.
"""
        Path(args.output).write_text(memo)
        print(f"Research memo written to {args.output}")
    else:
        print(json.dumps(research, indent=2))


if __name__ == "__main__":
    main()
