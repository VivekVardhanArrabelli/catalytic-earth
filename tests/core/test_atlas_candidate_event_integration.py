from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from catalytic_earth import core_cli


class CandidateEventIntegrationTests(unittest.TestCase):
    def command(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(core_cli.main(["atlas-candidate-events", *args]), 0)
        return json.loads(output.getvalue())

    def bindings(self, result):
        return [m["candidate_row"]["candidate"]["source_binding"] for m in result["matches"]]

    def test_cli_matches_exact_changes_in_one_candidate_with_original_scope(self):
        all_rows = self.command()
        self.assertEqual(all_rows["candidate_count"], 12)
        self.assertEqual(all_rows["filters"]["support"], "after_graph_confirmed")
        result = self.command("--bond", "C", "C", "0", "1")
        self.assertEqual([(b["record_id"], b["mechanism_id"], b["before_step_id"])
                          for b in self.bindings(result)], [("M0219", 1, 2), ("M0219", 1, 4)])
        narrowed = self.command("--bond", "C", "C", "0", "1", "--charge", "C", "-1", "0")
        self.assertEqual([b["before_step_id"] for b in self.bindings(narrowed)], [2])
        empty = self.command("--bond", "C", "C", "0", "1", "--bond", "S", "H", "1", "0")
        self.assertEqual(empty["candidate_count"], 0)
        self.assertEqual(self.command("--mcsa-id", "M0222")["candidate_count"], 0)
        inferred = next(m["candidate_row"] for m in all_rows["matches"]
                        if m["candidate_row"]["candidate"]["source_binding"]["record_id"] == "M0106"
                        and m["candidate_row"]["candidate"]["source_binding"]["before_step_id"] == 8)
        before = next(s for s in inferred["source_context"]["step_bindings"] if s["role"] == "before")
        self.assertIs(before["is_inferred"], True)
        self.assertIn("inferred", before["summary"].lower())
        for match in result["matches"]:
            row = match["candidate_row"]
            candidate = row["candidate"]
            self.assertEqual(candidate["status"], "unreviewed")
            self.assertEqual(candidate["source_binding"]["snapshot_sha256"],
                             "054f1c3bee9ff38938b59e81b6b4065fe4d4204cb899171f4f68c284bad7d01c")
            self.assertFalse(candidate["scope_effect"]["experimentally_validated"])
            self.assertFalse(candidate["scope_effect"]["physical_atom_map"])
            self.assertTrue(candidate["coverage"]["full_covalent_graph_replay_asserted"])
            self.assertTrue(row["source_context"])

    def test_cli_rejects_invalid_filters_and_never_overwrites_output(self):
        for args in (("--bond", "C", "C", "NaN", "1"),
                     ("--bond", "R", "C", "0", "1"),
                     ("--charge", "C", "1", "1"),
                     ("--mcsa-id", "M0219-any")):
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    self.command(*args)
                self.assertEqual(raised.exception.code, 2)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.json"
            result = self.command("--bond", "C", "C", "0", "1", "--output", str(output))
            original = output.read_bytes()
            self.assertEqual(json.loads(original), result)
            with self.assertRaises(FileExistsError):
                self.command("--mcsa-id", "M0049", "--output", str(output))
            self.assertEqual(output.read_bytes(), original)

    def test_packaged_catalog_and_attribution_must_match_hashes(self):
        original = core_cli._resource_bytes
        for filename in ("catalog.json", "attribution.md"):
            def altered(path):
                raw = original(path)
                return raw + b" " if path == "candidate_event_data/" + filename else raw
            with self.subTest(filename=filename), patch.object(core_cli, "_resource_bytes", side_effect=altered):
                with self.assertRaisesRegex(ValueError, "differs from its expected hash"):
                    core_cli.verified_candidate_events()
