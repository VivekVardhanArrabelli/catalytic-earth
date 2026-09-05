from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from catalytic_earth.atlas50_crosswalk_v2 import (
    EXPECTED_INPUT_SHA256,
    OUTPUT_RELATIVE,
    PHASE_A_RELATIVE,
    REVIEW_RELATIVE,
    build_crosswalk_v2_documents,
    build_crosswalk_v2_outputs,
    canonical_json_bytes,
    validate_crosswalk_v2,
)


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / OUTPUT_RELATIVE


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _row(document: dict, fingerprint_id: str) -> dict:
    return next(
        row for row in document["rows"] if row["fingerprint_id"] == fingerprint_id
    )


class Atlas50CrosswalkV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.phase_a = _load(ROOT / PHASE_A_RELATIVE)
        cls.review = _load(ROOT / REVIEW_RELATIVE)
        cls.crosswalk = _load(OUTPUT / "crosswalk.json")
        cls.change_map = _load(OUTPUT / "change_map.json")

    def test_repository_artifacts_are_byte_current_and_inputs_are_pinned(self) -> None:
        outputs = build_crosswalk_v2_outputs(ROOT)

        self.assertEqual(set(outputs), {"crosswalk.json", "change_map.json", "manifest.json"})
        for filename, value in outputs.items():
            self.assertEqual((OUTPUT / filename).read_bytes(), canonical_json_bytes(value))
        self.assertEqual(
            {item["path"]: item["sha256"] for item in outputs["manifest.json"]["inputs"]},
            EXPECTED_INPUT_SHA256,
        )
        for document in (outputs["crosswalk.json"], outputs["change_map.json"], outputs["manifest.json"]):
            self.assertFalse(document["review_independence"]["statistically_independent"])
            self.assertTrue(document["review_independence"]["correlated_error_risk"])
            self.assertEqual(
                document["review_independence"]["reviewer_kind"],
                "same_model_computational_agents",
            )

    def test_wrong_mcsa_anchor_cannot_propagate_a_derived_bundle(self) -> None:
        phase_a = copy.deepcopy(self.phase_a)
        plp = _row(phase_a, "plp_dependent_enzyme")
        plp["source_links"]["interpro"]["records"].append(
            {
                "record_id": "INVENTED:M0049-DERIVED",
                "role": "candidate_anchor_propagation",
            }
        )
        plp["source_links"]["interpro"]["lookup_keys"].append(
            "INVENTED:M0049-DERIVED"
        )

        crosswalk, _ = build_crosswalk_v2_documents(phase_a, self.review)
        corrected = _row(crosswalk, "plp_dependent_enzyme")
        positive_targets = [
            target
            for target in corrected["relation_targets"]
            if target["relation"] not in {"rejected_mapping", "counterevidence", "scope_exclusion"}
        ]
        removed = corrected["rejected_source_mappings"][0]["removed_source_bundle"]
        removed_interpro = next(
            item for item in removed if item["source_key"] == "interpro"
        )

        self.assertIn("INVENTED:M0049-DERIVED", removed_interpro["record_ids"])
        self.assertNotIn(
            "INVENTED:M0049-DERIVED",
            json.dumps(positive_targets, sort_keys=True),
        )
        self.assertEqual(
            [
                target["relation"]
                for target in corrected["relation_targets"]
                if target["target_id"] == "M0049"
            ],
            ["rejected_mapping"],
        )
        self.assertTrue(
            corrected["rejected_source_mappings"][0][
                "anchor_valid_outside_this_mapping"
            ]
        )

    def test_same_reaction_locator_cannot_be_promoted_to_invented_equivalence(self) -> None:
        changed = copy.deepcopy(self.crosswalk)
        ndpk = _row(changed, "nucleoside_diphosphate_kinase")
        ndpk["computational_classification"] = "exact_duplicate"
        ndpk["status"] = "computational_provisional_relation"
        ndpk["relation_targets"][0]["mechanistic_applicability"][
            "status"
        ] = "exact_scope_supported"
        changed["classification_counts"]["unresolved"] -= 1
        changed["classification_counts"]["exact_duplicate"] = 1

        with self.assertRaisesRegex(
            ValueError, "exact equivalence is not supported at that scope"
        ):
            validate_crosswalk_v2(changed)

    def test_source_identity_and_mechanistic_applicability_are_never_conflated(self) -> None:
        validate_crosswalk_v2(self.crosswalk)

        for row in self.crosswalk["rows"]:
            for target in row["relation_targets"]:
                self.assertIn("status", target["source_identity"])
                self.assertIn("name", target["source_identity"])
                self.assertIn("status", target["mechanistic_applicability"])
                self.assertIn("scope", target["mechanistic_applicability"])
                self.assertNotEqual(
                    target["source_identity"]["status"],
                    target["mechanistic_applicability"]["status"],
                )

        sod = _row(self.crosswalk, "manganese_iron_superoxide_dismutase")
        target = sod["relation_targets"][0]
        self.assertEqual(target["source_identity"]["status"], "official_entry_checked")
        self.assertEqual(target["mechanistic_applicability"]["status"], "counterexample_only")
        self.assertEqual(sod["computational_classification"], "unresolved")

    def test_heme_p450_and_laccase_have_separate_positive_coverage(self) -> None:
        heme = _row(self.crosswalk, "heme_peroxidase_oxidase")
        p450 = _row(self.crosswalk, "cytochrome_p450_monooxygenase")
        copper = _row(self.crosswalk, "copper_oxidoreductase")

        positive = lambda row: {
            target["target_id"]
            for target in row["relation_targets"]
            if target["mechanistic_applicability"]["status"]
            in {"supported_branch", "representative_scope_only"}
        }
        self.assertEqual(positive(heme), {"M0239"})
        self.assertEqual(positive(p450), {"M0133"})
        self.assertEqual(positive(copper), {"M0135", "M0390"})

    def test_same_ec_counterevidence_and_beta_lactamase_class_scopes_are_explicit(self) -> None:
        aldolase = _row(self.crosswalk, "class_ii_metal_aldolase")
        aldolase_targets = {
            target["target_id"]: target for target in aldolase["relation_targets"]
        }
        self.assertEqual(aldolase_targets["M0052"]["relation"], "specialization")
        self.assertEqual(aldolase_targets["M0222"]["relation"], "counterevidence")
        self.assertEqual(
            aldolase_targets["M0052"]["source_identity"]["ec"],
            aldolase_targets["M0222"]["source_identity"]["ec"],
        )

        serine = _row(self.crosswalk, "serine_beta_lactamase")
        metallo = _row(self.crosswalk, "metallo_beta_lactamase")
        self.assertEqual(
            {
                target["mechanistic_applicability"]["scope"]
                for target in serine["relation_targets"]
            },
            {"Ambler Class A", "Ambler Class C", "Ambler Class D"},
        )
        self.assertEqual(
            {
                target["mechanistic_applicability"]["scope"]
                for target in metallo["relation_targets"]
            },
            {
                "Ambler Class B1, dimetallic mechanism",
                "Ambler Class B1, monometallic mechanism",
            },
        )
        self.assertIn("B2/B3 remain unrepresented", metallo["scope_statement"])

    def test_dhfr_keeps_one_bounded_exact_core_without_broad_applicability(self) -> None:
        dhfr = _row(self.crosswalk, "dihydrofolate_reductase")

        self.assertEqual(dhfr["prior_classification"], "exact_duplicate")
        self.assertEqual(dhfr["computational_classification"], "exact_duplicate")
        self.assertIn("Conserved water donates the N5 proton", dhfr["scope_statement"])
        self.assertIn("Asp26 tunes", dhfr["scope_statement"])
        self.assertEqual(len(dhfr["relation_targets"]), 1)
        exact = dhfr["relation_targets"][0]
        self.assertEqual(exact["target_id"], "M0112")
        self.assertEqual(
            exact["mechanistic_applicability"]["scope"],
            "reaction_core: EC 1.5.1.3 NADPH-dependent DHF-to-THF chemistry",
        )
        self.assertIn("Protein, organism, resistance, fusion, and structure", dhfr["scope_statement"])

    def test_correlated_same_model_disclosure_is_required(self) -> None:
        changed = copy.deepcopy(self.crosswalk)
        changed.pop("review_independence")

        with self.assertRaisesRegex(ValueError, "correlated same-model review"):
            validate_crosswalk_v2(changed)

    def test_every_old_row_has_an_explicit_change_record_and_claim_boundary(self) -> None:
        self.assertEqual(self.crosswalk["row_count"], 57)
        self.assertEqual(self.change_map["row_count"], 57)
        self.assertEqual(
            [row["fingerprint_id"] for row in self.crosswalk["rows"]],
            [change["fingerprint_id"] for change in self.change_map["changes"]],
        )
        self.assertEqual(self.crosswalk["classification_counts"]["unresolved"], 34)
        self.assertTrue(all(change["reason"] for change in self.change_map["changes"]))
        self.assertTrue(
            all(
                "no independent-human review" in row["claim_boundary"]
                for row in self.crosswalk["rows"]
            )
        )


if __name__ == "__main__":
    unittest.main()
