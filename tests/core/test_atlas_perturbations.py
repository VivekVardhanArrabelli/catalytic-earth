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
    SPEC_PATH, REVIEW_PATH, _connectivity_relation, _model_link, _project_candidate, compare, pointer, project, verify_witnesses,
)


ROOT = Path(__file__).resolve().parents[2]


class PerturbationRelationTests(unittest.TestCase):
    def test_calmodulin_controls_keep_domain_treatment_and_analogue_boundaries(self):
        rows = {row["source_row_id"]: row for row in self.view["observations"]
                if row["study_id"] == "calmodulin_2015"}
        self.assertEqual(set(rows), {"CaM", "cCaM", "CaMWN", "Ac-CaMWN", "CaM-L105K"})
        for name, value, error in (("CaM", .006, .001), ("cCaM", .007, .002),
                                   ("CaMWN", .005, .001), ("Ac-CaMWN", .004, .002),
                                   ("CaM-L105K", .038, .002)):
            with self.subTest(construct=name):
                self.assertEqual((rows[name]["value"], rows[name]["uncertainty"]["value"]),
                                 (value, error))
                self.assertEqual(rows[name]["uncertainty"]["kind"],
                                 "source_reported_plus_minus_statistic_unspecified")
        controls = next(c for c in self.spec["comparisons"]
                        if c["id"] == "calmodulin_2015:CaMWN:over-cCaM")
        self.assertAlmostEqual(compare(self.rows, controls)["value"], .005 / .007)
        wrong = deepcopy(controls)
        wrong["roles"]["denominator"] = rows["CaM"]["id"]
        result = compare(self.rows, wrong)
        self.assertFalse(result["eligible"])
        self.assertIn("mismatched_background_id", result["reasons"])
        # The terminal chemical treatment is observed, but is not a genetic ratio.
        self.assertFalse(any(rows["Ac-CaMWN"]["id"] in c["roles"].values()
                             for c in self.spec["comparisons"]))
        acetylated = self.view["constructs"]["calmodulin_2015:Ac-CaMWN"]["source_record"]
        self.assertNotIn("N-terminal acetylation", acetylated["substitutions"])
        self.assertIn("N-terminal acetylation", acetylated["perturbations"])
        self.assertEqual(acetylated["preparation_parent"], "CaMWN")
        self.assertEqual(acetylated["domain_scope"], "C-terminal domain")
        request = next(c for c in self.view["comparisons"]
                       if c["id"] == "calmodulin_2015:nucleophile-control-context")
        self.assertIn(rows["Ac-CaMWN"]["id"], request["context_observations"])
        evidence = request["source_evidence"]
        spectral = next(e for e in evidence if isinstance(e, dict) and
                        e.get("context_id") == "calmodulin_2015:diketone-spectral-control")
        calcium = next(e for e in evidence if isinstance(e, dict) and
                       e.get("context_id") == "calmodulin_2015:calcium-dependence")
        self.assertEqual(spectral["construct_ids"], ["CaM", "CaM-L105K"])
        self.assertIsNone(spectral["bond_order"])
        self.assertFalse(spectral["direct_covalent_attachment_observed"])
        self.assertIsNone(calcium["calcium_free_rate"])
        self.assertFalse(calcium["direct_catalytic_metal_role_established"])

    def ra61_model_relation(self, context=None, link=None):
        if link is None:
            link = deepcopy(next(item for item in self.spec["model_links"]
                                 if item["id"] == "ra61_2010:RA61:aldehyde_reporter_path"))
        return self.model_relation(context, link)

    def test_ra61_initial_rate_stops_at_reporter_product_without_arrow_rates(self):
        result = self.ra61_model_relation()
        fit = result["fit_models"][0]
        self.assertEqual(fit["phase_transition_ids"], ["source_step1", "source_step2", "source_step3"])
        self.assertEqual(fit["measurement_boundary"]["to_state"], "enamine_and_aldehyde")
        self.assertEqual(fit["resolved_parameters"]["k_cat/K_M"],
                         self.rows["ra61-water:Table4:RA61:kcat_over_KM_obs"]["source_parameter"])
        transitions = {item["transition_id"]: item for item in result["transitions"]}
        self.assertEqual(transitions["product_sequestration"]["from_state"], "free_enzyme_and_products")
        self.assertNotEqual(transitions["product_sequestration"]["to_state"], "substrate_iminium")
        self.assertFalse(set(fit["transition_ids"]) & {"source_step4", "source_step5", "product_sequestration"})
        for transition in transitions.values():
            self.assertEqual(transition["resolved_parameters"], {"forward": None, "reverse": None})
        self.assertIsNone(result["arrangement"])
        self.assertIsNone(result["source_context"]["residue_scope"]["numbered_product_attachment_site"])

    def test_ra61_initial_fit_rejects_late_path_hybrid_and_microscopic_transfers(self):
        original = self.ra61_model_relation()["source_context"]
        for name in ("extend-phase", "extra-covered-step", "wrong-boundary", "missing-boundary",
                     "saturated-role", "hybrid-fit", "arrow-rate"):
            with self.subTest(name=name):
                context = deepcopy(original)
                fit = context["source_model"]["fit_models"][0]
                if name in {"extend-phase", "extra-covered-step"}:
                    context["source_model"]["transitions"][3]["assay_binding"] = deepcopy(fit["assay_binding"])
                    fit["transition_ids"].append("source_step4")
                    if name == "extend-phase":
                        fit["phase_transition_ids"].append("source_step4")
                elif name == "wrong-boundary":
                    fit["measurement_boundary"]["to_state"] = "product_schiff_base"
                elif name == "missing-boundary":
                    fit.pop("measurement_boundary")
                elif name == "saturated-role":
                    fit["parameter_bindings"]["k_cat/K_M"]["role"] = "saturated_multistep_rate"
                elif name == "hybrid-fit":
                    fit["parameter_bindings"]["kobs"] = {
                        "binding": {"provider": "component_evidence", "pointer": "/observations/7"},
                        "role": "observed_second_order_initial_rate", "unit": "M^-1 s^-1"}
                else:
                    transition = context["source_model"]["transitions"][2]
                    transition["parameter_slots"]["forward"] = {
                        "status": "bound_source_parameter", "is_zero": False,
                        "binding": deepcopy(fit["parameter_bindings"]["k_cat/K_M"]["binding"])}
                    transition.update(parameter_units={"forward": "M^-1 s^-1"},
                                      parameter_roles={"forward": "second_order_association"})
                with self.assertRaises(ValueError):
                    self.ra61_model_relation(context)

    def test_ra61_model_query_preserves_conditional_binding_evidence_and_parent_scope(self):
        view = json.loads(subprocess.check_output([
            sys.executable, str(ROOT / "scripts/query_atlas_perturbations.py"),
            "--model-link", "ra61_2010:RA61:aldehyde_reporter_path"], text=True))
        self.assertEqual([row["id"] for row in view["observations"]],
                         ["ra61-water:Table4:RA61:kcat_over_KM_obs"])
        self.assertEqual(view["comparisons"], [])
        self.assertEqual(view["state_links"], [])
        self.assertEqual(len(view["model_links"]), 1)
        source = json.loads((ROOT / self.spec["sources"]["ra61"]["path"]).read_text())
        self.assertIn(source["initial_rate_boundary"], view["evidence_context"]["ra61"])
        self.assertEqual(view["model_links"][0]["context_evidence"][0]["evidence"],
                         source["initial_rate_boundary"])
        # An existing same-unit mutant endpoint cannot replace the named parent.
        context = self.ra61_model_relation()["source_context"]
        link = deepcopy(view["model_links"][0])
        replacement = "ra61-water:Table4:RA61-Y78F:kcat_over_KM_obs"
        link["observation_ids"] = [replacement]
        context["endpoint_relations"][0]["observation_id"] = replacement
        with self.assertRaisesRegex(ValueError, "construct differs"):
            self.ra61_model_relation(context, link)

    def test_model_context_requires_resolved_objects_and_explicit_branch_semantics(self):
        original = self.ra61_model_relation()["source_context"]
        for name in ("bare-affinity", "unknown-context-transition", "unknown-context-fit",
                     "duplicate-context", "mixed-branch-declarations", "mixed-state-identity"):
            with self.subTest(name=name):
                context = deepcopy(original)
                binding = context["context_evidence_bindings"][0]
                if name == "bare-affinity":
                    binding["binding"]["pointer"] += "/product_binding_estimate/value"
                elif name == "unknown-context-transition":
                    binding["transition_ids"] = ["missing"]
                elif name == "unknown-context-fit":
                    binding["fit_ids"] = ["missing"]
                elif name == "duplicate-context":
                    context["context_evidence_bindings"].append(deepcopy(binding))
                elif name == "mixed-branch-declarations":
                    context["ligand_bindings"] = deepcopy(context["reaction_branch_bindings"])
                else:
                    context["source_model"]["states"][-1]["ligand_id"] = "full_naphthyl"
                with self.assertRaises(ValueError):
                    self.ra61_model_relation(context)

    def pox_model_relation(self, context=None, link=None):
        if link is None:
            link = deepcopy(next(item for item in self.spec["model_links"]
                                 if item["id"] == "pox_2019:wild_type:MAP_pyruvate_models"))
        return self.model_relation(context, link)

    def test_pox_model_keeps_multistep_reporter_fit_off_individual_arrows(self):
        result = self.pox_model_relation()
        transitions = {item["transition_id"]: item for item in result["transitions"]}
        binding = transitions["map_binding"]
        self.assertEqual(binding["resolved_parameters"]["forward"]["unit"], "mM^-1 s^-1")
        self.assertEqual(binding["resolved_parameters"]["reverse"]["unit"], "s^-1")
        for key in ("pyruvate_binding", "pyruvate_conjugate_formation", "pyruvate_processing"):
            self.assertEqual(transitions[key]["resolved_parameters"], {"forward": None, "reverse": None})
        fit = next(item for item in result["fit_models"] if item["fit_id"] == "pyruvate_FAD_response")
        self.assertEqual(fit["phase_transition_ids"], ["pyruvate_conjugate_formation", "pyruvate_processing"])
        self.assertEqual(fit["resolved_parameters"]["k_app_max"]["value"], 136)
        self.assertEqual(fit["resolved_parameters"]["K_0.5"]["value"], 3.4)
        self.assertEqual(fit["assay"]["conditions"]["wavelength_nm"], 457)
        self.assertIsNone(fit["assay"]["conditions"]["pH"])
        self.assertIsNone(result["arrangement"])
        self.assertEqual(result["existing_state_observation_relations"], [])

    def test_pox_model_rejects_ligand_fit_and_missing_structure_transfers(self):
        original = self.pox_model_relation()["source_context"]
        cases = [
            ("MAP-to-pyruvate-state", lambda c: c["source_model"]["transitions"][0].update(to_state="pyruvate_conjugate")),
            ("wrong-ligand", lambda c: c["source_model"]["fit_models"][1].update(ligand_id="pox:MAP")),
            ("missing-ligand-binding", lambda c: c.pop("ligand_bindings")),
            ("wrong-source-ligand", lambda c: c["ligand_bindings"]["pox:MAP"].update(source_name="pyruvate")),
            ("wrong-assay", lambda c: c["endpoint_relations"][3].update(assay_pointer="/assays/1")),
            ("one-arrow-phase", lambda c: c["source_model"]["fit_models"][1].update(phase_transition_ids=["pyruvate_processing"])),
            ("reversed-phase", lambda c: c["source_model"]["fit_models"][1]["phase_transition_ids"].reverse()),
            ("unknown-phase", lambda c: c["source_model"]["fit_models"][1]["phase_transition_ids"].append("missing")),
            ("mixed-assay-fit", lambda c: c["source_model"]["fit_models"][1]["transition_ids"].append("map_binding")),
            ("wrong-fit-kind", lambda c: c["source_model"]["fit_models"][1].update(kind="two_state_equilibrium")),
            ("wrong-directional-unit", lambda c: c["source_model"]["transitions"][0]["parameter_units"].update(forward="s^-1")),
            ("wrong-directional-role", lambda c: c["source_model"]["transitions"][0]["parameter_roles"].update(forward="first_order_dissociation")),
            ("missing-directional-roles", lambda c: c["source_model"]["transitions"][0].pop("parameter_roles")),
            ("missing-directional-units", lambda c: c["source_model"]["transitions"][0].pop("parameter_units")),
            ("wrong-fit-unit", lambda c: c["source_model"]["fit_models"][1]["parameter_bindings"]["K_0.5"].update(unit="uM")),
            ("fit-as-elementary-rate", lambda c: c["source_model"]["fit_models"][1]["parameter_bindings"]["k_app_max"].update(role="elementary_decarboxylation_rate")),
            ("different-enzyme-same-DOI", lambda c: c["study"].update(reported_enzyme="human transketolase")),
            ("misnamed-fit-parameter", lambda c: c["endpoint_relations"][3].update(parameter_key="K_0.5")),
            ("missing-absence-reason", lambda c: c.pop("deposit_absence_reason")),
            ("invalid-absence-reason", lambda c: c.update(deposit_absence_reason=True)),
            ("invented-arrangement", lambda c: c["source_model"]["states"][1].update(arrangement_bindings=[{"provider": "6HAF", "pointer": "/arrangement"}])),
            ("invented-deposit", lambda c: c.update(deposit_association={"arrangement_id": "6HAF"})),
            ("invented-atomic-bond", lambda c: c["source_model"]["transitions"][0]["bond_annotations"].append({"role": "formed_bond"})),
            ("elementary-promotion", lambda c: c["source_model"].update(elementary_step_sequence_established=True)),
            ("unassigned-as-zero", lambda c: c["source_model"]["transitions"][2]["parameter_slots"]["forward"].update(is_zero=True)),
            ("invented-original-ID", lambda c: c["endpoint_relations"][0].update(original_observation_id="invented")),
        ]
        for name, mutate in cases:
            with self.subTest(name=name):
                context = deepcopy(original)
                mutate(context)
                with self.assertRaises(ValueError):
                    self.pox_model_relation(context)
        context = deepcopy(original)
        context["source_model"]["transitions"][2]["parameter_slots"]["forward"] = {
            "status": "bound_source_parameter", "binding": context["source_model"]["fit_models"][1]["parameter_bindings"]["k_app_max"]["binding"], "is_zero": False}
        context["source_model"]["transitions"][2].update(parameter_units={"forward": "s^-1"},
                                                       parameter_roles={"forward": "first_order_dissociation"})
        with self.assertRaisesRegex(ValueError, "individual transition rate"):
            self.pox_model_relation(context)
        context = deepcopy(original)
        context["source_model"]["transitions"][2]["parameter_slots"]["forward"] = {
            "status": "bound_source_parameter", "binding": {"provider": "functional_comparison", "pointer": "/variants/0/steady_state/k_cat"}, "is_zero": False}
        context["source_model"]["transitions"][2].update(parameter_units={"forward": "s^-1"},
                                                       parameter_roles={"forward": "first_order_dissociation"})
        with self.assertRaisesRegex(ValueError, "exactly one endpoint relation"):
            self.pox_model_relation(context)
        context = deepcopy(original)
        context["source_model"]["fit_models"][1]["parameter_bindings"]["n_H"] = {
            "binding": {"provider": "functional_comparison", "pointer": "/variants/2/single_turnover/hill_coefficient"},
            "role": "hill_coefficient", "unit": "dimensionless"}
        with self.assertRaisesRegex(ValueError, "existing projected endpoint"):
            self.pox_model_relation(context)

    def test_pox_model_rejects_same_unit_parameter_and_construct_substitution(self):
        original = self.pox_model_relation()["source_context"]
        for index, replacement in ((3, "pox-analogue_binding:wild_type:k_off"),
                                   (4, "pox-analogue_binding:wild_type:K_D_app"),
                                   (0, "pox-analogue_binding:E59Q:k_on"),
                                   (3, "pox-single_turnover:H89N:k_app_max")):
            with self.subTest(replacement=replacement):
                context = deepcopy(original)
                link = deepcopy(next(item for item in self.spec["model_links"] if item["study_id"] == "pox_2019"))
                link["observation_ids"][index] = replacement
                context["endpoint_relations"][index]["observation_id"] = replacement
                with self.assertRaises(ValueError):
                    self.pox_model_relation(context, link)

    def test_pox_model_query_returns_existing_fit_evidence_without_new_measurements(self):
        view = json.loads(subprocess.check_output([
            sys.executable, str(ROOT / "scripts/query_atlas_perturbations.py"),
            "--model-link", "pox_2019:wild_type:MAP_pyruvate_models"], text=True))
        self.assertEqual({row["parameter"] for row in view["observations"]},
                         {"k_on", "k_off", "K_D_app", "k_app_max", "K_0.5"})
        self.assertEqual(len(view["observations"]), 5)
        self.assertEqual(len(view["model_links"]), 1)
        self.assertEqual(view["comparisons"], [])
        self.assertEqual(view["state_links"], [])
        self.assertTrue(all(row == {**self.rows[row["id"]], "comparison_memberships": []}
                            for row in view["observations"]))

    def model_relation(self, context=None, link=None):
        sources = {key: json.loads((ROOT / binding["path"]).read_text())
                   for key, binding in self.spec["sources"].items()}
        link = deepcopy(self.spec["model_links"][0]) if link is None else link
        if context is None:
            context = deepcopy(sources[link["context_provider"]["source"]])
        return _model_link(context, link, self.view["constructs"], self.rows, self.view["assays"],
                           self.spec["sources"], lambda ref: pointer(sources[ref["source"]], ref["pointer"]))

    def test_model_link_separates_reverse_adduct_formation_from_donor_cleavage(self):
        result = self.model_relation()
        transitions = {item["transition_id"]: item for item in result["transitions"]}
        formation = transitions["adduct_formation"]
        self.assertEqual(formation["direction_endpoints"]["reverse"], ["conjugate", "michaelis"])
        self.assertEqual(formation["resolved_parameters"]["reverse"]["value"], 0.47)
        self.assertEqual(transitions["donor_cleavage"]["resolved_parameters"], {"forward": None, "reverse": None})
        self.assertFalse(transitions["donor_cleavage"]["missing_parameter_is_zero"])
        self.assertFalse(result["source_context"]["source_model"]["graph_replay_verified"])
        self.assertEqual(result["arrangement"]["component_dictionary_bonds"][1]["atom_ids"], ["CF2", "CF3"])

    def test_model_link_rejects_direction_state_atom_and_endpoint_transfers(self):
        original = self.model_relation()["source_context"]
        cases = [
            ("reverse-as-cleavage", lambda c: c["endpoint_relations"][1].update(transition_id="donor_cleavage")),
            ("reverse-as-forward", lambda c: c["endpoint_relations"][1].update(transition_direction="forward")),
            ("accumulation-as-cleavage", lambda c: c["endpoint_relations"][2].update(state_id="cleaved")),
            ("missing-is-zero", lambda c: c["source_model"]["transitions"][2]["parameter_slots"]["forward"].update(is_zero=True)),
            ("invented-cleavage-scalar", lambda c: c["source_model"]["transitions"][2]["parameter_slots"]["forward"].update(value=0.47)),
            ("unwitnessed-cleavage-parameter", lambda c: c["source_model"]["transitions"][2]["parameter_slots"].update(forward={"status": "bound_source_parameter", "binding": {"provider": "functional_comparison", "pointer": "/variants/2/steady_state/k_cat"}, "is_zero": False})),
            ("swapped-bond", lambda c: c["deposit_association"]["bond_annotations"][0].update(dictionary_bond_pointer="/arrangement/component_dictionary_bonds/1")),
            ("elementary-promotion", lambda c: c["source_model"].update(elementary_step_sequence_established=True)),
            ("dangling-state", lambda c: c["source_model"]["transitions"][1].update(to_state="missing")),
            ("duplicate-transition", lambda c: c["source_model"]["transitions"].append(deepcopy(c["source_model"]["transitions"][0]))),
            ("turnover-source-observation", lambda c: c["endpoint_relations"][2].update(observation_pointer="/observations/2")),
            ("turnover-source-relation", lambda c: c["deposit_association"].update(existing_relation_pointers=["/relations/0", "/relations/2"])),
            ("turnover-assay", lambda c: c["endpoint_relations"][0].update(assay_pointer="/assays/0")),
            ("reverse-turnover-assay", lambda c: c["endpoint_relations"][1].update(assay_pointer="/assays/0")),
            ("wrong-arrangement", lambda c: c["deposit_association"].update(arrangement_id="other")),
            ("wrong-original-observation", lambda c: c["endpoint_relations"][0].update(original_observation_id="other")),
            ("wrong-bond-role", lambda c: c["source_model"]["transitions"][1]["bond_annotations"][0].update(role="scissile_bond")),
            ("wrong-atom-alias", lambda c: c["deposit_association"]["atom_correspondence"][1].update(source_atom_label="other")),
        ]
        for name, mutate in cases:
            with self.subTest(name=name):
                context = deepcopy(original)
                mutate(context)
                with self.assertRaises(ValueError):
                    self.model_relation(context)
        for replacement in ("tkt-steady_state:E160Q:kcat", "tkt-stopped_flow:E160A:k_forward"):
            with self.subTest(replacement=replacement):
                context = deepcopy(original)
                context["endpoint_relations"][0]["observation_id"] = replacement
                link = deepcopy(self.spec["model_links"][0])
                link["observation_ids"][0] = replacement
                with self.assertRaises(ValueError):
                    self.model_relation(context, link)

    def test_model_link_query_reuses_only_existing_f6p_endpoints(self):
        view = json.loads(subprocess.check_output([
            sys.executable, str(ROOT / "scripts/query_atlas_perturbations.py"),
            "--model-link", "tkt_2019:E160Q:F6P_transitions"], text=True))
        self.assertEqual({row["id"] for row in view["observations"]}, {
            "tkt-stopped_flow:E160Q:k_forward", "tkt-nmr:E160Q:covalent_intermediate_accumulation"})
        self.assertEqual(view["comparisons"], [])
        self.assertEqual(view["state_links"], [])
        self.assertEqual(len(view["model_links"]), 1)
        self.assertFalse(any(row["parameter"] == "k_reverse" for row in view["observations"]))
        nmr = next(row for row in view["observations"] if row["result_kind"] == "qualitative")
        self.assertIsNone(nmr["value"])

    def core_relation(self, annotation=None):
        binding = self.spec["sources"]["da2010"]
        source = json.loads((ROOT / binding["path"]).read_text(encoding="utf-8"))
        if annotation is None:
            annotation = json.loads((ROOT / self.spec["sources"]["da2010_core"]["path"]).read_text(encoding="utf-8"))
        return _connectivity_relation(annotation, source["reaction"], binding, source)

    def test_source_core_replay_requires_all_six_changes_and_preserves_stereo_boundary(self):
        relation = self.view["reactions"]["diels_alder_2010:diene1-dienophile2-cycloaddition"]["connectivity_relations"][0]
        annotation = relation["source_annotation"]
        self.assertTrue(relation["replay_verified"])
        self.assertIsNone(relation["computed_atom_stereochemistry"])
        self.assertIsNone(relation["computed_product_stereoisomer"])
        self.assertFalse(relation["map_uniqueness_established"])
        edits = annotation["panel_correspondence"]["graph_edits"]
        self.assertEqual(sum(edit["operation"] == "add_bond" for edit in edits), 2)
        self.assertEqual(sum(edit["operation"] == "set_bond_order" for edit in edits), 4)
        for index in range(len(edits)):
            changed = deepcopy(annotation)
            del changed["panel_correspondence"]["graph_edits"][index]
            with self.assertRaisesRegex(ValueError, "do not reproduce"):
                self.core_relation(changed)
        self.assertEqual([column["source_product_label"] for column in annotation["source_stereochemistry"]["source_product_labels"]],
                         ["3S,4S", "3R,4R", "3S,4R", "3R,4S"])

    def test_source_core_rejects_incomplete_maps_wrong_participants_and_boundary_loss(self):
        annotation = self.core_relation()["source_annotation"]
        changes = [
            (lambda value: value["panel_correspondence"]["atom_map"].pop(), "complete bijection"),
            (lambda value: value["atom_locators"]["before"][0].update(participant_id="4"), "source reaction participants"),
            (lambda value: value["atom_locators"]["after"].pop(), "cover the complete selected graph"),
            (lambda value: value.update(boundary_attachments=[]), "boundary anchors"),
            (lambda value: value["boundary_attachments"].pop(), "cover each input participant"),
            (lambda value: value["boundary_attachments"][0].update(after_atom_id="a"), "boundary anchor differs"),
            (lambda value: value["boundary_attachments"][0].update(before_atom_id="ZZ", after_atom_id=None), "boundary anchor differs"),
            (lambda value: value["reaction_binding"].update(reaction_id="other-reaction"), "reaction binding differs"),
            (lambda value: value["source_stereochemistry"].update(source_product_observation_pointer="/structural_context"), "different reaction or context identity"),
            (lambda value: value["source_stereochemistry"].update(source_product_observation_pointer="/product_context/conversion"), "different reaction or context identity"),
            (lambda value: value.update(relation_id=None), "requires an identity"),
            (lambda value: value["panel_correspondence"]["graph_edits"][0].update(source_flow_id="o1"), "not source arrows"),
        ]
        for mutate, message in changes:
            changed = deepcopy(annotation)
            mutate(changed)
            with self.assertRaisesRegex(ValueError, message):
                self.core_relation(changed)

    def test_connectivity_replay_cannot_be_promoted_to_stereo_or_full_chemistry(self):
        annotation = self.core_relation()["source_annotation"]
        for key in (key for key in annotation["scope"] if key != "kind"):
            changed = deepcopy(annotation)
            changed["scope"][key] = True
            with self.assertRaisesRegex(ValueError, "complete chemistry or stereochemistry"):
                self.core_relation(changed)
        changed = deepcopy(annotation)
        changed["panel_correspondence"]["computed_stereochemistry"] = "3R,4S"
        with self.assertRaisesRegex(ValueError, "panel fields differ"):
            self.core_relation(changed)
        changed = deepcopy(annotation)
        changed["physical_atom_identity"] = True
        with self.assertRaisesRegex(ValueError, "relation fields differ"):
            self.core_relation(changed)
        changed = deepcopy(annotation)
        changed["source_stereochemistry"]["computed_mechanism"] = "concerted"
        with self.assertRaisesRegex(ValueError, "stereochemistry fields differ"):
            self.core_relation(changed)
        changed = deepcopy(annotation)
        changed["panel_correspondence"]["after_graph"]["atoms"][0]["stereochemistry"] = "R"
        with self.assertRaisesRegex(ValueError, "cannot carry atom stereochemistry"):
            self.core_relation(changed)
        for key in ("mapped_atom_configurations", "computed_target_selection"):
            changed = deepcopy(annotation)
            changed["source_stereochemistry"][key] = {"d1": "R", "a": "S"}
            with self.assertRaisesRegex(ValueError, "cannot assert mapped stereochemistry"):
                self.core_relation(changed)
        for operation, after in (("set_stereochemistry", "R"), ("set_formal_charge", 1)):
            changed = deepcopy(annotation)
            changed["panel_correspondence"]["graph_edits"].append(
                {"edit_id": "unsupported", "operation": operation, "atom_ids": ["d1"],
                 "before": None if operation == "set_stereochemistry" else 0,
                 "after": after, "source_flow_id": annotation["project_difference_id"]})
            with self.assertRaisesRegex(ValueError, "bond edits only"):
                self.core_relation(changed)

    def test_coherent_wrong_regiochemistry_needs_source_review_not_just_replay(self):
        changed = deepcopy(self.core_relation()["source_annotation"])
        panel = changed["panel_correspondence"]
        for edit in panel["graph_edits"]:
            if edit["operation"] == "add_bond":
                edit["atom_ids"] = ["b" if atom == "a" else "a" if atom == "b" else atom for atom in edit["atom_ids"]]
        for bond in panel["after_graph"]["bonds"]:
            if set(bond["atom_ids"]) in ({"d1", "a"}, {"d4", "b"}):
                bond["atom_ids"] = ["b" if atom == "a" else "a" if atom == "b" else atom for atom in bond["atom_ids"]]
        # A consistent invented after graph can pass literal replay. Only the
        # exact source-reviewed provider can enter the public reaction query.
        self.assertTrue(self.core_relation(changed)["replay_verified"])
        spec = deepcopy(self.spec)
        spec["sources"]["da2010_core"]["sha256"] = hashlib.sha256(json.dumps(changed).encode()).hexdigest()
        with self.assertRaisesRegex(ValueError, "candidate differs from reviewed"):
            project(ROOT, spec)

    def test_earlier_parent_state_keeps_attachment_and_reacted_graph_distinct(self):
        link = next(row for row in self.view["state_links"]
                    if row["id"] == "ra95_2013:RA95.5-5-states")
        state = link["source_context"]["states"][0]
        connections = state["covalent_state_evidence"]["deposited_connections"]
        self.assertEqual({row["protein"]["label_seq_id"] for row in connections}, {"83"})
        self.assertEqual({row["ligand"]["alt_id"] for row in connections}, {"A", "B"})
        self.assertTrue(all(row["bond_order"] is None for row in connections))
        self.assertEqual(state["ligand_dictionary_coordinate_difference"]["dictionary_only_atom_names"], ["ONA"])
        self.assertIsNone(state["covalent_state_evidence"]["complete_reacted_bond_order_graph"])
        self.assertIsNone(state["phosphate_concentration_M"]["resolved"])
        spec = deepcopy(self.spec)
        spec["state_links"][1]["observation_ids"] = [
            "ra95-kinetics:main-table1:RA95.5-5:" + parameter
            for parameter in ("kcat", "KM", "kcat_over_KM")
        ]
        with self.assertRaisesRegex(ValueError, "functional source row differs"):
            _project_candidate(ROOT, spec)

    def test_state_comparisons_preserve_abstentions_without_assigning_mutant_geometry(self):
        invalid = subprocess.run(
            [sys.executable, str(ROOT / "scripts/query_atlas_perturbations.py"), "--with-comparisons"],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(invalid.returncode, 2)
        self.assertIn("requires --state-link", invalid.stderr)
        for link_id, row_count, comparison_count in (
            ("ra95_2013:RA95.5-5-states", 12, 12),
            ("ra95_2017:RA95.5-8F-states", 21, 21),
        ):
            with self.subTest(link=link_id):
                result = subprocess.run(
                    [sys.executable, str(ROOT / "scripts/query_atlas_perturbations.py"),
                     "--state-link", link_id, "--with-comparisons"],
                    check=True, capture_output=True, text=True, encoding="utf-8",
                )
                view = json.loads(result.stdout)
                self.assertEqual(len(view["observations"]), row_count)
                self.assertEqual(len(view["comparisons"]), comparison_count)
                self.assertEqual(len(view["state_links"]), 1)
                link = view["state_links"][0]
                linked = [row for row in view["observations"] if row["id"] in link["observation_ids"]]
                self.assertEqual(len(linked), 3)
                self.assertEqual({row["construct_id"] for row in linked}, {link["construct_id"]})
                self.assertFalse(link["physical_preparation_identity_established"])
                ids = {row["id"] for row in view["observations"]}
                for comparison in view["comparisons"]:
                    self.assertTrue(set(comparison["roles"].values()) <= ids)
                if link_id.startswith("ra95_2013"):
                    self.assertEqual(sum(row["eligible"] for row in view["comparisons"]), 8)
                    self.assertTrue(all(not row["eligible"] and row["value"] is None
                                        for row in view["comparisons"] if row["id"].endswith(":KM")))
                    self.assertTrue(all(row["source_row_id"].startswith("si-table2:") for row in view["observations"]))
                    default = subprocess.run(
                        [sys.executable, str(ROOT / "scripts/query_atlas_perturbations.py"),
                         "--state-link", link_id],
                        check=True, capture_output=True, text=True, encoding="utf-8",
                    )
                    parent_view = json.loads(default.stdout)
                    self.assertEqual(len(parent_view["observations"]), 3)
                    self.assertEqual(parent_view["comparisons"], [])
                else:
                    paired = next(row for row in view["comparisons"]
                                  if row["id"] == "ra95_2017:Y51F-Y180F:kcat")
                    self.assertEqual(paired["operation"], "multiplicative")
                    self.assertAlmostEqual(paired["value"], 0.021, places=3)

    def test_parent_state_link_retains_chemical_and_model_conflicts(self):
        link = self.view["state_links"][0]
        self.assertEqual(len(link["observation_ids"]), 3)
        self.assertEqual({self.rows[key]["construct_id"] for key in link["observation_ids"]},
                         {"ra95_2017:RA95.5-8F"})
        self.assertFalse(link["physical_preparation_identity_established"])
        self.assertFalse(link["chemical_state_identity_from_sequence"])
        for state in link["states"]:
            self.assertTrue(state["canonical_sequence_equal"])
            selections = {row["selection_id"]: row for row in state["deposit_context"]["row_selections"]}
            polymer = selections["polymer-sequence"]["rows"][0]
            self.assertIn("(MHO)", polymer["pdbx_seq_one_letter_code"])
            self.assertEqual(selections["chemical-modification"]["rows"][0]["label_seq_id"], "237")
        context = link["source_context"]
        holo = context["states"][1]
        self.assertIsNone(holo["crystal_pH"]["resolved"])
        self.assertEqual((holo["crystal_pH"]["supplement"], holo["crystal_pH"]["deposit"]), (7.5, 4.5))
        self.assertIsNone(holo["covalent_state_evidence"]["normalized_interfragment_bond"])
        self.assertFalse(holo["covalent_state_evidence"]["absence_of_adduct_established"])
        conflict = context["sequence_correspondence"]["source_deposit_model_conflict"]
        self.assertEqual(conflict["deposits"]["5AN7_modeled_despite_source_statement"], [62, 63])

    def test_state_link_rejects_wrong_observation_and_deposit(self):
        for defect in ("mutant", "study", "packet", "duplicate", "polymer", "synthesis"):
            spec = deepcopy(self.spec)
            link = spec["state_links"][0]
            if defect == "mutant":
                link["observation_ids"][0] = "ra95-tetrad:S1:Y51F:kcat"
            elif defect == "study":
                link["study_id"] = "ra95_2013"
            elif defect == "packet":
                link["states"][0]["packet_id"] = link["states"][1]["packet_id"]
            elif defect == "duplicate":
                link["observation_ids"].append(link["observation_ids"][0])
            elif defect == "polymer":
                link["states"][0]["polymer_selection_id"] = "chemical-modification"
            else:
                link["observation_ids"] = [next(row["id"] for row in self.view["observations"]
                                               if row["construct_id"] == link["construct_id"]
                                               and row["parameter"] == "conversion")]
            with self.subTest(defect=defect), self.assertRaises(ValueError):
                _project_candidate(ROOT, spec)

    def test_state_link_rejects_changed_canonical_sequence(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            spec = deepcopy(self.spec)
            for binding in spec["sources"].values():
                target = root / binding["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / binding["path"], target)
            binding = spec["sources"]["ra95apo"]
            target = root / binding["path"]
            deposit = json.loads(target.read_text(encoding="utf-8"))
            selection = next(row for row in deposit["row_selections"] if row["selection_id"] == "polymer-sequence")
            selection["rows"][0]["pdbx_seq_one_letter_code_can"] += "A"
            target.write_text(json.dumps(deposit), encoding="utf-8")
            binding["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
            with self.assertRaisesRegex(ValueError, "canonical sequence differs"):
                _project_candidate(root, spec)

    def test_state_link_query_keeps_only_linked_observations(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/query_atlas_perturbations.py"),
             "--state-link", "ra95_2017:RA95.5-8F-states"],
            check=True, capture_output=True, text=True, encoding="utf-8",
        )
        view = json.loads(result.stdout)
        self.assertEqual({row["id"] for row in view["observations"]},
                         set(view["state_links"][0]["observation_ids"]))
        self.assertEqual(view["comparisons"], [])
        self.assertEqual(len(view["state_links"][0]["states"]), 2)

    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads((ROOT / SPEC_PATH).read_text(encoding="utf-8"))
        cls.view = project(ROOT)
        cls.rows = {row["id"]: row for row in cls.view["observations"]}
        cls.comparisons = {row["id"]: row for row in cls.view["comparisons"]}

    def test_ksi_probe_and_compiled_rates_preserve_mechanism_and_assay_boundaries(self):
        context = self.view["evidence_context"]["ksi"][0]
        pairs = context["pairs"]
        self.assertEqual(len(pairs), 6)
        for pair in pairs:
            probe = self.rows[pair["probe_observation_id"]]
            rate = self.rows[pair["turnover_observation_id"]]
            self.assertEqual(probe["construct_id"], rate["construct_id"])
            self.assertNotEqual(probe["substrate_id"], rate["substrate_id"])
            self.assertTrue(probe["assay_qualified"])
            self.assertFalse(rate["assay_qualified"])
            self.assertEqual(probe["uncertainty"]["kind"], "standard_deviation")
            self.assertEqual(rate["uncertainty"]["kind"], "source_plus_minus_statistic_unresolved")
        self.assertEqual(context["source_regression"]["excluded_constructs"], ["D40N"])
        self.assertEqual(context["source_discriminator"]["underlying_mechanistic_reference"]["source_title_mutant"], "D38N")
        self.assertEqual([item["value"] for item in context["signed_field_context"]], [-144, -60])
        request = self.comparisons["ksi_2014:field_function_context"]
        self.assertEqual(len(request["context_observations"]), 12)
        self.assertFalse(request["eligible"])
        self.assertIsNone(request["value"])
        # Reading two numeric compiled rates never authorizes a matched assay.
        forced = {"id": "unsupported-ksi-ratio", "study_id": "ksi_2014", "operation": "ratio",
                  "roles": {"numerator": "ksi-rates:D40N:kcat", "denominator": "ksi-rates:WT:kcat"}}
        refused = compare(self.rows, forced)
        self.assertFalse(refused["eligible"])
        self.assertTrue(any(reason.startswith("unresolved_assay:") for reason in refused["reasons"]))
        self.assertEqual(self.rows["ksi-ir:D40N:carbonyl_frequency"]["value"], 1594.4)
        self.assertEqual(self.rows["ksi-rates:D40N:kcat"]["value"], 0.018)

    def test_ksi_donor_discrimination_does_not_transfer_analogue_states_or_rate_types(self):
        request = self.comparisons["ksi_2010:donor_solvation_context"]
        self.assertTrue(request["source_discriminant_assessed"])
        self.assertFalse(request["arithmetic_requested"])
        self.assertFalse(request["eligible"])
        self.assertIsNone(request["value"])
        rows = [self.rows[key] for key in request["context_observations"]]
        self.assertEqual([row["value"] for row in rows], [20000, 300, 200, 200, 200])
        self.assertTrue(all(row["source_parameter"]["approximate"] for row in rows))
        self.assertTrue(all(row["uncertainty"]["value"] is None for row in rows))
        self.assertEqual({row["parameter"] for row in rows}, {"source_reported_activity_reduction_factor"})
        self.assertEqual({row["substrate_id"] for row in rows}, {"ksi_2010:5-10-EST"})
        evidence = request["source_evidence"]
        self.assertFalse(evidence[0]["donor_control"]["residue16_hydroxyl_required_for_moderate_residual_turnover"])
        for relation in evidence[0]["context_relations"]:
            self.assertFalse(relation["same_construct_as_single_mutant_turnover"])
            self.assertFalse(relation["same_ligand_as_turnover"])
        self.assertEqual(evidence[1]["construct_id"], "Y16S/D40N")
        self.assertEqual(evidence[1]["ligand"], "equilenin")
        self.assertFalse(evidence[1]["water_evidence"]["discrete_water_sites_refined"])
        self.assertEqual([row["chemical_shift_ppm"] for row in evidence[2]["observations"]],
                         [-136.4, -134.7])
        self.assertEqual(evidence[-1], {"reference": 18, "doi": "10.1073/pnas.0911168107"})
        self.assertEqual(evidence[6]["doi"], evidence[-1]["doi"])
        self.assertFalse(evidence[6]["condition_or_factor_transfer_allowed"])
        self.assertFalse(evidence[6]["exact_compiled_row_lineage_established"])
        # A reported fold reduction cannot be silently relabeled as an absolute rate.
        candidate = deepcopy(self.spec)
        panel = next(p for p in candidate["panels"] if p["id"] == "ksi2010-reported-effects")
        panel["parameters"][0]["id"] = "kcat"
        with self.assertRaisesRegex(ValueError, "parameter source field differs"):
            _project_candidate(ROOT, candidate)

    def test_background_and_parameter_specific_retention(self):
        turnover = self.comparisons["ra95_2013:RA95.5-5-K210M:kcat"]
        efficiency = self.comparisons["ra95_2013:RA95.5-5-K210M:kcat_over_KM"]
        self.assertTrue(turnover["eligible"])
        self.assertAlmostEqual(turnover["value"], 0.023 / 0.048)
        self.assertEqual(efficiency["value"], 1)
        reduced = self.comparisons["ra95_2013:RA95.5-5-K83M:kcat_over_KM"]
        self.assertAlmostEqual(reduced["value"], 2.3 / 490)
        self.assertIsNone(efficiency["uncertainty"])

    def test_primary_ksi_assay_does_not_qualify_later_compiled_rates(self):
        primary = [row for row in self.rows.values() if row["study_id"] == "ksi_1995"]
        self.assertEqual(len(primary), 6)
        for row in primary:
            self.assertTrue(row["assay_qualified"])
            self.assertEqual(row["uncertainty"]["kind"], "two_standard_deviations")
            self.assertEqual(row["source_parameter"]["uncertainty"]["determinations"], 5)
            self.assertEqual(row["reaction_id"], "ksi_1995:steroid-double-bond-isomerization")
            self.assertEqual(row["reaction_context"]["source_record"]["participants"][0]["name"],
                             "5-androstene-3,17-dione")
        for construct, kcat, km in (("Y16F", 13.3, 17.1), ("D40N", 0.018, 13.3)):
            for parameter, numerator, denominator in (("kcat", kcat, 26722), ("KM", km, 59.3)):
                ratio = self.comparisons[f"ksi_1995:{construct}:{parameter}"]
                self.assertTrue(ratio["eligible"])
                self.assertAlmostEqual(ratio["value"], numerator / denominator)
                self.assertIsNone(ratio["uncertainty"])
        compiled = [row for row in self.rows.values() if row["id"].startswith("ksi-rates:")]
        self.assertEqual(len(compiled), 6)
        self.assertTrue(all(not row["assay_qualified"] for row in compiled))
        self.assertTrue(all(row["uncertainty"]["kind"] == "source_plus_minus_statistic_unresolved"
                            for row in compiled))
        relation = self.view["evidence_context"]["ksi_primary_provenance"][0]
        self.assertEqual([pair["central_value_equal"] for pair in relation["pairs"]],
                         [False, False, True])
        self.assertFalse(relation["whole_table_condition_transfer_allowed"])
        self.assertFalse(relation["whole_table_error_statistic_transfer_allowed"])
        for pair in relation["pairs"]:
            source = self.rows[pair["primary_observation_id"]]
            compiled_row = self.rows[pair["compiled_observation_id"]]
            self.assertEqual(pair["central_value_equal"], source["value"] == compiled_row["value"])
            self.assertEqual(pair["printed_uncertainty_magnitude_equal"],
                             source["uncertainty"]["value"] == compiled_row["uncertainty"]["value"])
            self.assertFalse(pair["error_statistic_equivalence_established"])
            self.assertFalse(pair["method_transfer_to_compiled_row_qualified"])
        # Matching D40N values cannot authorize a mixed-source control or a
        # transferred assay, even if a caller forces the old qualification flag.
        rows = deepcopy(self.rows)
        rows["ksi-rates:D40N:kcat"]["assay_qualified"] = True
        mixed = compare(rows, {"id": "unsupported-mixed-ksi", "study_id": "ksi_1995",
                               "operation": "ratio", "roles": {
                                   "numerator": "ksi-rates:D40N:kcat",
                                   "denominator": "ksi1995-kinetics:WT:kcat"}})
        self.assertFalse(mixed["eligible"])
        self.assertIn("mismatched_study_id", mixed["reasons"])
        self.assertIn("mismatched_assay_id", mixed["reasons"])

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

    def test_lysine_squares_bind_four_matching_cells_and_preserve_km_refusal(self):
        for background, expected, references in (
            ("RA95.5", {"kcat": 0.004940711462450593, "kcat_over_KM": 0.0026315789473684214},
             {"kcat": 0.001012, "kcat_over_KM": 2.66}),
            ("RA95.5-5", {"kcat": 0.1442455242966752, "kcat_over_KM": 0.036956521739130443},
             {"kcat": 0.0003258333333333333, "kcat_over_KM": 2.3}),
        ):
            for parameter in ("kcat", "kcat_over_KM", "KM"):
                request = self.comparisons[f"ra95_2013:{background}:K83M-K210M:{parameter}"]
                self.assertEqual(request["operation"], "multiplicative")
                self.assertEqual(len(set(request["roles"].values())), 4)
                witnesses = request["source_evidence"][:4]
                self.assertTrue(all(row["footnote_a_marker_present"] for row in witnesses))
                self.assertEqual({row["row_id"] for row in witnesses},
                                 {self.rows[key]["source_row_id"] for key in request["roles"].values()})
                self.assertIsNone(request["uncertainty"])
                if parameter == "KM":
                    self.assertFalse(request["eligible"])
                    self.assertIsNone(request["value"])
                    self.assertEqual(sum(reason.startswith("source_conflict:")
                                         for reason in request["reasons"]), 4)
                    self.assertEqual(sum(reason.startswith("unresolved_unit:")
                                         for reason in request["reasons"]), 4)
                    continue
                self.assertTrue(request["eligible"])
                self.assertAlmostEqual(request["value"], expected[parameter])
                self.assertAlmostEqual(request["expected_double"], references[parameter])
                wrong_parent = deepcopy(request)
                wrong_parent["roles"]["parent"] = f"ra95-kinetics:main-table1:{background}:{parameter}"
                rejected = compare(self.rows, wrong_parent)
                self.assertFalse(rejected["eligible"])
                self.assertIsNone(rejected["value"])
                self.assertIn("mismatched_assay_id", rejected["reasons"])

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

    def test_cited_preparation_does_not_repeat_prior_study_characterization(self):
        rows = [row for row in self.view["observations"] if row["id"].startswith("ra95-tetrad:")]
        self.assertEqual(len(rows), 21)
        for row in rows:
            substrate = row["substrate"]
            self.assertNotIn("preparation_source", substrate)
            self.assertEqual(substrate["source"]["source"], "ra95t")
            preparation = substrate["preparation"]
            self.assertEqual(preparation["reporting_study_id"], row["study_id"])
            self.assertEqual(preparation["procedure_reference_study_id"], "ra95_2013")
            prior = preparation["prior_study_characterization"]
            self.assertEqual(prior["reporting_study_id"], "ra95_2013")
            self.assertEqual(prior["repeat_for_2017_assay_substrate"], "not_established_in_inspected_scope")
            self.assertFalse(preparation["same_substrate_lot_established"])
            self.assertIsNone(preparation["exact_2017_substrate_ee"])
            chain = preparation["evidence_chain"]
            self.assertEqual(len(chain), 3)
            for link in chain:
                ref = link["provider"]
                source = json.loads((ROOT / self.spec["sources"][ref["source"]]["path"]).read_text(encoding="utf-8"))
                witness = pointer(source, ref["pointer"])
                self.assertTrue(any(item["sha256"] == witness["sha256"] for item in self.view["source_witnesses"]))
        self.assertIn("preparation_source", self.view["substrates"]["methodol:R"])
        self.assertAlmostEqual(self.comparisons["ra95_2017:Y51F-Y180F:kcat"]["value"], 0.021)

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
        assessment_id = "beta_barrel_2022:benzoate-control-to-8AH9"
        assessment = next(row for row in spec["comparisons"] if row["id"] == assessment_id)
        assessment["context_observations"].append("missing-row")
        with self.assertRaisesRegex(ValueError, "unbound or cross-study context"):
            _project_candidate(ROOT, spec)
        spec = deepcopy(self.spec)
        assessment = next(row for row in spec["comparisons"] if row["id"] == assessment_id)
        assessment["evidence"] = []
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

    def test_pox_nonbinding_keeps_two_positive_pyruvate_endpoints(self):
        for parameter, expected in [("kcat", 0.49 / 31.8), ("k_app_max", 1.07 / 136)]:
            result = self.comparisons["pox_2019:E59Q:" + parameter]
            self.assertTrue(result["eligible"])
            self.assertAlmostEqual(result["value"], expected)
            self.assertIsNone(result["uncertainty"])
        for parameter in ("k_on", "k_off", "K_D_app"):
            row = self.rows["pox-analogue_binding:E59Q:" + parameter]
            self.assertEqual(row["result_kind"], "unavailable")
            self.assertIsNone(row["value"])
            self.assertIsNone(row["nondetection"])
            self.assertEqual(row["unavailability"]["source_token"], "n.a.")
            self.assertIn("does not bind MAP", row["unavailability"]["reason"])
            self.assertIsNone(row["unavailability"]["numeric_detection_limit"])
            self.assertFalse(row["unavailability"]["is_zero_rate"])
            self.assertFalse(self.comparisons["pox_2019:E59Q:" + parameter]["eligible"])
        # The common field exposes different source-reported missingness causes.
        reasons = {row["id"]: row["unavailability"]["reason"]
                   for row in self.view["observations"] if row["result_kind"] == "unavailable"}
        self.assertIn("325 nm", reasons["tkt-stopped_flow:E366Q:k_forward"])
        self.assertIn("does not bind MAP", reasons["pox-analogue_binding:E59Q:k_on"])

    def test_pox_same_units_or_publication_do_not_qualify_endpoint_transfer(self):
        for denominator, reasons in [
            ("pox-single_turnover:wild_type:k_app_max", ["mismatched_assay_id", "mismatched_endpoint_kind", "mismatched_parameter"]),
            ("pox-analogue_binding:wild_type:k_off", ["mismatched_substrate_id", "mismatched_endpoint_kind"]),
            ("tkt-steady_state:wild_type:kcat", ["mismatched_study_id", "mismatched_background_id"]),
            ("pox-steady_state:H89N:kcat", ["control_is_not_declared_perturbation_background"]),
        ]:
            with self.subTest(denominator=denominator):
                request = deepcopy(self.comparisons["pox_2019:E59Q:kcat"])
                request["roles"]["denominator"] = denominator
                result = compare(self.rows, request)
                self.assertFalse(result["eligible"])
                self.assertIsNone(result["value"])
                for reason in reasons:
                    self.assertIn(reason, result["reasons"])

    def test_pox_source_identity_and_unselected_parameters_remain_bound(self):
        source = json.loads((ROOT / self.spec["sources"]["poxf"]["path"]).read_text(encoding="utf-8"))
        adapter = json.loads((ROOT / self.spec["sources"]["poxi"]["path"]).read_text(encoding="utf-8"))
        providers = {}
        for binding in adapter["source_bindings"]:
            raw = (ROOT / binding["path"]).read_bytes().replace(b"\r\n", b"\n")
            self.assertEqual(hashlib.sha256(raw).hexdigest(), binding["sha256"])
            providers[binding["path"]] = json.loads(raw)
        for construct in adapter["constructs"]:
            ref = construct["source_provider"]
            row = pointer(providers[ref["path"]], ref["json_pointer"])
            background_ref = construct["background_source_provider"]
            background = pointer(providers[background_ref["path"]], background_ref["json_pointer"])
            self.assertEqual(construct["construct_id"], row[construct["source_identity_field"]])
            self.assertEqual(construct["source_row_label"], row["source_row_label"])
            self.assertEqual(construct["background_construct_id"], background["reported_variant"])
            self.assertEqual(background["source_row_label"], "wild-type")
            self.assertIsNone(construct["sequence"])
            self.assertIsNone(construct["sequence_sha256"])
            self.assertFalse(construct["assay_specimen_sequence_verified"])
        projected = [r for r in self.view["observations"] if r["study_id"] == "pox_2019"]
        self.assertEqual({r["source_row_id"] for r in projected},
                         {r["reported_variant"] for r in source["variants"]})
        self.assertEqual(len(projected), 42)
        for row in projected:
            self.assertEqual(row["source_parameter"], pointer(source, row["parameter_provider"]["pointer"]))
            self.assertEqual(row["source_record"], pointer(source, row["provider"]["pointer"]))
            if row["parameter"] == "KM":
                self.assertEqual(row["source_parameter"]["parameter"], "K_M")
        e60a = self.rows["pox-single_turnover:E60A:k_app_max"]["source_record"]
        self.assertEqual(e60a["single_turnover"]["source_reported_efficiency"]["value"], 12.5)
        self.assertNotEqual(113 / 9.0, 12.5)
        self.assertEqual(e60a["single_turnover"]["hill_coefficient"]["parameter"], "n_H")
        kd = self.rows["pox-analogue_binding:wild_type:K_D_app"]
        self.assertIsNone(kd["uncertainty"]["value"])
        self.assertEqual(kd["uncertainty"]["kind"], "not_reported")
        self.assertFalse(kd["source_parameter"]["source_derivation"]["independent_measurement"])
        map_assay = self.view["assays"]["pox_2019:map_stopped_flow"]["source_record"]
        fad_assay = self.view["assays"]["pox_2019:pyruvate_single_turnover"]["source_record"]
        self.assertEqual(map_assay["conditions"]["source_path_length_display"], "10 mM")
        self.assertIsNone(map_assay["conditions"]["path_length_mm"])
        self.assertIsNone(fad_assay["conditions"]["pH"])

    def test_pox_apparent_constants_keep_substrate_assay_and_model_identity(self):
        for numerator_parameter, denominator in [
            ("K_D_app", "pox-steady_state:wild_type:KM"),
            ("K_D_app", "pox-single_turnover:wild_type:K_0.5"),
            ("KM", "pox-single_turnover:wild_type:K_0.5"),
        ]:
            request = deepcopy(self.comparisons["pox_2019:H89N:" + numerator_parameter])
            request["roles"]["denominator"] = denominator
            result = compare(self.rows, request)
            self.assertFalse(result["eligible"])
            self.assertIsNone(result["value"])
            self.assertIn("mismatched_assay_id", result["reasons"])
            self.assertIn("mismatched_parameter", result["reasons"])
            if numerator_parameter == "K_D_app":
                self.assertIn("mismatched_substrate_id", result["reasons"])
        km = self.rows["pox-steady_state:E59Q:KM"]
        k05 = self.rows["pox-single_turnover:E59Q:K_0.5"]
        self.assertEqual(km["unit"], k05["unit"])
        self.assertEqual(km["value"], 979)
        self.assertEqual(k05["value"], 888)
        spec = deepcopy(self.spec)
        panel = next(p for p in spec["panels"] if p["id"] == "pox-single_turnover")
        next(p for p in panel["parameters"] if p["id"] == "K_0.5")["pointer"] = "/steady_state/substrate_response_constant"
        with self.assertRaisesRegex(ValueError, "parameter source field differs"):
            _project_candidate(ROOT, spec)

    def test_pox_filtered_relation_keeps_both_arms_of_each_distinct_endpoint(self):
        completed = subprocess.run([sys.executable, str(ROOT / "scripts/query_atlas_perturbations.py"),
                                    "--comparison", "pox_2019:E59Q:kcat"],
                                   capture_output=True, text=True, encoding="utf-8", check=True)
        view = json.loads(completed.stdout)
        self.assertEqual(len(view["comparisons"]), 1)
        comparison = view["comparisons"][0]
        rows = {row["id"]: row for row in view["observations"]}
        self.assertEqual(len(rows), 14)
        self.assertEqual(set(rows), set(comparison["roles"].values()) | set(comparison["context_observations"]))
        self.assertEqual({rows[r]["parameter"] for r in comparison["roles"].values()}, {"kcat"})
        for parameter in ("kcat", "KM", "k_on", "k_off", "K_D_app", "k_app_max", "K_0.5"):
            self.assertEqual({r["source_row_id"] for r in rows.values() if r["parameter"] == parameter},
                             {"wild_type", "E59Q"})
        self.assertEqual(sum(r["result_kind"] == "unavailable" for r in rows.values()), 3)
        self.assertEqual(view["assays"], self.view["assays"])

    def test_beta_barrel_combined_perturbation_keeps_parameter_and_error_scope(self):
        for parameter, expected in (("kcat", 1.6 / 1.5), ("KM", 50 / 230),
                                    ("kcat_over_KM", 30000 / 6500)):
            comparison = self.comparisons["beta_barrel_2022:16.2-over-16.1:" + parameter]
            self.assertTrue(comparison["eligible"])
            self.assertAlmostEqual(comparison["value"], expected)
            self.assertIsNone(comparison["uncertainty"])
            row = self.rows[comparison["roles"]["numerator"]]
            self.assertEqual(row["perturbation"], ["K49E", "S51H"])
            self.assertFalse(row["sequence_identity_available"])
        turnover = self.rows["beta-kinetics:S-methodol-16.2:kcat"]
        self.assertEqual(turnover["uncertainty"]["value"], 0.1)
        self.assertEqual(turnover["uncertainty"]["kind"], "unresolved_source_error_statistic")
        efficiency = self.rows["beta-kinetics:S-methodol-16.2:kcat_over_KM"]
        self.assertIsNone(efficiency["uncertainty"]["value"])
        self.assertNotEqual(efficiency["value"], 1.6 / (50e-6))
        self.assertEqual(efficiency["source_record"]["source_reported_selectivity"]["value"], 500)
        assay = self.view["assays"][turnover["assay_id"]]["source_record"]
        self.assertIsNone(assay["pH"])
        self.assertEqual({p["value"] for p in assay["pH_source_values"]}, {7, 7.5})
        self.assertIsNone(assay["replicate_n"])

    def test_beta_barrel_all_qualitative_arms_refuse_numeric_dose_ratios(self):
        arms = [r for r in self.view["observations"] if r["parameter"] == "relative_activity_plot"]
        by_condition = {(r["source_record"]["preincubation_minutes"],
                         r["source_record"]["benzoate_mM"]): r for r in arms}
        self.assertEqual(set(by_condition), {(t, c) for t in (10, 840) for c in (0, 0.25, 2.5, 25)})
        for (time, concentration), row in by_condition.items():
            self.assertEqual(row["result_kind"], "qualitative")
            self.assertIsNone(row["value"])
            self.assertIsNone(row["uncertainty"]["value"])
            self.assertFalse(row["assay_qualified"])
            self.assertEqual(row["qualitative_result"]["preincubation_minutes"], time)
            self.assertEqual(row["qualitative_result"]["benzoate_mM"], concentration)
            if concentration in (2.5, 25):
                self.assertIn("below the same-panel", row["qualitative_result"]["source_token"])
            else:
                self.assertNotIn("below the same-panel", row["qualitative_result"]["source_token"])
            if concentration == 0:
                continue
            request = {"id": "attempted-dose-ratio", "study_id": "beta_barrel_2022", "operation": "ratio",
                       "roles": {"numerator": row["id"], "denominator": by_condition[time, 0]["id"]}}
            result = compare(self.rows, request)
            self.assertFalse(result["eligible"])
            self.assertIsNone(result["value"])
            self.assertIn("qualitative:" + row["id"], result["reasons"])
            self.assertIn("unresolved_assay:" + row["id"], result["reasons"])
        spec = deepcopy(self.spec)
        parameter = next(p for p in spec["panels"] if p["id"] == "beta-benzoate-lower")["parameters"][0]
        parameter["status_kinds"]["not_tabulated_not_digitized"] = "numeric"
        with self.assertRaisesRegex(ValueError, "numeric result requires"):
            _project_candidate(ROOT, spec)

        # An unreviewed mapping must not relabel benzoate concentration as activity.
        spec = deepcopy(self.spec)
        parameter = next(p for p in spec["panels"] if p["id"] == "beta-benzoate-lower")["parameters"][0]
        parameter["kind"] = {"literal": "numeric"}
        parameter.pop("status_kinds")
        parameter["value"] = {"pointer": "/benzoate_mM"}
        with self.assertRaisesRegex(ValueError, "candidate differs from reviewed projection"):
            project(ROOT, spec)

    def test_beta_barrel_filtered_transfer_keeps_assessed_arms_and_conflicting_target(self):
        completed = subprocess.run([sys.executable, str(ROOT / "scripts/query_atlas_perturbations.py"),
                                    "--comparison", "beta_barrel_2022:benzoate-control-to-8AH9"],
                                   capture_output=True, text=True, encoding="utf-8", check=True)
        view = json.loads(completed.stdout)
        comparison, = view["comparisons"]
        self.assertFalse(comparison["eligible"])
        self.assertIsNone(comparison["value"])
        self.assertTrue(comparison["reported_benzoate_arms_assessed"])
        self.assertEqual(comparison["roles"], {})
        self.assertEqual(len(view["observations"]), 14)
        self.assertEqual({r["id"] for r in view["observations"]}, set(comparison["context_observations"]))
        self.assertIn("control_construct_differs_from_crystallized_construct", comparison["reasons"])
        self.assertIn("source_internal_benzoate_prose_plot_conflict", comparison["reasons"])
        self.assertIn("zero_added_benzoate_is_not_ligand_depleted_protein", comparison["reasons"])
        conflict = comparison["source_evidence"][0]
        self.assertIsNone(conflict["author_statement"]["explicit_variant_in_sentence"])
        self.assertEqual(conflict["counterevidence"]["caption_variant"], "RA-beta-b-16.2")
        self.assertEqual(comparison["source_evidence"][2]["construct_id"], "RA-beta-b-16.1")
        self.assertEqual(comparison["target_structure_id"], "8AH9")
        assay = comparison["source_evidence"][3]
        self.assertEqual(assay["independently_purified_batches"], 2)
        for field in ("assay_temperature_C", "assay_pH", "buffer", "enzyme_concentration", "readout", "replicate_n_per_arm", "normalization_definition"):
            self.assertIsNone(assay[field])

    def test_beta_barrel_assay_identity_does_not_inherit_deposited_sequence(self):
        source = json.loads((ROOT / self.spec["sources"]["betaf"]["path"]).read_text(encoding="utf-8"))
        adapter = json.loads((ROOT / self.spec["sources"]["betai"]["path"]).read_text(encoding="utf-8"))
        for record in adapter["sequences"]:
            provider = record["source_provider"]
            original = pointer(source, provider["json_pointer"])
            self.assertEqual(record["construct_id"], original["construct_id"])
            self.assertIsNone(original["exact_assay_sequence"])
            construct = self.view["constructs"]["beta_barrel_2022:" + record["construct_id"]]
            self.assertIsNone(construct["sequence"])
            self.assertIsNone(construct["sequence_sha256"])
            self.assertFalse(construct["assay_specimen_sequence_verified"])
        deposited = source["deposited_context"]["sequence"]
        self.assertEqual(len(deposited["sequence"]), 120)
        self.assertEqual(hashlib.sha256(deposited["sequence"].encode("ascii")).hexdigest(), deposited["sha256"])
        parent = self.view["constructs"]["beta_barrel_2022:RA-beta-b-16.1"]
        self.assertIn("V49K", parent["source_record"]["source_substitutions"])
        spec = deepcopy(self.spec)
        spec["constructs"]["beta_barrel_2022:RA-beta-b-16.2"]["sequence_provider"] = {"source": "betai", "pointer": "/sequences/0"}
        with self.assertRaisesRegex(ValueError, "sequence provider construct differs"):
            _project_candidate(ROOT, spec)

    def test_beta_barrel_array_markers_and_assay_substrate_boundaries_fail_closed(self):
        for selected, wrong in (("kcat", 1), ("KM", 2), ("kcat_over_KM", 0)):
            spec = deepcopy(self.spec)
            panel = next(p for p in spec["panels"] if p["id"] == "beta-kinetics")
            next(p for p in panel["parameters"] if p["id"] == selected)["pointer"] = f"/parameters/{wrong}"
            with self.assertRaisesRegex(ValueError, "parameter source field differs|parameter source marker differs"):
                _project_candidate(ROOT, spec)
        request = deepcopy(self.comparisons["beta_barrel_2022:16.2-over-16.1:kcat"])
        for denominator in ("ra95-tetrad:S1:RA95.5-8F:kcat", "beta-benzoate-reference:benzoate-10min-0mM:relative_activity_plot"):
            request["roles"]["denominator"] = denominator
            result = compare(self.rows, request)
            self.assertFalse(result["eligible"])
            self.assertIsNone(result["value"])
            self.assertIn("mismatched_assay_id", result["reasons"])
            self.assertIn("mismatched_substrate_id", result["reasons"])
        source = json.loads((ROOT / self.spec["sources"]["betaf"]["path"]).read_text(encoding="utf-8"))
        for row in self.view["observations"]:
            if row["study_id"] == "beta_barrel_2022":
                self.assertEqual(row["source_record"], pointer(source, row["provider"]["pointer"]))
                self.assertEqual(row["source_parameter"], pointer(source, row["parameter_provider"]["pointer"]))
                self.assertNotIn("preparation_source", row["substrate"])

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
