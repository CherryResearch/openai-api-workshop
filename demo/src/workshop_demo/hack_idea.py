from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")


def build_prompt(theme: str) -> str:
    return f"""
You are helping a hackathon team choose a small, demoable OpenAI API project.

Theme: {theme}

Return a compact JSON object with exactly these keys:
- title: short project name
- one_liner: one sentence product pitch
- user_story: one sentence in "As a..., I want..., so that..." format
- build_steps: exactly three concrete implementation steps
- demo_script: exactly three short beats for a 60-second demo
- api_surface: the most relevant OpenAI API capability to use first

Keep the idea realistic for a weekend hackathon.
""".strip()


def require_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is not set. In PowerShell, run: "
            '$env:OPENAI_API_KEY="your_api_key_here"'
        )


def call_openai(theme: str, model: str) -> dict[str, Any]:
    require_api_key()
    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=build_prompt(theme),
        text={
            "format": {
                "type": "json_schema",
                "name": "hackathon_idea",
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "title": {"type": "string"},
                        "one_liner": {"type": "string"},
                        "user_story": {"type": "string"},
                        "build_steps": {
                            "type": "array",
                            "minItems": 3,
                            "maxItems": 3,
                            "items": {"type": "string"},
                        },
                        "demo_script": {
                            "type": "array",
                            "minItems": 3,
                            "maxItems": 3,
                            "items": {"type": "string"},
                        },
                        "api_surface": {"type": "string"},
                    },
                    "required": [
                        "title",
                        "one_liner",
                        "user_story",
                        "build_steps",
                        "demo_script",
                        "api_surface",
                    ],
                },
                "strict": True,
            }
        },
    )
    return json.loads(response.output_text)


def render_text(payload: dict[str, Any]) -> str:
    build_steps = "\n".join(f"  {i}. {step}" for i, step in enumerate(payload["build_steps"], 1))
    demo_script = "\n".join(f"  {i}. {beat}" for i, beat in enumerate(payload["demo_script"], 1))
    return f"""
{payload["title"]}

{payload["one_liner"]}

User story
  {payload["user_story"]}

Build steps
{build_steps}

Demo script
{demo_script}

Start with
  {payload["api_surface"]}
""".strip()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a small hackathon project idea using the OpenAI API."
    )
    parser.add_argument("theme", help="Hackathon theme or product direction")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"OpenAI model to use. Defaults to OPENAI_MODEL or {DEFAULT_MODEL}.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        payload = call_openai(args.theme, args.model)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(render_text(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

