---
name: regulatory-monitor
description: Monitor regulatory changes and flag issues in documents. Use proactively during document review to identify potential regulatory concerns, or when user asks about compliance issues.
allowed-tools: Read, Bash, Grep, Glob, WebSearch
---

# Regulatory Monitor

Proactively search for regulatory changes and flag potential issues in legal documents.

## When to Use

- During document review, automatically check for regulatory concerns
- User asks "are there any regulatory issues with this agreement?"
- Periodic monitoring for changes in relevant jurisdictions
- When drafting provisions that touch regulated areas

## Available Scripts

### scripts/analyze_document.py

Extract regulatory-relevant terms from a document.

```bash
python scripts/analyze_document.py contract.docx --output analysis.json
```

### scripts/search_regulatory.py

Search for regulatory updates related to identified terms.

```bash
python scripts/search_regulatory.py --terms "data privacy,GDPR" --jurisdiction EU
python scripts/search_regulatory.py --analysis analysis.json
```

### scripts/flag_issues.py

Compare document provisions against current regulations.

```bash
python scripts/flag_issues.py contract.docx --regulations regs.json --output flags.json
```

### scripts/suggest_edits.py

Generate suggested edits to address regulatory issues.

```bash
python scripts/suggest_edits.py flags.json --output suggestions.md
```

## Workflow

1. **Analyze document**: Extract jurisdictions, industries, regulated terms
2. **Search for updates**: Query regulatory databases and news
3. **Compare provisions**: Check document language against current requirements
4. **Flag issues**: Identify potential compliance gaps
5. **Suggest edits**: Propose language changes if issues found
6. **Queue for review**: Present findings to user as micro-task

## Example Session

```
[Document review triggered for new SaaS agreement]

Claude (automatic processing):
1. Analyzing document for regulatory terms...
   [Runs: python scripts/analyze_document.py agreement.docx]

   Found:
   - Jurisdiction: Delaware, EU (GDPR references)
   - Industry: Technology, SaaS
   - Regulated areas: Data privacy, Data processing

2. Searching for regulatory updates...
   [Runs: python scripts/search_regulatory.py --terms "GDPR,data processing" --jurisdiction EU]

   Found 2 relevant updates:
   - EU AI Act (2024) - May affect automated processing provisions
   - GDPR standard contractual clauses update (2023)

3. Checking document provisions...
   [Runs: python scripts/flag_issues.py agreement.docx]

   ⚠️ 1 potential issue found:
   - Section 7.3 (Data Processing): References old SCCs from 2010
     Recommendation: Update to 2021 SCCs

4. [Sends notification]
   🔔 Regulatory Issue Detected
   Document: SaaS Agreement
   Issue: Outdated Standard Contractual Clauses
   [View Details] [Propose Fix]
```

## CLI Dependencies

- `aech-cli-legal documents convert` - Extract document text
- `aech-cli-legal research statutes` - Search regulatory databases
- `aech-cli-legal documents edit` - Apply suggested fixes
- WebSearch tool - Search for regulatory news/updates
