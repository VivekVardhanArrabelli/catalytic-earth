"""Entry point: ``python -m catalytic_earth.workbench``."""

from __future__ import annotations

from .server import main

if __name__ == "__main__":
    raise SystemExit(main())
