from __future__ import annotations

import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from catalytic_earth import core_cli
from scripts.scan_atlas_candidates import render, scan


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/atlas/atlas10/sources/mcsa/M0173.json"
REGISTRY = ROOT / "data/atlas/candidate_extraction/source_registry.json"
REPORT = ROOT / "data/atlas/candidate_extraction/scan.json"


class CandidateIntegrationTests(unittest.TestCase):
    def test_local_source_cli_and_output_do_not_overwrite_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.json"
            output = Path(directory) / "candidate.json"
            source.write_bytes(SOURCE.read_bytes())
            args = ["atlas-candidates", "--source", str(source), "--mechanism-id", "1", "--before-step", "2"]
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                self.assertEqual(core_cli.main([*args, "--output", str(output)]), 0)
            result = json.loads(stdout.getvalue())
            self.assertEqual(output.read_text(encoding="utf-8"), stdout.getvalue())
            self.assertEqual(result["source_binding"]["snapshot_sha256"], hashlib.sha256(source.read_bytes()).hexdigest())
            self.assertEqual(result["status"], "unreviewed")
            self.assertEqual(result["extraction_status"], "candidate")
            self.assertEqual(len(result["proposed_graph_edits"]), 6)
            self.assertFalse(result["coverage"]["full_panel_replay_asserted"])
            self.assertFalse(result["scope_effect"]["lone_pair_annotations_replayed"])
            before = source.read_bytes()
            with self.assertRaises(FileExistsError):
                core_cli.main([*args, "--output", str(source)])
            self.assertEqual(source.read_bytes(), before)

    def test_scan_reproduces_every_retained_pair_without_promoting_candidates(self):
        result = scan(REGISTRY)
        self.assertEqual(render(result).encode("utf-8"), REPORT.read_bytes())
        self.assertEqual(result["aggregate"]["record_count"], 11)
        self.assertEqual(result["aggregate"]["mechanism_count"], 13)
        self.assertEqual(result["aggregate"]["pair_count"], 101)
        self.assertEqual(result["aggregate"]["candidate_count"] + result["aggregate"]["needs_review_count"], 101)
        self.assertTrue(all(r["status"] == "unreviewed" for r in result["pairs"]))
        self.assertFalse(result["scope"]["reviewed_evidence"])
        self.assertFalse(result["scope"]["candidate_count_is_validated_transition_count"])

    def test_scan_rejects_corrupt_hash_or_incomplete_panel_inventory(self):
        for mutation in ("hash", "omitted_panel", "split_mechanism", "float_step", "bool_mechanism"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                registry = json.loads(REGISTRY.read_bytes())
                if mutation == "hash":
                    registry["records"][0]["snapshot_sha256"] = "0" * 64
                elif mutation == "omitted_panel":
                    registry["records"][0]["mechanisms"][0]["step_ids"].pop()
                elif mutation == "split_mechanism":
                    mechanism = registry["records"][0]["mechanisms"][0]
                    rest = {**mechanism, "step_ids": mechanism["step_ids"][4:]}
                    mechanism["step_ids"] = mechanism["step_ids"][:4]
                    registry["records"][0]["mechanisms"].append(rest)
                elif mutation == "float_step":
                    registry["records"][0]["mechanisms"][0]["step_ids"][-1] = 9.0
                else:
                    registry["records"][0]["mechanisms"][0]["mechanism_id"] = True
                path = Path(directory) / "registry.json"
                path.write_text(json.dumps(registry), encoding="utf-8")
                with self.assertRaises(ValueError):
                    scan(path)

    def test_scan_rejects_duplicate_json_keys_and_alternate_implementation_root(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            raw = REGISTRY.read_text(encoding="utf-8")
            path.write_text(raw.replace('"record_id": "M0106"', '"record_id": "M0001", "record_id": "M0106"'), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                scan(path)
            with self.assertRaisesRegex(ValueError, "executing implementation"):
                scan(REGISTRY, repo_root=Path(directory))
