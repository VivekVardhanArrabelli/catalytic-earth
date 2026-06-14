"""Offline tests for the reaction-saturation trim (synthetic registries, no network)."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from catalytic_earth.coverage_redundancy_audit import reaction_aware_cap
from catalytic_earth.reaction_saturation_trim import (
    apply_reaction_saturation_trim_to_registry,
    build_reaction_saturation_trim,
    select_diverse_keep,
    write_reaction_saturation_trim,
)


def _label(
    entry_id: str,
    fingerprint: str | None,
    *,
    rxn: str | None = "RHEA:1",
    organism: str = "Org A",
    length: int = 200,
    label_type: str = "seed_fingerprint",
) -> dict:
    reaction_equations = (
        [{"rhea_id": rxn, "reaction": "a = b", "ec_number": "1.1.1.1"}] if rxn else []
    )
    return {
        "entry_id": entry_id,
        "fingerprint_id": fingerprint,
        "label_type": label_type,
        "tier": "bronze",
        "review_status": "automation_curated",
        "ontology_version_at_decision": "label_factory_v1_test",
        "confidence": "high",
        "evidence_score": 0.7,
        "rationale": "synthetic reaction-saturation trim test label row " + entry_id,
        "evidence": {
            "sources": ["reviewed_swissprot"],
            "cofactor_evidence_level": "annotated",
            "conflicts": [],
            "excluded_context": [
                "protein_name",
                "ec_label",
                "uniprot_prose",
                "source_annotation",
                "curated_mechanism_text",
                "target_family_lane",
            ],
            "mechanism_evidence": {
                "ec_numbers": ["1.1.1.1"],
                "reaction_equations": reaction_equations,
            },
            "source_provenance": {
                "organism": organism,
                "sequence_length": length,
                "target_family_lane": fingerprint,
            },
        },
    }


class SelectDiverseKeepTests(unittest.TestCase):
    def test_keeps_all_when_under_cap(self) -> None:
        rows = [_label(f"uniprot:K{i}", "fp", organism=f"o{i}") for i in range(5)]
        sel = select_diverse_keep(rows, cap=10)
        self.assertEqual(len(sel["kept"]), 5)
        self.assertEqual(sel["demoted"], [])

    def test_keeps_one_per_distinct_reaction_first(self) -> None:
        # 3 distinct reactions; many orthologs of reaction R1, single rows for R2/R3.
        rows = [
            _label(f"uniprot:A{i}", "fp", rxn="RHEA:1", organism=f"oA{i}")
            for i in range(8)
        ]
        rows.append(_label("uniprot:B", "fp", rxn="RHEA:2", organism="oB"))
        rows.append(_label("uniprot:C", "fp", rxn="RHEA:3", organism="oC"))
        sel = select_diverse_keep(rows, cap=4)
        self.assertEqual(len(sel["kept"]), 4)
        # all three distinct reactions must survive the trim
        self.assertEqual(sel["kept_distinct_reactions"], 3)
        self.assertIn("uniprot:B", sel["kept"])
        self.assertIn("uniprot:C", sel["kept"])

    def test_demotes_near_duplicate_clusters_first(self) -> None:
        # one reaction, 6 rows: 4 share an identical cluster key (same org+length bin),
        # 2 are diverse. With cap 3 the near-dups should be demoted preferentially.
        rows = [
            _label(f"uniprot:D{i}", "fp", rxn="RHEA:1", organism="same", length=200)
            for i in range(4)
        ]
        rows.append(_label("uniprot:E", "fp", rxn="RHEA:1", organism="diff1", length=500))
        rows.append(_label("uniprot:F", "fp", rxn="RHEA:1", organism="diff2", length=900))
        sel = select_diverse_keep(rows, cap=3)
        self.assertEqual(len(sel["kept"]), 3)
        self.assertIn("uniprot:E", sel["kept"])
        self.assertIn("uniprot:F", sel["kept"])
        # at most one of the 4 identical-cluster rows survives
        kept_dups = [k for k in sel["kept"] if k.startswith("uniprot:D")]
        self.assertEqual(len(kept_dups), 1)

    def test_deterministic(self) -> None:
        rows = [_label(f"uniprot:G{i}", "fp", organism=f"o{i % 3}") for i in range(20)]
        a = select_diverse_keep(rows, cap=7)
        b = select_diverse_keep(list(reversed(rows)), cap=7)
        self.assertEqual(a["kept"], b["kept"])


class BuildTrimTests(unittest.TestCase):
    def _registry(self) -> tuple[list, list]:
        frozen = [_label("mcsa:1", "saturated_fp"), _label("mcsa:2", "diverse_fp")]
        expansion: list = []
        # saturated_fp: 1 reaction, 12 orthologs -> reaction-saturated
        for i in range(12):
            expansion.append(
                _label(f"uniprot:S{i}", "saturated_fp", rxn="RHEA:1", organism=f"o{i}")
            )
        # diverse_fp: 12 rows across 12 reactions -> not saturated
        for i in range(12):
            expansion.append(
                _label(f"uniprot:V{i}", "diverse_fp", rxn=f"RHEA:{100 + i}", organism=f"v{i}")
            )
        return frozen, expansion

    def test_trims_only_reaction_saturated_family(self) -> None:
        frozen, expansion = self._registry()
        # small bounds so the synthetic saturated family is trimmed to the floor
        audit = build_reaction_saturation_trim(
            frozen,
            expansion,
            reaction_cap_rate=2,
            target_floor=4,
            cap_ceiling=10,
            saturation_ratio_threshold=3.0,
        )
        self.assertEqual(audit["totals"]["families_trimmed"], 1)
        fam = audit["trimmed_families"][0]
        self.assertEqual(fam["fingerprint"], "saturated_fp")
        # 1 distinct reaction -> reaction-aware cap clamps to the floor (not dropped below)
        self.assertEqual(fam["reaction_aware_cap"], 4)
        self.assertEqual(fam["kept"], 4)
        self.assertEqual(fam["demoted"], 8)
        self.assertTrue(fam["reaction_diversity_preserved"])
        # the diverse family is never trimmed
        trimmed_names = {f["fingerprint"] for f in audit["trimmed_families"]}
        self.assertNotIn("diverse_fp", trimmed_names)

    def test_counters_drop_only_positive_bronze(self) -> None:
        frozen, expansion = self._registry()
        audit = build_reaction_saturation_trim(
            frozen, expansion, reaction_cap_rate=2, target_floor=4, cap_ceiling=10,
            saturation_ratio_threshold=3.0,
        )
        before = audit["separate_honest_counters"]["before"]
        after = audit["separate_honest_counters"]["after"]
        self.assertEqual(
            before["positive_bronze_count"] - after["positive_bronze_count"],
            audit["totals"]["rows_demoted"],
        )
        self.assertEqual(before["oos_bronze_count"], after["oos_bronze_count"])

    def test_write_is_non_destructive(self) -> None:
        frozen, expansion = self._registry()
        with TemporaryDirectory() as tmp:
            frozen_path = Path(tmp) / "frozen.json"
            exp_path = Path(tmp) / "expansion.json"
            frozen_path.write_text(json.dumps(frozen))
            exp_path.write_text(json.dumps(expansion))
            frozen_before = frozen_path.read_bytes()
            exp_before = exp_path.read_bytes()
            out = Path(tmp) / "trim.json"
            report = Path(tmp) / "trim.md"
            audit = write_reaction_saturation_trim(
                out_path=out,
                report_path=report,
                frozen_benchmark_path=frozen_path,
                expansion_registry_path=exp_path,
                reaction_cap_rate=2,
                target_floor=4,
                cap_ceiling=10,
                saturation_ratio_threshold=3.0,
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertFalse(audit["applied"])
            # neither registry is written by the preview
            self.assertEqual(frozen_path.read_bytes(), frozen_before)
            self.assertEqual(exp_path.read_bytes(), exp_before)
            self.assertEqual(audit["guardrails"]["expansion_registry_written"], False)


class ApplyTrimTests(unittest.TestCase):
    def test_apply_drops_only_demoted_and_leaves_frozen_untouched(self) -> None:
        frozen = [_label("mcsa:1", "fp")]
        expansion = [
            _label(f"uniprot:S{i}", "fp", rxn="RHEA:1", organism=f"o{i}") for i in range(12)
        ]
        with TemporaryDirectory() as tmp:
            frozen_path = Path(tmp) / "frozen.json"
            exp_path = Path(tmp) / "expansion.json"
            preview_path = Path(tmp) / "trim.json"
            frozen_path.write_text(json.dumps(frozen))
            exp_path.write_text(json.dumps(expansion))
            audit = write_reaction_saturation_trim(
                out_path=preview_path,
                frozen_benchmark_path=frozen_path,
                expansion_registry_path=exp_path,
                reaction_cap_rate=2,
                target_floor=4,
                cap_ceiling=10,
                saturation_ratio_threshold=3.0,
            )
            demoted = audit["demoted_entry_ids"]
            self.assertEqual(len(demoted), 8)
            frozen_before = frozen_path.read_bytes()

            result = apply_reaction_saturation_trim_to_registry(
                preview_path=preview_path,
                expansion_registry_path=exp_path,
                frozen_benchmark_registry_path=frozen_path,
            )
            self.assertTrue(result["applied"])
            self.assertEqual(result["rows_removed"], 8)
            self.assertEqual(result["expansion_registry_after"], 4)
            self.assertFalse(result["frozen_benchmark_registry_written"])
            # frozen registry is byte-identical after apply
            self.assertEqual(frozen_path.read_bytes(), frozen_before)
            # the rewritten registry contains exactly the kept rows
            kept = json.loads(exp_path.read_text())
            kept_ids = {r["entry_id"] for r in kept}
            self.assertTrue(kept_ids.isdisjoint(set(demoted)))
            self.assertEqual(len(kept), 4)

    def test_apply_rejects_non_trim_preview(self) -> None:
        with TemporaryDirectory() as tmp:
            preview = Path(tmp) / "other.json"
            preview.write_text(json.dumps({"audit": "something_else"}))
            with self.assertRaises(ValueError):
                apply_reaction_saturation_trim_to_registry(
                    preview_path=preview,
                    expansion_registry_path=Path(tmp) / "e.json",
                    frozen_benchmark_registry_path=Path(tmp) / "f.json",
                )


class ReactionAwareCapTests(unittest.TestCase):
    def test_clamp_bounds(self) -> None:
        self.assertEqual(reaction_aware_cap(1, rate=8, floor=100, ceiling=250), 100)
        self.assertEqual(reaction_aware_cap(16, rate=8, floor=100, ceiling=250), 128)
        self.assertEqual(reaction_aware_cap(40, rate=8, floor=100, ceiling=250), 250)
        self.assertEqual(reaction_aware_cap(0, rate=8, floor=100, ceiling=250), 100)


if __name__ == "__main__":
    unittest.main()
