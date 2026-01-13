"""Sigpage subcommand group: generate."""

import json
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer()


@app.command()
def generate(
    parties: str = typer.Argument(..., help="JSON file with party information"),
    output: str = typer.Option(..., "--output", "-o", help="Output DOCX path"),
    template: Optional[str] = typer.Option(
        None, "--template", "-t", help="Signature page template (default: standard)"
    ),
):
    """Generate signature pages from party information.

    Input: parties JSON, template.
    Output: signature pages DOCX.
    Use when user needs execution-ready signature blocks.
    """
    parties_file = Path(parties)
    output_file = Path(output)

    if not parties_file.exists():
        print(json.dumps({"error": f"Parties file not found: {parties}"}))
        raise typer.Exit(code=1)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    # TODO: Generate signature pages from party data
    print(
        json.dumps(
            {
                "status": "stub",
                "action": "sigpage generate",
                "parties": str(parties_file),
                "output": str(output_file),
                "template": template or "standard",
            }
        )
    )
