"""Dataroom subcommand group: connect, download."""

import json
from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def connect(
    provider: str = typer.Argument(
        ..., help="Data room provider (intralinks, datasite, firmex)"
    ),
    project_id: str = typer.Option(..., "--project-id", "-p", help="Project/deal room ID"),
):
    """Authenticate to a data room.

    Input: provider, credentials.
    Output: session token.
    Use when user needs to access deal documents in a data room.
    """
    # TODO: Implement OAuth/auth flow for data room providers
    print(
        json.dumps(
            {
                "status": "stub",
                "action": "dataroom connect",
                "provider": provider,
                "project_id": project_id,
                "session": None,
            }
        )
    )


@app.command()
def download(
    doc_id: str = typer.Argument(..., help="Document ID in data room"),
    output_dir: str = typer.Option(
        ..., "--output-dir", "-o", help="Local directory for download"
    ),
):
    """Download document from data room.

    Input: document ID.
    Output: local file path.
    Use when user needs a specific document from the deal room.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # TODO: Implement data room download
    print(
        json.dumps(
            {
                "status": "stub",
                "action": "dataroom download",
                "doc_id": doc_id,
                "output_dir": str(out_path),
                "local_path": None,
            }
        )
    )
