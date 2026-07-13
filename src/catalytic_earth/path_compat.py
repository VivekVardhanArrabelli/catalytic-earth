"""Small cross-platform helpers for filesystem I/O boundaries."""

from __future__ import annotations

import os
from pathlib import Path


def io_path(path: str | Path) -> Path:
    """Return an absolute path usable beyond legacy Windows MAX_PATH.

    Python can address long Windows paths through the extended-length prefix
    even when the host-wide ``LongPathsEnabled`` registry policy is disabled.
    The prefix is applied only at the I/O boundary; persisted provenance keeps
    the original portable repository-relative spelling.
    """

    absolute = os.path.abspath(os.fspath(path))
    if os.name != "nt" or absolute.startswith("\\\\?\\"):
        return Path(absolute)
    if absolute.startswith("\\\\"):
        return Path("\\\\?\\UNC\\" + absolute[2:])
    return Path("\\\\?\\" + absolute)
