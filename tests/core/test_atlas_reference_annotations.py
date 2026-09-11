"""Adversarial checks for entry-level reference mutagenesis annotations."""

from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import unittest

from catalytic_earth import core_cli
from catalytic_earth.atlas_fragment_sites import derive_fragment_site, query_fragment_sites
from catalytic_earth.atlas_mechanism_evidence import query_mechanism_evidence
from catalytic_earth.atlas_reference_annotations import reference_mutagenesis_context


ROOT = Path(__file__).resolve().parents[2]
ATLAS10 = ROOT / "src/catalytic_earth/atlas_data/atlas10_kernel.json"
MCSA = ROOT / "data/atlas/atlas10/sources/mcsa/M0187.json"
UNIPROT = ROOT / "data/atlas/atlas10/sources/uniprot/P11444.json"
SPEC = ROOT / "data/atlas/mechanism_evidence/source_fragment_spec.json"
PACKAGE = ROOT / "src/catalytic_earth/mechanism_evidence_data/source_fragments.json"
EVIDENCE = ROOT / "data/atlas/mechanism_evidence/m0187/evidence.json"
TRANSFORMATIONS = ROOT / "data/atlas/transformations/m0187/transformations.json"


def _records(bundle: dict) -> list[dict]:
    rows = list(bundle.get("records", [])) + list(bundle.get("follow_on_records", []))
    inherited = bundle.get("inherited_kernel")
    if isinstance(inherited, dict):
        rows.extend(_records(inherited))
    return rows


