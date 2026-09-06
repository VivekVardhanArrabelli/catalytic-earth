from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from catalytic_earth import core_cli
from catalytic_earth.atlas_reaction_correspondence import (
    canonical_reaction_correspondence_payload_sha256,
    validate_reaction_correspondence,
)


ROOT = Path(__file__).resolve().parents[2]
SIDECAR_PATH = (
    ROOT
    / "data/atlas/source_drafts/batches/plp-pyruvoyl/review/"
    "reaction_correspondence_annotations.json"
)


def _binding(sidecar: dict, artifact_kind: str) -> dict:
    rows = [
        row for row in sidecar["source_bindings"]
        if row["artifact_kind"] == artifact_kind
    ]
    if len(rows) != 1:
        raise AssertionError(f"expected one {artifact_kind} binding")
    return rows[0]


def _repin_review(sidecar: dict) -> None:
    sidecar["review"]["annotation_payload_sha256"] = (
        canonical_reaction_correspondence_payload_sha256(sidecar)
    )


class ReactionCorrespondenceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = core_cli.verified_source_drafts("plp-pyruvoyl")
        cls.sidecar = json.loads(SIDECAR_PATH.read_text(encoding="utf-8"))

    def validate(self, sidecar: dict, *, repo_root: Path | None = None) -> dict:
        return validate_reaction_correspondence(
            sidecar, bundle=self.bundle, repo_root=repo_root,
        )

    def test_reviewed_sidecar_validates_against_exact_retained_sources(self) -> None:
        summary = self.validate(self.sidecar, repo_root=ROOT)
        self.assertEqual(summary["annotation_count"], 1)
        self.assertEqual(summary["record_count"], 1)
        self.assertEqual(
            summary["record_ids"],
            ["atlas50-draft:m0213:source-scoped-mechanism-draft"],
        )
        annotation = self.sidecar["annotations"][0]
        self.assertEqual(
            annotation["source_direction"]["record_cross_reference"]["scope"],
            "source_record_only",
        )
        self.assertTrue(all(value is False for value in annotation["scope_effect"].values()))

    def test_direction_and_proposal_witness_cannot_be_reversed_or_promoted(self) -> None:
        cases = []

        reverse = copy.deepcopy(self.sidecar)
        reverse["annotations"][0]["curated_reaction"]["selected_directed_id"] = (
            "RHEA:20251"
        )
        cases.append((reverse, "left-to-right"))

        promoted = copy.deepcopy(self.sidecar)
        promoted["annotations"][0]["source_direction"]["record_cross_reference"][
            "grounds_proposal"
        ] = True
        cases.append((promoted, "overstates"))

        reverse_sentence = copy.deepcopy(self.sidecar)
        reverse_sentence["annotations"][0]["source_direction"][
            "proposal_declared_direction"
        ]["exact_text"] = (
            "In the D-Ala to L-Ala direction, the roles of Tyr265B and Lys39 "
            "are reversed."
        )
        cases.append((reverse_sentence, "direction witness differs"))

        for changed, message in cases:
            with self.subTest(message=message):
                _repin_review(changed)
                with self.assertRaisesRegex(ValueError, message):
                    self.validate(changed)

    def test_source_participant_identity_and_stoichiometry_remain_exact(self) -> None:
        cases = []
        changed_identity = copy.deepcopy(self.sidecar)
        changed_identity["annotations"][0]["curated_reaction"][
            "left_participants"
        ][0]["chebi_id"] = "CHEBI:57416"
        cases.append(changed_identity)

        changed_stoichiometry = copy.deepcopy(self.sidecar)
        changed_stoichiometry["annotations"][0]["curated_reaction"][
            "right_participants"
        ][0]["stoichiometry"] = 2
        cases.append(changed_stoichiometry)

        for changed in cases:
            with self.subTest(change=changed["annotations"][0]["curated_reaction"]):
                _repin_review(changed)
                with self.assertRaisesRegex(ValueError, "participants differ"):
                    self.validate(changed)

    def test_terminal_conflict_abstentions_and_scope_cannot_be_erased(self) -> None:
        relabeled = copy.deepcopy(self.sidecar)
        relabeled["annotations"][0]["terminal_depiction"][
            "alanine_fragment_raw_source_labels"
        ] = ["chebi:57416"]

        dropped = copy.deepcopy(self.sidecar)
        dropped["annotations"][0]["required_abstentions"].remove(
            "terminal_product_identity"
        )

        promoted = copy.deepcopy(self.sidecar)
        promoted["annotations"][0]["scope_effect"][
            "source_step_trajectory_validated"
        ] = True

        for changed, message in (
            (relabeled, "source-label/product conflict"),
            (dropped, "required_abstentions differ"),
            (promoted, "expand the source draft"),
        ):
            with self.subTest(message=message):
                _repin_review(changed)
                with self.assertRaisesRegex(ValueError, message):
                    self.validate(changed)

    def _correlated_repin(self, mutate) -> tuple[dict, tempfile.TemporaryDirectory, Path]:
        sidecar = copy.deepcopy(self.sidecar)
        annotation = sidecar["annotations"][0]
        projection_binding = _binding(sidecar, "project_reaction_projection")
        projection = json.loads(
            (ROOT / projection_binding["path"]).read_text(encoding="utf-8")
        )
        mutate(annotation, projection)

        temp = tempfile.TemporaryDirectory()
        temp_root = Path(temp.name)
        for binding in sidecar["source_bindings"]:
            source = ROOT / binding["path"]
            target = temp_root / binding["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

        projection_path = temp_root / projection_binding["path"]
        projection_path.write_text(
            json.dumps(projection, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        projection_sha = hashlib.sha256(projection_path.read_bytes()).hexdigest()
        projection_binding["sha256"] = projection_sha
        annotation["projection_binding"]["sha256"] = projection_sha
        _repin_review(sidecar)
        return sidecar, temp, temp_root

    def test_correlated_repin_cannot_reverse_the_raw_rhea_equation(self) -> None:
        def mutate(annotation: dict, projection: dict) -> None:
            for row in (annotation, projection):
                row["curated_reaction"]["directed_equation"] = (
                    "D-alanine => L-alanine"
                )

        changed, temp, temp_root = self._correlated_repin(mutate)
        self.addCleanup(temp.cleanup)
        # The internally consistent project layers and refreshed review pin pass
        # without retained sources; the official RDF still rejects the false claim.
        self.validate(changed)
        with self.assertRaisesRegex(ValueError, "Rhea RDF lacks"):
            self.validate(changed, repo_root=temp_root)

    def test_correlated_repin_cannot_swap_curated_participant_stereo(self) -> None:
        def mutate(annotation: dict, projection: dict) -> None:
            edges = (
                annotation["projection_excerpt"]["support_edges"],
                projection["support_edges"],
            )
            for rows in edges:
                edge = next(
                    row for row in rows
                    if row["edge_id"] == "edge:rhea-participant-forms"
                )
                participant = next(
                    row for row in edge["extracted_values"]["participants"]
                    if row["chebi_id"] == "CHEBI:57416"
                )
                participant["alpha_c_n_mdl_stereo_code"] = 1

        changed, temp, temp_root = self._correlated_repin(mutate)
        self.addCleanup(temp.cleanup)
        self.validate(changed)
        with self.assertRaisesRegex(ValueError, "participant structure facts differ"):
            self.validate(changed, repo_root=temp_root)

    def test_correlated_repin_cannot_normalize_endpoint_charge_or_cip(self) -> None:
        def changed_charge(annotation: dict, projection: dict) -> None:
            for row in (annotation, projection):
                row["terminal_depiction"]["endpoint_diagnostic"]["initial"][
                    "fragment_formal_charge"
                ] = 0

        sidecar, temp, temp_root = self._correlated_repin(changed_charge)
        self.addCleanup(temp.cleanup)
        self.validate(sidecar)
        with self.assertRaisesRegex(ValueError, "fragment charge differs"):
            self.validate(sidecar, repo_root=temp_root)

        def changed_cip(annotation: dict, projection: dict) -> None:
            for row in (annotation, projection):
                diagnostic = row["terminal_depiction"]["endpoint_diagnostic"]
                diagnostic["initial"]["computed_cip"] = "S"
                diagnostic["terminal"]["computed_cip"] = "R"

        sidecar, temp, temp_root = self._correlated_repin(changed_cip)
        self.addCleanup(temp.cleanup)
        self.validate(sidecar)
        with self.assertRaisesRegex(ValueError, "computational .* endpoint diagnostic differs"):
            self.validate(sidecar, repo_root=temp_root)

    def test_correlated_repin_cannot_remove_step3_trajectory_counterexample(self) -> None:
        def mutate(annotation: dict, projection: dict) -> None:
            for row in (annotation, projection):
                row["terminal_depiction"]["step_3_exception"]["computed_cip"] = "R"

        changed, temp, temp_root = self._correlated_repin(mutate)
        self.addCleanup(temp.cleanup)
        self.validate(changed)
        with self.assertRaisesRegex(ValueError, "Step3 exception diagnostic differs"):
            self.validate(changed, repo_root=temp_root)

    def test_bound_source_hash_rejects_changed_raw_bytes(self) -> None:
        sidecar = copy.deepcopy(self.sidecar)
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        temp_root = Path(temp.name)
        for binding in sidecar["source_bindings"]:
            source = ROOT / binding["path"]
            target = temp_root / binding["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        raw_binding = _binding(sidecar, "official_reaction_cross_reference_map")
        changed_path = temp_root / raw_binding["path"]
        changed_path.write_bytes(changed_path.read_bytes() + b"\n")
        with self.assertRaisesRegex(ValueError, "source hash differs"):
            self.validate(sidecar, repo_root=temp_root)


if __name__ == "__main__":
    unittest.main()
