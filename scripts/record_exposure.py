from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from catalytic_earth.truth_guard import (
    EXPOSURE_EVENT_TYPES,
    EXPOSURE_STATES,
    append_exposure_event,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Append a validated evaluation-surface exposure event"
    )
    parser.add_argument("--surface-id", required=True)
    parser.add_argument("--event-type", required=True, choices=sorted(EXPOSURE_EVENT_TYPES))
    parser.add_argument("--state-after", required=True, choices=sorted(EXPOSURE_STATES))
    parser.add_argument("--effective-at", required=True, help="ISO-8601 UTC timestamp ending in Z")
    parser.add_argument("--row-count", required=True, type=int)
    parser.add_argument("--scope", required=True)
    parser.add_argument(
        "--source-artifact",
        action="append",
        required=True,
        help="repository-relative evidence path; repeat for multiple artifacts",
    )
    parser.add_argument("--note", required=True)
    parser.add_argument("--historical-backfill", action="store_true")
    parser.add_argument("--repo-root", default=".")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    event = {
        "surface_id": args.surface_id,
        "event_type": args.event_type,
        "state_after": args.state_after,
        "effective_at": args.effective_at,
        "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "historical_backfill": args.historical_backfill,
        "row_count": args.row_count,
        "scope": args.scope,
        "source_artifacts": args.source_artifact,
        "note": args.note,
    }
    appended = append_exposure_event(event, repo_root=Path(args.repo_root))
    print(
        f"Appended {appended['event_id']} for {appended['surface_id']} "
        f"({appended['state_after']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
