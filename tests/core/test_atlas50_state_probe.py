from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from catalytic_earth.atlas50_state_probe import (
    build_state_probe,
    canonical_json_bytes,
    file_sha256,
    validate_probe_spec,
    validate_state_probe,
)


ROOT = Path(__file__).resolve().parents[2]
STATE_ROOT = ROOT / "data/atlas/atlas50/state_probe"
SPEC_PATH = STATE_ROOT / "spec.json"
REPORT_PATH = STATE_ROOT / "report.json"
INPUT_PATHS = {
    "candidate_spec": ROOT / "data/atlas/atlas50/phase_a/candidate_spec.json",
    "computational_panel_review": (
        ROOT / "data/atlas/atlas50/computational_review/panel_review.json"
    ),
    "mechanism_record_v3_schema": (
        ROOT / "src/catalytic_earth/schemas/mechanism-record-v3.schema.json"
    ),
    "atlas3_kernel": ROOT / "data/atlas/atlas3/kernel.json",
    "atlas10_kernel": ROOT / "data/atlas/atlas10/kernel.json",
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class Atlas50StateProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = _load(SPEC_PATH)
        cls.report = _load(REPORT_PATH)
        cls.candidate_spec = _load(INPUT_PATHS["candidate_spec"])
        cls.panel_review = _load(INPUT_PATHS["computational_panel_review"])
        cls.mechanism_schema = _load(INPUT_PATHS["mechanism_record_v3_schema"])
        cls.atlas3 = _load(INPUT_PATHS["atlas3_kernel"])
        cls.atlas10 = _load(INPUT_PATHS["atlas10_kernel"])
        cls.basis_inputs = {
            name: file_sha256(path) for name, path in sorted(INPUT_PATHS.items())
        }

    def _build(self, spec: dict | None = None) -> dict:
        return build_state_probe(
            self.spec if spec is None else spec,
            candidate_spec=self.candidate_spec,
            panel_review=self.panel_review,
            mechanism_v3_schema=self.mechanism_schema,
            atlas3_kernel=self.atlas3,
            atlas10_kernel=self.atlas10,
            basis_inputs=self.basis_inputs,
        )

    def test_committed_report_is_deterministic_and_byte_current(self) -> None:
        expected = self._build()
        self.assertEqual(REPORT_PATH.read_bytes(), canonical_json_bytes(expected))
        summary = validate_state_probe(
            self.report,
            spec=self.spec,
            candidate_spec=self.candidate_spec,
            panel_review=self.panel_review,
            mechanism_v3_schema=self.mechanism_schema,
            atlas3_kernel=self.atlas3,
            atlas10_kernel=self.atlas10,
            basis_inputs=self.basis_inputs,
        )
        self.assertEqual(
            summary,
            {
                "case_count": 6,
                "PASS": 1,
                "SCOPED_PASS": 4,
                "ABSTAIN": 1,
                "external_response_bytes": 166234,
            },
        )

    def test_case_dispositions_and_allowed_operations_are_bounded(self) -> None:
        cases = {case["mcsa_id"]: case for case in self.report["cases"]}
        self.assertEqual(
            {mcsa_id: case["disposition"] for mcsa_id, case in cases.items()},
            {
                "M0064": "SCOPED_PASS",
                "M0106": "SCOPED_PASS",
                "M0107": "PASS",
                "M0212": "SCOPED_PASS",
                "M0753": "SCOPED_PASS",
                "M0970": "ABSTAIN",
            },
        )
        self.assertEqual(cases["M0064"]["allowed_operations"], ["source_annotation"])
        self.assertEqual(cases["M0970"]["allowed_operations"], ["source_annotation"])
        for mcsa_id in ("M0106", "M0107", "M0212", "M0753"):
            self.assertIn(
                "source_scoped_mechanism_draft",
                cases[mcsa_id]["allowed_operations"],
            )
        self.assertFalse(
            any(
                "exact_reaction_instance" in case["allowed_operations"]
                for case in cases.values()
            )
        )

    def test_carrier_context_does_not_promote_p11961_to_carrier_identity(self) -> None:
        case = next(case for case in self.report["cases"] if case["mcsa_id"] == "M0106")
        components = {
            item["component_id"]: item for item in case["representation"]["components"]
        }
        context = components["protein:P11961-context"]
        self.assertEqual(context["identity_scope"], "context_only")
        self.assertIn("not assigned as the lipoyl carrier", context["role"])
        self.assertEqual(
            case["representation"]["tethered_carrier"]["structure_component_ids"],
            [],
        )
        self.assertEqual(
            case["missing_clauses"],
            ["carrier_host_identity", "attachment_site", "structure_localization"],
        )

    def test_fixed_codh_and_nucleotide_coupled_nitrogenase_share_one_contract(self) -> None:
        cases = {case["mcsa_id"]: case for case in self.report["cases"]}
        codh = cases["M0107"]
        nitrogenase = cases["M0212"]
        self.assertEqual(codh["contract_kind"], nitrogenase["contract_kind"])
        self.assertEqual(codh["representation"]["assembly"]["mode"], "fixed_multisubunit")
        self.assertEqual(
            nitrogenase["representation"]["assembly"]["mode"],
            "cycle_coupled_association",
        )
        self.assertEqual(codh["missing_clauses"], [])
        self.assertEqual(nitrogenase["missing_clauses"], ["complete_target_state"])
        transition = nitrogenase["representation"]["state_transitions"][0]
        self.assertEqual(
            (transition["before_state_id"], transition["after_state_id"]),
            ("CHEBI:30616", "CHEBI:456216"),
        )

    def test_hisf_scope_does_not_claim_full_channel_mechanism(self) -> None:
        case = next(case for case in self.report["cases"] if case["mcsa_id"] == "M0753")
        self.assertEqual(case["scope_status"], "source_narrowed")
        self.assertIn("CHEBI:28938", {item["state_id"] for item in case["source_extract"]["state_catalog"]})
        assembly = case["representation"]["assembly"]
        self.assertEqual(assembly["member_component_ids"], ["protein:Q9X0C6"])
        his_h = next(
            item
            for item in case["representation"]["components"]
            if item["component_id"] == "protein-role:HisH-context"
        )
        self.assertEqual(his_h["identity_scope"], "role_only")
        self.assertEqual(case["representation"]["state_transitions"], [])
        self.assertEqual(case["missing_clauses"], ["complete_target_state"])

    def test_topology_and_polymer_instances_abstain_at_the_exact_missing_fields(self) -> None:
        cases = {case["mcsa_id"]: case for case in self.report["cases"]}
        topo = cases["M0064"]
        polymer = cases["M0970"]
        self.assertIn("topology_before", topo["missing_clauses"])
        self.assertIn("topology_after", topo["missing_clauses"])
        self.assertEqual(
            topo["representation"]["polymer_topology"]["reactant_state_id"],
            topo["representation"]["polymer_topology"]["product_state_id"],
        )
        self.assertIn("polymer_product_identity", polymer["missing_clauses"])
        self.assertEqual(
            polymer["representation"]["polymer_topology"]["source_product_placeholder"],
            "X00676",
        )
        self.assertIsNone(
            polymer["representation"]["polymer_topology"]["product_state_id"]
        )

    def test_invented_state_and_source_identity_fail_closed(self) -> None:
        invented_state = copy.deepcopy(self.spec)
        transition = invented_state["cases"][2]["representation"]["state_transitions"][0]
        transition["after_state_id"] = "state:M0107:invented"
        with self.assertRaisesRegex(ValueError, "invents a state"):
            validate_probe_spec(
                invented_state,
                candidate_spec=self.candidate_spec,
                panel_review=self.panel_review,
            )

        invented_identity = copy.deepcopy(self.spec)
        invented_identity["cases"][4]["source_extract"]["uniprot_ids"] = ["Q9XXXXX"]
        with self.assertRaisesRegex(ValueError, "invents or omits M-CSA protein identity"):
            validate_probe_spec(
                invented_identity,
                candidate_spec=self.candidate_spec,
                panel_review=self.panel_review,
            )

    def test_current_v3_limits_are_measured_not_silently_extended(self) -> None:
        compatibility = self.report["v3_compatibility"]
        self.assertEqual(
            compatibility["status"],
            "sidecar_probe_requires_schema_decision_before_kernel_compilation",
        )
        self.assertEqual(
            compatibility["missing_structured_fields"],
            [
                "assembly",
                "components",
                "polymer_topology",
                "state_transitions",
                "tethered_carrier",
            ],
        )
        self.assertEqual(
            compatibility["kernel_evidence"]["atlas10"]["record_schema_versions"],
            ["catalytic-earth.mechanism-record.v3"],
        )
        self.assertEqual(self.report["summary"]["mechanisms_compiled"], 0)

    def test_same_model_review_correlation_is_explicit(self) -> None:
        disclosure = self.report["review_independence"]
        self.assertTrue(disclosure["same_model_agents"])
        self.assertFalse(disclosure["blind_review"])
        self.assertFalse(disclosure["statistical_independence_claimed"])
        self.assertEqual(disclosure["human_reviewers"], 0)
        self.assertFalse(disclosure["domain_expert_review_claimed"])
        self.assertIn("correlated", disclosure["correlation_warning"])


if __name__ == "__main__":
    unittest.main()
