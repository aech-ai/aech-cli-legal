#!/usr/bin/env python3
"""
List available precedent deals for a contract type.

Uses: aech-cli-legal clauses search (to find indexed deals)
"""
import argparse
import json
import subprocess


def main():
    parser = argparse.ArgumentParser(description="List precedent deals")
    parser.add_argument("--type", required=True, help="Contract type (e.g., asset-purchase, nda)")
    parser.add_argument("--jurisdiction", help="Filter by jurisdiction")
    parser.add_argument("--output-format", choices=["json", "table"], default="table")
    args = parser.parse_args()

    # Search for deals of this type
    cmd = ["aech-cli-legal", "clauses", "search", f"contract type: {args.type}", "--top-k", "20"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        # TODO: Filter and dedupe by deal name when real implementation exists
        if args.output_format == "json":
            print(json.dumps(data, indent=2))
        else:
            results = data.get("results", [])
            if not results:
                print(f"No precedent deals found for type: {args.type}")
                return

            print(f"\nPrecedent deals for '{args.type}':\n")
            # Group by deal name
            deals = {}
            for r in results:
                deal = r.get("deal_name", "Unknown")
                if deal not in deals:
                    deals[deal] = r

            for deal, info in deals.items():
                print(f"- {deal} ({info.get('deal_date', 'N/A')})")

    except subprocess.CalledProcessError as e:
        print(json.dumps({"error": f"CLI failed: {e.stderr}"}))
    except json.JSONDecodeError:
        print(json.dumps({"status": "stub", "type": args.type}))


if __name__ == "__main__":
    main()
