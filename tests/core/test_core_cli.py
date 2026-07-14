from __future__ import annotations

import io
import json
import os
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

from catalytic_earth.core_cli import main, verified_golden_result
from catalytic_earth.schema import MechanismRecord, SCHEMA_VERSION


class CoreCliTests(unittest.TestCase):
    def test_typed_record_rejects_unknown_object_type(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported object_type"):
            MechanismRecord.from_dict(
                {
                    "schema_version": SCHEMA_VERSION,
                    "record_id": "fixture:bad",
                    "object_type": "mechanisms",
                    "evidence_tier": 0,
                    "label": "bad counted object",
                    "fixture_only": True,
                    "evidence": [],
                    "mechanism_steps": [],
                    "counterevidence": [],
                    "outcome": None,
                }
            )

    def test_golden_result_matches_from_an_empty_working_directory(self) -> None:
        original = Path.cwd()
        with TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                result = verified_golden_result()
            finally:
                os.chdir(original)

        self.assertEqual(result["record_count"], 4)
        self.assertEqual(result["negative_observation_count"], 1)
        self.assertEqual(
            result["result_sha256"],
            "a2374c6530dfd3b4681db5c3db691fdcdedbf645604c6e7dfe0b95ab7e89ea98",
        )
        self.assertTrue(result["matches_expected"])

    def test_reproduce_command_emits_declared_result(self) -> None:
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = main(["reproduce"])
        result = json.loads(stdout.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertTrue(result["matches_expected"])
        self.assertIn("not a biological benchmark", result["what_it_does_not_claim"])


if __name__ == "__main__":
    unittest.main()
