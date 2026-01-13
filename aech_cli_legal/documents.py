"""Documents subcommand group: convert, edit, redline."""

import json
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer()


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
