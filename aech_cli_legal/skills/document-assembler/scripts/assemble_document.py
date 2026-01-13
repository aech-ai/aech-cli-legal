#!/usr/bin/env python3
"""
Assemble a new document from precedent sections.

Uses: aech-cli-legal documents edit
"""
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="Assemble document from sections")
    parser.add_argument("--template", help="Base template to use")
    parser.add_argument("--sections", required=True, help="Section mappings (format: section:source,section:source)")
    parser.add_argument("--output", required=True, help="Output DOCX path")
    args = parser.parse_args()

    # Parse section mappings
    sections = {}
    for mapping in args.sections.split(","):
        if ":" in mapping:
            section, source = mapping.split(":", 1)
            sections[section] = source

    # TODO: Implement actual assembly with aech-cli-legal documents edit
    print(json.dumps({
        "status": "stub",
        "action": "assemble_document",
        "template": args.template,
        "sections": sections,
        "output": args.output,
        "message": "Will assemble document from selected precedent sections"
    }))


if __name__ == "__main__":
    main()
