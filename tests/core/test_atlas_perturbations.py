"""Scientific transfer failures for the shared source perturbation relation."""

from copy import deepcopy
import json
import os
from pathlib import Path
import hashlib
import subprocess
import sys
import shutil
from tempfile import TemporaryDirectory
import unittest

from catalytic_earth.atlas_perturbations import (
    SPEC_PATH, REVIEW_PATH, _project_candidate, compare, pointer, project, verify_witnesses,
)


ROOT = Path(__file__).resolve().parents[2]


class PerturbationRelationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads((ROOT / SPEC_PATH).read_text(encoding="utf-8"))
        cls.view = project(ROOT)
        cls.rows = {row["id"]: row for row in cls.view["observations"]}
        cls.comparisons = {row["id"]: row for row in cls.view["comparisons"]}

    def test_background_and_parameter_specific_retention(self):
        turnover = self.comparisons["ra95_2013:RA95.5-5-K210M:kcat"]
        efficiency = self.comparisons["ra95_2013:RA95.5-5-K210M:kcat_over_KM"]
        self.assertTrue(turnover["eligible"])
        self.assertAlmostEqual(turnover["value"], 0.023 / 0.048)
        self.assertEqual(efficiency["value"], 1)
        reduced = self.comparisons["ra95_2013:RA95.5-5-K83M:kcat_over_KM"]
        self.assertAlmostEqual(reduced["value"], 2.3 / 490)
        self.assertIsNone(efficiency["uncertainty"])

    def test_nondetection_is_not_zero_or_a_ratio(self):
        row = self.rows["ra95-kinetics:si-table2:RA95.0-K210M:kcat"]
        self.assertEqual(row["result_kind"], "nondetection")
        self.assertIsNone(row["value"])
        self.assertEqual(row["nondetection"]["source_token"], "nd")
        self.assertFalse(row["nondetection"]["is_zero_rate"])
        self.assertIsNone(row["source_record"]["unavailable_reason"]["numeric_detection_limit"])
        self.assertFalse(row["assay_qualified"])
        comparison = self.comparisons["ra95_2013:RA95.0-K210M:kcat"]
        self.assertFalse(comparison["eligible"])
        self.assertIsNone(comparison["value"])

    def test_conflicting_unit_is_not_silently_repaired(self):
        row = self.rows["ra95-kinetics:si-table2:RA95.5-5-K210M:KM"]
        self.assertEqual(row["result_kind"], "source_conflict")
        self.assertIsNone(row["value"])
        self.assertIsNone(row["unit"])
        self.assertEqual(row["source_parameter"]["source_reported_unit"], "M")
        self.assertFalse(self.comparisons["ra95_2013:RA95.5-5-K210M:KM"]["eligible"])

    def test_source_preference_conflict_blocks_integrated_label(self):
        conflict = self.comparisons["ra95_2013:RA95.5:R-over-S"]
        self.assertFalse(conflict["eligible"])
        self.assertIsNone(conflict["value"])
        self.assertEqual(conflict["source_reported_preference"], "R")
        self.assertEqual(conflict["source_reported_factor"], 3.2)
        initial = self.comparisons["ra95_2013:RA95.0:R-over-S"]
        final = self.comparisons["ra95_2013:RA95.5-8:R-over-S"]
        self.assertEqual(initial["preferred_substrate_id"], "methodol:S")
        self.assertEqual(final["preferred_substrate_id"], "methodol:R")
        self.assertNotEqual(initial["value"], initial["source_reported_factor"])

    def test_tyrosine_square_and_missing_higher_order_controls(self):
        for parameter, expected in [("kcat", 0.021), ("KM", 0.4228571428571429),
                                    ("kcat_over_KM", 0.05029761904761905)]:
            comparison = self.comparisons["ra95_2017:Y51F-Y180F:" + parameter]
            self.assertTrue(comparison["eligible"])
            self.assertAlmostEqual(comparison["value"], expected)
            coverage = comparison["source_evidence"][1]
            self.assertEqual(len(coverage["missing_cells"]), 2)
            self.assertIsNone(coverage["three_way_interaction"])
        triple = self.rows["ra95-tetrad:S1:Y51F/N110S/Y180F:kcat"]
        self.assertGreater(triple["value"], 0)

    def test_ra61_named_background_without_sequence_or_full_cycle_transfer(self):
        result = self.comparisons["ra61_2010:RA61-Y78F-S87A:kcat_over_KM_obs"]
        self.assertTrue(result["eligible"])
        self.assertAlmostEqual(result["value"], 2.6 / 0.49)
        self.assertEqual(result["source_reported_factor"], 5.3)
        row = self.rows[result["roles"]["numerator"]]
        self.assertFalse(row["sequence_identity_available"])
        self.assertEqual(row["endpoint_kind"], "initial_rate_through_aldehyde_formation")
        self.assertEqual(row["parameter"], "kcat_over_KM_obs")
        self.assertIn("later cycle steps not measured", row["reaction_direction"])
        self.assertEqual(result["source_evidence"][2]["product_binding_estimate"]["value"], 26)

    def test_ke59_unassessed_is_not_a_negative_measurement(self):
        result = self.comparisons["ke59_2012:E230-matched-perturbation"]
        self.assertEqual(result["result_kind"], "unassessed")
        self.assertFalse(result["eligible"])
        self.assertEqual(result["roles"], {})
        self.assertIsNone(result["matched_control"])
        self.assertIsNone(result["observed_value"])
        self.assertIsNone(result["unit"])
        self.assertIn("No matched perturbation comparison was evaluated", result["interpretation_limit"])
        self.assertIsNone(result["source_evidence"][0]["matched_E230_perturbation_rows_in_uninspected_SI"])
        self.assertEqual(self.rows["ke59-pH:Table2:R4-5/11B:apparent_pKa_from_kcat"]["value"], 5.5)

    def test_cross_assay_background_study_substrate_and_endpoint_swaps_abstain(self):
        request = deepcopy(self.comparisons["ra95_2013:RA95.5-5-K210M:kcat_over_KM"])
        swaps = [
            ("ra95-kinetics:main-table1:RA95.5-5:kcat_over_KM", "mismatched_assay_id"),
            ("ra95-kinetics:si-table2:RA95.5:kcat_over_KM", "mismatched_background_id"),
            ("ra95-tetrad:S1:RA95.5-8F:kcat_over_KM", "mismatched_study_id"),
            ("ra95-stereo:RA95.5-5:R:kcat_over_KM", "mismatched_substrate_id"),
            ("ra61-water:Table4:RA61:kcat_over_KM_obs", "mismatched_endpoint_kind"),
        ]
        for denominator, reason in swaps:
            with self.subTest(denominator=denominator):
                request["roles"]["denominator"] = denominator
                result = compare(self.rows, request)
                self.assertFalse(result["eligible"])
                self.assertIsNone(result["value"])
                self.assertIn(reason, result["reasons"])

    def test_incomplete_square_cannot_be_replaced_with_triple(self):
        request = deepcopy(self.comparisons["ra95_2017:Y51F-Y180F:kcat"])
        request["roles"]["double"] = "ra95-tetrad:S1:Y51F/N110S/Y180F:kcat"
        result = compare(self.rows, request)
        self.assertFalse(result["eligible"])
        self.assertIn("incomplete_or_mismatched_perturbation_square", result["reasons"])

    def test_source_hash_and_perturbation_provider_drift_fail_closed(self):
        spec = deepcopy(self.spec)
        spec["sources"]["ra61"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "source hash differs"):
            _project_candidate(ROOT, spec)
        spec = deepcopy(self.spec)
        spec["constructs"]["ra61_2010:RA61-Y78F"]["perturbation"] = ["Y78A"]
        with self.assertRaisesRegex(ValueError, "perturbation differs from source"):
            _project_candidate(ROOT, spec)

    def test_sequence_provider_cannot_be_borrowed_from_nearby_construct(self):
        spec = deepcopy(self.spec)
        spec["constructs"]["ra95_2013:RA95.5-5-K210M"]["sequence_provider"] = {
            "source": "ra95f", "pointer": "/constructs/2"}
        with self.assertRaisesRegex(ValueError, "sequence provider construct differs"):
            _project_candidate(ROOT, spec)

    def test_unknown_status_and_nondetection_zero_are_rejected(self):
        spec = deepcopy(self.spec)
        spec["panels"][0]["parameters"][0]["status_kinds"][
            "unavailable_no_activity_above_background_detected"] = "numeric"
        with self.assertRaisesRegex(ValueError, "numeric result requires"):
            _project_candidate(ROOT, spec)
        self.assertEqual(pointer({"a/b": {"~": 2}}, "/a~1b/~0"), 2)

    def test_unresolved_statistic_preserves_printed_error_magnitude(self):
        for row_id, error, kind in [
            ("si-table2:RA95.0:kcat", 0.00003, "unresolved_for_unmarked_row"),
            ("si-table2:RA95.0-T83K/K210M:kcat", 0.00006, "unresolved_for_unmarked_row"),
            ("si-table2:RA95.0:KM", 120, "unresolved_for_unmarked_row"),
        ]:
            uncertainty = self.rows["ra95-kinetics:" + row_id]["uncertainty"]
            self.assertEqual(uncertainty["value"], error)
            self.assertEqual(uncertainty["kind"], kind)
        self.assertEqual(self.rows["ra95-kinetics:si-table2:RA95.0:KM"]["uncertainty"]["unit"], "M")

    def test_assay_and_parameter_provider_swaps_are_rejected(self):
        spec = deepcopy(self.spec)
        spec["assays"]["ra95_2013:racemic_methodol_fluorescence"]["provider"]["pointer"] = "/assays/0"
        with self.assertRaisesRegex(ValueError, "assay provider identity differs"):
            _project_candidate(ROOT, spec)
        spec = deepcopy(self.spec)
        spec["panels"][2]["parameters"][0]["pointer"] = "/KM"
        with self.assertRaisesRegex(ValueError, "parameter source field differs"):
            _project_candidate(ROOT, spec)

    def test_unbound_context_and_evidence_free_assessment_are_rejected(self):
        spec = deepcopy(self.spec)
        spec["comparisons"][-1]["context_observations"].append("missing-row")
        with self.assertRaisesRegex(ValueError, "unbound or cross-study context"):
            _project_candidate(ROOT, spec)
        spec = deepcopy(self.spec)
        spec["comparisons"][-1]["evidence"] = []
        with self.assertRaisesRegex(ValueError, "requires bound source evidence"):
            _project_candidate(ROOT, spec)

    def test_boolean_uncertainty_and_unbound_witness_hash_are_rejected(self):
        spec = deepcopy(self.spec)
        spec["panels"][2]["parameters"][0]["uncertainty"]["value"] = {"literal": True}
        with self.assertRaisesRegex(ValueError, "uncertainty must be finite"):
            _project_candidate(ROOT, spec)
        spec = deepcopy(self.spec)
        spec["panels"][2]["parameters"][0]["uncertainty"]["kind"] = {"literal": "not_reported"}
        with self.assertRaisesRegex(ValueError, "reported uncertainty requires"):
            _project_candidate(ROOT, spec)
        spec = deepcopy(self.spec)
        spec["panels"][2]["parameters"][0]["uncertainty"]["unreported_is_zero"] = {"literal": True}
        with self.assertRaisesRegex(ValueError, "unreported uncertainty is not zero"):
            _project_candidate(ROOT, spec)
        spec = deepcopy(self.spec)
        spec["source_witnesses"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "source witness hash differs"):
            _project_candidate(ROOT, spec)

    def test_local_primary_witness_tampering_is_detected(self):
        with TemporaryDirectory() as directory:
            common = Path(directory)
            raw = b"source witness bytes"
            path = common / "witness.bin"
            path.write_bytes(raw)
            view = {"source_witnesses": [{"git_common_dir_relative_path": "witness.bin",
                     "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}]}
            self.assertEqual(verify_witnesses(common, view)["verified_files"], 1)
            path.write_bytes(b"changed witness body")
            with self.assertRaisesRegex(ValueError, "local source witness bytes differ"):
                verify_witnesses(common, view)

    def test_filtered_query_keeps_controls_and_only_returned_memberships(self):
        completed = subprocess.run([sys.executable, str(ROOT / "scripts/query_atlas_perturbations.py"),
                                    "--comparison", "ra95_2017:Y51F-Y180F:kcat"],
                                   cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8")
        view = json.loads(completed.stdout)
        comparison = view["comparisons"][0]
        self.assertEqual({row["id"] for row in view["observations"]}, set(comparison["roles"].values()))
        for row in view["observations"]:
            self.assertEqual({item["comparison_id"] for item in row["comparison_memberships"]}, {comparison["id"]})

    def test_curated_mapping_edits_require_renewed_source_review(self):
        for field, value in [("reaction_direction", "forward aldol synthesis"),
                             ("endpoint_kind", "arbitrary"), ("qualified", False)]:
            spec = deepcopy(self.spec)
            spec["assays"]["ra95_2013:racemic_methodol_fluorescence"][field] = value
            with self.assertRaisesRegex(ValueError, "candidate differs from reviewed"):
                project(ROOT, spec)
        spec = deepcopy(self.spec)
        spec["panels"][0]["fields"]["substrate_id"] = {"literal": "methodol:R"}
        with self.assertRaisesRegex(ValueError, "candidate differs from reviewed"):
            project(ROOT, spec)
        spec = deepcopy(self.spec)
        spec["panels"][0]["parameters"][0]["status_kinds"][
            "unavailable_no_activity_above_background_detected"] = "source_conflict"
        with self.assertRaisesRegex(ValueError, "candidate differs from reviewed"):
            project(ROOT, spec)
        spec = deepcopy(self.spec)
        spec["panels"][1]["row_checks"] = []
        with self.assertRaisesRegex(ValueError, "candidate differs from reviewed"):
            project(ROOT, spec)
        candidate = _project_candidate(ROOT, self.spec)
        self.assertIn("internal_unreviewed_candidate", candidate["review_status"])

    def test_public_query_rejects_changed_consumer_or_projection_bytes(self):
        review = json.loads((ROOT / REVIEW_PATH).read_text(encoding="utf-8"))
        for changed in [SPEC_PATH, "src/catalytic_earth/atlas_perturbations.py"]:
            with TemporaryDirectory() as directory:
                root = Path(directory)
                for relative in [REVIEW_PATH, *review["reviewed_bindings"]]:
                    target = root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(ROOT / relative, target)
                target = root / changed
                target.write_bytes(target.read_bytes() + b"\n")
                with self.assertRaisesRegex(ValueError, "reviewed binding differs"):
                    project(root)

    def test_forward_synthesis_keeps_reaction_sides_and_distinct_endpoints(self):
        conversion = self.rows["ra95-synthesis-conversion:synthesis-8F-conversion:conversion"]
        isolation = self.rows["ra95-synthesis-isolation:synthesis-8F-isolation:isolated_yield"]
        self.assertEqual(conversion["value"], 67)
        self.assertEqual(isolation["value"], 60.1)
        self.assertNotEqual(conversion["endpoint_kind"], isolation["endpoint_kind"])
        reaction = conversion["reaction_context"]["source_record"]
        self.assertEqual({p["participant_id"] for p in reaction["participants"] if p["side"] == "reactant"},
                         {"2a", "acetone"})
        self.assertEqual({p["participant_id"] for p in reaction["participants"] if p["side"] == "product"}, {"1a"})
        product = next(p for p in reaction["participants"] if p["side"] == "product")
        self.assertIsNone(product["source_reported_major_configuration"])
        cleavage = self.rows["ra95-tetrad:S1:RA95.5-8F:kcat_over_KM"]
        self.assertIsNone(cleavage["reaction_context"])
        request = {"id": "invalid-forward-cleavage-transfer", "study_id": "ra95_2017", "operation": "ratio",
                   "roles": {"numerator": conversion["id"], "denominator": cleavage["id"]}}
        result = compare(self.rows, request)
        self.assertFalse(result["eligible"])
        self.assertIn("mismatched_reaction_direction", result["reasons"])
        self.assertIn("mismatched_reaction_id", result["reasons"])

    def test_synthesis_amount_and_stereo_conflicts_remain_unrepaired(self):
        source = json.loads((ROOT / self.spec["sources"]["ra95syn"]["path"]).read_text(encoding="utf-8"))
        amount, retention = source["source_conflicts"]
        self.assertEqual(amount["printed"]["amount_umol"], 130)
        self.assertEqual(amount["project_arithmetic"]["amount_umol"], 100)
        self.assertEqual(source["isolation_observations"][0]["isolated_yield"]["value"], 60.1)
        self.assertEqual(retention["methods_p11_retention_min"], {"R": 6.0, "S": 7.9})
        self.assertEqual(retention["figure_S12_retention_min"], {"S": 6.0, "R": 7.9})
        stereo = self.rows["ra95-synthesis-composition:synthesis-8F-composition:source_reported_R_product_parts"]["source_record"]
        self.assertEqual(stereo["ee_report"]["source_comparator"], ">")
        self.assertEqual(stereo["ee_report"]["threshold"], 98.4)
        self.assertFalse(stereo["ee_from_printed_ratio"]["replaces_source_bound"])
        self.assertIsNone(stereo["product"]["normalized_retention_time_assignment"])

    def test_precursor_conversion_cannot_inherit_altered_or_8f_stereo(self):
        control = self.rows["ra95-synthesis-conversion:synthesis-8-conversion:conversion"]
        altered = self.rows["ra95-synthesis-composition:synthesis-8-altered-composition:source_reported_R_product_parts"]
        self.assertEqual(control["value"], 0.7)
        self.assertIsNone(control["source_record"]["product"]["source_reported_major_configuration"])
        self.assertNotEqual(control["assay_id"], altered["assay_id"])
        self.assertFalse(altered["assay_qualified"])
        self.assertEqual(altered["source_record"]["ee_report"]["value"], 44)
        self.assertNotIn("optical_rotation", altered["source_record"])
        self.assertEqual(altered["source_record"]["product"]["configuration_status"],
                         "source_caption_assignment_for_altered_precursor_conditions")

    def test_reaction_product_as_input_and_wrong_direction_are_rejected(self):
        spec = deepcopy(self.spec)
        panel = next(p for p in spec["panels"] if p["source"] == "ra95syn")
        panel["fields"]["substrate_id"] = {"literal": "methodol:R"}
        with self.assertRaisesRegex(ValueError, "reaction reactants differ"):
            _project_candidate(ROOT, spec)
        spec = deepcopy(self.spec)
        spec["substrates"]["aldol-inputs:acetone+6-methoxy-2-naphthaldehyde"]["participant_ids"] = ["1a", "acetone"]
        with self.assertRaisesRegex(ValueError, "substrate participant IDs differ"):
            _project_candidate(ROOT, spec)
        spec = deepcopy(self.spec)
        spec["assays"]["ra95_2017:methodol-synthesis-3h-HPLC"]["reaction_direction"] = "retro-aldol cleavage"
        with self.assertRaisesRegex(ValueError, "reaction differs from source assay"):
            _project_candidate(ROOT, spec)

    def test_reaction_requires_both_sides_and_participant_roles(self):
        for defect in ("missing_product", "missing_role"):
            with self.subTest(defect=defect), TemporaryDirectory() as directory:
                root = Path(directory)
                spec = deepcopy(self.spec)
                for binding in spec["sources"].values():
                    target = root / binding["path"]
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(ROOT / binding["path"], target)
                binding = spec["sources"]["ra95syn"]
                path = root / binding["path"]
                source = json.loads(path.read_text(encoding="utf-8"))
                participants = source["reaction"]["participants"]
                if defect == "missing_product":
                    participants[:] = [p for p in participants if p["side"] != "product"]
                else:
                    participants[0].pop("role")
                raw = (json.dumps(source) + "\n").encode("utf-8")
                path.write_bytes(raw)
                binding["sha256"] = hashlib.sha256(raw).hexdigest()
                with self.assertRaisesRegex(ValueError, "reactant and product sides|source name and role"):
                    _project_candidate(root, spec)

    def test_reported_activity_factors_cannot_become_matched_mutant_kinetics(self):
        question = self.comparisons["diels_alder_2010:qualified-mutant-parameter"]
        self.assertFalse(question["eligible"])
        self.assertTrue(question["reported_mutation_effects_assessed"])
        self.assertEqual(question["roles"], {})
        for mutation in ("Q195E", "Y121F"):
            factor_id = f"da-reported-effects:P9:{mutation}:source_reported_activity_reduction_factor"
            factor = self.rows[factor_id]
            self.assertFalse(factor["assay_qualified"])
            self.assertIsNone(factor["source_record"]["numeric_mutant_value"])
            self.assertIsNone(factor["source_record"]["numeric_parent_value"])
            for parameter in ("kcat", "KM_diene", "KM_dienophile"):
                request = {"id": "invalid-factor-as-mutant-parameter", "study_id": "diels_alder_2010",
                           "operation": "ratio", "roles": {"numerator": factor_id,
                           "denominator": f"da-kinetics:Table1:DA_20_10:{parameter}"}}
                result = compare(self.rows, request)
                self.assertFalse(result["eligible"])
                self.assertIn("mismatched_parameter", result["reasons"])
                self.assertIn("mismatched_assay_id", result["reasons"])
                self.assertIn(f"unresolved_assay:{factor_id}", result["reasons"])
                self.assertIsNone(result["value"])

    def test_tkt_reporter_unavailability_nmr_nondetection_and_turnover_differ(self):
        result = self.comparisons["tkt_2019:E366Q:kcat"]
        self.assertTrue(result["eligible"])
        self.assertAlmostEqual(result["value"], 0.012 / 2.79)
        self.assertIsNone(result["uncertainty"])
        rate = self.rows["tkt-steady_state:E366Q:kcat"]
        reporter = self.rows["tkt-stopped_flow:E366Q:k_forward"]
        nmr = self.rows["tkt-nmr:E366Q:covalent_intermediate_accumulation"]
        reference = self.rows["tkt-nmr:wild_type:covalent_intermediate_accumulation"]
        self.assertEqual(rate["uncertainty"]["value"], 0.001)
        self.assertEqual(reporter["result_kind"], "unavailable")
        self.assertIsNone(reporter["value"])
        self.assertIsNone(reporter["nondetection"])
        self.assertEqual(reporter["unavailability"]["source_token"], "n.a.")
        self.assertIn("325 nm", reporter["unavailability"]["reason"])
        self.assertFalse(reporter["unavailability"]["is_zero_rate"])
        self.assertEqual(nmr["result_kind"], "nondetection")
        self.assertIsNone(nmr["nondetection"]["numeric_detection_limit"])
        self.assertFalse(nmr["nondetection"]["is_zero_rate"])
        self.assertEqual(reference["result_kind"], "qualitative")
        self.assertEqual(reference["qualitative_result"]["source_token"], "F6P-ThDP accumulated")
        self.assertIn("not_verbatim", reference["qualitative_result"]["wording_basis"])
        self.assertIsNone(reference["value"])
        self.assertFalse(self.comparisons["tkt_2019:E366Q:k_forward"]["eligible"])
        self.assertFalse(self.comparisons["tkt_2019:E366Q:NMR-accumulation-ratio"]["eligible"])
        self.assertEqual(self.view["assays"][rate["assay_id"]]["source_record"]["conditions"]["temperature_celsius"], 20)
        self.assertEqual(self.view["assays"][reporter["assay_id"]]["source_record"]["conditions"]["temperature_celsius"], 4)
        self.assertNotEqual(rate["substrate_id"], reporter["substrate_id"])
        construct = self.view["constructs"][rate["construct_id"]]
        self.assertIsNone(construct["sequence"])
        self.assertFalse(construct["assay_specimen_sequence_verified"])

    def test_tkt_cross_endpoint_and_wrong_mutant_control_ratios_abstain(self):
        for denominator, reasons in [
            ("tkt-stopped_flow:wild_type:k_forward", ["mismatched_assay_id", "mismatched_substrate_id", "mismatched_parameter", "mismatched_endpoint_kind"]),
            ("tkt-nmr:wild_type:covalent_intermediate_accumulation", ["mismatched_assay_id", "mismatched_parameter"]),
            ("tkt-steady_state:E160Q:kcat", ["control_is_not_declared_perturbation_background"]),
        ]:
            with self.subTest(denominator=denominator):
                request = deepcopy(self.comparisons["tkt_2019:E366Q:kcat"])
                request["roles"]["denominator"] = denominator
                result = compare(self.rows, request)
                self.assertFalse(result["eligible"])
                self.assertIsNone(result["value"])
                for reason in reasons:
                    self.assertIn(reason, result["reasons"])

    def test_tkt_missing_reporter_cannot_be_coerced_to_zero_or_lose_reason(self):
        for defect in ("numeric", "zero_semantics", "missing_reason"):
            spec = deepcopy(self.spec)
            parameter = next(p for p in spec["panels"] if p["id"] == "tkt-stopped_flow")["parameters"][0]
            if defect == "numeric":
                parameter["status_kinds"]["not_applicable_reporter_absent"] = "numeric"
                expected = "numeric result requires"
            elif defect == "zero_semantics":
                parameter["unavailability"]["is_zero_rate"] = {"literal": True}
                expected = "unavailable result is not a zero rate"
            else:
                parameter["unavailability"]["reason"] = {"literal": None}
                expected = "unavailable result requires"
            with self.subTest(defect=defect), self.assertRaisesRegex(ValueError, expected):
                _project_candidate(ROOT, spec)
        spec = deepcopy(self.spec)
        parameter = next(p for p in spec["panels"] if p["id"] == "tkt-stopped_flow")["parameters"][0]
        parameter["pointer"] = "/stopped_flow/k_max_ES"
        with self.assertRaisesRegex(ValueError, "parameter source field differs"):
            _project_candidate(ROOT, spec)

    def test_tkt_unselected_bounds_and_missing_panel_arms_remain_context(self):
        source = self.rows["tkt-stopped_flow:wild_type:k_forward"]["source_record"]
        self.assertEqual(source["stopped_flow"]["k_max_ES"]["status"], "lower_bound")
        self.assertEqual(source["stopped_flow"]["k_max_ES"]["comparator"], ">")
        for variant in ("T382E", "T382Q"):
            self.assertNotIn(f"tkt-nmr:{variant}:covalent_intermediate_accumulation", self.rows)
            result = self.comparisons[f"tkt_2019:{variant}:kcat"]
            self.assertFalse(any(r.startswith("tkt-nmr:") for r in result["context_observations"]))
            self.assertIn({"source": "tktf", "pointer": "/reused_accumulation_context/T382E_T382Q_status"}, result["evidence"])
        t382q = self.rows["tkt-stopped_flow:T382Q:k_forward"]
        self.assertIn("pKa cell", t382q["unavailability"]["reason_basis"])
        nmr_rows = [r for r in self.view["observations"] if r["id"].startswith("tkt-nmr:")]
        self.assertEqual({r["source_row_id"] for r in nmr_rows},
                         {"wild_type", "E160Q", "E160A", "E366Q", "E165Q"})
        for result in self.view["comparisons"]:
            if result["study_id"] == "tkt_2019" and ":E366Q:" not in result["id"]:
                self.assertNotIn({"source": "tkta", "pointer": "/source_reviewed_context/relation"}, result["evidence"])

    def test_tkt_legacy_identity_adapter_resolves_original_source_records(self):
        adapter = json.loads((ROOT / self.spec["sources"]["tkti"]["path"]).read_text(encoding="utf-8"))
        providers = {}
        for binding in adapter["source_bindings"]:
            raw = (ROOT / binding["path"]).read_bytes().replace(b"\r\n", b"\n")
            self.assertEqual(hashlib.sha256(raw).hexdigest(), binding["sha256"])
            providers[binding["path"]] = json.loads(raw)
        for construct in adapter["constructs"]:
            ref = construct["source_provider"]
            document = providers[ref["path"]]
            row = pointer(document, ref["json_pointer"])
            self.assertEqual(construct["construct_id"], row[construct["source_identity_field"]])
            self.assertEqual(construct["source_row_label"], row["source_row_label"])
            self.assertEqual(construct["background_construct_id"], document["derived_comparisons"]["reference_variant"])
            self.assertIsNone(construct["sequence"])
            self.assertIsNone(construct["sequence_sha256"])
            self.assertFalse(construct["assay_specimen_sequence_verified"])
        assay = adapter["assays"][0]
        ref = assay["source_provider"]
        original = pointer(providers[ref["path"]], ref["json_pointer"])
        for field in ("method", "endpoint", "typical_method_conditions", "conditions_limit", "replication"):
            self.assertEqual(assay[field], original[field])

    def test_tkt_filtered_turnover_relation_keeps_separate_contexts(self):
        completed = subprocess.run([sys.executable, str(ROOT / "scripts/query_atlas_perturbations.py"),
                                    "--comparison", "tkt_2019:E366Q:kcat"],
                                   capture_output=True, text=True, encoding="utf-8", check=True,
                                   env={**os.environ, "PYTHONIOENCODING": "cp1252"})
        view = json.loads(completed.stdout)
        self.assertEqual(len(view["comparisons"]), 1)
        comparison = view["comparisons"][0]
        rows = {r["id"]: r for r in view["observations"]}
        self.assertEqual(set(rows), set(comparison["roles"].values()) | set(comparison["context_observations"]))
        self.assertEqual(len(rows), 6)
        self.assertEqual({rows[r]["parameter"] for r in comparison["roles"].values()}, {"kcat"})
        self.assertEqual({rows[r]["result_kind"] for r in comparison["context_observations"]},
                         {"numeric", "unavailable", "qualitative", "nondetection"})
        self.assertEqual(view["evidence_context"], self.view["evidence_context"])
        self.assertEqual(view["constructs"], self.view["constructs"])

    def test_diels_alder_substrate_markers_and_product_contexts_do_not_transfer(self):
        for parameter, wrong_participant in (("KM_diene", "2"), ("KM_dienophile", "1")):
            spec = deepcopy(self.spec)
            spec["parameter_contracts"][parameter]["source_markers"]["participant_id"] = [wrong_participant]
            with self.assertRaisesRegex(ValueError, "parameter source marker differs"):
                _project_candidate(ROOT, spec)
        source = json.loads((ROOT / self.spec["sources"]["da2010"]["path"]).read_text(encoding="utf-8"))
        conversion = source["product_context"]["conversion"]
        stereo = source["product_context"]["stereochemical_composition"]
        self.assertNotEqual(conversion["context_id"], stereo["context_id"])
        for outcome in (conversion, stereo):
            self.assertIsNone(outcome["value"])
            self.assertEqual(outcome["source_comparator"], ">")
        self.assertIsNone(conversion["product_configuration"])
        self.assertFalse(stereo["matched_comparison_eligible"])
        product = next(p for p in source["reaction"]["participants"] if p["side"] == "product")
        self.assertIsNone(product["configuration"])
        self.assertIsNone(source["reaction"]["atom_map"])
        self.assertIsNone(stereo["ee"])


if __name__ == "__main__":
    unittest.main()
