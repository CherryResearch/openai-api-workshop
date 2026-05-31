from __future__ import annotations

import argparse
import functools
import http.server
import socket
import sys
import webbrowser
from pathlib import Path


DEFAULT_PORT = 8765
DEFAULT_PAGE = "index.html"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def find_port(host: str, preferred: int) -> int:
    for port in range(preferred, preferred + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.settimeout(0.2)
            if probe.connect_ex((host, port)) != 0:
                return port
    raise RuntimeError(f"No open port found from {preferred} to {preferred + 19}")


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
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=root)
    server = http.server.ThreadingHTTPServer((args.host, port), handler)
    url = f"http://{args.host}:{port}/{args.page}"

    print(f"Serving workshop pages from {root}")
    print(f"Open {url}")
    print("Press Ctrl+C to stop.")

    if not args.no_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped workshop page server.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
