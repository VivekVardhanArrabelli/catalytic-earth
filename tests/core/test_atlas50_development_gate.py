"""Adversarial checks for computational draft permission boundaries."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from catalytic_earth.atlas50_development_gate import (
    ADJUDICATIONS,
    CHALLENGE,
    CROSSWALK,
    CROSSWALK_MANIFEST,
    DIRECTORY,
    POLICY,
    PROBE,
    PROBE_SPEC,
    REQUIRED_INPUTS,
    STATE_BASIS_INPUTS,
    build_development_status,
    canonical_bytes,
    require_operation,
    validate_adjudications,
    validate_policy,
)
from catalytic_earth.canonical_hash import canonical_file_sha256


ROOT = Path(__file__).resolve().parents[2]
BINDINGS = str(DIRECTORY / "review_bindings.json")


def _read(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def fixtures() -> tuple[dict, dict, dict]:
    """Use reviewed object shapes rather than a simplified parallel schema."""

    return (
        copy.deepcopy(_read(ADJUDICATIONS)),
        copy.deepcopy(_read(PROBE)),
        copy.deepcopy(_read(CHALLENGE)),
    )


def _case(value: dict, mcsa_id: str) -> dict:
    return next(row for row in value["cases"] if row["mcsa_id"] == mcsa_id)


def _copy_gate_inputs(destination: Path) -> None:
    manifest = _read(CROSSWALK_MANIFEST)
    relative_paths = (
        set(REQUIRED_INPUTS)
        | {BINDINGS, CROSSWALK_MANIFEST, PROBE_SPEC}
        | set(STATE_BASIS_INPUTS.values())
        | {item["path"] for item in manifest["inputs"]}
    )
    for relative in relative_paths:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)


def _write_json(path: Path, value: dict) -> None:
    path.write_bytes(canonical_bytes(value))


def _refresh_direct_binding(root: Path, relative: str) -> None:
    path = root / BINDINGS
    bindings = json.loads(path.read_text(encoding="utf-8"))
    bindings["inputs"][relative] = canonical_file_sha256(root / relative)
    _write_json(path, bindings)


class DevelopmentGateTests(unittest.TestCase):
    def test_live_status_is_scoped_and_discloses_correlated_review(self) -> None:
        status = build_development_status(ROOT)
        self.assertEqual(status["status"], "open_for_scoped_development")
        disclosure = status["review_independence"]
        self.assertEqual(disclosure["reviewer_kind"], "same_model_computational_agents")
        self.assertFalse(disclosure["statistically_independent"])
        self.assertTrue(disclosure["correlated_error_risk"])
        for key in (
            "human_review_completed",
            "independent_validation_established",
            "experimental_validation_established",
            "protected_registry_expansion_permitted",
            "frozen_phase_b_completed",
        ):
            self.assertFalse(status[key])

        cases = {row["mcsa_id"]: row for row in status["cases"]}
        self.assertEqual(cases["M0064"]["allowed_operations"], ["source_annotation"])
        self.assertEqual(cases["M0970"]["allowed_operations"], ["source_annotation"])
        self.assertIn("source_scoped_mechanism_draft", cases["M0753"]["allowed_operations"])
        self.assertIn(
            "resolved_aspartate_roles",
            {item["clause_id"] for item in cases["M0753"]["mandatory_abstentions"]},
        )

    def test_computational_policy_cannot_claim_scientific_authority(self) -> None:
        policy = _read(POLICY)
        validate_policy(policy)
        for field in (
            "independent_validation_claim_permitted",
            "experimental_validation_claim_permitted",
            "agent_consensus_is_evidence",
            "gold_label_admission_permitted",
            "protected_registry_expansion_permitted",
            "frozen_phase_b_completion_permitted",
        ):
            bad = copy.deepcopy(policy)
            bad[field] = True
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_policy(bad)

    def test_structured_abstention_clause_and_reason_cannot_be_lost(self) -> None:
        value, probe, challenge = fixtures()
        source_clause = _case(probe, "M0064")["mandatory_abstentions"][0]
        self.assertIsInstance(source_clause, dict)

        dropped = copy.deepcopy(value)
        _case(dropped, "M0064")["mandatory_abstentions"].pop(0)
        with self.assertRaisesRegex(ValueError, "abstentions or reasons differ"):
            validate_adjudications(dropped, probe, challenge)

        changed = copy.deepcopy(value)
        _case(changed, "M0064")["mandatory_abstentions"][0]["reason"] = "Reason silently replaced."
        with self.assertRaisesRegex(ValueError, "abstentions or reasons differ"):
            validate_adjudications(changed, probe, challenge)

        malformed = copy.deepcopy(value)
        _case(malformed, "M0064")["mandatory_abstentions"][0] = source_clause["clause_id"]
        with self.assertRaisesRegex(ValueError, "must be an object"):
            validate_adjudications(malformed, probe, challenge)

    def test_additional_distinct_abstention_is_conservative(self) -> None:
        value, probe, challenge = fixtures()
        row = _case(value, "M0107")
        added = {
            "clause_id": "new_source_conflict",
            "reason": "A direct source conflict remains unresolved.",
        }
        row["mandatory_abstentions"].append(added)
        cases = validate_adjudications(value, probe, challenge)
        validated = next(item for item in cases if item["mcsa_id"] == "M0107")
        self.assertIn(added, validated["mandatory_abstentions"])

        duplicate = copy.deepcopy(value)
        _case(duplicate, "M0107")["mandatory_abstentions"].append(copy.deepcopy(added))
        with self.assertRaisesRegex(ValueError, "repeats clause"):
            validate_adjudications(duplicate, probe, challenge)

    def test_scope_and_probe_evidence_cannot_be_broadened_or_replaced(self) -> None:
        value, probe, challenge = fixtures()
        row = _case(value, "M0064")
        row["scope"] = "Exact validated gold mechanism and universal reaction instance are authorized."
        with self.assertRaisesRegex(ValueError, "scope differs"):
            validate_adjudications(value, probe, challenge)

        value, probe, challenge = fixtures()
        row = _case(value, "M0064")
        row["evidence_ids"][0] = _case(probe, "M0106")["evidence_ids"][0]
        with self.assertRaisesRegex(ValueError, "probe evidence binding differs"):
            validate_adjudications(value, probe, challenge)

    def test_challenge_cannot_be_cherry_picked_or_faked(self) -> None:
        value, probe, challenge = fixtures()
        _case(value, "M0753")["challenge_claim_ids"] = [
            "sc-m0753-hisf-development-inclusion"
        ]
        with self.assertRaisesRegex(ValueError, "challenge evidence coverage differs"):
            validate_adjudications(value, probe, challenge)

        value, probe, challenge = fixtures()
        claim = next(
            row
            for row in challenge["claims"]
            if row["claim_id"] == "sc-m0064-current-reaction-represents-topology"
        )
        claim["evidence"] = [{}]
        with self.assertRaisesRegex(ValueError, "malformed challenge evidence"):
            validate_adjudications(value, probe, challenge)

        value, probe, challenge = fixtures()
        claim = next(
            row
            for row in challenge["claims"]
            if row["claim_id"] == "sc-m0064-current-reaction-represents-topology"
        )
        claim["subject_ids"] = "M0064"
        with self.assertRaisesRegex(ValueError, "subject_ids must be an array"):
            validate_adjudications(value, probe, challenge)

    def test_unresolved_material_objection_cannot_be_bypassed(self) -> None:
        value, probe, challenge = fixtures()
        challenge["cross_review"]["material_open_objections"] = []
        with self.assertRaisesRegex(ValueError, "unresolved challenge lacks"):
            validate_adjudications(value, probe, challenge)

        value, probe, challenge = fixtures()
        row = _case(value, "M0970")
        row["open_objections"][0]["blocks"] = ["exact_reaction_instance"]
        with self.assertRaisesRegex(ValueError, "unavailable operations lack"):
            validate_adjudications(value, probe, challenge)

    def test_unanimous_votes_cannot_overrule_a_blocking_objection(self) -> None:
        value, probe, challenge = fixtures()
        row = _case(value, "M0106")
        row["agent_votes_for_acceptance"] = 100
        row["open_objections"][0]["blocks"].append(
            "source_scoped_mechanism_draft"
        )
        with self.assertRaisesRegex(ValueError, "unresolved objection"):
            validate_adjudications(value, probe, challenge)

    def test_same_model_inputs_cannot_claim_independence(self) -> None:
        mutations = (
            ("adjudication", lambda a, p, c: a.__setitem__("independent_review", True)),
            (
                "probe",
                lambda a, p, c: p["review_independence"].__setitem__(
                    "statistical_independence_claimed", True
                ),
            ),
            (
                "challenge",
                lambda a, p, c: c["review_boundary"].__setitem__(
                    "statistically_independent", True
                ),
            ),
        )
        for label, mutate in mutations:
            value, probe, challenge = fixtures()
            mutate(value, probe, challenge)
            with self.subTest(label=label), self.assertRaises(ValueError):
                validate_adjudications(value, probe, challenge)

    def test_adjudications_are_a_pinned_permission_input(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _copy_gate_inputs(root)
            build_development_status(root)
            adjudications = json.loads(
                (root / ADJUDICATIONS).read_text(encoding="utf-8")
            )
            _case(adjudications, "M0106")["resolution"] += " Harmless wording edit."
            _write_json(root / ADJUDICATIONS, adjudications)
            with self.assertRaisesRegex(ValueError, "review input changed"):
                build_development_status(root)

    def test_direct_pin_refresh_cannot_bypass_source_challenge_review(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _copy_gate_inputs(root)
            crosswalk = json.loads((root / CROSSWALK).read_text(encoding="utf-8"))
            crosswalk["rows"][0]["rationale"] += (
                " Semantically valid but not challenge-reviewed."
            )
            _write_json(root / CROSSWALK, crosswalk)
            _refresh_direct_binding(root, CROSSWALK)
            with self.assertRaisesRegex(
                ValueError, "source-challenge reviewed input changed"
            ):
                build_development_status(root)

    def test_operation_checks_rebuild_authority_and_remain_scoped(self) -> None:
        require_operation(ROOT, "corrected_crosswalk_development")
        require_operation(ROOT, "source_annotation", "M0064")
        require_operation(ROOT, "source_scoped_mechanism_draft", "M0106")
        with self.assertRaisesRegex(ValueError, "not authorized"):
            require_operation(ROOT, "source_scoped_mechanism_draft", "M0064")
        with self.assertRaisesRegex(ValueError, "not authorized"):
            require_operation(ROOT, "exact_reaction_instance", "M0106")
        with self.assertRaisesRegex(ValueError, "outside computational"):
            require_operation(ROOT, "gold_label_admission")


if __name__ == "__main__":
    unittest.main()
