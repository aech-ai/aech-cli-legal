#!/usr/bin/env python3
"""
Parse email content for document edit instructions.

Uses: aech-cli-legal documents extract-edits (LLM-powered)
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Parse email for document edits")
    parser.add_argument("email_file", nargs="?", help="Path to .eml or text file")
    parser.add_argument("--message-id", help="Fetch email by message ID (requires aech-cli-msgraph)")
    parser.add_argument("--output", help="Output JSON file")
    parser.add_argument("--output-format", choices=["json", "summary"], default="json")
    args = parser.parse_args()

    # Get email text
    email_text = ""
    temp_file = None

    if args.email_file:
        email_text = Path(args.email_file).read_text()
    elif args.message_id:
        # Fetch from msgraph
        cmd = ["aech-cli-msgraph", "get-message", args.message_id, "--format", "text"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            email_text = result.stdout
        except subprocess.CalledProcessError:
            print(json.dumps({"error": "Failed to fetch email from msgraph"}))
            sys.exit(1)
    else:
        # Read from stdin
        email_text = sys.stdin.read()

    if not email_text.strip():
        print(json.dumps({"error": "No email content provided"}))
        sys.exit(1)

    # Write to temp file for CLI
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(email_text)
        temp_file = f.name

    try:
        # Use LLM-powered extraction from CLI
        cmd = ["aech-cli-legal", "documents", "extract-edits", temp_file]
        if args.output:
            cmd.extend(["--output", args.output])

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        if args.output_format == "summary":
            # Parse and format as summary
            data = json.loads(result.stdout)
            edits = data.get("edits", [])
            print(f"Found {len(edits)} edit(s):")
            for i, edit in enumerate(edits, 1):
                section = edit.get("section", "unspecified")
                orig = edit.get("original_text", "")[:30]
                repl = edit.get("replacement_text", "")[:30]
                print(f"  {i}. Section {section}: '{orig}...' → '{repl}...'")
        else:
            print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(json.dumps({"error": f"Edit extraction failed: {e.stderr}"}))
        sys.exit(1)
    finally:
        if temp_file:
            Path(temp_file).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
