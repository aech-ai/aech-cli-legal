---
name: comment-implementer
description: Junior associate agent that processes client emails and implements changes. Use when client sends random document changes, research questions, or comments that need to be acted upon.
allowed-tools: Read, Bash, Write, Grep, Glob, WebSearch
---

# Comment Implementer (Junior Associate Agent)

Automatically process incoming client communications, implement document changes, conduct research, and update project tracking - all subject to user approval.

## When to Use

- Client emails with document comments or change requests
- Research questions that need investigation
- Project updates that need to be tracked
- Any client communication requiring follow-up action

## Available Scripts

### scripts/classify_email.py

Classify incoming email as edit request, research question, or informational.

```bash
python scripts/classify_email.py --message-id "ABC123"
python scripts/classify_email.py email.eml
```

### scripts/implement_edits.py

Implement document edits from classified email (delegates to email-edit-extractor).

```bash
python scripts/implement_edits.py --message-id "ABC123" --document current_draft.docx
```

### scripts/conduct_research.py

Research a legal question and prepare summary.

```bash
python scripts/conduct_research.py "What are the Delaware requirements for board approval of M&A?"
python scripts/conduct_research.py --question-file question.txt --output research_memo.md
```

### scripts/update_checklist.py

Update project checklist with new items or status changes.

```bash
python scripts/update_checklist.py --add "Review client comments on Section 5"
python scripts/update_checklist.py --complete "Draft indemnification section"
python scripts/update_checklist.py --list
```

### scripts/prepare_alert.py

Prepare a conspicuous alert for user when work is ready for review.

```bash
python scripts/prepare_alert.py --type "edit" --summary "3 client edits implemented" --document redline.docx
```

## Workflow

### For Document Edits:
1. **Classify**: Determine email contains edit requests
2. **Extract**: Parse edit instructions
3. **Implement**: Apply edits to parallel document version
4. **Redline**: Generate Track Changes comparison
5. **Update checklist**: Mark as pending review
6. **Alert**: Send conspicuous notification

### For Research Questions:
1. **Classify**: Determine email contains research question
2. **Research**: Query legal databases and web
3. **Draft memo**: Prepare research summary
4. **Update checklist**: Add research task
5. **Alert**: Send notification with findings

## Example Session

```
[Email arrives from client: "Can you check if we need board approval for this size deal in Delaware?"]

Claude (automatic processing):
1. Classifying email...
   [Runs: python scripts/classify_email.py --message-id "XYZ789"]

   Classification: research_question
   Topic: "Delaware board approval requirements for M&A"

2. Conducting research...
   [Runs: python scripts/conduct_research.py "Delaware board approval M&A deal size"]
   [Uses: aech-cli-legal research cases, aech-cli-legal research statutes]

   Findings:
   - DGCL § 251: Board approval required for mergers
   - DGCL § 271: Asset sales >substantially all assets need board + stockholder approval
   - Relevant case: Revlon, Inc. v. MacAndrews & Forbes Holdings

3. Preparing research memo...
   [Writes: research_memo.md]

4. Updating project checklist...
   [Runs: python scripts/update_checklist.py --add "Research: Delaware board approval - DONE"]

5. [Sends Teams notification]
   📋 Research Complete - Awaiting Review

   Question: Delaware board approval requirements
   From: client@example.com

   Summary: Under DGCL, board approval is required for mergers (§251).
   For asset sales, if >substantially all assets, also need stockholder approval (§271).

   [View Full Memo] [Mark Reviewed]
```

## CLI Dependencies

- `aech-cli-msgraph` - Email access
- `aech-cli-legal research cases` - Case law search
- `aech-cli-legal research statutes` - Statute search
- `aech-cli-legal documents edit` - Document modifications
- `aech-cli-legal documents redline` - Track Changes
- `aech-cli-inbox-assistant` - Working memory / checklist
