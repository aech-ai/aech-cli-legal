"""Entry point for aech-cli-legal with subcommand groups."""

import json
import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

import typer
from pydantic import BaseModel
from pydantic_ai import Agent

from . import clauses, dataroom, documents, research, sigpage

app = typer.Typer(help="Legal document workflows: editing, redlining, clause search, research, data rooms")

# Register subcommand groups
app.add_typer(documents.app, name="documents", help="Document manipulation and comparison")
app.add_typer(clauses.app, name="clauses", help="Precedent and clause management")
app.add_typer(research.app, name="research", help="Legal research (cases, statutes)")
app.add_typer(dataroom.app, name="dataroom", help="Data room connections")
app.add_typer(sigpage.app, name="sigpage", help="Signature page generation")


# --- LLM-powered classification ---

class EmailClassification(BaseModel):
    """Structured output for email classification."""
    classification: Literal["edit_request", "research_question", "approval_request", "informational", "urgent_action"]
    confidence: float  # 0.0 to 1.0
    topic: str  # Brief topic summary
    suggested_action: str  # What to do next
    reasoning: str  # Why this classification


def _get_model() -> str:
    """Get the configured LLM model from environment."""
    return os.environ.get("AECH_LLM_WORKER_MODEL", "openai:gpt-4o")


@app.command()
def classify(
    input_path: str = typer.Argument(..., help="Path to email or text file to classify"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output JSON file"),
):
    """Classify email/text content using LLM.

    Input: Text file (email content, message, etc.)
    Output: JSON with classification, confidence, topic, and suggested action.
    Use when triaging incoming communications to determine appropriate handling.

    Classifications:
    - edit_request: Contains document change requests
    - research_question: Asks for legal research or analysis
    - approval_request: Needs sign-off or decision
    - informational: FYI only, no action needed
    - urgent_action: Requires immediate attention
    """
    input_file = Path(input_path)

    if not input_file.exists():
        print(json.dumps({"error": f"File not found: {input_path}"}))
        raise typer.Exit(code=1)

    text = input_file.read_text()

    agent = Agent(_get_model(), result_type=EmailClassification)

    prompt = f"""Classify this email/message for a legal workflow system.

Determine:
1. Classification type:
   - edit_request: Contains specific document changes ("change X to Y", "please revise", attached redlines)
   - research_question: Asks for legal research, case law, statute lookup, or analysis
   - approval_request: Needs sign-off, decision, or authorization
   - informational: FYI, status update, no action needed
   - urgent_action: Time-sensitive, deadline-driven, requires immediate response

2. Confidence level (0.0 to 1.0)
3. Brief topic summary (one sentence)
4. Suggested next action
5. Reasoning for the classification

Email/Message:
{text}
"""

    try:
        result = agent.run_sync(prompt)
        classification = result.data.model_dump()
        classification["source"] = str(input_file)
    except Exception as e:
        print(json.dumps({"error": f"LLM classification failed: {e}"}))
        raise typer.Exit(code=1)

    output_json = json.dumps(classification, indent=2)
    if output:
        Path(output).write_text(output_json)
        print(json.dumps({"status": "complete", "output": output, "classification": classification["classification"]}))
    else:
        print(output_json)


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
