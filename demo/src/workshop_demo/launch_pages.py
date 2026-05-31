from __future__ import annotations

import argparse
import base64
import http.server
import json
import os
import platform
import socket
import subprocess
import sys
import webbrowser
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

DEFAULT_PORT = 8765
DEFAULT_PAGE = "index.html"
DEFAULT_TEXT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")
DEFAULT_IMAGE_MODEL = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2")
DEFAULT_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
DEFAULT_TTS_VOICE = os.getenv("OPENAI_TTS_VOICE", "marin")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def find_port(host: str, preferred: int) -> int:
    for port in range(preferred, preferred + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.settimeout(0.2)
            if probe.connect_ex((host, port)) != 0:
                return port
    raise RuntimeError(f"No open port found from {preferred} to {preferred + 19}")


def json_bytes(payload: dict[str, object]) -> bytes:
    return json.dumps(payload).encode("utf-8")


def read_json(handler: http.server.BaseHTTPRequestHandler) -> dict[str, object]:
    length = int(handler.headers.get("Content-Length", "0"))
    if length <= 0:
        return {}
    return json.loads(handler.rfile.read(length).decode("utf-8"))


def binary_response_bytes(response: object) -> bytes:
    if hasattr(response, "read"):
        return response.read()
    if hasattr(response, "content"):
        return response.content
    return bytes(response)


def make_handler(root: Path) -> type[http.server.SimpleHTTPRequestHandler]:
    class WorkshopHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args: object, **kwargs: object) -> None:
            super().__init__(*args, directory=root, **kwargs)

        def send_json(self, status: int, payload: dict[str, object]) -> None:
            body = json_bytes(payload)
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def send_api_error(self, exc: Exception) -> None:
            self.send_json(500, {"error": str(exc)})

        def do_GET(self) -> None:
            if self.path == "/api/welcome":
                try:
                    if not os.getenv("OPENAI_API_KEY"):
                        raise RuntimeError("OPENAI_API_KEY is not set.")
                    client = OpenAI()
                    response = client.responses.create(
                        model=os.getenv("OPENAI_MODEL", DEFAULT_TEXT_MODEL),
                        input=(
                            "Write a warm, energetic 35-word opening welcome for a "
                            "vibe coding hackathon. Address builders, mentors, and "
                            "judges. Make it practical, not corporate."
                        ),
                    )
                    self.send_json(200, {"message": response.output_text})
                except Exception as exc:  # Keep the workshop moving on API errors.
                    self.send_api_error(exc)
                return
            super().do_GET()

        def do_POST(self) -> None:
            if self.path == "/api/poster":
                try:
                    data = read_json(self)
                    message = str(data.get("message") or "")
                    if not os.getenv("OPENAI_API_KEY"):
                        raise RuntimeError("OPENAI_API_KEY is not set.")
                    if not message:
                        raise RuntimeError("Run the welcome text step first.")
                    client = OpenAI()
                    prompt = (
                        "Create a polished hackathon opening poster. Bright, modern, "
                        "builder-focused, laptops and stage energy, no fake logos. "
                        f"Use this welcome message as the concept: {message}"
                    )
                    result = client.images.generate(
                        model=os.getenv("OPENAI_IMAGE_MODEL", DEFAULT_IMAGE_MODEL),
                        prompt=prompt,
                    )
                    image_base64 = result.data[0].b64_json
                    self.send_json(
                        200,
                        {
                            "prompt": prompt,
                            "image": f"data:image/png;base64,{image_base64}",
                        },
                    )
                except Exception as exc:
                    self.send_api_error(exc)
                return

            if self.path == "/api/voice":
                try:
                    data = read_json(self)
                    message = str(data.get("message") or "")
                    if not os.getenv("OPENAI_API_KEY"):
                        raise RuntimeError("OPENAI_API_KEY is not set.")
                    if not message:
                        raise RuntimeError("Run the welcome text step first.")
                    client = OpenAI()
                    response = client.audio.speech.create(
                        model=os.getenv("OPENAI_TTS_MODEL", DEFAULT_TTS_MODEL),
                        voice=os.getenv("OPENAI_TTS_VOICE", DEFAULT_TTS_VOICE),
                        input=message,
                        response_format="mp3",
                    )
                    audio = base64.b64encode(binary_response_bytes(response)).decode("ascii")
                    self.send_json(200, {"audio": f"data:audio/mpeg;base64,{audio}"})
                except Exception as exc:
                    self.send_api_error(exc)
                return

            self.send_error(404)

    return WorkshopHandler


def open_browser(url: str) -> bool:
    if platform.system() == "Windows":
        try:
            os.startfile(url)  # type: ignore[attr-defined]
            return True
        except OSError:
            pass
        try:
            subprocess.Popen(
                ["cmd", "/c", "start", "", url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=False,
            )
            return True
        except OSError:
            pass
    return webbrowser.open(url)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Serve and open the Codex-first API workshop pages."
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind. Use 0.0.0.0 only when you want LAN access.",
    )
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument(
        "--page",
        default=DEFAULT_PAGE,
        choices=["index.html", "slides.html", "speaker-notes.md", "attendee-handout.md"],
        help="Page to open first.",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Start the server without opening a browser tab.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = repo_root()
    port = find_port(args.host, args.port)
    handler = make_handler(root)
    server = http.server.ThreadingHTTPServer((args.host, port), handler)
    url = f"http://{args.host}:{port}/{args.page}"

    print(f"Serving workshop pages from {root}", flush=True)
    print(f"Open {url}", flush=True)
    print("Press Ctrl+C to stop.", flush=True)

    if not args.no_browser:
        if not open_browser(url):
            print(f"Could not open a browser automatically. Open {url}", flush=True)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped workshop page server.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
