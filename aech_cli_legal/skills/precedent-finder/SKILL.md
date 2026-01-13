---
name: precedent-finder
description: Find precedent clauses from past deals. Use when user asks to find similar clauses, search for precedent, or look up how a provision was worded in previous deals.
allowed-tools: Read, Bash, Grep, Glob
---

# Precedent Finder

Search the clause database for similar provisions from past deals. Returns matching clauses with source attribution.

## When to Use

- User asks "find precedent for this indemnification clause"
- User wants to see how a provision was worded in previous deals
- User needs comparable language from similar transactions

## Available Scripts

### scripts/search_precedent.py

Search for similar clauses by text or type.

```bash
python scripts/search_precedent.py "limitation of liability" --top-k 5
python scripts/search_precedent.py --clause-type indemnification --top-k 10
python scripts/search_precedent.py --file clause.txt --top-k 5
```

### scripts/show_context.py

Get full context for a matched clause (surrounding sections).

```bash
python scripts/show_context.py --clause-id "deal123_section5.2" --context-lines 20
```

## Workflow

1. **Extract clause text**: If user provides a document, extract the relevant clause
2. **Search**: Run `search_precedent.py` with the clause text or type
3. **Present results**: Show matches with deal name, date, and similarity score
4. **Offer context**: Ask if user wants to see full context for any match
5. **Import option**: Offer to import selected clause into current document

## Example Session

```
User: Find precedent for this limitation of liability clause:
"The total liability of either party shall not exceed the fees paid in the 12 months..."

Claude:
1. Searching clause database...
   [Runs: python scripts/search_precedent.py "The total liability..." --top-k 5]

2. Found 5 similar clauses:
   | Deal | Date | Similarity | Preview |
   |------|------|------------|---------|
   | Acme Corp Acquisition | 2024-01 | 94% | "Total liability shall not exceed..." |
   | Beta Inc License | 2023-11 | 87% | "Aggregate liability limited to..." |
   ...

3. Would you like to see the full context for any of these?
```

## CLI Dependencies

- `aech-cli-legal clauses search` - Semantic clause search
- `aech-cli-legal documents convert` - Extract clauses from DOCX
