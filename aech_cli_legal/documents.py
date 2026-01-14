"""Documents subcommand group: convert, edit, redline, analyze."""

import json
import os
from pathlib import Path
from typing import Literal, Optional

import typer
from pydantic import BaseModel
from pydantic_ai import Agent

app = typer.Typer()


# --- LLM-powered analysis models ---

class RegulatoryAnalysis(BaseModel):
    """Structured output for regulatory document analysis."""
    regulatory_categories: dict[str, list[str]]  # category -> matched terms/concepts
    jurisdictions: list[str]  # Identified jurisdictions (Delaware, EU, GDPR, etc.)
    risk_level: Literal["high", "medium", "low", "none"]
    key_concerns: list[str]  # Specific concerns identified
    reasoning: str  # Explanation of the analysis


class EditInstruction(BaseModel):
    """A single edit instruction extracted from text."""
    section: Optional[str]  # Section reference if mentioned (e.g., "3.2")
    original_text: str  # Text to be changed
    replacement_text: str  # New text
    context: str  # Surrounding context or instruction


class ExtractedEdits(BaseModel):
    """Structured output for edit extraction."""
    edits: list[EditInstruction]
    summary: str  # Brief summary of the edit requests


def _get_model() -> str:
    """Get the configured LLM model from environment."""
    return os.environ.get("AECH_LLM_WORKER_MODEL", "openai:gpt-4o")


@app.command()
def convert(
    input_path: str = typer.Argument(..., help="Path to DOCX file"),
    output_dir: str = typer.Option(..., "--output-dir", "-o", help="Directory for output"),
    preserve_structure: bool = typer.Option(
        True, "--preserve-structure", help="Keep section hierarchy"
    ),
):
    """Convert DOCX to Markdown preserving document structure.

    Input: DOCX file path.
    Output: Markdown file with sections mapped.
    Use when user needs editable text from a contract.
    """
    input_file = Path(input_path)
    out_path = Path(output_dir)

    if not input_file.exists():
        print(json.dumps({"error": f"File not found: {input_path}"}))
        raise typer.Exit(code=1)

    out_path.mkdir(parents=True, exist_ok=True)

    # TODO: Implement with python-docx preserving section structure
    print(
        json.dumps(
            {
                "status": "stub",
                "action": "documents convert",
                "input": str(input_file),
                "output_dir": str(out_path),
                "preserve_structure": preserve_structure,
            }
        )
    )


@app.command()
def edit(
    input_path: str = typer.Argument(..., help="Path to DOCX file"),
    section: str = typer.Option(
        ..., "--section", "-s", help="Section ID to edit (e.g., '3.2' or 'definitions')"
    ),
    content: Optional[str] = typer.Option(
        None, "--content", "-c", help="New content for the section"
    ),
    output: str = typer.Option(..., "--output", "-o", help="Output DOCX path"),
):
    """Edit a specific section of a DOCX document.

    Input: DOCX path, section ID, new content.
    Output: Modified DOCX.
    Use when user wants to change a specific clause.
    """
    input_file = Path(input_path)
    output_file = Path(output)

    if not input_file.exists():
        print(json.dumps({"error": f"File not found: {input_path}"}))
        raise typer.Exit(code=1)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    # TODO: Implement section-level editing with python-docx
    print(
        json.dumps(
            {
                "status": "stub",
                "action": "documents edit",
                "input": str(input_file),
                "section": section,
                "content": content,
                "output": str(output_file),
            }
        )
    )


@app.command()
def redline(
    original: str = typer.Option(..., "--original", help="Path to original DOCX"),
    modified: str = typer.Option(..., "--modified", help="Path to modified DOCX"),
    output: str = typer.Option(..., "--output", "-o", help="Output path for redlined DOCX"),
):
    """Generate Word Track Changes between two DOCX versions.

    Input: original and modified DOCX paths.
    Output: DOCX with Track Changes markup.
    Use when user needs to review changes between contract versions.
    """
    original_file = Path(original)
    modified_file = Path(modified)
    output_file = Path(output)

    if not original_file.exists():
        print(json.dumps({"error": f"Original file not found: {original}"}))
        raise typer.Exit(code=1)

    if not modified_file.exists():
        print(json.dumps({"error": f"Modified file not found: {modified}"}))
        raise typer.Exit(code=1)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    # TODO: Implement Track Changes generation
    print(
        json.dumps(
            {
                "status": "stub",
                "action": "documents redline",
                "original": str(original_file),
                "modified": str(modified_file),
                "output": str(output_file),
            }
        )
    )


