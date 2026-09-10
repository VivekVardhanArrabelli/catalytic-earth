"""Failure modes for cross-record depiction correspondence and proton scope."""

import copy
import json
from pathlib import Path
import unittest
import tempfile

from scripts.compare_source_steps import compare

ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "data/atlas/source_step_correspondence/thdp.json"


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


if __name__ == "__main__":
    unittest.main()
