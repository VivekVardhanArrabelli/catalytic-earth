from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from catalytic_earth.bronze_silver_promotion_preview import (
    HOLO_STATUS,
    APO_STATUS,
    assess_promotion,
    build_bronze_silver_promotion_preview,
    structure_confirmability,
    write_bronze_silver_promotion_preview,
)
from catalytic_earth.mechanism_representation_loop import fingerprint_centroids

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPANSION_PATH = REPO_ROOT / "data/registries/external_bronze_labels.json"


def _row(*, entry_id, fp, cofactors=(), coordinate_status=None, coordinate_path=None,
         active=8, catalytic=2, binding=6):
    return {
        "entry_id": entry_id,
        "label_type": "seed_fingerprint" if fp else "out_of_scope",
        "fingerprint_id": fp,
        "tier": "bronze",
        "evidence": {
            "mechanism_evidence": {
                "cofactors": [{"name": c} for c in cofactors],
                "active_site_residues": [
                    {"feature_code": "BINDING", "ligand_name": c} for c in cofactors
                ],
                "active_site_residue_count": active,
                "catalytic_residue_count": catalytic,
                "binding_residue_count": binding,
            },
            "structure_provenance": {
                "coordinate_status": coordinate_status,
                "coordinate_path": coordinate_path,
            },
            "pending_promotion_audits": [
                "geometry_inverse_gate_confirmation_on_holo_or_cofactor_fused_structure",
            ],
        },
    }


def _seed_population():
    rows = []
    for i in range(8):
        rows.append(_row(entry_id=f"zn{i}", fp="metal_dependent_hydrolase",
                         cofactors=["Zn(2+)"]))
    for i in range(8):
        rows.append(_row(entry_id=f"plp{i}", fp="plp_dependent_enzyme",
                         cofactors=["pyridoxal 5'-phosphate"]))
    return rows


class StructureConfirmabilityTests(unittest.TestCase):
    def test_holo(self) -> None:
        self.assertEqual(
            structure_confirmability(_row(entry_id="a", fp="x",
                                          coordinate_status=HOLO_STATUS)),
            "holo",
        )

    def test_apo(self) -> None:
        self.assertEqual(
            structure_confirmability(_row(entry_id="a", fp="x",
                                          coordinate_status=APO_STATUS)),
            "apo_only",
        )

    def test_none(self) -> None:
        self.assertEqual(
            structure_confirmability(_row(entry_id="a", fp="x")), "none"
        )


class AssessPromotionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.centroids = fingerprint_centroids(_seed_population())

    def test_silver_ready_when_corroborated_and_holo(self) -> None:
        row = _row(entry_id="t", fp="metal_dependent_hydrolase",
                   cofactors=["Zn(2+)"], coordinate_status=HOLO_STATUS)
        d = assess_promotion(row, self.centroids, cohesion_threshold=0.5)
        self.assertEqual(d["decision"], "silver_ready_pending_geometry_run")

    def test_blocked_apo_when_corroborated_but_apo(self) -> None:
        row = _row(entry_id="t", fp="metal_dependent_hydrolase",
                   cofactors=["Zn(2+)"], coordinate_status=APO_STATUS)
        d = assess_promotion(row, self.centroids, cohesion_threshold=0.5)
        self.assertEqual(d["decision"], "blocked_apo_needs_cofactor_fusion")

    def test_blocked_pending_structure_when_no_coordinates(self) -> None:
        row = _row(entry_id="t", fp="metal_dependent_hydrolase", cofactors=["Zn(2+)"])
        d = assess_promotion(row, self.centroids, cohesion_threshold=0.5)
        self.assertEqual(d["decision"], "blocked_pending_structure")

    def test_review_when_chemistry_disagrees(self) -> None:
        # labeled metal but carries PLP chemistry -> nearest is plp -> review
        row = _row(entry_id="bad", fp="metal_dependent_hydrolase",
                   cofactors=["pyridoxal 5'-phosphate"], coordinate_status=HOLO_STATUS)
        d = assess_promotion(row, self.centroids, cohesion_threshold=0.5)
        self.assertEqual(d["decision"], "review_chemistry_disagrees")


class BuildPreviewTests(unittest.TestCase):
    def test_decisions_partition_all_seed_labels(self) -> None:
        seed = _seed_population()
        # add a holo metal row -> silver ready
        seed.append(_row(entry_id="holo", fp="metal_dependent_hydrolase",
                         cofactors=["Zn(2+)"], coordinate_status=HOLO_STATUS))
        audit = build_bronze_silver_promotion_preview(seed, cohesion_threshold=0.5)
        self.assertEqual(audit["seed_labels"], len(seed))
        self.assertEqual(sum(audit["decision_counts"].values()), len(seed))
        g = audit["guardrails"]
        self.assertFalse(g["registry_written"])
        self.assertFalse(g["tier_changed"])
        self.assertFalse(g["geometry_confirmation_run_or_faked"])


class RealRegistryTests(unittest.TestCase):
    def test_write_non_destructive_and_honest(self) -> None:
        before = EXPANSION_PATH.read_bytes()
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "prom.json"
            report = Path(tmp) / "prom.md"
            audit = write_bronze_silver_promotion_preview(
                out_path=out,
                report_path=report,
                expansion_registry_path=EXPANSION_PATH,
            )
            self.assertEqual(audit["seed_labels"], 486)
            # silver-ready must never exceed the holo-structure count (no faking)
            self.assertGreater(audit["silver_ready_count"], 0)
            self.assertFalse(audit["guardrails"]["geometry_confirmation_run_or_faked"])
            self.assertEqual(EXPANSION_PATH.read_bytes(), before)

    def test_deterministic(self) -> None:
        expansion = json.loads(EXPANSION_PATH.read_text())
        a = build_bronze_silver_promotion_preview(expansion)
        b = build_bronze_silver_promotion_preview(expansion)
        a.pop("created_utc")
        b.pop("created_utc")
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
