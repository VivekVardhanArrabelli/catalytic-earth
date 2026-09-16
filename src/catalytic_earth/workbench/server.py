"""Loopback HTTP server for the Mechanism Workbench.

Standard library only, consistent with the dependency-free packaged runtime.
The server binds to the loopback interface, serves a fixed allowlist of static
files from inside this package, and exposes read-only JSON endpoints backed by
:mod:`catalytic_earth.workbench.adapter`.

It reads no arbitrary filesystem paths, exposes no private source cache, runs
no external command and opens no network connection.
"""

from __future__ import annotations

import argparse
import json
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from .adapter import (
    AdapterError,
    evidence_view,
    external_sources_view,
    match_chemistry_view,
    mechanism_list,
    pattern_query,
    sites_view,
    transformation_view,
)

__all__ = ["build_server", "main"]

_STATIC_DIR = Path(__file__).resolve().parent / "static"

#: Fixed allowlist. Requests are matched against these names exactly, so no
#: path traversal or directory listing is possible.
_STATIC_FILES: dict[str, str] = {
    "/": "index.html",
    "/index.html": "index.html",
    "/app.js": "app.js",
    "/style.css": "style.css",
}

_CONTENT_TYPES = {
    ".css": "text/css; charset=utf-8",
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
}

_MAX_BODY_BYTES = 64 * 1024


class _Handler(BaseHTTPRequestHandler):
    server_version = "CatalyticEarthWorkbench/0.1"
    protocol_version = "HTTP/1.1"

    # -- helpers ---------------------------------------------------------
    def _send(self, status: HTTPStatus, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _send_json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self._send(status, body, "application/json; charset=utf-8")

    def _send_error_json(self, status: HTTPStatus, message: str) -> None:
        self._send_json({"error": message, "status": int(status)}, status)

    def log_message(self, fmt: str, *args: Any) -> None:  # pragma: no cover
        sys.stderr.write("workbench %s - %s\n" % (self.address_string(), fmt % args))

    # -- routing ---------------------------------------------------------
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        route = parsed.path
        if route == "/favicon.ico":
            self._send(HTTPStatus.NO_CONTENT, b"", "image/x-icon")
            return
        if route in _STATIC_FILES:
            self._serve_static(_STATIC_FILES[route])
            return
        try:
            if route == "/api/external-sources":
                self._send_json(external_sources_view())
                return
            if route == "/api/mechanisms":
                self._send_json(mechanism_list())
                return
            if route.startswith("/api/mechanism/"):
                mcsa_id = route[len("/api/mechanism/") :]
                self._send_json(transformation_view(mcsa_id))
                return
            if route.startswith("/api/sites/"):
                self._send_json(sites_view(route[len("/api/sites/") :]))
                return
            if route == "/api/evidence":
                query = parse_qs(parsed.query)
                self._send_json(
                    evidence_view(
                        variant=(query.get("variant") or [None])[0],
                        endpoint=(query.get("endpoint") or [None])[0],
                    )
                )
                return
        except AdapterError as exc:
            self._send_error_json(HTTPStatus.BAD_REQUEST, str(exc))
            return
        except Exception as exc:  # surface failures rather than hiding them
            self._send_error_json(HTTPStatus.INTERNAL_SERVER_ERROR, repr(exc))
            return
        self._send_error_json(HTTPStatus.NOT_FOUND, f"no route {route}")

    def do_HEAD(self) -> None:  # noqa: N802
        self.do_GET()

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path not in {"/api/patterns", "/api/match-chemistry"}:
            self._send_error_json(HTTPStatus.NOT_FOUND, f"no route {parsed.path}")
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            self._send_error_json(HTTPStatus.BAD_REQUEST, "invalid Content-Length")
            return
        if length <= 0 or length > _MAX_BODY_BYTES:
            self._send_error_json(HTTPStatus.BAD_REQUEST, "unsupported request body size")
            return
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            self._send_error_json(HTTPStatus.BAD_REQUEST, f"invalid JSON body: {exc}")
            return
        if not isinstance(payload, dict):
            self._send_error_json(HTTPStatus.BAD_REQUEST, "body must be a JSON object")
            return
        try:
            if parsed.path == "/api/match-chemistry":
                candidate_id = payload.get("candidate_id")
                if not isinstance(candidate_id, str) or not candidate_id.strip():
                    raise AdapterError("candidate_id is required")
                index = payload.get("binding_index", 0)
                if isinstance(index, bool) or not isinstance(index, int):
                    raise AdapterError("binding_index must be an integer")
                self._send_json(
                    match_chemistry_view(
                        payload.get("clauses") or [],
                        candidate_id=candidate_id.strip(),
                        binding_index=index,
                        mcsa_id=payload.get("mcsa_id"),
                        support=payload.get("support") or "after_graph_confirmed",
                    )
                )
                return
            self._send_json(
                pattern_query(
                    payload.get("clauses") or [],
                    mcsa_id=payload.get("mcsa_id"),
                    support=payload.get("support") or "after_graph_confirmed",
                )
            )
        except AdapterError as exc:
            self._send_error_json(HTTPStatus.BAD_REQUEST, str(exc))
        except Exception as exc:
            self._send_error_json(HTTPStatus.INTERNAL_SERVER_ERROR, repr(exc))

    def _serve_static(self, name: str) -> None:
        path = _STATIC_DIR / name
        if not path.is_file():
            self._send_error_json(HTTPStatus.NOT_FOUND, f"missing asset {name}")
            return
        self._send(HTTPStatus.OK, path.read_bytes(), _CONTENT_TYPES[path.suffix])


def build_server(host: str = "127.0.0.1", port: int = 8765) -> ThreadingHTTPServer:
    """Create the workbench server bound to a loopback address."""
    if host not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("the workbench binds to loopback only")
    return ThreadingHTTPServer((host, port), _Handler)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m catalytic_earth.workbench",
        description="Run the Catalytic Earth Mechanism Workbench on loopback.",
    )
    parser.add_argument("--host", default="127.0.0.1", help="loopback host (default 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8765, help="port (default 8765)")
    args = parser.parse_args(argv)

    try:
        server = build_server(args.host, args.port)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
        return 2

    host, port = server.server_address[:2]
    print(f"Mechanism Workbench on http://{host}:{port}/ (Ctrl-C to stop)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopping", flush=True)
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
