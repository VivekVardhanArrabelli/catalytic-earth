"""Installed-command behavior and packaged primary-projection integrity."""

import contextlib
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from catalytic_earth import core_cli


class MechanismEvidenceCliTests(unittest.TestCase):
    def test_filter_retains_the_full_adjudicated_case(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(core_cli.main([
                "atlas-mechanism-evidence", "--variant", "K166R", "--endpoint", "turnover",
            ]), 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["matched_observation_count"], 2)
        match = result["matches"][0]
        self.assertEqual(len(match["case"]["observations"]), 6)
        self.assertEqual(match["case"]["focal_variant_id"], "H297N")
        self.assertEqual(match["case"]["adjudication"]["selected_alternative_id"], "endpoint-selective-impairment")

    def test_new_output_file_is_exact_and_existing_file_is_preserved(self):
        with TemporaryDirectory() as temporary:
            target = Path(temporary) / "evidence.json"
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                core_cli.main(["atlas-mechanism-evidence", "--output", str(target)])
            self.assertEqual(target.read_text(encoding="utf-8"), output.getvalue())
            before = target.read_bytes()
            with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(FileExistsError):
                core_cli.main(["atlas-mechanism-evidence", "--output", str(target)])
            self.assertEqual(target.read_bytes(), before)

    def test_invalid_filter_reports_a_command_error(self):
        error = io.StringIO()
        with contextlib.redirect_stderr(error), self.assertRaises(SystemExit) as raised:
            core_cli.main(["atlas-mechanism-evidence", "--variant", "297"])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("variant", error.getvalue())

    def test_primary_projection_drift_fails_before_query(self):
        original = core_cli._resource_bytes

        def changed(path):
            raw = original(path)
            if path == "mechanism_evidence_data/pmid_1909893_projection.json":
                projection = json.loads(raw)
                projection["observations"][0]["result"]["value"] = 0
                return json.dumps(projection).encode()
            return raw

        with patch.object(core_cli, "_resource_bytes", side_effect=changed):
            with self.assertRaisesRegex(ValueError, "expected hash"):
                core_cli.verified_mechanism_evidence()


if __name__ == "__main__":
    unittest.main()
