"""Offline validation of the evidence-handle expansion scout.

No network: the count fetcher is injected with deterministic per-query supplies, so the full
recon (per-handle supply -> best corroborator -> uplift -> handle-blocked unlock roll-up) is
exercised and the guardrails asserted.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from catalytic_earth.evidence_handle_expansion import (
    HANDLE_FAMILIES,
    build_evidence_handle_expansion,
    evaluate_handle_family,
    write_evidence_handle_expansion,
)

# One synthetic family modelling the NAD(P) case: cofactor handle is weak (7), the keyword handle
# recovers almost the whole EC ceiling (7700/7804).
_NADP = {
    "family": "synthetic_nadp",
    "ec_class": "EC 1.1.1 (synthetic)",
    "chemistry": "synthetic NAD(P) dehydrogenase",
    "ec_filter": "(ec:1.1.1.*)",
    "current_handle": "((cc_cofactor:nad) OR (cc_cofactor:nadp))",
    "candidate_handles": (
        ("functional_keyword", "((keyword:NAD) OR (keyword:NADP))"),
        ("binding_site", "(ft_binding:*)"),
        ("active_site", "(ft_act_site:*)"),
    ),
    "confusable": True,
    "recommended_entry_level_corroborators": ["Rhea NAD(P) participant"],
    "notes": "synthetic",
}

_SUPPLY = {
    "(reviewed:true) AND (ec:1.1.1.*)": 7804,
    "(reviewed:true) AND (ec:1.1.1.*) AND ((cc_cofactor:nad) OR (cc_cofactor:nadp))": 7,
    "(reviewed:true) AND (ec:1.1.1.*) AND ((keyword:NAD) OR (keyword:NADP))": 7700,
    "(reviewed:true) AND (ec:1.1.1.*) AND (ft_binding:*)": 7234,
    "(reviewed:true) AND (ec:1.1.1.*) AND (ft_act_site:*)": 5588,
}


def _count_fetcher(query):
    return {"total_results": _SUPPLY.get(query), "metadata": {"query": query}}


class EvidenceHandleExpansionTests(unittest.TestCase):
    def test_best_handle_and_uplift(self) -> None:
        probe = evaluate_handle_family(
            _NADP, count_fetcher=_count_fetcher, target_floor=100, cap_ceiling=250
        )
        self.assertEqual(probe["ec_ceiling_supply"], 7804)
        self.assertEqual(probe["current_handle_supply"], 7)
        self.assertEqual(probe["best_corroborated_handle"], "functional_keyword")
        self.assertEqual(probe["recovered_supply"], 7700)
        self.assertEqual(probe["uplift_vs_current_handle"], 7693)
        # current handle (7 * 0.5 = 4) is below floor; best handle (cap 150) is above floor.
        self.assertFalse(probe["floor_reachable_current_handle"])
        self.assertTrue(probe["floor_reachable_best_handle"])
        self.assertEqual(probe["applied_cap"], 150)  # confusable
        self.assertEqual(probe["reachable_bronze_best_handle"], 150)
        self.assertEqual(probe["reachable_bronze_current_handle"], 4)
        self.assertEqual(probe["reachable_bronze_uplift"], 146)

    def test_ec_family_is_not_a_corroborator(self) -> None:
        # The bare EC ceiling must never be selected as the corroborating handle.
        probe = evaluate_handle_family(
            _NADP, count_fetcher=_count_fetcher, target_floor=100, cap_ceiling=250
        )
        self.assertIn(probe["best_corroborated_handle"], ("functional_keyword", "binding_site", "active_site"))
        for h in probe["candidate_handle_supplies"]:
            self.assertTrue(h["is_corroborator"])

    def test_rollup_counts_handle_blocked_unlock(self) -> None:
        audit = build_evidence_handle_expansion(
            handle_families=(_NADP,),
            count_fetcher=_count_fetcher,
            created_utc="2026-06-12T00:00:00Z",
        )
        c = audit["counts"]
        self.assertEqual(c["families_probed"], 1)
        self.assertEqual(c["handle_blocked_families_unlocked_by_better_handle"], 1)
        self.assertEqual(c["handle_blocked_family_ids"], ["synthetic_nadp"])
        self.assertEqual(c["total_reviewed_supply_uplift_over_current_handles"], 7693)
        self.assertEqual(c["total_reachable_positive_bronze_uplift"], 146)

    def test_guardrails_no_registry_or_labels(self) -> None:
        audit = build_evidence_handle_expansion(
            handle_families=(_NADP,), count_fetcher=_count_fetcher
        )
        g = audit["guardrails"]
        self.assertFalse(g["registry_written"])
        self.assertFalse(g["labels_created"])
        self.assertTrue(g["ec_keyword_used_for_scope_estimate_only_never_predictive"])
        blob = json.dumps(audit)
        self.assertNotIn('"tier": "bronze"', blob)
        self.assertNotIn("predictive_evidence", blob)

    def test_writer_non_destructive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "handle.json"
            report = Path(tmp) / "handle.md"
            audit = write_evidence_handle_expansion(
                out_path=out,
                report_path=report,
                handle_families=(_NADP,),
                count_fetcher=_count_fetcher,
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertIn("Evidence-Handle Expansion", report.read_text(encoding="utf-8"))
            self.assertEqual(audit["counts"]["families_probed"], 1)

    def test_shipped_families_well_formed(self) -> None:
        for spec in HANDLE_FAMILIES:
            for key in ("family", "ec_class", "chemistry", "ec_filter", "candidate_handles"):
                self.assertIn(key, spec)
            self.assertTrue(spec["candidate_handles"])
        ids = [s["family"] for s in HANDLE_FAMILIES]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
