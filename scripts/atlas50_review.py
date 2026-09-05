"""Run local Atlas-50 review intake from a source checkout."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.atlas50_review import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main(repo_root=ROOT))
