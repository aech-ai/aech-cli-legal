---
name: email-edit-extractor
description: Extract edits from client/team emails and apply to documents. Use when emails arrive with document changes, comments, or markup that need to be implemented into the working document.
allowed-tools: Read, Bash, Write, Grep, Glob
---

# Email Edit Extractor

Parse incoming emails for document edits and apply them to a parallel version of the agreement, generating a redline for review.

## When to Use

- Client emails with "please change Section 3.2 to say..."
- Team member sends marked-up document attachment
- Email contains inline edits or strikethrough text
- Counterparty sends comments that need implementation

## Available Scripts

### scripts/parse_email_edits.py

Extract edit instructions from email text.

```bash
python scripts/parse_email_edits.py email.eml --output-format json
python scripts/parse_email_edits.py --message-id "ABC123" --output edits.json
```

### scripts/extract_attachment_markup.py

Extract Track Changes or comments from attached document.

```bash
python scripts/extract_attachment_markup.py marked_up.docx --output changes.json
```

### scripts/apply_edits.py

Apply extracted edits to the current document version.

```bash
python scripts/apply_edits.py current.docx --edits edits.json --output modified.docx
```

### scripts/generate_summary.py

Generate a summary of proposed changes for user review.

```bash
python scripts/generate_summary.py edits.json --format markdown
```

## Workflow

1. **Parse email**: Extract edit instructions from email body or attachment
2. **Map to sections**: Identify which document sections are affected
3. **Apply to parallel**: Create modified version without touching original
4. **Generate redline**: Compare original vs modified using `aech-cli-legal documents redline`
5. **Summarize changes**: Create human-readable summary
6. **Queue for approval**: Present to user as a micro-task

## Example Session

```
[Email arrives from client: "In Section 5.2, change 'best efforts' to 'commercially reasonable efforts'"]

Claude (automatic processing):
1. Parsing email for edits...
   [Runs: python scripts/parse_email_edits.py --message-id "ABC123"]

   Extracted edits:
   - Section: 5.2
   - Change: "best efforts" → "commercially reasonable efforts"

2. Applying to parallel version...
   [Runs: python scripts/apply_edits.py current_draft.docx --edits edits.json --output modified.docx]

3. Generating redline...
   [Runs: aech-cli-legal documents redline --original current_draft.docx --modified modified.docx --output redline.docx]

4. [Sends Teams notification]
   📝 Client edit received and applied
   From: client@example.com
   Changes: 1 edit in Section 5.2
   [View Redline] [Approve] [Reject]
```

## CLI Dependencies

- `aech-cli-msgraph list-messages` - Fetch email content
- `aech-cli-msgraph get-attachment` - Download attachments
- `aech-cli-legal documents edit` - Apply section changes
- `aech-cli-legal documents redline` - Generate Track Changes
- `aech-cli-documents convert-to-markdown` - Parse document structure
