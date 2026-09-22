from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from catalytic_earth import atlas_stereo_transition_candidates
from catalytic_earth.atlas_candidate_events import canonical_bytes
from catalytic_earth.atlas_candidate_patterns import _WorkBudget
from catalytic_earth.atlas_candidate_patterns import query_candidate_patterns
from catalytic_earth.atlas_stereo_transition_candidates import (
    PACKAGE_ID,
    QUERY_SCHEMA_VERSION,
    _derive_row,
    _load_packaged,
    _load_verified_draft_bundle,
    _query_with_packaged_stereo_transitions,
    _validate_payload,
)
from catalytic_earth.core_cli import verified_candidate_events


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIRECTORY = (
    ROOT / "data/atlas/source_drafts/batches/plp-pyruvoyl/sources"
)


class StereoTransitionCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload, cls.summary = _load_packaged()
        cls.draft_bundle, cls.draft_sha = _load_verified_draft_bundle()
        cls.rows = {
            row["raw_source_binding"]["record_id"]: row
            for row in cls.payload["candidates"]
        }

    def test_repository_reconstruction_equals_packaged_payload(self):
        expectations = {
            "M0066": {
                "support_counts": {
                    "after_graph_confirmed": 8,
                    "source_arrow_only": 2,
                },
                "raw_text": "H",
                "bond_id": "b18",
                "atom_refs": ["a18", "a19"],
                "mapped_node_count": 57,
            },
            "M0213": {
                "support_counts": {
                    "after_graph_confirmed": 6,
                    "source_arrow_only": 2,
                },
                "raw_text": "W",
                "bond_id": "b20",
                "atom_refs": ["a17", "a20"],
                "mapped_node_count": 69,
            },
        }
        self.assertEqual(set(self.rows), set(expectations))
        for record_id, expected in expectations.items():
            with self.subTest(record_id=record_id):
                packaged = self.rows[record_id]
                raw = (SOURCE_DIRECTORY / f"{record_id}.json").read_bytes()
                self.assertEqual(
                    hashlib.sha256(raw).hexdigest(),
                    packaged["raw_source_binding"]["snapshot_sha256"],
                )
                reconstructed = _derive_row(
                    raw, packaged["declaration"], self.draft_bundle
                )
                self.assertEqual(reconstructed, packaged)
                self.assertEqual(packaged["support_counts"], expected["support_counts"])
                transition = packaged["raw_context_transition"]
                self.assertEqual(transition["direction"], "disappearance")
                stereo = transition["before"]["bond_stereo"]
                self.assertEqual(len(stereo), 1)
                self.assertEqual(stereo[0]["raw_text"], expected["raw_text"])
                self.assertEqual(stereo[0]["bond_id"], expected["bond_id"])
                self.assertEqual(
                    stereo[0]["ordered_atom_refs2"], expected["atom_refs"]
                )
                self.assertEqual(
                    packaged["candidate"]["coverage"]["mapped_node_count"],
                    expected["mapped_node_count"],
                )
                self.assertNotEqual(
                    packaged["raw_source_binding"]["snapshot_sha256"],
                    packaged["candidate"]["source_binding"]["snapshot_sha256"],
                )
                self.assertTrue(
                    packaged["source_context"]["mandatory_abstentions"]
                )
                self.assertNotIn("context_preservation", packaged["candidate"])

    def test_installed_payload_identity_and_maturity_boundary(self):
        self.assertEqual(self.summary["package_id"], PACKAGE_ID)
        self.assertEqual(self.summary["candidate_count"], 2)
        self.assertEqual(
            self.summary["candidate_ids"],
            [
                "panel-candidate:M0066:mechanism-1:steps-3-4",
                "panel-candidate:M0213:mechanism-1:steps-3-4",
            ],
        )
        self.assertEqual(self.payload["status"], "unreviewed")
        boundary = self.payload["audit_boundary"]
        self.assertTrue(boundary["computationally_checked"])
        self.assertEqual(boundary["audit_independence"], "same_model_only")
        self.assertFalse(boundary["independent_scientific_review"])
        self.assertFalse(boundary["reviewed_evidence"])
        self.assertFalse(boundary["stereochemistry_interpreted"])
        self.assertFalse(boundary["achirality_inferred"])
        self.assertTrue(boundary["development_material"])
        self.assertFalse(boundary["held_out_transfer_claim"])
        self.assertFalse(boundary["original_source_bytes_packaged"])
        self.assertFalse(boundary["original_source_hashes_recomputed_at_runtime"])
        self.assertEqual(
            self.payload["source_draft_binding"]["sha256"], self.draft_sha
        )

    def test_opt_in_query_keeps_source_identities_separate(self):
        catalog = verified_candidate_events()
        m0213_clauses = [{
            "kind": "charge",
            "elements": ["C"],
            "variables": ["alpha"],
            "before": 0,
            "after": -1,
        }]
        frozen = query_candidate_patterns(
            catalog, clauses=m0213_clauses, mcsa_id="M0213"
        )
        self.assertEqual((frozen["candidate_count"], frozen["binding_count"]), (0, 0))
        m0213 = _query_with_packaged_stereo_transitions(
            catalog, clauses=m0213_clauses, mcsa_id="M0213"
        )
        self.assertEqual(m0213["schema_version"], QUERY_SCHEMA_VERSION)
        self.assertEqual((m0213["matched_candidate_count"], m0213["binding_count"]), (1, 1))
        self.assertFalse({"catalog_id", "catalog_sha256", "candidate_count"} & set(m0213))
        self.assertEqual(
            m0213["sources"]["frozen_v1_catalog"],
            {
                "catalog_id": "atlas-context-candidate-events-v1",
                "catalog_sha256": "682e6f1a6d30f5328c2efcd3c8f85d661ffb068ef5ed3e31b2aac3f7bd3726e0",
                "catalog_candidate_count": 12,
            },
        )
        witness_source = m0213["sources"]["raw_stereo_transition_candidates"]
        self.assertEqual(witness_source["source_candidate_count"], 2)
        self.assertEqual(witness_source["audit_independence"], "same_model_only")
        self.assertFalse(witness_source["independent_scientific_review"])
        match = m0213["matches"][0]
        self.assertEqual(match["source_kind"], "raw_stereo_transition_candidates")
        self.assertEqual(match["source_id"], PACKAGE_ID)
        self.assertEqual(match["bindings"][0]["atom_bindings"], {"alpha": "a17"})

        m0066_clauses = [
            {"kind": "bond", "elements": ["C", "N"], "variables": ["alpha", "imine"], "before": 1, "after": 2},
            {"kind": "bond", "elements": ["N", "C"], "variables": ["imine", "plp"], "before": 2, "after": 1},
            {"kind": "bond", "elements": ["N", "C"], "variables": ["ring", "ring_c"], "before": 2, "after": 1},
            {"kind": "charge", "elements": ["N"], "variables": ["ring"], "before": 1, "after": 0},
        ]
        m0066 = _query_with_packaged_stereo_transitions(
            catalog, clauses=m0066_clauses, mcsa_id="M0066"
        )
        self.assertEqual((m0066["matched_candidate_count"], m0066["binding_count"]), (1, 1))
        self.assertEqual(
            m0066["matches"][0]["bindings"][0]["atom_bindings"],
            {
                "alpha": "a18",
                "imine": "a19",
                "plp": "a57",
                "ring": "a4",
                "ring_c": "a5",
            },
        )

    def test_opt_in_union_uses_one_search_budget(self):
        instances = []

        class TrackingBudget(_WorkBudget):
            def __init__(self):
                super().__init__()
                instances.append(self)

        clauses = [{
            "kind": "charge",
            "elements": ["C"],
            "variables": ["alpha"],
            "before": 0,
            "after": -1,
        }]
        with patch.object(
            atlas_stereo_transition_candidates, "_WorkBudget", TrackingBudget
        ):
            result = _query_with_packaged_stereo_transitions(
                verified_candidate_events(), clauses=clauses
            )
        self.assertEqual(len(instances), 1)
        self.assertGreater(instances[0].used, 0)
        self.assertEqual(result["filters"]["clauses"], clauses)

    def test_compiled_payload_mutations_fail_closed(self):
        mutations = []

        def refresh(witness, *, candidate=False, transition=False, events=False):
            if candidate:
                digest = hashlib.sha256(
                    canonical_bytes(witness["candidate"])
                ).hexdigest()
                witness["candidate_sha256"] = digest
                witness["derivation"]["projected_candidate_sha256"] = digest
            if transition:
                witness["derivation"]["raw_context_transition_sha256"] = (
                    hashlib.sha256(
                        canonical_bytes(witness["raw_context_transition"])
                    ).hexdigest()
                )
            if events:
                witness["derivation"]["events_sha256"] = hashlib.sha256(
                    canonical_bytes(witness["events"])
                ).hexdigest()

        changed = copy.deepcopy(self.payload)
        changed["candidates"][0]["raw_source_binding"]["snapshot_sha256"] = "0" * 64
        mutations.append(changed)

        changed = copy.deepcopy(self.payload)
        changed["candidates"][0]["raw_context_transition"]["before"]["bond_stereo"][0]["raw_text"] = "X"
        mutations.append(changed)

        changed = copy.deepcopy(self.payload)
        changed["candidates"][0]["events"][0]["support"] = "after_graph_confirmed"
        mutations.append(changed)

        changed = copy.deepcopy(self.payload)
        changed["candidates"][0]["source_context"]["mandatory_abstentions"] = []
        mutations.append(changed)

        changed = copy.deepcopy(self.payload)
        changed["candidates"][0]["scope"]["reviewed_evidence"] = True
        mutations.append(changed)

        changed = copy.deepcopy(self.payload)
        candidate = changed["candidates"][1]["candidate"]
        for flow in candidate["source_flow_bindings"]:
            flow["source_step_id"] = 4
        candidate_sha = hashlib.sha256(canonical_bytes(candidate)).hexdigest()
        changed["candidates"][1]["candidate_sha256"] = candidate_sha
        changed["candidates"][1]["derivation"]["projected_candidate_sha256"] = candidate_sha
        mutations.append(changed)

        changed = copy.deepcopy(self.payload)
        witness = changed["candidates"][1]
        edits = witness["candidate"]["proposed_graph_edits"]
        arrow_only = next(edit for edit in edits if edit["support"] == "source_arrow_only")
        confirmed = next(edit for edit in edits if edit["support"] == "after_graph_confirmed")
        arrow_only["support"], confirmed["support"] = (
            confirmed["support"],
            arrow_only["support"],
        )
        support_by_id = {edit["edit_id"]: edit["support"] for edit in edits}
        for event in witness["events"]:
            event["support"] = support_by_id[event["edit_id"]]
            event["source_edit"]["support"] = support_by_id[event["edit_id"]]
        witness["candidate_sha256"] = hashlib.sha256(
            canonical_bytes(witness["candidate"])
        ).hexdigest()
        witness["derivation"]["projected_candidate_sha256"] = witness[
            "candidate_sha256"
        ]
        witness["derivation"]["events_sha256"] = hashlib.sha256(
            canonical_bytes(witness["events"])
        ).hexdigest()
        mutations.append(changed)

        changed = copy.deepcopy(self.payload)
        witness = changed["candidates"][1]
        witness["candidate"]["source_binding"]["provider"] = "OTHER"
        refresh(witness, candidate=True)
        mutations.append(changed)

        changed = copy.deepcopy(self.payload)
        witness = changed["candidates"][1]
        witness["raw_context_transition"]["before"]["bond_stereo"][0][
            "order_token"
        ] = "3"
        refresh(witness, transition=True)
        mutations.append(changed)

        changed = copy.deepcopy(self.payload)
        witness = changed["candidates"][1]
        transition = witness["raw_context_transition"]
        transition["before"]["bond_stereo"][0]["ordered_atom_refs2"] = [
            "a17", "a22",
        ]
        mapping = {
            item["before_atom_id"]: item["after_atom_id"]
            for item in witness["candidate"]["correspondence"]["atom_map"]
        }
        transition["mapped_endpoint_bindings"] = [
            {"before_atom_id": atom_id, "after_atom_id": mapping[atom_id]}
            for atom_id in ("a17", "a22")
        ]
        transition["blocked_context_assessment"]["special_before_atom_ids"] = [
            "a17", "a22",
        ]
        refresh(witness, transition=True)
        mutations.append(changed)

        changed = copy.deepcopy(self.payload)
        witness = changed["candidates"][1]
        witness["raw_context_transition"]["blocked_context_assessment"][
            "special_before_atom_ids"
        ] = ["bogus"]
        refresh(witness, transition=True)
        mutations.append(changed)

        for index, changed in enumerate(mutations):
            with self.subTest(index=index), self.assertRaises(ValueError):
                _validate_payload(
                    changed,
                    self.draft_bundle,
                    draft_bundle_sha256=self.draft_sha,
                )

    def test_raw_snapshot_and_panel_mutations_cannot_reproduce_packaged_row(self):
        packaged = self.rows["M0213"]
        raw = (SOURCE_DIRECTORY / "M0213.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "snapshot differs"):
            _derive_row(raw + b" ", packaged["declaration"], self.draft_bundle)

        source = json.loads(raw)
        scheme = next(
            row for row in source["step_schemes"]
            if row["mechanism_id"] == 1 and row["step_id"] == 3
        )
        scheme["content_utf8"] = scheme["content_utf8"].replace(
            "<bondStereo>W</bondStereo>", "<bondStereo>H</bondStereo>", 1
        )
        scheme["content_sha256"] = hashlib.sha256(
            scheme["content_utf8"].encode("utf-8")
        ).hexdigest()
        changed_raw = json.dumps(source, indent=2, sort_keys=True).encode("utf-8") + b"\n"
        declaration = copy.deepcopy(packaged["declaration"])
        declaration["source_snapshot_sha256"] = hashlib.sha256(changed_raw).hexdigest()
        declaration["before_scheme_sha256"] = scheme["content_sha256"]
        with self.assertRaisesRegex(ValueError, "compiled draft"):
            _derive_row(changed_raw, declaration, self.draft_bundle)


if __name__ == "__main__":
    unittest.main()
