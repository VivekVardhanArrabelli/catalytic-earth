"""Pin the perturbation query's real save behaviour, so the docs cannot drift.

`scripts/query_atlas_perturbations.py` is bound by sha256 in
`data/atlas/perturbations/review.json`; changing it requires a renewed source
review. So its `--output` behaviour is documented rather than altered, and these
checks pin what the instructions in `START_HERE.md` and the project skill
promise: this route replaces an existing file and requires its directory to
exist already.

If a renewed review ever makes this route refuse an existing path — matching the
`catalytic-earth` subcommands that already do — these checks fail, which is the
signal to correct the instructions in the same change.
"""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/query_atlas_perturbations.py"

_spec = importlib.util.spec_from_file_location("query_atlas_perturbations", SCRIPT)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
_emit = _module._emit


class SavedOutputBehaviourTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_a_new_path_is_written(self) -> None:
        target = self.dir / "perturbation.json"
        _emit({"comparisons": ["fixture"]}, target)
        self.assertEqual(json.loads(target.read_text())["comparisons"], ["fixture"])

    def test_an_existing_file_is_replaced_as_documented(self) -> None:
        # Not a guarantee of protection: this route overwrites, which is why the
        # instructions tell the caller to name a new path every time.
        target = self.dir / "perturbation.json"
        target.write_bytes(b'{"previous_saved_result": true}\n')
        _emit({"new_result": "fixture"}, target)
        self.assertNotIn("previous_saved_result", target.read_text())

    def test_a_missing_directory_is_not_created(self) -> None:
        # The caller creates the session directory first; the route will not.
        target = self.dir / "new-session" / "perturbation.json"
        with self.assertRaises(FileNotFoundError):
            _emit({"comparisons": []}, target)
        self.assertFalse(target.parent.exists())


class CoreCliContrastTest(unittest.TestCase):
    """The core CLI surfaces that promise no overwrite must actually refuse."""

    def test_documented_subcommands_create_exclusively(self) -> None:
        source = (ROOT / "src/catalytic_earth/core_cli.py").read_text(encoding="utf-8")
        # Every --output that promises the guarantee is matched by an exclusive
        # create, so the promise is kept where it is made.
        promised = source.count(
            'help="optional new JSON file; existing files are never overwritten"'
        )
        exclusive = source.count('args.output.open("x", encoding="utf-8", newline="\\n")')
        self.assertEqual(promised, 6)
        self.assertEqual(exclusive, promised)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