class ReferenceMutagenesisContextTests(unittest.TestCase):
    def setUp(self) -> None:
        atlas10 = json.loads(ATLAS10.read_text(encoding="utf-8"))
        [self.record] = [
            row for row in _records(atlas10)
            if row.get("record_id") == "mechanism:mandelate-racemase-pputida-enolate-v1"
            and row.get("evidence_tier") == 2
        ]
        [proposal] = [
            row for row in self.record["mechanism_proposals"]
            if row.get("source_record_id") == "M0187"
            and row.get("source_mechanism_id") == 1
        ]
        self.step = next(
            row for row in proposal["mechanism_steps"] if row["source_step_id"] == 1
        )
        self.mcsa = json.loads(MCSA.read_text(encoding="utf-8"))
        self.snapshot_utf8 = UNIPROT.read_text(encoding="utf-8")
        spec = json.loads(SPEC.read_text(encoding="utf-8"))
        [self.binding] = spec["reference_annotation_sources"]
        self.his = derive_fragment_site(self.mcsa, self.record, self.step, "a58")
        self.glu = derive_fragment_site(self.mcsa, self.record, self.step, "a63")

    def context(
        self, relation: dict, feature_index: int, *, snapshot_utf8: str | None = None,
        binding: dict | None = None, record: dict | None = None,
    ) -> dict:
        return reference_mutagenesis_context(
            record=self.record if record is None else record,
            step=self.step,
            label=relation["source_residue_label"],
            mcsa_id="M0187",
            binding=self.binding if binding is None else binding,
            snapshot_utf8=self.snapshot_utf8 if snapshot_utf8 is None else snapshot_utf8,
            feature_index=feature_index,
        )

    def repinned_snapshot(self, source: dict) -> tuple[str, dict, dict]:
        snapshot = json.dumps(source, ensure_ascii=False, separators=(",", ":"))
        digest = hashlib.sha256(snapshot.encode("utf-8")).hexdigest()
        binding = copy.deepcopy(self.binding)
        binding["sha256"] = digest
        record = copy.deepcopy(self.record)
        [evidence] = [
            row for row in record["evidence"]
            if row.get("evidence_id") == "source:UniProtKB:P11444"
        ]
        evidence["snapshot_sha256"] = digest
        return snapshot, binding, record

    def test_e317_annotation_is_record_scope_without_step_or_quantity_promotion(self) -> None:
        self.assertEqual(self.step["catalyst_site_ids"], ["P11444:H297"])
        self.assertIsNone(self.glu["source_record_residue_mapping"]["site_id"])

        result = self.context(self.glu, 9)

        self.assertEqual(result["status"], "source_database_annotation_at_reference_site")
        self.assertFalse(result["selected_step_declares_site"])
        self.assertEqual(
            (result["reference_site_mapping"]["status"],
             result["reference_site_mapping"]["site_id"]),
            ("unique_record_site_match", "P11444:E317"),
        )
        annotation = result["annotation"]
        self.assertEqual(
            (annotation["uniprot_id"], annotation["site_id"], annotation["feature_index"]),
            ("P11444", "P11444:E317", 9),
        )
        self.assertEqual(annotation["feature"]["type"], "Mutagenesis")
        self.assertEqual(annotation["feature"]["location"], {
            "start": {"value": 317, "modifier": "EXACT"},
            "end": {"value": 317, "modifier": "EXACT"},
        })
        self.assertEqual(annotation["feature"]["alternativeSequence"], {
            "originalSequence": "E", "alternativeSequences": ["Q"],
        })
        self.assertEqual(annotation["feature"]["description"],
                         "Reduces activity 10000-fold.")
        self.assertEqual(annotation["feature"]["evidences"], [
            {"evidenceCode": "ECO:0000269", "source": "PubMed", "id": "7893689"},
        ])
        self.assertEqual((annotation["entry_audit"]["entryVersion"],
                          annotation["entry_audit"]["sequenceVersion"]), (141, 1))
        [reference] = annotation["cited_reference_metadata"]
        self.assertTrue(any(
            row == {"database": "PubMed", "id": "7893689"}
            for row in reference["citation"]["citationCrossReferences"]
        ))
        self.assertEqual(annotation["interpreted_quantity"], {
            "status": "not_assessed_from_database_annotation",
            "endpoint": None,
            "parameter": None,
            "value": None,
            "unit": None,
            "denominator": None,
            "reaction_direction": None,
            "assay_conditions": None,
            "uncertainty": None,
        })
        self.assertFalse(annotation["exact_assayed_construct_identity"])
        self.assertEqual(annotation["evidence_basis"],
                         "retained_uniprot_database_annotation")
        self.assertFalse(annotation["primary_result_details_supplied_by_annotation"])
        self.assertFalse(annotation["source_arrow_experimentally_validated"])
        self.assertFalse(annotation["source_residue_roles_assign_atom_role"])

    def test_coarse_h297_loss_annotation_cannot_erase_retained_activity(self) -> None:
        result = self.context(self.his, 8)

        self.assertTrue(result["selected_step_declares_site"])
        self.assertEqual(result["reference_site_mapping"]["site_id"], "P11444:H297")
        annotation = result["annotation"]
        self.assertEqual(annotation["feature"]["description"], "Loss of activity.")
        self.assertEqual(annotation["feature"]["alternativeSequence"], {
            "originalSequence": "H", "alternativeSequences": ["N"],
        })
        self.assertIsNone(annotation["interpreted_quantity"]["parameter"])
        self.assertIsNone(annotation["interpreted_quantity"]["value"])
        self.assertIsNone(annotation["interpreted_quantity"]["denominator"])

    def test_snapshot_index_sequence_and_citation_joins_fail_closed(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "reference annotation is not an exact point-mutagenesis feature at this site",
        ):
            self.context(self.glu, 8)

        # Binding-site feature 6 has the same position/PMID but is not mutagenesis.
        with self.assertRaisesRegex(ValueError, "not an exact point-mutagenesis feature"):
            self.context(self.glu, 6)

        wrong_chain = copy.deepcopy(self.glu)
        wrong_chain["source_residue_label"]["residue_label"]["author_chain_id"] = "B"
        unresolved = self.context(wrong_chain, 9)
        self.assertEqual(unresolved["status"], "not_resolved")
        self.assertIsNone(unresolved["annotation"])
        self.assertIn("no_record_site_matches", unresolved["reason"])

        source = json.loads(self.snapshot_utf8)
        sequence = source["sequence"]["value"]
        source["sequence"]["value"] = sequence[:316] + "Q" + sequence[317:]
        snapshot, binding, record = self.repinned_snapshot(source)
        with self.assertRaisesRegex(
            ValueError, "reference annotation wild-type residue or sequence differs",
        ):
            self.context(self.glu, 9, snapshot_utf8=snapshot, binding=binding, record=record)

        source = json.loads(self.snapshot_utf8)
        source["features"][9]["evidences"][0]["id"] = "missing-reference"
        snapshot, binding, record = self.repinned_snapshot(source)
        with self.assertRaisesRegex(
            ValueError, "reference annotation citation is absent or ambiguous",
        ):
            self.context(self.glu, 9, snapshot_utf8=snapshot, binding=binding, record=record)

        source = json.loads(self.snapshot_utf8)
        del source["features"][9]["evidences"][0]["id"]
        snapshot, binding, record = self.repinned_snapshot(source)
        with self.assertRaisesRegex(ValueError, "reference annotation lacks source evidence"):
            self.context(self.glu, 9, snapshot_utf8=snapshot, binding=binding, record=record)

        altered = self.snapshot_utf8.replace("Reduces activity 10000-fold.",
                                             "Reduces activity.")
        with self.assertRaisesRegex(ValueError, "reference annotation source hash differs"):
            self.context(self.glu, 9, snapshot_utf8=altered)


