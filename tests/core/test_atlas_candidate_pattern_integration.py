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

    def test_opt_in_keeps_raw_source_identity_and_support_separate_from_catalog(self):
        cases = [
            (
                "M0213",
                ("--charge", "C:alpha", "0", "-1", "--bond", "N:base", "H:h", "0", "1",
                 "--charge", "N:base", "0", "1"),
                {"alpha": "a17", "base": "a22", "h": "a70"},
                "375d66615ee7a38cb3adc817b39ae28308d554590c26c3b4bbb7d08f2a74728d",
                {"after_graph_confirmed": 6, "source_arrow_only": 2},
            ),
            (
                "M0066",
                ("--bond", "C:alpha", "N:imine", "1", "2", "--bond", "N:imine", "C:plp", "2", "1",
                 "--bond", "N:ring", "C:ring_c", "2", "1", "--charge", "N:ring", "1", "0"),
                {"alpha": "a18", "imine": "a19", "plp": "a57", "ring": "a4", "ring_c": "a5"},
                "89fa34b9238e224ed7772492165dd331ef455d9bbc32252b98c8148fd2c35770",
                {"after_graph_confirmed": 8, "source_arrow_only": 2},
            ),
        ]
        for mcsa_id, args, atom_bindings, source_sha, support_counts in cases:
            with self.subTest(mcsa_id=mcsa_id):
                default = self.command("atlas-candidate-patterns", *args)
                self.assertEqual((default["candidate_count"], default["binding_count"]), (0, 0))
                result = self.command("atlas-candidate-patterns", "--include-raw-stereo-transition-candidates", *args)
                self.assertEqual(result["schema_version"], "catalytic-earth.candidate-pattern-query.opt-in-source-candidates.v1")
                self.assertEqual(result["status"], "unreviewed")
                self.assertEqual((result["matched_candidate_count"], result["binding_count"]), (1, 1))
                self.assertFalse({"catalog_id", "catalog_sha256", "candidate_count"} & result.keys())
                frozen = result["sources"]["frozen_v1_catalog"]
                self.assertEqual(frozen["catalog_candidate_count"], 12)
                self.assertEqual(frozen["catalog_sha256"], default["catalog_sha256"])
                additional = result["sources"]["raw_stereo_transition_candidates"]
                self.assertEqual(additional["source_candidate_count"], 2)
                self.assertEqual(additional["audit_independence"], "same_model_only")
                self.assertIs(additional["independent_scientific_review"], False)
                match = result["matches"][0]
                self.assertTrue(match["source_kind"])
                self.assertTrue(match["source_id"])
                self.assertEqual(match["bindings"][0]["atom_bindings"], atom_bindings)
                row = match["candidate_row"]
                candidate = row["candidate"]
                self.assertEqual(candidate["schema_version"], "catalytic-earth.panel-candidate.v1")
                self.assertNotIn("context_preservation", candidate)
                self.assertEqual(row["raw_source_binding"]["record_id"], mcsa_id)
                self.assertEqual(row["raw_source_binding"]["snapshot_sha256"], source_sha)
                self.assertNotEqual(candidate["source_binding"]["snapshot_sha256"], source_sha)
                self.assertEqual(row["support_counts"], support_counts)
                self.assertTrue(row["source_context"]["mandatory_abstentions"])
                self.assertIs(candidate["scope_effect"]["physical_atom_map"], False)
                self.assertIs(candidate["scope_effect"]["experimentally_validated"], False)
                for witness in match["bindings"][0]["clause_witnesses"]:
                    self.assertTrue(all(e["support"] == "after_graph_confirmed" for e in witness["events"]))

        retained = self.command("atlas-candidate-patterns", "--include-raw-stereo-transition-candidates",
                                "--bond", "C:x", "C:y", "0", "1", "--charge", "C:x", "-1", "0")
        self.assertEqual((retained["matched_candidate_count"], retained["binding_count"]), (1, 1))
        self.assertEqual(retained["matches"][0]["bindings"][0]["atom_bindings"], {"x": "a10", "y": "a28"})

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
