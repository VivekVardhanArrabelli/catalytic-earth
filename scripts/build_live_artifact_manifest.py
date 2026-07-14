"""Build a live, index-bound manifest for every tracked artifact blob."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "release/live_artifact_manifest.json"
LARGE_THRESHOLD = 5 * 1024 * 1024


def _tracked_entries() -> list[dict[str, Any]]:
    raw = subprocess.check_output(
        ["git", "ls-files", "-s", "-z", "--", "artifacts"], cwd=ROOT
    )
    entries: list[dict[str, Any]] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        metadata, path_raw = item.split(b"\t", 1)
        mode, object_id, stage = metadata.decode("ascii").split()
        if stage != "0":
            raise ValueError(f"unmerged artifact index entry: {path_raw!r}")
        entries.append(
            {
                "mode": mode,
                "git_object_id": object_id,
                "path": path_raw.decode("utf-8"),
            }
        )
    entries.sort(key=lambda row: row["path"])
    return entries


def _object_sizes(object_ids: list[str]) -> dict[str, int]:
    unique = sorted(set(object_ids))
    result = subprocess.run(
        ["git", "cat-file", "--batch-check=%(objectname) %(objecttype) %(objectsize)"],
        cwd=ROOT,
        input="".join(f"{object_id}\n" for object_id in unique),
        text=True,
        capture_output=True,
        check=True,
    )
    sizes: dict[str, int] = {}
    for line in result.stdout.splitlines():
        object_id, object_type, size = line.split()
        if object_type != "blob":
            raise ValueError(f"artifact object is not a blob: {object_id} ({object_type})")
        sizes[object_id] = int(size)
    return sizes


def _untracked_artifacts() -> list[str]:
    raw = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard", "-z", "--", "artifacts"],
        cwd=ROOT,
    )
    return sorted(path.decode("utf-8") for path in raw.split(b"\0") if path)


def build() -> bytes:
    entries = _tracked_entries()
    sizes = _object_sizes([row["git_object_id"] for row in entries])
    canonical = bytearray()
    large: list[dict[str, Any]] = []
    total_bytes = 0
    for row in entries:
        size = sizes[row["git_object_id"]]
        total_bytes += size
        canonical.extend(
            f"{row['mode']}\t{row['git_object_id']}\t{size}\t{row['path']}\n".encode("utf-8")
        )
        if size > LARGE_THRESHOLD:
            large.append(
                {
                    "path": row["path"],
                    "bytes": size,
                    "git_object_id": row["git_object_id"],
                    "storage_state": "legacy_git_history_not_in_lean_release",
                }
            )
    manifest = {
        "schema_version": "catalytic-earth.live-artifact-manifest.v1",
        "scope": "Every tracked file under artifacts/ at the Git index state",
        "hash_rule": "SHA-256 over mode, Git object ID, blob size, and UTF-8 path, sorted by path",
        "artifact_index_sha256": hashlib.sha256(canonical).hexdigest(),
        "artifact_git_index_sha256": hashlib.sha256(
            "".join(
                f"{row['mode']}\t{row['git_object_id']}\t{row['path']}\n"
                for row in entries
            ).encode("utf-8")
        ).hexdigest(),
        "tracked_artifact_files": len(entries),
        "tracked_artifact_logical_bytes": total_bytes,
        "large_file_threshold_bytes": LARGE_THRESHOLD,
        "large_file_count": len(large),
        "large_files": large,
        "untracked_artifacts_at_generation": _untracked_artifacts(),
        "restore_policy": (
            "The full historical artifact surface remains in Git. The canonical lean release "
            "contains only explicitly hashed core/governance inputs."
        ),
    }
    return (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--index-only",
        action="store_true",
        help="validate path/mode/object IDs without materializing partial-clone blobs",
    )
    args = parser.parse_args()
    if args.check:
        if args.index_only:
            if not OUTPUT.is_file():
                raise SystemExit("release/live_artifact_manifest.json is missing")
            manifest = json.loads(OUTPUT.read_text(encoding="utf-8"))
            entries = _tracked_entries()
            digest = hashlib.sha256(
                "".join(
                    f"{row['mode']}\t{row['git_object_id']}\t{row['path']}\n"
                    for row in entries
                ).encode("utf-8")
            ).hexdigest()
            if digest != manifest.get("artifact_git_index_sha256"):
                raise SystemExit("live artifact Git index differs from manifest")
            if len(entries) != manifest.get("tracked_artifact_files"):
                raise SystemExit("live artifact file count differs from manifest")
            print("Live artifact Git index is current (partial-clone mode)")
            return 0
        expected = build()
        if not OUTPUT.is_file() or OUTPUT.read_bytes() != expected:
            raise SystemExit("release/live_artifact_manifest.json is stale")
        if subprocess.run(
            ["git", "diff", "--quiet", "--", "artifacts"], cwd=ROOT, check=False
        ).returncode:
            raise SystemExit("artifact worktree differs from the indexed live manifest")
        print("Live artifact manifest is current")
        return 0
    if args.index_only:
        parser.error("--index-only is valid only with --check")
    expected = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(expected)
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
