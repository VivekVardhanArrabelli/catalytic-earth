from __future__ import annotations

import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from catalytic_earth import core_cli
from scripts.scan_atlas_context_candidates import BASELINE, REGISTRY, render, scan_context_candidates


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/atlas/source_drafts/batches/aldolase-transketolase/sources/M0219.json"
REPORT = ROOT / "data/atlas/context_candidates/scan.json"


class ContextCandidateIntegrationTests(unittest.TestCase):
    def command(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(core_cli.main(list(args)), 0)
        return json.loads(output.getvalue())

    def test_context_cli_is_explicit_and_binds_original_local_source_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.json"
            source.write_bytes(SOURCE.read_bytes() + b"\n")
            args = ["atlas-candidates", "--source", str(source), "--mechanism-id", "1", "--before-step", "2"]
            old = self.command(*args)
            self.assertEqual(old["schema_version"], "catalytic-earth.panel-candidate.v1")
            self.assertEqual(old["extraction_status"], "needs_review")
            output = Path(directory) / "context.json"
            result = self.command(*args, "--preserve-context", "--output", str(output))
            self.assertEqual(json.loads(output.read_bytes()), result)
            self.assertEqual(result["schema_version"], "catalytic-earth.context-panel-candidate.v1")
            self.assertEqual(result["extraction_status"], "candidate")
            self.assertEqual(result["source_binding"]["snapshot_sha256"], hashlib.sha256(source.read_bytes()).hexdigest())
            self.assertEqual(result["coverage"]["mapped_node_count"], 75)
            self.assertTrue(result["coverage"]["full_covalent_graph_replay_asserted"])
            self.assertNotIn("full_panel_replay_asserted", result["coverage"])
            self.assertEqual(len(result["proposed_graph_edits"]), 12)
            for side in ("before", "after"):
                context = result["opaque_source_context"][side]
                self.assertEqual((len(context["bond_stereo"]), len(context["bond_conventions"])), (4, 2))

    def test_scan_reproduces_all_pairs_preserving_frozen_baseline(self):
        baseline_bytes = BASELINE.read_bytes()
        registry_bytes = REGISTRY.read_bytes()
        result = scan_context_candidates()
        self.assertEqual(render(result).encode("utf-8"), REPORT.read_bytes())
        self.assertEqual(BASELINE.read_bytes(), baseline_bytes)
        self.assertEqual(REGISTRY.read_bytes(), registry_bytes)
        aggregate = result["aggregate"]
        self.assertEqual((aggregate["record_count"], aggregate["mechanism_count"], aggregate["pair_count"]), (11, 13, 101))
        self.assertEqual(aggregate["baseline_candidate_count"], 7)
        self.assertEqual(aggregate["baseline_retained_candidate_count"] + aggregate["baseline_withheld_count"], 7)
        self.assertEqual(aggregate["candidate_count"], aggregate["baseline_retained_candidate_count"] + aggregate["newly_supported_count"])
        self.assertEqual(aggregate["candidate_count"] + aggregate["needs_review_count"], 101)
        first = next(r for r in result["pairs"] if (r["record_id"], r["mechanism_id"], r["before_step_id"]) == ("M0219", 1, 2))
        self.assertTrue(first["newly_supported"])
        self.assertTrue(all(r["status"] == "unreviewed" for r in result["pairs"]))
        self.assertFalse(result["scope"]["reviewed_evidence"])
        self.assertFalse(result["scope"]["experimentally_validated"])
