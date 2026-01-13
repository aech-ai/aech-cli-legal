"""Research subcommand group: cases, statutes."""

import json
from typing import Optional

import typer

app = typer.Typer()


@app.command()
def cases(
    query: str = typer.Argument(..., help="Search query"),
    jurisdiction: Optional[str] = typer.Option(
        None, "--jurisdiction", "-j", help="Jurisdiction filter (e.g., 'US-Federal', 'UK')"
    ),
):
    """Search legal case database.

    Input: search query, jurisdiction.
    Output: case summaries with citations.
    Use when user needs case law precedent.
    """
    # TODO: Integrate with legal research API (Westlaw, LexisNexis)
    print(
        json.dumps(
            {
                "status": "stub",
                "action": "research cases",
                "query": query,
                "jurisdiction": jurisdiction,
                "results": [],
            }
        )
    )


@app.command()
def statutes(
    query: str = typer.Argument(..., help="Search query"),
    jurisdiction: Optional[str] = typer.Option(
        None, "--jurisdiction", "-j", help="Jurisdiction filter"
    ),
):
    """Search regulatory/statute database.

    Input: query, jurisdiction.
    Output: statute text with citations.
    Use when user needs regulatory references.
    """
    # TODO: Integrate with legal research API
    print(
        json.dumps(
            {
                "status": "stub",
                "action": "research statutes",
                "query": query,
                "jurisdiction": jurisdiction,
                "results": [],
            }
        )
    )
