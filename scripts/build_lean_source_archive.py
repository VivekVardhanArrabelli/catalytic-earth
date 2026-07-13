"""Build a deterministic, artifact-free source ZIP from an exact commit."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "dist/catalytic-earth-0.1.0-lean-source.zip"
ROOT_FILES = {
    ".gitattributes",
    ".gitignore",
    "CITATION.cff",
    "CLAIMS.md",
    "ERRATA.md",
    "LICENSE",
    "NOTICE",
    "README.md",
    "pyproject.toml",
}
PREFIXES = (
    "config/",
    "data/governance/",
    "environments/",
    "release/",
    "requirements/",
    "scripts/",
    "src/",
    "tests/core/",
)
DOCS = {
    "docs/ARCHITECTURE.md",
    "docs/ATLAS_TRUTH_POLICY.md",
    "docs/CORE_REPRODUCTION.md",
    "docs/EVALUATION_MEMORY.md",
    "docs/LEAN_RELEASE.md",
    "docs/P0_COMPLETION.md",
    "docs/SOURCE_DATA_RIGHTS.md",
}


def _included(path: str) -> bool:
    return path in ROOT_FILES or path in DOCS or path.startswith(PREFIXES)


def _commit_paths(commit: str) -> list[str]:
    raw = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", "-z", commit], cwd=ROOT
    )
    return sorted(
        path.decode("utf-8")
        for path in raw.split(b"\0")
        if path and _included(path.decode("utf-8"))
    )


def build(commit: str, output: Path) -> tuple[str, int, int, int]:
    resolved = subprocess.check_output(
        ["git", "rev-parse", f"{commit}^{{commit}}"], cwd=ROOT, text=True
    ).strip()
    paths = _commit_paths(resolved)
    if not paths or "pyproject.toml" not in paths or "src/catalytic_earth/core_cli.py" not in paths:
        raise ValueError("source commit does not contain the canonical core release files")
    archive_root = "catalytic-earth-0.1.0"
    output.parent.mkdir(parents=True, exist_ok=True)
    max_path = 0
    with zipfile.ZipFile(
        output,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        strict_timestamps=True,
    ) as archive:
        for path in paths:
            content = subprocess.check_output(["git", "show", f"{resolved}:{path}"], cwd=ROOT)
            member = f"{archive_root}/{path}"
            max_path = max(max_path, len(member))
            info = zipfile.ZipInfo(member, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    raw = output.read_bytes()
    return hashlib.sha256(raw).hexdigest(), len(raw), len(paths), max_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    digest, size, files, max_path = build(args.source_commit, args.output)
    if size >= 100 * 1024 * 1024:
        raise SystemExit(f"lean source archive is not lean: {size} bytes")
    if max_path > 180:
        raise SystemExit(f"lean source member exceeds path ceiling: {max_path}")
    print(
        f"Lean source: {args.output}, files={files}, bytes={size}, "
        f"max_path={max_path}, sha256={digest}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
