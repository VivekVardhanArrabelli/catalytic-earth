"""Current scientific caveats must survive packaged and historical CLI views."""

import contextlib
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from catalytic_earth import core_cli


class StructuralContextCliTests(unittest.TestCase):
    def test_historical_runtime_keeps_current_state_corrections_alongside(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            core_cli.main(["atlas10"])
        result = json.loads(output.getvalue())
        self.assertEqual(result["runtime_result_sha256"],
                         "57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb")
        rows = {r["pdb_id"]: r for r in result["current_structure_annotations"]}
        self.assertEqual(rows["1SUP"]["interpretation"]["chemical_state"],
                         "deposited_PMS_covalent_modification_of_catalytic_serine")
        self.assertEqual(rows["1PQ5"]["interpretation"]["chemical_state"],
                         "autoproteolytic_product_fragment_bound_source_described")
        self.assertIn("separate", result["current_annotation_hash_scope"])

    def test_output_is_exact_and_does_not_overwrite(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "context.json"
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                core_cli.main(["atlas-structural-context", "--pdb-id", "1SUP", "--output", str(path)])
            self.assertEqual(path.read_text(), output.getvalue())
            original = path.read_bytes()
            with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(FileExistsError):
                core_cli.main(["atlas-structural-context", "--output", str(path)])
            self.assertEqual(original, path.read_bytes())

    def test_changed_scientific_interpretation_fails_package_integrity(self):
        original = core_cli._resource_bytes

        def altered(path):
            raw = original(path)
            if path == "structural_context_data/bundle.json":
                data = json.loads(raw)
                data["structures"][1]["interpretation"]["chemical_state"] = "unmodified_active_site"
                return json.dumps(data).encode()
            return raw

        with patch.object(core_cli, "_resource_bytes", side_effect=altered):
            with self.assertRaisesRegex(ValueError, "expected hash"):
                core_cli.verified_structural_context()


if __name__ == "__main__":
    unittest.main()