class ReferenceAnnotationIntegratedQueryTests(unittest.TestCase):
    def command(self, *args: str) -> dict:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(core_cli.main(["atlas-mechanism-evidence", *args]), 0)
        return json.loads(output.getvalue())

    @staticmethod
    def relation(result: dict, atom_id: str) -> dict:
        return next(
            row for row in result["source_fragment_query"]["relations"]
            if row["source_step_id"] == 1 and row["source_atom_id"] == atom_id
        )

    def test_annotations_do_not_change_selected_step_or_observation_planes(self) -> None:
        baseline = self.command()
        included = self.command("--include-source-fragments")
        query = included.pop("source_fragment_query")

        self.assertEqual(included, baseline)
        self.assertEqual(
            (query["relation_count"], query["resolved_relation_count"],
             query["reference_annotation_count"]),
            (3, 2, 2),
        )
        glu = self.relation({"source_fragment_query": query}, "a63")
        self.assertIsNone(glu["source_record_residue_mapping"]["site_id"])
        self.assertEqual(glu["functional_evidence"]["matched_observations"], [])
        self.assertEqual(
            glu["reference_annotation_context"]["reference_site_mapping"]["site_id"],
            "P11444:E317",
        )
        self.assertFalse(
            glu["reference_annotation_context"]["selected_step_declares_site"]
        )

        his = self.relation({"source_fragment_query": query}, "a58")
        self.assertEqual(his["source_record_residue_mapping"]["site_id"], "P11444:H297")
        self.assertTrue(his["reference_annotation_context"]["selected_step_declares_site"])
        observations = his["functional_evidence"]["matched_observations"]
        retained = next(row for row in observations
                        if row["observation_id"] == "H297N-S-exchange")
        self.assertEqual(retained["result"]["result_class"], "measured")
        self.assertEqual(retained["result"]["reported_relation"],
                         "fold_lower_than_wild_type")
        self.assertEqual(retained["result"]["value"], 3.3)
        self.assertEqual(
            his["reference_annotation_context"]["annotation"]["feature"]["description"],
            "Loss of activity.",
        )

        semantics = query["query_semantics"]
        self.assertEqual(
            semantics["reference_annotation_scope"],
            "whole_record_site_not_selected_step_catalyst_or_measured_observation",
        )
        self.assertFalse(semantics["observation_filters_apply_to_reference_annotations"])
        self.assertFalse(semantics["database_activity_text_is_numeric_kinetic_parameter"])
        self.assertEqual(
            semantics["reference_annotation_count_unit"],
            "distinct_source_snapshot_features_not_attachments_or_observations",
        )

    def test_observation_filters_leave_both_database_annotations_in_context(self) -> None:
        result = self.command(
            "--variant", "H297N", "--endpoint", "isotope_exchange",
            "--include-source-fragments",
        )
        query = result["source_fragment_query"]
        self.assertEqual(query["reference_annotation_count"], 2)
        self.assertIsNotNone(self.relation(result, "a58")["reference_annotation_context"])
        glu = self.relation(result, "a63")
        self.assertIsNotNone(glu["reference_annotation_context"])
        self.assertEqual(glu["functional_evidence"]["matched_observations"], [])


class ReferenceAnnotationBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.bundle = json.loads(PACKAGE.read_text(encoding="utf-8"))
        self.atlas10 = json.loads(ATLAS10.read_text(encoding="utf-8"))
        self.transformations = {
            "M0187": json.loads(TRANSFORMATIONS.read_text(encoding="utf-8")),
        }
        self.evidence_query = query_mechanism_evidence(
            json.loads(EVIDENCE.read_text(encoding="utf-8")),
            atlas10_bundle=self.atlas10,
            transformation_values=self.transformations,
        )

    @staticmethod
    def canonical_sha256(value: dict) -> str:
        encoded = json.dumps(
            value, ensure_ascii=True, allow_nan=False,
            separators=(",", ":"), sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    @classmethod
    def repin_review(cls, bundle: dict) -> None:
        bundle["review"]["spec_sha256"] = cls.canonical_sha256(bundle["spec"])

    def query(self, bundle: dict) -> dict:
        return query_fragment_sites(
            bundle,
            atlas10_bundle=self.atlas10,
            evidence_query=self.evidence_query,
            transformation_values=self.transformations,
        )

    def test_reference_sources_must_be_unique_packaged_and_selected(self) -> None:
        duplicate = copy.deepcopy(self.bundle)
        duplicate["spec"]["reference_annotation_sources"].append(copy.deepcopy(
            duplicate["spec"]["reference_annotation_sources"][0]
        ))
        self.repin_review(duplicate)
        with self.assertRaisesRegex(
            ValueError, "reference annotation source bindings repeat or differ",
        ):
            self.query(duplicate)

        missing_snapshot = copy.deepcopy(self.bundle)
        missing_snapshot["reference_snapshots_utf8"].clear()
        with self.assertRaisesRegex(
            ValueError, "reference annotation source bindings repeat or differ",
        ):
            self.query(missing_snapshot)

        unselected = copy.deepcopy(self.bundle)
        for request in unselected["spec"]["requests"]:
            request.pop("reference_annotation", None)
        self.repin_review(unselected)
        with self.assertRaisesRegex(
            ValueError, "reference annotation source is unselected or unbound",
        ):
            self.query(unselected)

    def test_reference_selectors_reject_extra_fields_and_unbound_sources(self) -> None:
        extra_field = copy.deepcopy(self.bundle)
        extra_field["spec"]["requests"][0]["reference_annotation"]["pmid"] = "1909893"
        self.repin_review(extra_field)
        with self.assertRaisesRegex(ValueError, "reference annotation selector is invalid"):
            self.query(extra_field)

        negative_index = copy.deepcopy(self.bundle)
        negative_index["spec"]["requests"][0]["reference_annotation"]["feature_index"] = -1
        self.repin_review(negative_index)
        with self.assertRaisesRegex(ValueError, "reference annotation selector is invalid"):
            self.query(negative_index)

        unbound = copy.deepcopy(self.bundle)
        unbound["spec"]["requests"][0]["reference_annotation"]["source_id"] = (
            "UniProtKB:UNBOUND"
        )
        self.repin_review(unbound)
        with self.assertRaisesRegex(
            ValueError, "reference annotation source is unselected or unbound",
        ):
            self.query(unbound)

    def test_annotation_count_is_distinct_source_feature_not_attachment_count(self) -> None:
        duplicated_attachment = copy.deepcopy(self.bundle)
        request = copy.deepcopy(duplicated_attachment["spec"]["requests"][0])
        request["relation_id"] += ":second-attachment"
        duplicated_attachment["spec"]["requests"].append(request)
        self.repin_review(duplicated_attachment)

        result = self.query(duplicated_attachment)

        self.assertEqual(result["relation_count"], 4)
        self.assertEqual(sum(
            row.get("reference_annotation_context", {}).get("annotation") is not None
            for row in result["relations"]
        ), 3)
        self.assertEqual(result["reference_annotation_count"], 2)


if __name__ == "__main__":
    unittest.main()
