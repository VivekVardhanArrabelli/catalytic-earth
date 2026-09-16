"""Provider-neutral ledger for external tool contributions.

The Workbench's own science comes from the packaged offline queries. Some
workflow steps instead come from an external research suite: a literature
lookup, a database lookup, or a structure view. Those contributions have to be
credited to the suite that actually performed them, separately from local
Python calculations, and they must never be confused with, merged into, or
allowed to alter the reviewed packaged payload.

This module records them in one narrow, provider-neutral shape so the suite
behind them can be swapped without touching the interface. Nothing here knows
what a given suite's response looks like; a caller reduces a real call to the
fields below and records it.

Honesty rules enforced in code, not left to convention:

- The ledger starts empty and stays empty until a real call is recorded. There
  is no seeding, no example row and no placeholder contribution.
- Every record must name the suite and the exact tool that produced it. An
  anonymous or unattributed contribution is refused.
- Every record is marked as an external tool call. A local calculation cannot
  be recorded here, and recording one does not make it a plugin receipt.
- A contribution is context alongside the packaged evidence. It never changes
  a packaged claim, and the flag saying so cannot be set to anything else.

Recording a call that did not happen would be a fabricated receipt. Record a
contribution only from a call you actually made and whose output you hold.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

__all__ = [
    "ACTIONS",
    "DEFAULT_LEDGER_PATH",
    "LEDGER_PATH_ENV",
    "MATCH_STATUSES",
    "ExternalSourceError",
    "load_ledger",
    "record_contribution",
]

#: How a declared association compares with the packaged record. Defined here,
#: beside the ledger that has to accept it, so the writer and the reader of a
#: record cannot drift apart on what a status may say.
#:
#: ``external_context`` is neither a match nor a contradiction: the identifier
#: is in a role the packaged record does not enumerate, so the record has
#: nothing to agree or disagree with, and the declared value stays as the caller
#: gave it.
MATCH_STATUSES = ("confirmed", "conflict", "external_context", "unresolved")

SCHEMA_VERSION = "catalytic-earth.workbench-external-sources.v1"

#: Repository-relative default. Kept in ``work/`` with the other coordination
#: records so the attribution travels with the repository.
DEFAULT_LEDGER_PATH = Path("work/workbench_external_sources.json")

#: Overrides the ledger location, so a test or a demo can exercise a populated
#: ledger without ever writing into the repository's real attribution record.
LEDGER_PATH_ENV = "CATALYTIC_EARTH_WORKBENCH_LEDGER"


def _default_path() -> Path:
    override = os.environ.get(LEDGER_PATH_ENV)
    return Path(override) if override else DEFAULT_LEDGER_PATH

#: The workflow steps an external suite may contribute.
ACTIONS = ("literature_lookup", "database_lookup", "structure_view")

_MAX_FIELD = 4000


class ExternalSourceError(ValueError):
    """Raised when a contribution cannot be recorded honestly."""


def _empty_ledger() -> dict[str, Any]:
    return {
        "active_provider": None,
        "contributions": [],
        "schema_version": SCHEMA_VERSION,
        "semantics": {
            "attribution": (
                "Each contribution credits the suite and tool that actually "
                "produced it. Local Python calculations are not recorded here "
                "and are never presented as external tool output."
            ),
            "empty_means": (
                "No external tool contribution has been recorded. This is not "
                "a claim that no suite is available, and it is not a receipt."
            ),
            "scope": (
                "Contributions are context recorded alongside the packaged "
                "evidence. They do not change, override or extend any "
                "packaged scientific claim or review status."
            ),
        },
    }


def _canonical_sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _require_text(name: str, value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ExternalSourceError(f"{name} is required and must be a non-empty string")
    text = value.strip()
    if len(text) > _MAX_FIELD:
        raise ExternalSourceError(f"{name} exceeds {_MAX_FIELD} characters")
    return text


def load_ledger(path: Path | str | None = None) -> dict[str, Any]:
    """Read the ledger, returning an empty one when no file exists yet."""
    target = Path(path) if path is not None else _default_path()
    if not target.is_file():
        return _empty_ledger()
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ExternalSourceError(f"ledger at {target} is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict) or payload.get("schema_version") != SCHEMA_VERSION:
        raise ExternalSourceError(f"ledger at {target} has an unsupported schema")
    payload.setdefault("contributions", [])
    if not isinstance(payload["contributions"], list):
        raise ExternalSourceError("ledger contributions must be a list")
    return payload


def record_contribution(
    *,
    provider_suite: str,
    provider_tool: str,
    action: str,
    query: str,
    retrieved: list[str] | None = None,
    subject: str | None = None,
    note: str | None = None,
    path: Path | str | None = None,
    recorded_at: str | None = None,
    result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Append one external tool contribution to the ledger.

    ``retrieved`` holds the identifiers or values the call actually returned.
    An empty list is a legitimate result and is recorded as such; it is not
    padded, and a call that returned nothing is never written up as a hit.
    """
    if action not in ACTIONS:
        raise ExternalSourceError(f"action must be one of {ACTIONS}, got {action!r}")

    suite = _require_text("provider_suite", provider_suite)
    tool = _require_text("provider_tool", provider_tool)
    query_text = _require_text("query", query)

    items = list(retrieved or [])
    if not all(isinstance(entry, str) and entry.strip() for entry in items):
        raise ExternalSourceError("every retrieved entry must be a non-empty string")

    target = Path(path) if path is not None else _default_path()
    ledger = load_ledger(target)

    record = {
        "action": action,
        "changes_packaged_claim": False,
        "origin": "external_tool_call",
        "provider_suite": suite,
        "provider_tool": tool,
        "query": query_text,
        "recorded_at": recorded_at or datetime.now(timezone.utc).isoformat(
            timespec="seconds"
        ),
        "result_count": len(items),
        "retrieved": [entry.strip() for entry in items],
        "subject": subject.strip() if isinstance(subject, str) and subject.strip() else None,
    }
    if note:
        record["note"] = _require_text("note", note)
    if result is not None:
        # The returned output and its association, recorded beside the packaged
        # evidence. It never rewrites a packaged record.
        if not isinstance(result, dict):
            raise ExternalSourceError("result must be an object")
        if not result.get("artifacts"):
            raise ExternalSourceError("a result must reference at least one saved artifact")
        if result.get("match_status") not in MATCH_STATUSES:
            raise ExternalSourceError(
                "result match_status must be one of " + ", ".join(MATCH_STATUSES)
            )
        record["result"] = result
    record["contribution_id"] = f"{suite}:{tool}:{_canonical_sha(record)[:16]}"

    ledger["contributions"].append(record)
    ledger["active_provider"] = suite
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(ledger, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return record


def ledger_view(path: Path | str | None = None) -> dict[str, Any]:
    """Shape the ledger for the interface, keeping its emptiness explicit."""
    ledger = load_ledger(path)
    contributions = ledger.get("contributions", [])
    # The index carries each record's action, provider and tool, so a consumer
    # can never infer the kind of work from the subject alone. A database
    # lookup against a structure accession is not a structure view.
    by_subject: dict[str, list[dict[str, Any]]] = {}
    for record in contributions:
        subject = record.get("subject")
        if subject:
            by_subject.setdefault(subject, []).append(
                {
                    "action": record["action"],
                    "contribution_id": record["contribution_id"],
                    "provider_suite": record["provider_suite"],
                    "provider_tool": record["provider_tool"],
                    "result_count": record["result_count"],
                }
            )
    return {
        "active_provider": ledger.get("active_provider"),
        "contribution_count": len(contributions),
        "contributions": contributions,
        "contributions_by_subject": by_subject,
        "providers_used": sorted({r["provider_suite"] for r in contributions}),
        "schema_version": ledger.get("schema_version"),
        "semantics": ledger.get("semantics", {}),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m catalytic_earth.workbench.external_sources",
        description=(
            "Record one external research-suite contribution. Run this only "
            "for a call you actually made and whose output you hold."
        ),
    )
    parser.add_argument("--provider-suite", help='e.g. "Rosalind"')
    parser.add_argument("--provider-tool", help="exact tool invoked")
    parser.add_argument("--action", choices=ACTIONS)
    parser.add_argument("--query", help="the exact query sent")
    parser.add_argument("--subject", default=None, help="related atlas identifier")
    parser.add_argument("--note", default=None)
    parser.add_argument(
        "--retrieved",
        action="append",
        default=[],
        help="an identifier or value the call returned; repeatable",
    )
    parser.add_argument("--ledger", type=Path, default=None)
    parser.add_argument("--show", action="store_true", help="print the ledger and exit")
    args = parser.parse_args(argv)

    if args.show:
        print(json.dumps(ledger_view(args.ledger), indent=2, sort_keys=True))
        return 0

    missing = [
        name
        for name, value in (
            ("--provider-suite", args.provider_suite),
            ("--provider-tool", args.provider_tool),
            ("--action", args.action),
            ("--query", args.query),
        )
        if not value
    ]
    if missing:
        parser.error("missing required arguments: " + ", ".join(missing))
    try:
        record = record_contribution(
            provider_suite=args.provider_suite,
            provider_tool=args.provider_tool,
            action=args.action,
            query=args.query,
            retrieved=args.retrieved,
            subject=args.subject,
            note=args.note,
            path=args.ledger,
        )
    except ExternalSourceError as exc:
        parser.error(str(exc))
        return 2
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
