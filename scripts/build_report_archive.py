"""Index and deterministically bundle historical work/ reports."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "release/report_archive_index.json"
DEFAULT_BUNDLE = ROOT / "dist/catalytic-earth-report-archive-0.1.0.zip"


def _work_entries() -> list[dict[str, Any]]:
    raw = subprocess.check_output(["git", "ls-files", "-s", "-z", "--", "work"], cwd=ROOT)
    entries: list[dict[str, Any]] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        metadata, path_raw = item.split(b"\t", 1)
        mode, object_id, stage = metadata.decode("ascii").split()
        if stage != "0":
            raise ValueError(f"unmerged report path: {path_raw!r}")
        path = path_raw.decode("utf-8")
        date_match = re.search(r"(20\d{6})", path)
        month = date_match.group(1)[:6] if date_match else "undated"
        entries.append(
            {
                "path": path,
                "git_object_id": object_id,
                "bytes": 0,
                "bundle_group": month,
            }
        )
    size_result = subprocess.run(
        ["git", "cat-file", "--batch-check=%(objectname) %(objectsize)"],
        cwd=ROOT,
        input="".join(f"{row['git_object_id']}\n" for row in entries),
        text=True,
        capture_output=True,
        check=True,
    )
    sizes = {
        object_id: int(size)
        for object_id, size in (line.split() for line in size_result.stdout.splitlines())
    }
    for row in entries:
        row["bytes"] = sizes[row["git_object_id"]]
    return sorted(entries, key=lambda row: row["path"])


def _membership_sha(entries: list[dict[str, Any]]) -> str:
    payload = "".join(
        f"{row['git_object_id']}\t{row['bytes']}\t{row['path']}\n" for row in entries
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_index() -> bytes:
    entries = _work_entries()
    groups = Counter(row["bundle_group"] for row in entries)
    payload = {
        "schema_version": "catalytic-earth.report-archive-index.v1",
        "bundle_asset": DEFAULT_BUNDLE.name,
        "member_count": len(entries),
        "logical_bytes": sum(row["bytes"] for row in entries),
        "membership_sha256": _membership_sha(entries),
        "bundle_groups": dict(sorted(groups.items())),
        "members": entries,
        "provenance": (
            "Members are the exact Git-index blobs under work/. The deterministic ZIP is a "
            "release asset; Git history remains authoritative and is not rewritten."
        ),
        "current_storage_state": (
            "Indexed and bundle-buildable. External upload remains blocked until a release "
            "destination is approved and rights checks pass."
        ),
    }
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def build_bundle(output: Path) -> tuple[str, int]:
    entries = _work_entries()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        output,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        strict_timestamps=True,
    ) as archive:
        for row in entries:
            content = subprocess.check_output(
                ["git", "cat-file", "blob", row["git_object_id"]], cwd=ROOT
            )
            info = zipfile.ZipInfo(row["path"], date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    raw = output.read_bytes()
    return hashlib.sha256(raw).hexdigest(), len(raw)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--build-bundle", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT_BUNDLE)
    args = parser.parse_args()
    index = build_index()
    if args.check:
        if not INDEX_PATH.is_file() or INDEX_PATH.read_bytes() != index:
            raise SystemExit("release/report_archive_index.json is stale")
        print("Report archive index is current")
    else:
        INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        INDEX_PATH.write_bytes(index)
        print(f"Wrote {INDEX_PATH.relative_to(ROOT)}")
    if args.build_bundle:
        digest, size = build_bundle(args.output)
        print(f"Bundle {args.output}: {size} bytes, sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
