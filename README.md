# aech-cli-legal

Legal document workflows CLI for Agent Aech.

## Overview

A domain-specific CLI that groups legal workflow capabilities into logical subcommands:

- **documents** - Document manipulation and comparison (convert, edit, redline)
- **clauses** - Precedent and clause management (search, index)
- **research** - Legal research (cases, statutes)
- **dataroom** - Data room connections (connect, download)
- **sigpage** - Signature page generation (generate)

## Installation

```bash
# Development install
uv venv
source .venv/bin/activate
uv pip install -e .

# Build wheel
uv build
```

## Usage

```bash
# View manifest (for LLM agent discovery)
aech-cli-legal --help

# Document operations
aech-cli-legal documents convert contract.docx --output-dir ./output
aech-cli-legal documents edit contract.docx --section "3.2" --content "New clause text" --output modified.docx
aech-cli-legal documents redline --original v1.docx --modified v2.docx --output redlined.docx

# Clause search
aech-cli-legal clauses search "limitation of liability" --top-k 5
aech-cli-legal clauses index contract.docx --deal-name "Acme Acquisition" --deal-date "2024-03-15"

# Legal research
aech-cli-legal research cases "breach of fiduciary duty" --jurisdiction US-Federal
aech-cli-legal research statutes "securities fraud" --jurisdiction US-Federal

# Data room
aech-cli-legal dataroom connect intralinks --project-id "ABC123"
aech-cli-legal dataroom download "doc-456" --output-dir ./downloads

# Signature pages
aech-cli-legal sigpage generate parties.json --output signatures.docx --template counterpart
```

## Architecture

This CLI follows the **domain vertical pattern** - a single CLI with grouped subcommands rather than many separate micro-CLIs. This provides:

- **Better discoverability** for LLM agents (logical hierarchy)
- **Explicit relationships** between related features
- **Reduced context tokens** (one manifest vs many)
- **User mental model** alignment (legal workflows, not technical features)

See `CLI_MANIFEST_SPEC_v4.md` for manifest specification.

## Integration with Agent Aech

1. Build: `uv build`
2. Copy wheel: `cp dist/*.whl ../aech-main/capabilities/clis/`
3. Regenerate manifest: `cd ../aech-main && python capabilities/installer.py`

The CLI will then be available to worker agents in the sandbox.
