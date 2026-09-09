"""Regression tests for source-bound Atlas study-context packets."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest


REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "data/atlas/study_context/6ha3"
SCRIPT = REPO / "scripts/validate_atlas_study_context.py"
SPEC = importlib.util.spec_from_file_location("validate_atlas_study_context", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class AtlasStudyContextTests(unittest.TestCase):
    def test_repository_packet_validates(self) -> None:
        summary = MODULE.validate_packet(PACKET, REPO)
        self.assertEqual(summary["packet_id"], "atlas-study-context:6HA3:E160Q:F6P-ThDP:2026-09-09")
        self.assertEqual(summary["atom_count"], 42)
        self.assertEqual(summary["selected_atom_count"], 5)
        self.assertEqual(summary["incident_connection_count"], 4)
        self.assertEqual(summary["observation_count"], 3)

    def _copy_packet(self, directory: str) -> Path:
        target = Path(directory) / "packet"
        shutil.copytree(PACKET, target, ignore=shutil.ignore_patterns("6HA3.cif"))
        return target

    def _repin_projection(self, packet: Path) -> None:
        review_path = packet / "review.json"
        review = json.loads(review_path.read_text(encoding="utf-8"))
        review["reviewed_sha256"]["evidence_projection.json"] = _sha(
            packet / "evidence_projection.json"
        )
        _write_json(review_path, review)

    def test_source_hash_swap_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            packet = self._copy_packet(directory)
            projection_path = packet / "evidence_projection.json"
            projection = json.loads(projection_path.read_text(encoding="utf-8"))
            projection["arrangement"]["coordinate_source"]["sha256"] = "0" * 64
            _write_json(projection_path, projection)
            self._repin_projection(packet)
            with self.assertRaisesRegex(ValueError, "bound source hash differs"):
                MODULE.validate_packet(packet, REPO)

    def test_selected_atom_occupancy_loss_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            packet = self._copy_packet(directory)
            projection_path = packet / "evidence_projection.json"
            projection = json.loads(projection_path.read_text(encoding="utf-8"))
            projection["arrangement"]["selected_atoms"][2]["occupancy"] = 1.0
            _write_json(projection_path, projection)
            self._repin_projection(packet)
            with self.assertRaisesRegex(ValueError, "selected atom facts differ"):
                MODULE.validate_packet(packet, REPO)

    def test_metal_connection_cannot_be_retyped_as_covalent(self) -> None:
        with TemporaryDirectory() as directory:
            packet = self._copy_packet(directory)
            projection_path = packet / "evidence_projection.json"
            projection = json.loads(projection_path.read_text(encoding="utf-8"))
            projection["arrangement"]["incident_connections"][0]["connection_type"] = "covale"
            _write_json(projection_path, projection)
            self._repin_projection(packet)
            with self.assertRaisesRegex(ValueError, "incident connection inventory differs"):
                MODULE.validate_packet(packet, REPO)

    def test_m0219_step_promotion_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            packet = self._copy_packet(directory)
            projection_path = packet / "evidence_projection.json"
            projection = json.loads(projection_path.read_text(encoding="utf-8"))
            projection["atlas_record_binding"]["proposal_step_grounding"] = True
            _write_json(projection_path, projection)
            self._repin_projection(packet)
            with self.assertRaisesRegex(ValueError, "unsupported mechanism-step promotion"):
                MODULE.validate_packet(packet, REPO)

    def test_geometry_atoms_and_metric_type_drive_recomputation(self) -> None:
        with TemporaryDirectory() as directory:
            packet = self._copy_packet(directory)
            projection_path = packet / "evidence_projection.json"
            projection = json.loads(projection_path.read_text(encoding="utf-8"))
            metric = projection["arrangement"]["deposited_geometry"][1]
            metric["atom_ids"] = ["C5", "S1"]
            metric["metric_type"] = "distance_nanometers"
            _write_json(projection_path, projection)
            self._repin_projection(packet)
            with self.assertRaisesRegex(ValueError, "unsupported geometry metric type"):
                MODULE.validate_packet(packet, REPO)

    def test_relation_foreign_key_and_scope_cannot_be_promoted(self) -> None:
        with TemporaryDirectory() as directory:
            packet = self._copy_packet(directory)
            projection_path = packet / "evidence_projection.json"
            projection = json.loads(projection_path.read_text(encoding="utf-8"))
            relation = projection["relations"][0]
            relation["arrangement_id"] = "1ABC:FAKE:A:A1:model1"
            relation["relation"] = "causal_geometry_to_full_cycle_turnover"
            _write_json(projection_path, projection)
            self._repin_projection(packet)
            with self.assertRaisesRegex(ValueError, "relation arrangement binding differs"):
                MODULE.validate_packet(packet, REPO)

    def test_complete_active_site_and_uniprot_promotions_are_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            packet = self._copy_packet(directory)
            projection_path = packet / "evidence_projection.json"
            projection = json.loads(projection_path.read_text(encoding="utf-8"))
            projection["arrangement"]["assembly_scope"]["complete_active_site_represented"] = True
            projection["arrangement"]["protein"]["uniprot_accession"] = "P23254"
            _write_json(projection_path, projection)
            self._repin_projection(packet)
            with self.assertRaisesRegex(ValueError, "unsupported complete-active-site promotion"):
                MODULE.validate_packet(packet, REPO)

    def test_functional_endpoint_cannot_be_promoted(self) -> None:
        with TemporaryDirectory() as directory:
            packet = self._copy_packet(directory)
            projection_path = packet / "evidence_projection.json"
            projection = json.loads(projection_path.read_text(encoding="utf-8"))
            projection["observations"][0]["endpoint"] = "productive full-cycle F6P turnover"
            _write_json(projection_path, projection)
            self._repin_projection(packet)
            with self.assertRaisesRegex(ValueError, "stopped-flow endpoint scope differs"):
                MODULE.validate_packet(packet, REPO)

    def test_stale_manual_review_pin_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            packet = self._copy_packet(directory)
            review_path = packet / "review.json"
            review = json.loads(review_path.read_text(encoding="utf-8"))
            review["reviewed_sha256"]["evidence_projection.json"] = "0" * 64
            _write_json(review_path, review)
            with self.assertRaisesRegex(ValueError, "manual review pin is stale"):
                MODULE.validate_packet(packet, REPO)


if __name__ == "__main__":
    unittest.main()
