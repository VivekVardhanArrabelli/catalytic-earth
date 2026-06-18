from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from catalytic_earth.novelty_admission_gate import (
    DiversityState,
    build_diversity_state,
    build_novelty_admission_gate_audit,
    cluster_key,
    evaluate_batch,
    evaluate_candidate,
    self_audit,
    write_novelty_admission_gate_audit,
)
from catalytic_earth.registry_io import load_json

REPO_ROOT = Path(__file__).resolve().parents[1]
FROZEN_PATH = REPO_ROOT / "data/registries/curated_mechanism_labels.json"
EXPANSION_PATH = REPO_ROOT / "data/registries/external_bronze_labels.json"


def _row(
    *,
    entry_id,
    fp=None,
    label_type=None,
    organism="Homo sapiens (Human)",
    seq_len=400,
    ec=("3.4.24.1",),
    rhea=("RHEA:1001",),
):
    return {
        "entry_id": entry_id,
        "label_type": label_type
        or ("seed_fingerprint" if fp else "out_of_scope"),
        "fingerprint_id": fp,
        "evidence": {
            "source_provenance": {"organism": organism, "sequence_length": seq_len},
            "mechanism_evidence": {
                "ec_numbers": list(ec),
                "reaction_equations": [{"rhea_id": r} for r in rhea],
            },
        },
    }


class ClusterKeyTests(unittest.TestCase):
    def test_same_enzyme_org_length_share_key(self) -> None:
        a = _row(entry_id="a", fp="metal_dependent_hydrolase", seq_len=410)
        b = _row(entry_id="b", fp="metal_dependent_hydrolase", seq_len=455)
        self.assertEqual(cluster_key(a), cluster_key(b))  # same 400-499 bin

    def test_different_organism_splits_key(self) -> None:
        a = _row(entry_id="a", fp="metal_dependent_hydrolase", organism="Homo sapiens")
        b = _row(entry_id="b", fp="metal_dependent_hydrolase", organism="Escherichia coli")
        self.assertNotEqual(cluster_key(a), cluster_key(b))


class EvaluateCandidateTests(unittest.TestCase):
    def _state_with(self, rows):
        s = DiversityState()
        for r in rows:
            s.absorb(r)
        return s

    def test_new_cluster_admitted(self) -> None:
        state = DiversityState()
        cand = _row(entry_id="x", fp="plp_dependent_enzyme", ec=("4.1.1.1",))
        # seed fp_count 0 -> hole -> admit
        result = evaluate_candidate(cand, state)
        self.assertEqual(result["decision"], "admit")
        self.assertTrue(result["new_cluster"])

    def test_redundant_ortholog_throttled_for_balanced_fp(self) -> None:
        # make plp balanced (above floor) and a cluster saturated
        base = [
            _row(entry_id=f"seed{i}", fp="plp_dependent_enzyme", ec=("4.1.1.1",),
                 organism=f"org{i}", rhea=(f"RHEA:{i}",))
            for i in range(120)
        ]
        # saturate one cluster (same ec/org/len) with 3 identical-reaction rows
        sat = [
            _row(entry_id=f"sat{i}", fp="plp_dependent_enzyme", ec=("4.1.1.99",),
                 organism="Homo sapiens (Human)", seq_len=300, rhea=("RHEA:999",))
            for i in range(3)
        ]
        state = self._state_with(base + sat)
        # a 4th identical row: same cluster, same reaction, same organism -> throttle
        dup = _row(entry_id="dup", fp="plp_dependent_enzyme", ec=("4.1.1.99",),
                   organism="Homo sapiens (Human)", seq_len=320, rhea=("RHEA:999",))
        result = evaluate_candidate(dup, state)
        self.assertEqual(result["decision"], "throttle")

    def test_over_cap_rejected_without_new_reaction(self) -> None:
        base = [
            _row(entry_id=f"m{i}", fp="metal_dependent_hydrolase", ec=("3.4.24.1",),
                 organism=f"org{i}", seq_len=400 + i, rhea=("RHEA:1",))
            for i in range(300)
        ]
        state = self._state_with(base)
        # over cap, reaction RHEA:1 already known -> reject
        cand = _row(entry_id="z", fp="metal_dependent_hydrolase", ec=("3.4.24.1",),
                    organism="newOrg", seq_len=999, rhea=("RHEA:1",))
        result = evaluate_candidate(cand, state)
        self.assertEqual(result["decision"], "reject")

    def test_over_cap_admitted_with_new_reaction(self) -> None:
        base = [
            _row(entry_id=f"m{i}", fp="metal_dependent_hydrolase", ec=("3.4.24.1",),
                 organism=f"org{i}", seq_len=400 + i, rhea=("RHEA:1",))
            for i in range(300)
        ]
        state = self._state_with(base)
        cand = _row(entry_id="novel", fp="metal_dependent_hydrolase", ec=("3.4.24.1",),
                    organism="newOrg", seq_len=999, rhea=("RHEA:NEW",))
        result = evaluate_candidate(cand, state)
        self.assertEqual(result["decision"], "admit")
        self.assertEqual(result["reason"], "over_cap_but_new_reaction_chemistry")


