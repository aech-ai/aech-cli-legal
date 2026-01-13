#!/usr/bin/env python3
"""
Apply extracted edits to a document.

Uses: aech-cli-legal documents edit
"""
import argparse
import json
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Apply edits to document")
    parser.add_argument("input_docx", help="Path to current document")
    parser.add_argument("--edits", required=True, help="JSON file with edits")
    parser.add_argument("--output", required=True, help="Output document path")
    args = parser.parse_args()

    # Load edits
    edits = json.loads(Path(args.edits).read_text())

    # Apply each edit using aech-cli-legal documents edit
    current_doc = args.input_docx
    temp_docs = []

    for i, edit in enumerate(edits.get("edits", [])):
        section = edit.get("section", "unknown")
        replacement = edit.get("replacement", "")

        temp_output = f"/tmp/edit_step_{i}.docx"
        temp_docs.append(temp_output)

        cmd = [
            "aech-cli-legal", "documents", "edit",
            current_doc,
            "--section", section,
            "--content", replacement,
            "--output", temp_output
        ]

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            current_doc = temp_output
        except subprocess.CalledProcessError as e:
            print(json.dumps({
                "status": "error",
                "edit_index": i,
                "error": e.stderr
            }))

    # Copy final to output
    if temp_docs:
        import shutil
        shutil.copy(current_doc, args.output)

    print(json.dumps({
        "status": "stub" if not temp_docs else "complete",
        "edits_applied": len(edits.get("edits", [])),
        "output": args.output
    }))


if __name__ == "__main__":
    main()
