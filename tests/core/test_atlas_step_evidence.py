from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from catalytic_earth.atlas_step_evidence import (
    STEP_EVIDENCE_REVIEW_UPDATE_RULE,
    canonical_step_evidence_payload_sha256,
    match_step_evidence,
    normalize_step_filters,
    validate_step_evidence,
)
from catalytic_earth.atlas_draft_query import query_source_drafts


ROOT = Path(__file__).resolve().parents[2]
PLP_BUNDLE_PATH = Path(
    "data/atlas/source_drafts/batches/plp-pyruvoyl/records.json"
)
ALDOLASE_BUNDLE_PATH = Path(
    "data/atlas/source_drafts/batches/aldolase-transketolase/records.json"
)
PRIMARY_EVIDENCE_PATH = Path(
    "data/atlas/source_drafts/batches/aldolase-transketolase/"
    "review/primary_evidence_annotations.json"
)
DEFAULT_BUNDLE_PATH = Path("data/atlas/source_drafts/records.json")


def _read_json(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def _record(bundle: dict, mcsa_id: str) -> dict:
    return next(record for record in bundle["records"] if record["mcsa_id"] == mcsa_id)


def _proposal_and_step(
    record: dict, source_step_id: int, source_mechanism_id: int = 1
) -> tuple[dict, dict]:
    proposal = next(
        item
        for item in record["mechanism_proposals"]
        if item["source_mechanism_id"] == source_mechanism_id
    )
    step = next(
        item
        for item in proposal["mechanism_steps"]
        if item["source_step_id"] == source_step_id
    )
    return proposal, step


def _endpoint_labels(step: dict) -> list[str]:
    return sorted(
        {
            label
            for flow in step["electron_flows"]
            for endpoint in (flow["source_point"], flow["target_point"])
            for atom in endpoint["atoms"]
            for label in atom["semantic_labels"]
        }
    )


def _unresolved_context() -> dict:
    return {
        "value": "unresolved",
        "support_scope": "abstained",
        "source_witness": None,
    }


def _silent_assertion() -> dict:
    return {
        "status": "source_silent",
        "scope": "not_established",
        "subject_text": None,
        "support_scope": "source_record_only",
        "source_witness": None,
    }


def _unresolved_direction() -> dict:
    return {
        "value": "unresolved",
        "scope": "not_established",
        "support_scope": "abstained",
        "source_witness": None,
    }


def _cofactor(label: str) -> dict:
    return {
        "label": label,
        "support_scope": "source_record_only",
        "source_witness": {"field": "step_summary", "exact_text": label},
    }


def _limits() -> list[dict]:
    statements = {
        "atom_mapping": "No atom mapping is added.",
        "bond_edits": "No bond edits are compiled.",
        "exact_reaction_instance": "No exact reaction instance is asserted.",
        "source_step_trajectory": "The source arrow trajectory is not validated.",
        "whole_proposal_applicability": "The whole proposal is not validated.",
    }
    return [
        {"limit_id": limit_id, "status": "abstained", "statement": statement}
        for limit_id, statement in sorted(statements.items())
    ]


def _row(
    bundle: dict,
    mcsa_id: str,
    source_step_id: int,
    *,
    source_mechanism_id: int = 1,
    cofactor_labels: tuple[str, ...] = (),
    source_assertion: dict | None = None,
    enzyme_context: dict | None = None,
    direction: dict | None = None,
    primary_annotation_ids: tuple[str, ...] = (),
) -> dict:
    record = _record(bundle, mcsa_id)
    proposal, step = _proposal_and_step(
        record, source_step_id, source_mechanism_id=source_mechanism_id
    )
    return {
        "annotation_id": f"step-context:{mcsa_id.lower()}:{source_step_id}",
        "record_binding": {
            "record_id": record["record_id"],
            "mcsa_id": record["mcsa_id"],
            "source_snapshot_sha256": record["source"]["snapshot_sha256"],
        },
        "step_binding": {
            "proposal_id": proposal["proposal_id"],
            "source_mechanism_id": proposal["source_mechanism_id"],
            "step_id": step["step_id"],
            "source_step_id": step["source_step_id"],
            "source_scheme_sha256": step["source_scheme_sha256"],
        },
        "context": {
            "cofactor_labels": [_cofactor(label) for label in cofactor_labels],
            "flow_endpoint_source_labels": _endpoint_labels(step),
            "chemical_context": _unresolved_context(),
            "enzyme_context": enzyme_context or _unresolved_context(),
            "source_assertion": source_assertion or _silent_assertion(),
            "direction": direction or _unresolved_direction(),
            "roles": [],
        },
        "primary_annotation_ids": list(primary_annotation_ids),
        "limitations": _limits(),
        "scope_effect": {
            "record_evidence_tier_changed": False,
            "allowed_operations_changed": False,
            "whole_proposal_validated": False,
            "source_step_trajectory_validated": False,
            "atom_mapping_added": False,
            "bond_edits_added": False,
            "linked_primary_annotation_scope_expanded": False,
        },
    }


def _review() -> dict:
    return {
        "reviewed_on": "2026-09-06",
        "annotation_payload_sha256": "0" * 64,
        "update_rule": STEP_EVIDENCE_REVIEW_UPDATE_RULE,
        "reviewer_kind": "same_model_computational_agents",
        "same_model_agents": True,
        "blind_review": False,
        "statistically_independent": False,
        "correlated_error_risk": True,
        "human_reviewers": 0,
        "domain_expert_review_claimed": False,
    }


def _repin(sidecar: dict) -> None:
    sidecar["review"]["annotation_payload_sha256"] = (
        canonical_step_evidence_payload_sha256(sidecar)
    )


def _plp_sidecar(bundle: dict) -> dict:
    rows = [
        _row(
            bundle,
            "M0049",
            7,
            source_assertion={
                "status": "explicitly_inferred",
                "scope": "whole_step",
                "subject_text": None,
                "support_scope": "source_record_only",
                "source_witness": {
                    "field": "step_summary",
                    "exact_text": "inferred step",
                },
            },
        ),
        _row(
            bundle,
            "M0066",
            1,
            cofactor_labels=("PLP",),
        ),
        _row(
            bundle,
            "M0186",
            4,
            cofactor_labels=("PLP",),
            source_assertion={
                "status": "explicitly_inferred",
                "scope": "stated_detail_only",
                "subject_text": "the phosphate group acts as a base in this step",
                "support_scope": "source_record_only",
                "source_witness": {
                    "field": "step_summary",
                    "exact_text": (
                        "we infer that the phosphate group acts as a base in this step"
                    ),
                },
            },
        ),
        _row(
            bundle,
            "M0186",
            5,
            cofactor_labels=("PLP",),
            source_assertion={
                "status": "explicitly_assumed",
                "scope": "stated_detail_only",
                "subject_text": "the base in the previous step is the acid in this step",
                "support_scope": "source_record_only",
                "source_witness": {
                    "field": "step_summary",
                    "exact_text": (
                        "We assume that the base in the previous step is the acid in this step"
                    ),
                },
            },
        ),
        _row(
            bundle,
            "M0186",
            6,
            enzyme_context={
                "value": "extra_enzymatic",
                "support_scope": "source_record_only",
                "source_witness": {
                    "field": "step_summary",
                    "exact_text": "outside the enzyme active site",
                },
            },
        ),
        _row(
            bundle,
            "M0213",
            3,
            cofactor_labels=("PLP",),
            direction={
                "value": "source_forward_order",
                "scope": "proposal_context",
                "support_scope": "source_record_only",
                "source_witness": {
                    "field": "proposal_mechanism_text",
                    "exact_text": "In the L-Ala to D-Ala direction",
                },
            },
        ),
    ]
    rows[-1]["context"]["roles"] = [
        {
            "actor_label": "Tyr265B",
            "actor_mapping_status": "source_label_only",
            "role_text": "deprotonates the alpha carbon",
            "direction": "source_forward_order",
            "support_scope": "source_record_only",
            "source_witness": {
                "field": "step_summary",
                "exact_text": "Tyr265B deprotonates the alpha carbon",
            },
        }
    ]
    sidecar = {
        "schema_version": "catalytic-earth.atlas-step-evidence.v1",
        "annotation_set_id": "atlas-step-evidence:plp-pyruvoyl:test-v1",
        "batch_id": "plp-pyruvoyl",
        "status": "reviewed_source_step_context_not_mechanism_expansion",
        "primary_evidence_binding": None,
        "annotations": rows,
        "review": _review(),
    }
    _repin(sidecar)
    return sidecar


class AtlasStepEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = _read_json(PLP_BUNDLE_PATH)

    def test_valid_source_context_distinguishes_assertion_scope_and_silence(self):
        sidecar = _plp_sidecar(self.bundle)

        summary = validate_step_evidence(sidecar, bundle=self.bundle)

        self.assertEqual(summary["annotation_count"], 6)
        self.assertEqual(summary["record_count"], 4)
        rows = sidecar["annotations"]
        self.assertEqual(rows[0]["context"]["source_assertion"]["scope"], "whole_step")
        self.assertEqual(
            rows[2]["context"]["source_assertion"]["scope"],
            "stated_detail_only",
        )
        self.assertEqual(
            rows[-1]["context"]["source_assertion"]["status"],
            "source_silent",
        )
        self.assertIn("unclear", _proposal_and_step(_record(self.bundle, "M0213"), 3)[1]["summary"])

    def test_filters_are_exact_and_all_match_within_one_step(self):
        sidecar = _plp_sidecar(self.bundle)

        assumed_plp = match_step_evidence(
            sidecar,
            bundle=self.bundle,
            cofactors=("  plp ", "PLP"),
            source_assertions=("explicitly_assumed",),
        )
        impossible_cross_step = match_step_evidence(
            sidecar,
            bundle=self.bundle,
            cofactors=("PLP",),
            enzyme_contexts=("extra_enzymatic",),
        )

        self.assertEqual(assumed_plp["filters"]["cofactors"], ["plp"])
        self.assertEqual(list(assumed_plp["matches"]), [
            "atlas50-draft:m0186:source-scoped-mechanism-draft"
        ])
        witness = next(iter(assumed_plp["matches"].values()))[0]
        self.assertEqual(witness["step_binding"]["source_step_id"], 5)
        self.assertEqual(impossible_cross_step["matches"], {})

        sidecar = _plp_sidecar(self.bundle)
        partial = sidecar["annotations"][1]["context"]["cofactor_labels"][0]
        partial["label"] = partial["source_witness"]["exact_text"] = "LP"
        _repin(sidecar)
        with self.assertRaisesRegex(ValueError, "complete source token"):
            validate_step_evidence(sidecar, bundle=self.bundle)

    def test_filter_normalization_rejects_scalar_and_invalid_values(self):
        for kwargs, message in (
            ({"cofactors": "PLP"}, "list or tuple"),
            ({"enzyme_contexts": None}, "list or tuple"),
            ({"source_assertions": ("observed",)}, "invalid"),
            ({"cofactors": ("PLP,PMP",)}, "one value"),
        ):
            with self.subTest(kwargs=kwargs), self.assertRaisesRegex(ValueError, message):
                normalize_step_filters(**kwargs)

    def test_rejects_cross_step_proposal_and_scheme_hash_mixing(self):
        mutations = (
            ("source_step_id", 5, "step binding is absent or mixed"),
            ("source_mechanism_id", 2, "proposal binding is absent or mixed"),
            ("source_scheme_sha256", "0" * 64, "source scheme binding is stale"),
        )
        for field, value, message in mutations:
            with self.subTest(field=field):
                sidecar = _plp_sidecar(self.bundle)
                sidecar["annotations"][2]["step_binding"][field] = value
                _repin(sidecar)
                with self.assertRaisesRegex(ValueError, message):
                    validate_step_evidence(sidecar, bundle=self.bundle)

    def test_rejects_native_or_active_site_inference_from_unrelated_text(self):
        sidecar = _plp_sidecar(self.bundle)
        chemical = sidecar["annotations"][1]["context"]["chemical_context"]
        chemical.update({
            "value": "native",
            "support_scope": "source_record_only",
            "source_witness": {"field": "step_summary", "exact_text": "PLP"},
        })
        _repin(sidecar)
        with self.assertRaisesRegex(ValueError, "must remain unresolved"):
            validate_step_evidence(sidecar, bundle=self.bundle)

        sidecar = _plp_sidecar(self.bundle)
        enzyme = sidecar["annotations"][4]["context"]["enzyme_context"]
        enzyme["value"] = "active_site"
        _repin(sidecar)
        with self.assertRaisesRegex(ValueError, "active-site witness"):
            validate_step_evidence(sidecar, bundle=self.bundle)

    def test_rejects_whole_step_scope_for_detail_only_inference(self):
        sidecar = _plp_sidecar(self.bundle)
        assertion = sidecar["annotations"][2]["context"]["source_assertion"]
        assertion["scope"] = "whole_step"
        assertion["subject_text"] = None
        _repin(sidecar)

        with self.assertRaisesRegex(ValueError, "whole-step inference"):
            validate_step_evidence(sidecar, bundle=self.bundle)

    def test_role_must_be_step_local_and_agree_with_direction(self):
        sidecar = _plp_sidecar(self.bundle)
        role = sidecar["annotations"][-1]["context"]["roles"][0]
        role["direction"] = "source_reverse_order"
        _repin(sidecar)
        with self.assertRaisesRegex(ValueError, "differs from the step context"):
            validate_step_evidence(sidecar, bundle=self.bundle)

        sidecar = _plp_sidecar(self.bundle)
        role = sidecar["annotations"][-1]["context"]["roles"][0]
        role["source_witness"] = {
            "field": "proposal_mechanism_text",
            "exact_text": "Tyr265B abstracts a proton",
        }
        _repin(sidecar)
        with self.assertRaisesRegex(ValueError, "field is invalid"):
            validate_step_evidence(sidecar, bundle=self.bundle)

    def test_flow_endpoint_labels_are_exact_and_do_not_imply_cofactor_state(self):
        sidecar = _plp_sidecar(self.bundle)
        row = sidecar["annotations"][1]
        self.assertIn("chebi:29986", row["context"]["flow_endpoint_source_labels"])
        row["context"]["flow_endpoint_source_labels"] = []
        _repin(sidecar)

        with self.assertRaisesRegex(ValueError, "differ from the compiled step"):
            validate_step_evidence(sidecar, bundle=self.bundle)

    def test_primary_link_preserves_record_scope_and_cannot_authorize_native(self):
        bundle = _read_json(ALDOLASE_BUNDLE_PATH)
        primary = _read_json(PRIMARY_EVIDENCE_PATH)
        primary_row = next(
            row for row in primary["annotations"] if row["record_binding"]["mcsa_id"] == "M0222"
        )
        row = _row(
            bundle,
            "M0222",
            1,
            primary_annotation_ids=(primary_row["annotation_id"],),
        )
        sidecar = {
            "schema_version": "catalytic-earth.atlas-step-evidence.v1",
            "annotation_set_id": "atlas-step-evidence:aldolase:test-v1",
            "batch_id": "aldolase-transketolase",
            "status": "reviewed_source_step_context_not_mechanism_expansion",
            "primary_evidence_binding": {
                "annotation_set_id": primary["annotation_set_id"],
                "annotation_payload_sha256": primary["review"][
                    "annotation_payload_sha256"
                ],
            },
            "annotations": [row],
            "review": _review(),
        }
        _repin(sidecar)
        validate_step_evidence(
            sidecar, bundle=bundle, primary_evidence=primary, repo_root=ROOT
        )

        chemical = row["context"]["chemical_context"]
        chemical.update({
            "value": "native",
            "support_scope": "reviewed_primary_annotation",
            "source_witness": None,
        })
        _repin(sidecar)
        with self.assertRaisesRegex(ValueError, "must remain unresolved"):
            validate_step_evidence(
                sidecar, bundle=bundle, primary_evidence=primary, repo_root=ROOT
            )

    def test_primary_links_preserve_proposal_and_record_only_scopes(self):
        bundle = _read_json(ALDOLASE_BUNDLE_PATH)
        primary = _read_json(PRIMARY_EVIDENCE_PATH)
        primary_by_id = {
            annotation["annotation_id"]: annotation
            for annotation in primary["annotations"]
        }
        proposal_primary = primary_by_id[
            "m0219.proposal-2.4kxv.p29401-protein-context"
        ]
        record_primary = primary_by_id["m0222.2qut.dhap-derived-covalent-moiety"]
        rows = [
            _row(
                bundle,
                "M0219",
                2,
                source_mechanism_id=2,
                cofactor_labels=("Thiamine diphosphate",),
                primary_annotation_ids=(proposal_primary["annotation_id"],),
            ),
            _row(
                bundle,
                "M0222",
                1,
                primary_annotation_ids=(record_primary["annotation_id"],),
            ),
        ]
        sidecar = {
            "schema_version": "catalytic-earth.atlas-step-evidence.v1",
            "annotation_set_id": "atlas-step-evidence:primary-scope:test-v1",
            "batch_id": "aldolase-transketolase",
            "status": "reviewed_source_step_context_not_mechanism_expansion",
            "primary_evidence_binding": {
                "annotation_set_id": primary["annotation_set_id"],
                "annotation_payload_sha256": primary["review"][
                    "annotation_payload_sha256"
                ],
            },
            "annotations": rows,
            "review": _review(),
        }
        _repin(sidecar)
        validate_step_evidence(
            sidecar, bundle=bundle, primary_evidence=primary, repo_root=ROOT
        )

        rows[0] = _row(
            bundle,
            "M0219",
            1,
            source_mechanism_id=1,
            cofactor_labels=("thiamine diphosphate",),
            primary_annotation_ids=(proposal_primary["annotation_id"],),
        )
        sidecar["annotations"] = rows
        _repin(sidecar)
        with self.assertRaisesRegex(ValueError, "crosses source mechanism proposals"):
            validate_step_evidence(
                sidecar, bundle=bundle, primary_evidence=primary, repo_root=ROOT
            )

    def test_component_and_step_filters_cannot_join_m0107_alternatives(self):
        bundle = _read_json(DEFAULT_BUNDLE_PATH)
        rows = [
            _row(
                bundle,
                "M0107",
                4,
                source_mechanism_id=2,
                cofactor_labels=("Mo(IV)",),
            ),
            _row(
                bundle,
                "M0107",
                5,
                source_mechanism_id=3,
                cofactor_labels=("FAD",),
            ),
        ]
        sidecar = {
            "schema_version": "catalytic-earth.atlas-step-evidence.v1",
            "annotation_set_id": "atlas-step-evidence:m0107-alternatives:test-v1",
            "batch_id": "default",
            "status": "reviewed_source_step_context_not_mechanism_expansion",
            "primary_evidence_binding": None,
            "annotations": rows,
            "review": _review(),
        }
        _repin(sidecar)

        proposal_2 = query_source_drafts(
            bundle,
            step_evidence=sidecar,
            mechanism_components=("decoordination from a metal ion",),
            cofactors=("Mo(IV)",),
        )
        false_join = query_source_drafts(
            bundle,
            step_evidence=sidecar,
            mechanism_components=("decoordination from a metal ion",),
            cofactors=("FAD",),
        )
        proposal_3 = query_source_drafts(
            bundle,
            step_evidence=sidecar,
            mechanism_components=("decarboxylation",),
            cofactors=("FAD",),
        )

        self.assertEqual(proposal_2["record_count"], 1)
        self.assertEqual(
            proposal_2["records"][0]["step_evidence_annotations"][0][
                "step_binding"
            ]["source_mechanism_id"],
            2,
        )
        self.assertEqual(false_join["record_count"], 0)
        self.assertEqual(proposal_3["record_count"], 1)
        self.assertEqual(
            proposal_3["records"][0]["step_evidence_annotations"][0][
                "step_binding"
            ]["source_mechanism_id"],
            3,
        )

    def test_matching_does_not_mutate_source_or_annotation_bytes(self):
        bundle = copy.deepcopy(self.bundle)
        sidecar = _plp_sidecar(bundle)
        bundle_before = copy.deepcopy(bundle)
        sidecar_before = copy.deepcopy(sidecar)

        result = match_step_evidence(
            sidecar, bundle=bundle, enzyme_contexts=("extra_enzymatic",)
        )
        result["matches"][
            "atlas50-draft:m0186:source-scoped-mechanism-draft"
        ][0]["annotation_id"] = "changed"

        self.assertEqual(bundle, bundle_before)
        self.assertEqual(sidecar, sidecar_before)


if __name__ == "__main__":
    unittest.main()
