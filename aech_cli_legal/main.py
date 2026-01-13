"""Entry point for aech-cli-legal with subcommand groups."""

import json
import sys
from functools import lru_cache
from pathlib import Path

import typer

from . import clauses, dataroom, documents, research, sigpage

app = typer.Typer(help="Legal document workflows: editing, redlining, clause search, research, data rooms")

# Register subcommand groups
app.add_typer(documents.app, name="documents", help="Document manipulation and comparison")
app.add_typer(clauses.app, name="clauses", help="Precedent and clause management")
app.add_typer(research.app, name="research", help="Legal research (cases, statutes)")
app.add_typer(dataroom.app, name="dataroom", help="Data room connections")
app.add_typer(sigpage.app, name="sigpage", help="Signature page generation")


@lru_cache(maxsize=1)
def _load_manifest() -> dict:
    """Load the JSON manifest from disk, favoring the packaged copy."""
    package_manifest = Path(__file__).resolve().parent / "manifest.json"
    repo_manifest = package_manifest.parent.parent / "manifest.json"

    for candidate in (package_manifest, repo_manifest):
        if candidate.exists():
            with candidate.open(encoding="utf-8") as handle:
                return json.load(handle)

    raise FileNotFoundError("manifest.json not found alongside package or in project root")


def _should_emit_manifest(argv: list[str]) -> bool:
    """Return True when CLI should output the manifest instead of help text."""
    return len(argv) == 2 and argv[1] in ("-h", "--help")


def run() -> None:
    """CLI entry point that handles manifest-aware help output."""
    if _should_emit_manifest(sys.argv):
        print(json.dumps(_load_manifest(), indent=2))
        return
    app()


if __name__ == "__main__":
    run()
