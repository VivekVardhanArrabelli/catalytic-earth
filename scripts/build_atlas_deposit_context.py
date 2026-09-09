#!/usr/bin/env python3
"""Build or verify a generic, source-reviewed mmCIF deposit-context packet."""

from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath, PureWindowsPath
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas_deposit_context import (  # noqa: E402
    canonical_json_bytes,
    check_deposit_context,
    load_and_build_deposit_context,
)


def _repo_relative_packet(value: str) -> Path:
    posix = PurePosixPath(value)
    windows = PureWindowsPath(value)
    if (
        not value
        or "\\" in value
        or posix.is_absolute()
        or windows.is_absolute()
        or windows.drive
        or value != posix.as_posix()
        or "." in posix.parts
        or ".." in posix.parts
    ):
        raise argparse.ArgumentTypeError(
            "--packet must be a safe repository-relative POSIX path"
        )
    return Path(posix)


def build(packet: Path, root: Path = ROOT) -> dict:
    """Build a deposit-context projection without accepting it as reviewed."""

    return load_and_build_deposit_context(packet, root)


def check(packet: Path, root: Path = ROOT) -> dict:
    """Verify a projection and its exact source-review pins."""

    return check_deposit_context(packet, root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", required=True, type=_repo_relative_packet)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        result = check(args.packet)
        print(
            "Deposit context and source-review pins are current: "
            f"{result['packet_id']}"
        )
    else:
        result = build(args.packet)
        output = ROOT / args.packet / "projection.json"
        output.write_bytes(canonical_json_bytes(result))
        print("Wrote deposit-context projection; source review is required before --check succeeds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
