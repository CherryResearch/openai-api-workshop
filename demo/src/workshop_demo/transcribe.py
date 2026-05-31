from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def require_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is not set. In PowerShell, run: "
            '$env:OPENAI_API_KEY="your_api_key_here"'
        )


def transcribe(path: Path, model: str) -> str:
    require_api_key()
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")

    client = OpenAI()
    with path.open("rb") as audio_file:
        result = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            response_format="text",
        )
    return str(result)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe an audio file with the OpenAI speech-to-text API."
    )
    parser.add_argument("audio_file", type=Path, help="Path to an audio file")
    parser.add_argument(
        "--model",
        default="whisper-1",
        help="Transcription model. Defaults to whisper-1 for the workshop teaser.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        print(transcribe(args.audio_file, args.model))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
