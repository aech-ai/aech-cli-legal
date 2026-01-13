---
name: document-assembler
description: Assemble contract documents from precedent deals. Use when user asks to create a new contract, draft an agreement, or put together a document based on previous deals.
allowed-tools: Read, Bash, Write, Grep, Glob
---

# Document Assembler

Create new contract documents by pulling clauses from precedent deals and assembling them into a coherent document.

## When to Use

- User asks "put together a purchase agreement based on our Acme deal"
- User wants to draft a new contract using language from previous transactions
- User needs to create a shell document with standard provisions

## Available Scripts

### scripts/list_precedents.py

List available precedent deals for a contract type.

```bash
python scripts/list_precedents.py --type "asset-purchase"
python scripts/list_precedents.py --type "nda" --jurisdiction "delaware"
```

### scripts/extract_sections.py

Extract sections from a precedent document.

```bash
python scripts/extract_sections.py "acme-deal-2024.docx" --output-dir ./extracted
```

### scripts/assemble_document.py

Assemble a new document from selected precedent sections.

```bash
python scripts/assemble_document.py --template standard-apa \
    --sections definitions:acme-deal,indemnification:beta-deal \
    --output draft.docx
```

### scripts/fill_placeholders.py

Fill in deal-specific placeholders in assembled document.

```bash
python scripts/fill_placeholders.py draft.docx \
    --parties parties.json \
    --output final.docx
```

## Workflow

1. **Identify contract type**: Determine what kind of agreement user needs
2. **Find precedents**: Run `list_precedents.py` to show available deals
3. **User selects**: Let user choose which deals to pull from
4. **Extract sections**: Run `extract_sections.py` on selected deals
5. **Assemble**: Run `assemble_document.py` with user's section preferences
6. **Fill placeholders**: Use `fill_placeholders.py` with deal-specific info
7. **Generate redline**: Optionally compare to a base template

## Example Session

```
User: Create an asset purchase agreement based on our Acme and Beta deals

Claude:
1. Finding precedent deals...
   [Runs: python scripts/list_precedents.py --type "asset-purchase"]

   Available precedents:
   - Acme Corp APA (2024-01) - $50M deal
   - Beta Inc APA (2023-08) - $30M deal

2. Extracting sections from both deals...
   [Runs: python scripts/extract_sections.py "acme-apa.docx" --output-dir ./work]
   [Runs: python scripts/extract_sections.py "beta-apa.docx" --output-dir ./work]

3. Which sections would you like from each deal?
   - Definitions: [Acme/Beta]
   - Representations: [Acme/Beta]
   - Indemnification: [Acme/Beta]
   ...

User: Use Acme for definitions and reps, Beta for indemnification

4. Assembling document...
   [Runs: python scripts/assemble_document.py ...]

5. Here's your draft. Please provide party information to fill placeholders.
```

## CLI Dependencies

- `aech-cli-legal clauses search` - Find precedent sections
- `aech-cli-legal clauses index` - Index deals for future search
- `aech-cli-legal documents convert` - Extract DOCX to structured format
- `aech-cli-legal documents edit` - Assemble final document
- `aech-cli-legal documents redline` - Compare to template
