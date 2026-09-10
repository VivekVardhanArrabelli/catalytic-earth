"""Failure modes for cross-record depiction correspondence and proton scope."""

import copy
import json
from pathlib import Path
import unittest
import tempfile
import xml.etree.ElementTree as ET

from scripts.compare_source_steps import (
    _flow_signature, _panel, _read_bound, compare, parse_mcsa_scheme_flows,
)

ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "data/atlas/source_step_correspondence/thdp.json"
PLP_BOUNDARY = ROOT / "data/atlas/source_step_correspondence/plp_step2_boundary.json"


class SourceStepCorrespondenceTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(SPEC.read_text())

    def test_reset_is_complete_but_activation_retains_unmatched_hydrogen(self):
        result = compare(self.data, ROOT)
        activation, reset = result["relations"]
        self.assertFalse(result["after_state_replay"])
        self.assertFalse(activation["complete_selected_covalent_actor_graphs"])
        self.assertEqual(activation["left"]["selected_atom_count"], 35)
        self.assertEqual(activation["left"]["compared_atom_count"], 34)
        self.assertEqual(activation["left"]["excluded_atoms"][0]["atom_id"], "a65")
        self.assertEqual(activation["left"]["uncompared_boundary_bonds"],
                         [{"atom_ids": ["a64", "a65"], "order": 1}])
        self.assertTrue(reset["complete_selected_covalent_actor_graphs"])
        for row in result["relations"]:
            self.assertTrue(row["all_source_flow_endpoints_preserved"])
            self.assertTrue(row["reaction_endpoint_map_invariant_across_declared_maps"])
            self.assertEqual(row["declared_maps_checked"], 2)

    def test_cannot_remove_the_activation_hydrogen_qualification(self):
        self.data["relations"][0]["left"]["excluded_atoms"] = []
        with self.assertRaisesRegex(ValueError, "complete bijection"):
            compare(self.data, ROOT)

    def test_cannot_drop_a_transferred_proton_to_force_a_match(self):
        self.data["relations"][1]["left"]["excluded_atoms"] = [
            {"atom_id": "a65", "reason": "invalid omission of transferred H"}]
        with self.assertRaisesRegex(ValueError, "electron-flow endpoint"):
            compare(self.data, ROOT, "reset")

    def test_graph_symmetry_does_not_allow_swapping_transferred_hydrogens(self):
        mapping = self.data["relations"][1]["mappings"][0]["atom_map"]
        mapping["a65"], mapping["a66"] = mapping["a66"], mapping["a65"]
        with self.assertRaisesRegex(ValueError, "mapped covalent graph differs"):
            compare(self.data, ROOT, "reset")

    def test_same_graph_does_not_allow_a_wrong_directed_flow_join(self):
        mapping = self.data["relations"][1]["mappings"][0]["flow_map"]
        mapping["o35"], mapping["o36"] = mapping["o36"], mapping["o35"]
        with self.assertRaisesRegex(ValueError, "directed electron-flow endpoints differ"):
            compare(self.data, ROOT, "reset")

    def test_changed_source_and_wrong_proposal_fail_closed(self):
        changed = copy.deepcopy(self.data)
        changed["sources"]["M0106"]["snapshot"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "file hash differs"):
            compare(changed, ROOT)
        self.data["relations"][1]["right"]["mechanism_id"] = 2
        with self.assertRaisesRegex(ValueError, "scheme binding differs"):
            compare(self.data, ROOT, "reset")

    def test_missing_relation_is_not_a_successful_empty_comparison(self):
        with self.assertRaisesRegex(ValueError, "unknown relation ID"):
            compare(self.data, ROOT, "unknown")
        self.data["relations"] = []
        with self.assertRaisesRegex(ValueError, "no relations to check"):
            compare(self.data, ROOT)

    def test_source_alias_and_injected_finding_are_not_verified_claims(self):
        changed = copy.deepcopy(self.data)
        changed["sources"]["fake"] = changed["sources"].pop("M0106")
        changed["relations"][0]["left"]["source_id"] = "fake"
        with self.assertRaisesRegex(ValueError, "displayed source identity"):
            compare(changed, ROOT, "activation")
        self.data["relations"][0]["finding"] = "same complete cycle and physical atom map"
        with self.assertRaisesRegex(ValueError, "findings must be derived"):
            compare(self.data, ROOT)

    def test_query_does_not_emit_unused_unverified_source_bindings(self):
        self.data["sources"]["M9999"] = {"snapshot": {"path": "missing", "sha256": "0" * 64}}
        result = compare(self.data, ROOT, "reset")
        self.assertEqual(set(result["source_bindings"]), {"M0106", "M0219"})

    def test_git_lf_hashes_accept_crlf_checkouts_without_source_content_change(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for source in self.data["sources"].values():
                for key in ("snapshot", "records"):
                    relative = source[key]["path"]
                    target = root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes((ROOT / relative).read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
            result = compare(self.data, root, "reset")
            self.assertEqual(result["attribution"]["license"], "CC BY 4.0")
            self.assertTrue(result["relations"][0]["all_source_flow_endpoints_preserved"])

    def test_plp_local_arrows_retain_distinct_source_chemistry_and_stereo(self):
        data = json.loads(PLP_BOUNDARY.read_text())
        self.assertEqual(data["status"], "qualified_graph_relation_not_established")
        self.assertFalse(data["adjudication"]["scientific_non_equivalence_proven"])
        self.assertEqual(len(data["cases"]), 3)
        self.assertEqual({case["side"]["source_id"] for case in data["cases"]},
                         {"M0066", "M0186", "M0213"})
        self.assertEqual(set(data["source_bindings"]), {"M0066", "M0186", "M0213"})
        patterns = {
            "lysine_adduct_bond_to_lysine_n": (
                ("atom_set", ("adduct_c", "lysine_n")),
                ("atom_set", ("lysine_n",))),
            "substrate_n_lone_pair_to_adduct_bond": (
                ("electron_base_atom", ("substrate_n",)),
                ("atom_set", ("adduct_c", "substrate_n"))),
        }
        common_endpoint_signatures = None
        for case in data["cases"]:
            side = case["side"]
            with self.subTest(source=side["source_id"]):
                binding = data["source_bindings"][side["source_id"]]
                snapshot = _read_bound(ROOT, binding["snapshot"])
                records = _read_bound(ROOT, binding["records"])["records"]
                record = next(r for r in records if r["record_id"] == binding["record_id"])
                scheme = next(s for s in snapshot["step_schemes"] if
                              s["mechanism_id"] == 1 and s["step_id"] == 2)
                step = next(s for p in record["mechanism_proposals"] if
                            p["source_mechanism_id"] == 1 for s in p["mechanism_steps"] if
                            s["source_step_id"] == 2)
                self.assertEqual(record["mcsa_id"], side["source_id"])
                self.assertEqual(step["source_scheme_sha256"], side["scheme_sha256"])
                self.assertEqual(step["summary"], case["source_step_summary"])
                flows = parse_mcsa_scheme_flows(scheme)["electron_flows"]
                self.assertEqual(step["electron_flows"], flows)
                role_map = {atom: role for role, atom in case["local_atom_roles"].items()}
                by_id = {f["flow_id"]: f for f in flows}
                self.assertEqual(set(by_id), set(case["local_flow_roles"].values()))
                for role, flow_id in case["local_flow_roles"].items():
                    self.assertEqual(_flow_signature(by_id[flow_id], role_map), patterns[role])
                tree = ET.fromstring(scheme["content_utf8"])
                atoms = {a.get("id"): a for a in tree.iter("atom")}
                bonds = list(tree.iter("bond"))
                endpoint_signatures = {role: (
                    atoms[atom].get("elementType"),
                    int(atoms[atom].get("formalCharge", "0")),
                    atoms[atom].get("isotope"), atoms[atom].get("lonePair"),
                    atoms[atom].get("rgroupRef"), bool(atoms[atom].get("mrvAlias")))
                    for role, atom in case["local_atom_roles"].items()}
                if common_endpoint_signatures is None:
                    common_endpoint_signatures = endpoint_signatures
                self.assertEqual(endpoint_signatures, common_endpoint_signatures)
                for atom_id, tokens in case["source_atom_tokens"].items():
                    self.assertEqual({key: atoms[atom_id].get(key) for key in tokens}, tokens)
                endpoints = set(case["local_atom_roles"].values())
                local_bonds = [{"bond_id": b.get("id"),
                                "ordered_atom_refs2": b.get("atomRefs2").split(),
                                "order": b.get("order")} for b in bonds
                               if set(b.get("atomRefs2").split()) <= endpoints]
                self.assertEqual(local_bonds, case["local_bond_witnesses"])
                stereo = [{"bond_id": b.get("id"),
                           "ordered_atom_refs2": b.get("atomRefs2").split(),
                           "order": b.get("order"), "bond_stereo": b.findtext("bondStereo")}
                          for b in bonds if b.find("bondStereo") is not None]
                self.assertEqual(stereo, case["source_stereo_bonds"])
                hydrogens = [{"atom_id": a.get("id"), "attached_atom_ids": [
                    other for b in bonds if a.get("id") in b.get("atomRefs2").split()
                    for other in b.get("atomRefs2").split() if other != a.get("id")]}
                    for a in atoms.values() if a.get("elementType") == "H"]
                self.assertEqual(hydrogens, case["explicit_hydrogens_in_entire_panel"])

    def test_plp_stereo_at_required_endpoint_cannot_be_removed_by_boundary_exclusion(self):
        data = json.loads(PLP_BOUNDARY.read_text())
        for case in data["cases"]:
            side = case["side"]
            snapshot = _read_bound(ROOT, data["source_bindings"][side["source_id"]]["snapshot"])
            scheme = next(s for s in snapshot["step_schemes"] if
                          s["mechanism_id"] == 1 and s["step_id"] == 2)
            tree = ET.fromstring(scheme["content_utf8"])
            neighbors = {a.get("id"): set() for a in tree.iter("atom")}
            for bond in tree.iter("bond"):
                a, b = bond.get("atomRefs2").split()
                neighbors[a].add(b)
                neighbors[b].add(a)
            endpoints = set(case["local_atom_roles"].values())
            component, pending = set(), [next(iter(endpoints))]
            while pending:
                atom = pending.pop()
                if atom not in component:
                    component.add(atom)
                    pending.extend(neighbors[atom] - component)
            self.assertEqual(len(component), case["full_connected_actor_atom_count"])
            self.assertEqual(sum(set(b.get("atomRefs2").split()) <= component
                                 for b in tree.iter("bond")),
                             case["full_connected_actor_bond_count"])
            minimal = copy.deepcopy(side)
            minimal["excluded_atoms"] = [
                {"atom_id": atom, "reason": "Adversarial endpoint-only selection; not an accepted relation."}
                for atom in sorted(component - endpoints)]
            for selection in (side, minimal):
                with self.subTest(source=side["source_id"], minimal=bool(selection["excluded_atoms"])):
                    with self.assertRaisesRegex(ValueError, case["expected_consumer_rejection"]):
                        _panel(ROOT, data["source_bindings"], selection)


if __name__ == "__main__":
    unittest.main()
