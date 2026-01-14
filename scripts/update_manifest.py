#!/usr/bin/env python3
"""
Auto-generate manifest.json from CLI source code using LLM.

Usage:
    uv run python scripts/update_manifest.py              # Update manifest.json
    uv run python scripts/update_manifest.py --dry-run    # Print without writing

Requires AECH_LLM_WORKER_MODEL env var (e.g., "openai:gpt-4o")
"""

import argparse
import json
import os
import sys
import tomllib
from pathlib import Path

from pydantic import BaseModel
from pydantic_ai import Agent


class Parameter(BaseModel):
    name: str
    type: str  # "argument" or "option"
    required: bool
    description: str


class Action(BaseModel):
    name: str
    description: str
    parameters: list[Parameter]


class BundledSkill(BaseModel):
    name: str
    description: str


class Manifest(BaseModel):
    name: str
    type: str
    command: str
    spec_version: int
    description: str
    available_in_sandbox: bool
    actions: list[Action]
    documentation: dict
    bundled_skills: list[BundledSkill]


SYSTEM_PROMPT = """You are a CLI documentation expert. Generate a manifest.json
that accurately documents a CLI tool based on its source code.

Rules:

1. ACTION NAMES:
   - Root-level commands: use command name directly (e.g., "classify")
   - Subcommand groups: prefix with group name (e.g., "documents convert")
   - Match exact command name from @app.command() or function name

2. PARAMETER NAMES:
   - Must match CLI flags exactly (use hyphens, not underscores)
   - typer.Argument -> type: "argument"
   - typer.Option -> type: "option"
   - ... means required, None/default means optional

3. DESCRIPTIONS:
   - Action format: "What it does. Input: X. Output: Y. Use when: scenario."
   - Parameter: explain format, valid values, when to use (for optional)
   - Never mention implementation details (libraries, internal functions)

4. DOCUMENTATION NOTES:
   - Include notes about JSON output
   - Note environment variables required (e.g., AECH_LLM_WORKER_MODEL for LLM commands)

5. BUNDLED SKILLS:
   - Extract name and description from SKILL.md frontmatter

Do NOT include hidden commands (hidden=True in typer).
Do NOT invent commands that don't exist in the code.
"""


def find_package_dir(cli_dir: Path) -> Path:
    """Find the Python package directory (contains __init__.py)."""
    for child in cli_dir.iterdir():
        if child.is_dir() and (child / "__init__.py").exists():
            if not child.name.startswith(".") and child.name not in ("scripts", "tests", "dist", "build"):
                return child
    raise FileNotFoundError("No Python package directory found")


def read_pyproject(cli_dir: Path) -> dict:
    """Read pyproject.toml to get CLI metadata."""
    pyproject_path = cli_dir / "pyproject.toml"
    if not pyproject_path.exists():
        return {}
    with open(pyproject_path, "rb") as f:
        return tomllib.load(f)


def get_cli_metadata(cli_dir: Path) -> tuple[str, str, str]:
    """Extract CLI name, command, and description from pyproject.toml."""
    pyproject = read_pyproject(cli_dir)
    project = pyproject.get("project", {})

    # Get package name and derive CLI name (e.g., "aech-cli-legal" -> "legal")
    package_name = project.get("name", "unknown")
    cli_name = package_name.replace("aech-cli-", "")

    # Get command from scripts entry
    scripts = project.get("scripts", {})
    command = list(scripts.keys())[0] if scripts else package_name

    # Get description
    description = project.get("description", "")

    return cli_name, command, description


def collect_source_files(cli_dir: Path) -> dict[str, str]:
    """Collect all Python source files from the CLI package."""
    sources = {}
    package_dir = find_package_dir(cli_dir)

    for py_file in package_dir.glob("*.py"):
        if py_file.name.startswith("_") and py_file.name != "__init__.py":
            continue
        sources[py_file.name] = py_file.read_text()

    return sources


def collect_skills(cli_dir: Path) -> list[dict]:
    """Collect bundled skills from skills/ directory."""
    skills = []
    package_dir = find_package_dir(cli_dir)
    skills_dir = package_dir / "skills"

    if not skills_dir.exists():
        return skills

    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            skills.append({
                "name": skill_dir.name,
                "content": skill_md.read_text()[:2000]
            })

    return skills


def generate_manifest(cli_dir: Path) -> Manifest:
    """Generate manifest from source code using LLM."""
    cli_name, command, description = get_cli_metadata(cli_dir)
    sources = collect_source_files(cli_dir)
    skills = collect_skills(cli_dir)

    source_context = "\n\n".join([
        f"### {filename}\n```python\n{content}\n```"
        for filename, content in sources.items()
    ])

    skills_context = "\n\n".join([
        f"### skills/{s['name']}/SKILL.md\n```markdown\n{s['content']}\n```"
        for s in skills
    ]) or "No bundled skills."

    prompt = f"""Generate manifest.json for this CLI based on the source code.

## CLI Metadata (from pyproject.toml)
- name: "{cli_name}"
- command: "{command}"
- description: "{description}"
- spec_version: 5
- available_in_sandbox: true

## Source Files

{source_context}

## Bundled Skills

{skills_context}
"""

    model = os.environ.get("AECH_LLM_WORKER_MODEL", "openai:gpt-4o")
    agent = Agent(model, result_type=Manifest, system_prompt=SYSTEM_PROMPT)
    return agent.run_sync(prompt).data


def main():
    parser = argparse.ArgumentParser(description="Auto-generate manifest.json from CLI source")
    parser.add_argument("--dry-run", action="store_true", help="Print without writing")
    args = parser.parse_args()

    cli_dir = Path(__file__).parent.parent
    package_dir = find_package_dir(cli_dir)
    manifest_path = package_dir / "manifest.json"

    print("Analyzing CLI source code...", file=sys.stderr)
    manifest = generate_manifest(cli_dir)
    manifest_json = json.dumps(manifest.model_dump(), indent=2)

    if args.dry_run:
        print(manifest_json)
    else:
        manifest_path.write_text(manifest_json + "\n")
        print(f"Updated {manifest_path}", file=sys.stderr)
        print(f"  Actions: {len(manifest.actions)}", file=sys.stderr)
        print(f"  Skills: {len(manifest.bundled_skills)}", file=sys.stderr)


if __name__ == "__main__":
    main()
