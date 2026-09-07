from __future__ import annotations

import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from catalytic_earth import core_cli


class CandidatePatternIntegrationTests(unittest.TestCase):
    def command(self, name="atlas-candidate-patterns", *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(core_cli.main([name, *args]), 0)
        return json.loads(output.getvalue())

    def test_shared_source_atom_changes_selection_without_changing_event_query(self):
        old = self.command("atlas-candidate-events", "--bond", "C", "O", "2", "1", "--charge", "C", "-1", "0")
        self.assertEqual(old["schema_version"], "catalytic-earth.candidate-event-query.v1")
        self.assertEqual(old["candidate_count"], 1)
        negative = self.command("atlas-candidate-patterns", "--bond", "C:x", "O:y", "2", "1", "--charge", "C:x", "-1", "0")
        self.assertEqual((negative["candidate_count"], negative["binding_count"]), (0, 0))
        positive = self.command("atlas-candidate-patterns", "--bond", "C:x", "C:y", "0", "1", "--charge", "C:x", "-1", "0")
        self.assertEqual(positive["schema_version"], "catalytic-earth.candidate-pattern-query.v1")
        self.assertEqual((positive["candidate_count"], positive["binding_count"]), (1, 1))
        match = positive["matches"][0]
        self.assertEqual(match["bindings"][0]["atom_bindings"], {"x": "a10", "y": "a28"})
        candidate = match["candidate_row"]["candidate"]
        self.assertEqual(candidate["candidate_id"], "panel-context-candidate:M0219:mechanism-1:steps-2-3")
        self.assertFalse(candidate["scope_effect"]["physical_atom_map"])
        self.assertFalse(candidate["scope_effect"]["experimentally_validated"])
        self.assertEqual(candidate["status"], "unreviewed")
        self.assertTrue(match["candidate_row"]["source_context"]["mandatory_abstentions"])
        self.assertEqual(hashlib.sha256(core_cli._resource_bytes("candidate_event_data/catalog.json")).hexdigest(),
                         "682e6f1a6d30f5328c2efcd3c8f85d661ffb068ef5ed3e31b2aac3f7bd3726e0")

    def test_symmetry_and_arrow_only_witnesses_survive_cli(self):
        result = self.command("atlas-candidate-patterns", "--bond", "C:x", "C:y", "0", "1")
        self.assertEqual((result["candidate_count"], result["binding_count"]), (2, 4))
        reverse = self.command("atlas-candidate-patterns", "--bond", "C:y", "C:x", "0", "1")
        self.assertEqual(result, reverse)
        arrows = self.command("atlas-candidate-patterns", "--bond", "O:x", "H:y", "0", "1",
                              "--support", "source_arrow_only", "--mcsa-id", "M0212")
        self.assertEqual((arrows["candidate_count"], arrows["binding_count"]), (1, 2))
        for binding in arrows["matches"][0]["bindings"]:
            self.assertNotEqual(binding["atom_bindings"]["x"], binding["atom_bindings"]["y"])
            for witness in binding["clause_witnesses"]:
                self.assertTrue(witness["events"])
                self.assertTrue(all(e["support"] == "source_arrow_only" for e in witness["events"]))

    def test_invalid_patterns_and_exclusive_output(self):
        cases = [(), ("--charge", "C", "-1", "0"),
                 ("--bond", "C:x", "C:x", "0", "1"),
                 ("--bond", "C:x", "O:y", "2", "1", "--charge", "O:x", "-1", "0"),
                 ("--charge", "C:x", "NaN", "0")]
        for args in cases:
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    self.command("atlas-candidate-patterns", *args)
                self.assertEqual(raised.exception.code, 2)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "pattern.json"
            args = ("--bond", "C:x", "C:y", "0", "1", "--output", str(output))
            result = self.command("atlas-candidate-patterns", *args)
            raw = output.read_bytes()
            self.assertEqual(json.loads(raw), result)
            with self.assertRaises(FileExistsError):
                self.command("atlas-candidate-patterns", *args)
            self.assertEqual(output.read_bytes(), raw)
