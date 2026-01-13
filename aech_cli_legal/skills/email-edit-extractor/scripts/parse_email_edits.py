#!/usr/bin/env python3
"""
Parse email content for document edit instructions.

Uses: aech-cli-msgraph (to fetch email if needed)
"""
import argparse
import json
import re
import subprocess
from pathlib import Path


def extract_edits_from_text(text: str) -> list[dict]:
    """Extract edit instructions from email text using patterns."""
    edits = []

    # Pattern: "change X to Y" or "replace X with Y"
    change_patterns = [
        r"change ['\"](.+?)['\"] to ['\"](.+?)['\"]",
        r"replace ['\"](.+?)['\"] with ['\"](.+?)['\"]",
        r"['\"](.+?)['\"] should (?:be|read) ['\"](.+?)['\"]",
    ]

    # Pattern: "in Section X.Y" to identify location
    section_pattern = r"(?:in |at )?[Ss]ection (\d+(?:\.\d+)*)"

    current_section = None
    for line in text.split("\n"):
        # Check for section reference
        section_match = re.search(section_pattern, line)
        if section_match:
            current_section = section_match.group(1)

        # Check for change instructions
        for pattern in change_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                edits.append({
                    "section": current_section,
                    "original": match.group(1),
                    "replacement": match.group(2),
                    "source_line": line.strip()
                })

    return edits


def main():
    parser = argparse.ArgumentParser(description="Parse email for document edits")
    parser.add_argument("email_file", nargs="?", help="Path to .eml file")
    parser.add_argument("--message-id", help="Fetch email by message ID")
    parser.add_argument("--output", help="Output JSON file")
    parser.add_argument("--output-format", choices=["json", "summary"], default="json")
    args = parser.parse_args()

    email_text = ""

    if args.email_file:
        email_text = Path(args.email_file).read_text()
    elif args.message_id:
        # Fetch from msgraph
        cmd = ["aech-cli-msgraph", "get-message", args.message_id, "--format", "text"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            email_text = result.stdout
        except subprocess.CalledProcessError:
            email_text = ""
    else:
        # Read from stdin
        import sys
        email_text = sys.stdin.read()

    edits = extract_edits_from_text(email_text)

    output = {
        "edit_count": len(edits),
        "edits": edits
    }

    if args.output_format == "summary":
        print(f"Found {len(edits)} edit(s):")
        for i, edit in enumerate(edits, 1):
            section = edit.get("section", "unspecified")
            print(f"  {i}. Section {section}: '{edit['original']}' → '{edit['replacement']}'")
    else:
        result = json.dumps(output, indent=2)
        if args.output:
            Path(args.output).write_text(result)
            print(f"Edits written to {args.output}")
        else:
            print(result)


if __name__ == "__main__":
    main()