class PerReactionCapTests(unittest.TestCase):
    def _balanced_state_one_reaction(self, fp: str, n: int = 150) -> DiversityState:
        s = DiversityState()
        # n rows, all the SAME reaction, distinct organisms -> fp past floor, the
        # single reaction is heavily saturated.
        for i in range(n):
            s.absorb(
                _row(
                    entry_id=f"s{i}",
                    fp=fp,
                    organism=f"org{i}",
                    seq_len=200 + i % 5,
                    rhea=("RHEA:1001",),
                )
            )
        return s

    def test_default_none_admits_new_organism_same_reaction(self) -> None:
        state = self._balanced_state_one_reaction("plp_dependent_enzyme")
        cand = _row(entry_id="new", fp="plp_dependent_enzyme", organism="brand_new", seq_len=999)
        result = evaluate_candidate(cand, state)  # per_reaction_cap default None
        self.assertEqual(result["decision"], "admit")

    def test_cap_throttles_saturated_reaction_even_with_new_organism(self) -> None:
        state = self._balanced_state_one_reaction("plp_dependent_enzyme")
        cand = _row(entry_id="new", fp="plp_dependent_enzyme", organism="brand_new", seq_len=999)
        result = evaluate_candidate(cand, state, per_reaction_cap=12)
        self.assertEqual(result["decision"], "throttle")
        self.assertEqual(result["reason"], "reaction_saturated_per_reaction_cap")
        self.assertTrue(result["per_reaction_saturated"])

    def test_cap_admits_a_genuinely_new_reaction(self) -> None:
        state = self._balanced_state_one_reaction("plp_dependent_enzyme")
        cand = _row(
            entry_id="new",
            fp="plp_dependent_enzyme",
            organism="brand_new",
            rhea=("RHEA:9999",),
        )
        result = evaluate_candidate(cand, state, per_reaction_cap=12)
        self.assertEqual(result["decision"], "admit")

    def test_cap_does_not_block_under_floor_reaching_floor(self) -> None:
        # a single-reaction HOLE/under-floor family must still reach the floor even
        # though its one reaction repeats -- the cap bounds depth ABOVE the floor only.
        s = DiversityState()
        for i in range(5):
            s.absorb(_row(entry_id=f"u{i}", fp="cobalamin_radical_rearrangement", organism=f"o{i}"))
        cand = _row(entry_id="u6", fp="cobalamin_radical_rearrangement", organism="o6")
        result = evaluate_candidate(cand, s, per_reaction_cap=2)
        self.assertEqual(result["decision"], "admit")


class EvaluateBatchTests(unittest.TestCase):
    def test_within_batch_dedup_and_priority(self) -> None:
        state = DiversityState()
        # two identical OOS rows in one batch -> first admits, second throttles
        batch = [
            _row(entry_id="o1", ec=("2.7.11.1",), organism="Homo sapiens (Human)",
                 seq_len=400, rhea=("RHEA:5",)),
            _row(entry_id="o2", ec=("2.7.11.1",), organism="Homo sapiens (Human)",
                 seq_len=410, rhea=("RHEA:5",)),
        ]
        result = evaluate_batch(batch, state)
        self.assertEqual(result["decision_counts"].get("admit"), 1)
        self.assertIn("o1", result["admit_entry_ids"])
        self.assertNotIn("o2", result["admit_entry_ids"])


class SelfAuditRealRegistryTests(unittest.TestCase):
    def test_self_audit_flags_redundancy_concentrated_in_saturated_lanes(self) -> None:
        frozen = json.loads(FROZEN_PATH.read_text())
        expansion = load_json(EXPANSION_PATH)
        audit = self_audit(frozen, expansion)
        # 7420 prior rows + 150 N-ribosyl hydrolase bronze rows + 150 APH
        # tier-2 bronze rows + 100 SDR bronze rows applied on 2026-06-15,
        # plus 106 SBL tier-2 bronze rows and a reaction-cap-trimmed 100-row
        # metal-independent PDE tier-2 batch applied on 2026-06-16 through
        # mechanism-first lanes, plus a 2026-06-17 user-directed reviewed-Swiss-Prot
        # growth pass: 41 biotin + 3 SDR + 44 serine beta-lactamase + 1
        # protein-kinase + 25 metal-independent PDE + 28 aldo-keto reductase
        # + 32 aminoglycoside acetyltransferase + 4 metallo-beta-lactamase
        # + 150 peroxiredoxin/thiol-peroxidase (four new fingerprint families) =
        # 328 broadened-handle bronze rows.
        self.assertEqual(audit["expansion_rows"], 8354)
        # some redundancy exists and is bounded
        self.assertGreater(audit["would_not_readmit"], 0)
        self.assertLess(audit["would_not_readmit_fraction"], 1.0)
        # non-admit should be concentrated in OOS / metal (the saturated lanes)
        self.assertIn("out_of_scope", audit["non_admit_by_scope_top"])

    def test_write_is_non_destructive(self) -> None:
        frozen_before = FROZEN_PATH.read_bytes()
        expansion_before = EXPANSION_PATH.read_bytes()
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "gate.json"
            report = Path(tmp) / "gate.md"
            audit = write_novelty_admission_gate_audit(
                out_path=out,
                report_path=report,
                frozen_benchmark_path=FROZEN_PATH,
                expansion_registry_path=EXPANSION_PATH,
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertFalse(audit["guardrails"]["expansion_registry_written"])
            self.assertEqual(audit["guardrails"]["labels_emitted"], 0)
            self.assertEqual(FROZEN_PATH.read_bytes(), frozen_before)
            self.assertEqual(EXPANSION_PATH.read_bytes(), expansion_before)

    def test_audit_is_deterministic(self) -> None:
        frozen = json.loads(FROZEN_PATH.read_text())
        expansion = load_json(EXPANSION_PATH)
        a = build_novelty_admission_gate_audit(frozen, expansion)
        b = build_novelty_admission_gate_audit(frozen, expansion)
        a.pop("created_utc")
        b.pop("created_utc")
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
