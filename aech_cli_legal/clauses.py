"""Clauses subcommand group: search, index."""

import json
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer()


@app.command()
def search(
    query: str = typer.Argument(..., help="Clause text or type to search for"),
    top_k: int = typer.Option(5, "--top-k", "-k", help="Number of results"),
):
    """Semantic search for similar clauses in precedent database.

    Input: clause text or type.
    Output: matching clauses with source deals.
    Use when user wants precedent for a provision.
    """
    # TODO: Implement vector search over clause database
    print(
        json.dumps(
            {
                "status": "stub",
                "action": "clauses search",
                "query": query,
                "top_k": top_k,
                "results": [],
            }
        )
    )


@app.command()
def index(
    input_path: str = typer.Argument(..., help="Path to DOCX file"),
    deal_name: str = typer.Option(..., "--deal-name", "-n", help="Name of the deal"),
    deal_date: Optional[str] = typer.Option(
        None, "--deal-date", "-d", help="Date of deal (ISO-8601)"
    ),
):
    """Add document clauses to precedent database.

    Input: DOCX path, deal metadata.
    Output: indexed clause count.
    Use after closing a deal to build precedent library.
    """
    input_file = Path(input_path)

    if not input_file.exists():
        print(json.dumps({"error": f"File not found: {input_path}"}))
        raise typer.Exit(code=1)

    # TODO: Extract clauses and add to vector database
    print(
        json.dumps(
            {
                "status": "stub",
                "action": "clauses index",
                "input": str(input_file),
                "deal_name": deal_name,
                "deal_date": deal_date,
                "clauses_indexed": 0,
            }
        )
    )
