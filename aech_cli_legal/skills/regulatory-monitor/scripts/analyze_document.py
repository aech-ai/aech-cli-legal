#!/usr/bin/env python3
"""
Analyze document for regulatory-relevant terms.

Uses: aech-cli-legal documents analyze (LLM-powered)
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Analyze document for regulatory terms")
    parser.add_argument("input_path", help="Path to document")
    parser.add_argument("--output", help="Output JSON file")
    args = parser.parse_args()

    input_file = Path(args.input_path)
    if not input_file.exists():
        print(json.dumps({"error": f"File not found: {args.input_path}"}))
        sys.exit(1)

    # Use LLM-powered analysis from CLI
    cmd = ["aech-cli-legal", "documents", "analyze", str(input_file)]
    if args.output:
        cmd.extend(["--output", args.output])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(json.dumps({"error": f"Analysis failed: {e.stderr}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
