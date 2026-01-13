#!/usr/bin/env python3
"""
Analyze document for regulatory-relevant terms.

Uses: aech-cli-legal documents convert
"""
import argparse
import json
import subprocess
import re
from pathlib import Path


# Regulatory keywords by category
REGULATORY_KEYWORDS = {
    "data_privacy": [
        "personal data", "data protection", "GDPR", "CCPA", "privacy",
        "data subject", "data controller", "data processor", "PII"
    ],
    "financial": [
        "securities", "SEC", "FINRA", "investment", "broker-dealer",
        "anti-money laundering", "AML", "KYC"
    ],
    "healthcare": [
        "HIPAA", "PHI", "protected health information", "healthcare",
        "medical records", "patient data"
    ],
    "employment": [
        "employment", "labor law", "FLSA", "OSHA", "workers compensation"
    ],
    "intellectual_property": [
        "patent", "trademark", "copyright", "trade secret", "IP"
    ]
}

JURISDICTION_PATTERNS = [
    r"laws of (?:the State of )?(\w+)",
    r"governed by .*?(\w+) law",
    r"jurisdiction of (\w+)",
    r"(Delaware|California|New York|Texas|EU|UK|GDPR)",
]


def analyze_text(text: str) -> dict:
    """Analyze document text for regulatory terms and jurisdictions."""
    text_lower = text.lower()

    # Find regulatory categories
    found_categories = {}
    for category, keywords in REGULATORY_KEYWORDS.items():
        matches = []
        for keyword in keywords:
            if keyword.lower() in text_lower:
                matches.append(keyword)
        if matches:
            found_categories[category] = matches

    # Find jurisdictions
    jurisdictions = set()
    for pattern in JURISDICTION_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            jurisdictions.add(match.group(1))

    return {
        "regulatory_categories": found_categories,
        "jurisdictions": list(jurisdictions),
        "term_count": sum(len(v) for v in found_categories.values())
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze document for regulatory terms")
    parser.add_argument("input_path", help="Path to document")
    parser.add_argument("--output", help="Output JSON file")
    args = parser.parse_args()

    # Convert document to text
    cmd = [
        "aech-cli-legal", "documents", "convert",
        args.input_path,
        "--output-dir", "/tmp"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # Read the converted markdown
        data = json.loads(result.stdout)
        md_path = data.get("markdown_file", "")
        if md_path:
            text = Path(md_path).read_text()
        else:
            text = ""
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        # Fallback: try to read directly if it's text
        text = Path(args.input_path).read_text() if Path(args.input_path).suffix in [".txt", ".md"] else ""

    analysis = analyze_text(text)
    analysis["source"] = args.input_path

    output = json.dumps(analysis, indent=2)
    if args.output:
        Path(args.output).write_text(output)
        print(f"Analysis written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