@app.command()
def analyze(
    input_path: str = typer.Argument(..., help="Path to document (DOCX, TXT, or MD)"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output JSON file"),
):
    """Analyze document for regulatory concerns and jurisdictions using LLM.

    Input: Document file path (DOCX, TXT, or MD).
    Output: JSON with regulatory categories, jurisdictions, risk level, and concerns.
    Use when reviewing contracts for compliance issues or regulatory exposure.
    """
    input_file = Path(input_path)

    if not input_file.exists():
        print(json.dumps({"error": f"File not found: {input_path}"}))
        raise typer.Exit(code=1)

    # Read document text
    suffix = input_file.suffix.lower()
    if suffix in [".txt", ".md"]:
        text = input_file.read_text()
    elif suffix == ".docx":
        try:
            from docx import Document
            doc = Document(str(input_file))
            text = "\n".join(para.text for para in doc.paragraphs)
        except Exception as e:
            print(json.dumps({"error": f"Failed to read DOCX: {e}"}))
            raise typer.Exit(code=1)
    else:
        print(json.dumps({"error": f"Unsupported file type: {suffix}"}))
        raise typer.Exit(code=1)

    # LLM-powered analysis
    agent = Agent(_get_model(), result_type=RegulatoryAnalysis)

    prompt = f"""Analyze this legal document for regulatory concerns.

Identify:
1. Regulatory categories that apply (data_privacy, financial, healthcare, employment, intellectual_property, etc.)
2. Jurisdictions mentioned or implied (states, countries, regulatory frameworks like GDPR)
3. Risk level (high/medium/low/none) based on regulatory exposure
4. Specific concerns or issues that should be reviewed

Document text:
{text[:50000]}  # Limit to ~50k chars for context window
"""

    try:
        result = agent.run_sync(prompt)
        analysis = result.data.model_dump()
        analysis["source"] = str(input_file)
    except Exception as e:
        print(json.dumps({"error": f"LLM analysis failed: {e}"}))
        raise typer.Exit(code=1)

    output_json = json.dumps(analysis, indent=2)
    if output:
        Path(output).write_text(output_json)
        print(json.dumps({"status": "complete", "output": output}))
    else:
        print(output_json)


@app.command(name="extract-edits")
def extract_edits(
    input_path: str = typer.Argument(..., help="Path to text file with edit instructions"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output JSON file"),
):
    """Extract edit instructions from text (email, comments) using LLM.

    Input: Text file containing edit requests/comments.
    Output: JSON with structured edit instructions (section, original, replacement).
    Use when processing email feedback or markup comments into actionable edits.
    """
    input_file = Path(input_path)

    if not input_file.exists():
        print(json.dumps({"error": f"File not found: {input_path}"}))
        raise typer.Exit(code=1)

    text = input_file.read_text()

    # LLM-powered extraction
    agent = Agent(_get_model(), result_type=ExtractedEdits)

    prompt = f"""Extract edit instructions from this text.

For each edit request found, identify:
1. The section reference (if mentioned, e.g., "Section 3.2", "Article IV")
2. The original text that should be changed
3. The replacement text
4. Context around the instruction

Common patterns:
- "Change X to Y"
- "Replace X with Y"
- "In Section N, X should read Y"
- "Delete the phrase X"
- "Add Y after X"

Text to analyze:
{text}
"""

    try:
        result = agent.run_sync(prompt)
        extracted = result.data.model_dump()
        extracted["source"] = str(input_file)
        extracted["edit_count"] = len(extracted["edits"])
    except Exception as e:
        print(json.dumps({"error": f"LLM extraction failed: {e}"}))
        raise typer.Exit(code=1)

    output_json = json.dumps(extracted, indent=2)
    if output:
        Path(output).write_text(output_json)
        print(json.dumps({"status": "complete", "output": output, "edit_count": extracted["edit_count"]}))
    else:
        print(output_json)
