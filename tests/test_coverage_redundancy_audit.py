from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from catalytic_earth.coverage_redundancy_audit import (
    ALL_FINGERPRINTS,
    build_coverage_redundancy_audit,
    write_coverage_redundancy_audit,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
FROZEN_PATH = REPO_ROOT / "data/registries/curated_mechanism_labels.json"
EXPANSION_PATH = REPO_ROOT / "data/registries/external_bronze_labels.json"


def _seed(
    *,
    entry_id,
    fp,
    registry="expansion_bronze",
    organism="Homo sapiens (Human)",
    seq_len=400,
    ec=("3.4.24.1",),
    rhea=("RHEA:1001",),
    lane="metal hydrolase",
):
    return {
        "entry_id": entry_id,
        "label_type": "seed_fingerprint",
        "fingerprint_id": fp,
        "tier": "bronze",
        "evidence": {
            "source_provenance": {
                "organism": organism,
                "sequence_length": seq_len,
                "target_family_lane": lane,
            },
            "mechanism_evidence": {
                "ec_numbers": list(ec),
                "reaction_equations": [
                    {"rhea_id": rid} for rid in rhea
                ],
            },
        },
    }


def _oos(*, entry_id, organism="Homo sapiens (Human)", seq_len=400, ec=("2.7.11.1",)):
    return {
        "entry_id": entry_id,
        "label_type": "out_of_scope",
        "fingerprint_id": None,
        "tier": "bronze",
        "evidence": {
            "source_provenance": {
                "organism": organism,
                "sequence_length": seq_len,
                "target_family_lane": "kinase/phosphotransferase",
            },
            "mechanism_evidence": {
                "ec_numbers": list(ec),
                "reaction_equations": [{"rhea_id": "RHEA:9001"}],
            },
        },
    }


class BuildAuditSyntheticTests(unittest.TestCase):
    def _synthetic(self):
        frozen = [
            _seed(entry_id="m_csa:1", fp="ser_his_acid_hydrolase", registry="frozen"),
            _seed(entry_id="m_csa:2", fp="metal_dependent_hydrolase", registry="frozen"),
        ]
        expansion = []
        # heavily over-supply metal so it trips the cap, and leave the rare
        # fingerprints empty so they read as holes
        for i in range(300):
            expansion.append(
                _seed(
                    entry_id=f"uniprot:M{i}",
                    fp="metal_dependent_hydrolase",
                    ec=("3.4.24.-",),
                    rhea=(f"RHEA:{2000 + (i % 5)}",),  # only 5 distinct reactions
                    seq_len=700,
                )
            )
        expansion.append(_oos(entry_id="uniprot:O1"))
        return frozen, expansion

    def test_totals_and_fingerprint_distribution(self) -> None:
        frozen, expansion = self._synthetic()
        audit = build_coverage_redundancy_audit(frozen, expansion)
        self.assertEqual(audit["totals"]["frozen_current702"], 2)
        self.assertEqual(audit["totals"]["expansion_bronze"], 301)
        self.assertEqual(audit["totals"]["combined"], 303)
        dist = audit["fingerprint_distribution"]
        self.assertEqual(dist["metal_dependent_hydrolase"]["combined"], 301)
        self.assertEqual(dist["ser_his_acid_hydrolase"]["frozen"], 1)
        self.assertEqual(dist["ser_his_acid_hydrolase"]["expansion"], 0)

    def test_class_imbalance_flags_holes_and_cap(self) -> None:
        frozen, expansion = self._synthetic()
        audit = build_coverage_redundancy_audit(frozen, expansion)
        ci = audit["class_imbalance"]
        self.assertIn("metal_dependent_hydrolase", ci["fingerprints_above_cap"])
        # every fingerprint with no labels at all is below floor
        self.assertIn("radical_sam_enzyme", ci["fingerprints_below_floor"])
        # ser_his present only in frozen => an expansion hole
        self.assertIn("ser_his_acid_hydrolase", ci["expansion_holes"])

    def test_redundancy_reaction_saturation(self) -> None:
        frozen, expansion = self._synthetic()
        audit = build_coverage_redundancy_audit(frozen, expansion)
        div = audit["redundancy"]["per_fingerprint_diversity"][
            "metal_dependent_hydrolase"
        ]
        # 300 labels across only 5 distinct reactions => high redundancy ratio
        self.assertEqual(div["distinct_reactions"], 5)
        self.assertGreater(div["labels_per_distinct_reaction"], 10)

    def test_near_duplicate_clusters_detected(self) -> None:
        frozen, expansion = self._synthetic()
        audit = build_coverage_redundancy_audit(frozen, expansion)
        nd = audit["redundancy"]["near_duplicate_clusters"]
        # all 300 metal rows share EC/organism/length-bin => one big cluster
        self.assertGreaterEqual(nd["cluster_count"], 1)
        biggest = nd["clusters_top25"][0]
        self.assertEqual(biggest["fingerprint_or_scope"], "metal_dependent_hydrolase")
        self.assertEqual(biggest["size"], 300)

    def test_acquisition_targets_priority_order(self) -> None:
        frozen, expansion = self._synthetic()
        audit = build_coverage_redundancy_audit(frozen, expansion)
        at = audit["acquisition_targets"]
        # holes ranked ahead of the over-capped metal fingerprint
        ranks = {r["fingerprint"]: r["priority_rank"] for r in at["targets"]}
        self.assertLess(
            ranks["radical_sam_enzyme"], ranks["metal_dependent_hydrolase"]
        )
        self.assertIn("metal_dependent_hydrolase", at["over_cap"])
        # every fingerprint appears exactly once with a sourcing hint
        self.assertEqual(len(at["targets"]), len(ALL_FINGERPRINTS))
        for r in at["targets"]:
            self.assertIn("ec_prefixes", r["sourcing_hints"])

    def test_non_destructive_guardrails(self) -> None:
        frozen, expansion = self._synthetic()
        audit = build_coverage_redundancy_audit(frozen, expansion)
        g = audit["guardrails"]
        self.assertFalse(g["frozen_benchmark_written"])
        self.assertFalse(g["expansion_registry_written"])
        self.assertEqual(g["labels_emitted"], 0)


class WriteAuditRealRegistryTests(unittest.TestCase):
    def test_writes_artifact_and_report_without_touching_registries(self) -> None:
        frozen_before = FROZEN_PATH.read_bytes()
        expansion_before = EXPANSION_PATH.read_bytes()
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "audit.json"
            report = Path(tmp) / "audit.md"
            audit = write_coverage_redundancy_audit(
                out_path=out,
                report_path=report,
                frozen_benchmark_path=FROZEN_PATH,
                expansion_registry_path=EXPANSION_PATH,
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            written = json.loads(out.read_text())
            self.assertEqual(written["totals"]["combined"], 3642)
            self.assertEqual(written["totals"]["frozen_current702"], 702)
            self.assertEqual(written["totals"]["expansion_bronze"], 2940)
            # the real registries must be byte-identical after the audit
            self.assertEqual(FROZEN_PATH.read_bytes(), frozen_before)
            self.assertEqual(EXPANSION_PATH.read_bytes(), expansion_before)
            # The Stage-1 holes were closed (2026-06-11); the only expansion holes are the two
            # 2026-06-12 broadened-handle families (nad_p_dehydrogenase, glycosyltransferase),
            # which are holes BY CONSTRUCTION until their non-destructive preview is applied to
            # the expansion registry (this run sources nothing). metal_dependent_hydrolase
            # remains the known (intentional) over-cap.
            self.assertEqual(
                audit["class_imbalance"]["expansion_holes"],
                ["glycosyltransferase", "nad_p_dehydrogenase"],
            )
            self.assertIn(
                "metal_dependent_hydrolase",
                audit["acquisition_targets"]["over_cap"],
            )

    def test_audit_is_deterministic(self) -> None:
        frozen = json.loads(FROZEN_PATH.read_text())
        expansion = json.loads(EXPANSION_PATH.read_text())
        a = build_coverage_redundancy_audit(frozen, expansion)
        b = build_coverage_redundancy_audit(frozen, expansion)
        a.pop("created_utc")
        b.pop("created_utc")
        self.assertEqual(
            json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True)
        )


if __name__ == "__main__":
    unittest.main()
