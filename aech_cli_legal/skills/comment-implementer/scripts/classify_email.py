#!/usr/bin/env python3
"""
Classify incoming email type: edit_request, research_question, or informational.

Uses: aech-cli-msgraph get-message
"""
import argparse
import json
import re
import subprocess
from pathlib import Path


# Classification patterns
EDIT_PATTERNS = [
    r"please (?:change|update|modify|revise)",
    r"change .+ to",
    r"replace .+ with",
    r"in section \d",
    r"attached.+(?:markup|redline|comments)",
    r"see (?:my |the )?comments",
]

RESEARCH_PATTERNS = [
    r"can you (?:check|research|look into|find out)",
    r"what (?:is|are) the (?:requirements?|rules?|regulations?)",
    r"do we need",
    r"is it (?:required|necessary|possible)",
    r"please (?:research|investigate|look into)",
    r"\?$",  # Questions often end with ?
]


def classify_text(text: str) -> dict:
    """Classify email text into categories."""
    text_lower = text.lower()

    edit_score = sum(1 for p in EDIT_PATTERNS if re.search(p, text_lower))
    research_score = sum(1 for p in RESEARCH_PATTERNS if re.search(p, text_lower))

    # Check for attachments mentioned
    has_attachment = bool(re.search(r"attach|enclosed|see the file", text_lower))

    if edit_score > research_score or has_attachment:
        classification = "edit_request"
    elif research_score > 0:
        classification = "research_question"
    else:
        classification = "informational"

    # Extract topic/subject
    topic = ""
    lines = text.strip().split("\n")
    for line in lines[:5]:  # Check first 5 lines
        if len(line) > 10 and len(line) < 200:
            topic = line.strip()
            break

    return {
        "classification": classification,
        "confidence": max(edit_score, research_score) / 5.0,  # Normalize
        "edit_score": edit_score,
        "research_score": research_score,
        "has_attachment": has_attachment,
        "topic": topic
    }


def main():
    parser = argparse.ArgumentParser(description="Classify email type")
    parser.add_argument("email_file", nargs="?", help="Path to .eml file")
    parser.add_argument("--message-id", help="Fetch email by message ID")
    parser.add_argument("--output-format", choices=["json", "summary"], default="json")
    args = parser.parse_args()

    email_text = ""

    if args.email_file:
        email_text = Path(args.email_file).read_text()
    elif args.message_id:
        cmd = ["aech-cli-msgraph", "get-message", args.message_id, "--format", "text"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            email_text = result.stdout
        except subprocess.CalledProcessError:
            email_text = ""
    else:
        import sys
        email_text = sys.stdin.read()

    result = classify_text(email_text)

    if args.output_format == "summary":
        print(f"Classification: {result['classification']}")
        print(f"Confidence: {result['confidence']:.0%}")
        if result['topic']:
            print(f"Topic: {result['topic']}")
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
