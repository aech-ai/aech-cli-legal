#!/usr/bin/env python3
"""
Extract sections from a precedent document.

Uses: aech-cli-legal documents convert
"""
import argparse
import json
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Extract sections from document")
    parser.add_argument("input_path", help="Path to DOCX file")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Convert DOCX to structured format
    cmd = [
        "aech-cli-legal", "documents", "convert",
        args.input_path,
        "--output-dir", str(output_dir)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        print(json.dumps(data, indent=2))
    except subprocess.CalledProcessError as e:
        print(json.dumps({"error": f"CLI failed: {e.stderr}"}))
    except json.JSONDecodeError:
        print(json.dumps({
            "status": "stub",
            "action": "extract_sections",
            "input": args.input_path,
            "output_dir": str(output_dir)
        }))


if __name__ == "__main__":
    main()
