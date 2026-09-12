"""False joins and evidence promotion across reference and primary evidence planes."""
from copy import deepcopy
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from catalytic_earth.atlas_perturbations import _project_candidate, project
from catalytic_earth.atlas_reference_outcomes import (
    SPEC_PATH, REVIEW_PATH, _acceptance_payload, _bound, _compose, _fragment_query,
    _join, _raw, query_reference_outcomes,
)

ROOT = Path(__file__).resolve().parents[2]


class ReferenceOutcomeTests(unittest.TestCase):
    @contextmanager
    def reviewed_projection(self, projection):
        """Controlled globally accepted input; all actual project() checks still run."""
        projection_path = ROOT / "data/atlas/perturbations/projection.json"
        review_path = ROOT / "data/atlas/perturbations/review.json"
        raw = (json.dumps(projection, indent=2) + "\n").encode()
        review = json.loads(review_path.read_text())
        review["reviewed_bindings"]["data/atlas/perturbations/projection.json"] = hashlib.sha256(raw).hexdigest()
        replacements = {projection_path: raw, review_path: json.dumps(review).encode()}
        original_bytes, original_text = Path.read_bytes, Path.read_text
        def read_bytes(path):
            return replacements[path] if path in replacements else original_bytes(path)
        def read_text(path, *args, **kwargs):
            return replacements[path].decode() if path in replacements else original_text(path, *args, **kwargs)
        with patch.object(Path, "read_bytes", read_bytes), patch.object(Path, "read_text", read_text):
            yield

    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads((ROOT / SPEC_PATH).read_text(encoding="utf-8"))
        cls.view = _project_candidate(ROOT)
        cls.link = cls.spec["links"][0]
        cls.fragments = _fragment_query(ROOT, cls.spec["fragment_contexts"][cls.link["fragment_context_id"]])
        cls.fragment = next(row for row in cls.fragments["relations"]
                            if row["relation_id"] == cls.link["fragment_relation_id"])
        cls.sources = {key: _bound(ROOT, cls.view["sources"][key])
                       for key in cls.link["outcome_sources"]}
        cls.sources["reference_snapshot"] = _bound(
            ROOT, cls.sources[cls.link["primary_source"]]["reference_site_context"]["source_binding"])

    def candidate(self, **overrides):
        values = {"link": self.link, "fragment": self.fragment,
                  "view": self.view, "sources": self.sources}
        values.update(overrides)
        return _join(**values)

    def test_integrated_answer_reuses_rows_and_preserves_step_and_endpoint_limits(self):
        before = deepcopy(self.view)
        result = self.candidate()
        self.assertEqual(self.view, before)
        self.assertEqual(result["variant"], "E317Q")
        self.assertEqual(result["citation_match"], {"PubMed": "7893689", "DOI": "10.1021/bi00009a006"})
        self.assertFalse(result["selected_step_declares_site"])
        self.assertIsNone(result["fragment_relation"]["source_record_residue_mapping"]["site_id"])
        self.assertEqual(result["fragment_relation"]["functional_evidence"]["matched_observations"], [])
        self.assertFalse(result["exact_assayed_construct_identity"])
        self.assertFalse(result["deposited_atom_identity"])
        self.assertFalse(result["source_arrow_experimentally_validated"])
        self.assertFalse(result["new_arithmetic_performed"])
        observations = result["matched_observations"]
        self.assertEqual(len(observations), 4)
        self.assertEqual(len({row["id"] for row in observations}), 4)
        self.assertEqual(sorted(row["value"] for row in observations if row["result_kind"] == "numeric"), [4500, 29000])
        self.assertEqual({row["result_kind"] for row in observations}, {"numeric", "qualitative", "nondetection"})
        original = {row["id"]: row for row in self.view["observations"]}
        self.assertTrue(all(row == original[row["id"]] for row in observations))
        comparisons = {row["id"]: row for row in self.view["comparisons"]}
        self.assertTrue(all(row == comparisons[row["id"]] for row in result["comparisons"]))
        self.assertEqual(result["fragment_relation"], self.fragment)

    def test_identity_mismatch_cannot_join_by_variant_label_alone(self):
        changes = {"uniprot_id": "P00000", "sequence_position": 316,
                   "reference_residue": "D", "alternative_residue": "N",
                   "feature_index": 8, "reference_index": 4,
                   "reference_site_id": "P11444:H297"}
        for key, value in changes.items():
            with self.subTest(field=key):
                sources = deepcopy(self.sources)
                sources[self.link["primary_source"]]["reference_site_context"][key] = value
                with self.assertRaises(ValueError):
                    self.candidate(sources=sources)
        for key, value in (("pmid", "7893690"), ("doi", "10.1021/bi00009a007")):
            with self.subTest(citation=key):
                sources = deepcopy(self.sources)
                sources[self.link["primary_source"]]["source"][key] = value
                with self.assertRaises(ValueError):
                    self.candidate(sources=sources)

    def test_endpoint_wrapper_must_bind_same_primary_and_construct(self):
        mutations = [
            lambda d: d.update(study_id="another-study"),
            lambda d: d["source_binding"].update(sha256="0" * 64),
            lambda d: d.update(source_pointer="/excluded_context"),
            lambda d: d["construct_context"].update(pointer="/constructs/0"),
            lambda d: d["construct_context"]["source_binding"].update(sha256="0" * 64),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                sources = deepcopy(self.sources)
                mutation(sources["mr1995e317q_endpoints"])
                with self.assertRaises(ValueError):
                    self.candidate(sources=sources)

    def test_reference_citation_must_be_unique_and_feature_bound(self):
        fragment = deepcopy(self.fragment)
        fragment["reference_annotation_context"]["annotation"]["feature"]["evidences"][0]["id"] = "7893690"
        with self.assertRaises(ValueError):
            self.candidate(fragment=fragment)
        sources = deepcopy(self.sources)
        reference = sources["reference_snapshot"]["references"][5]
        reference["citation"]["citationCrossReferences"].append({"database": "PubMed", "id": "7893689"})
        with self.assertRaises(ValueError):
            self.candidate(sources=sources)

    def test_grouped_alternatives_and_disconnected_citation_wrapper_are_rejected(self):
        fragment = deepcopy(self.fragment)
        fragment["reference_annotation_context"]["annotation"]["feature"]["alternativeSequence"]["alternativeSequences"] = ["Q", "N"]
        with self.assertRaises(ValueError):
            self.candidate(fragment=fragment)
        sources = deepcopy(self.sources)
        primary = sources[self.link["primary_source"]]
        primary["other"] = deepcopy(primary["source"])
        link = deepcopy(self.link)
        link["primary_source_pointer"] = "/other"
        with self.assertRaises(ValueError):
            self.candidate(link=link, sources=sources)

    def test_arithmetic_and_changed_outcome_membership_cannot_hide_in_context(self):
        for change in ("arithmetic", "missing-outcome"):
            with self.subTest(change=change):
                view = deepcopy(self.view)
                context = next(row for row in view["comparisons"] if row["id"] == self.link["comparison_ids"][0])
                if change == "arithmetic":
                    context.update(operation="ratio", eligible=True, value=2.0)
                else:
                    context["context_observations"].pop()
                with self.assertRaises(ValueError):
                    self.candidate(view=view)

    def test_comparison_cannot_import_another_study_construct_or_perturbation(self):
        outcome_id = self.candidate()["matched_observations"][0]["id"]
        for key, value in (("study_id", "another-study"), ("construct_id", "mandelate_1995_e317q:WT"),
                           ("perturbation", ["E317Q", "H297N"])):
            with self.subTest(field=key):
                view = deepcopy(self.view)
                row = next(row for row in view["observations"] if row["id"] == outcome_id)
                row[key] = value
                with self.assertRaises(ValueError):
                    self.candidate(view=view)
        view = deepcopy(self.view)
        view["constructs"][self.link["construct_id"]]["perturbation"] = ["E317Q", "H297N"]
        with self.assertRaises(ValueError):
            self.candidate(view=view)

    def test_unmapped_reference_or_unknown_comparison_fails_closed(self):
        fragment = deepcopy(self.fragment)
        fragment["reference_annotation_context"]["status"] = "not_resolved"
        with self.assertRaises(ValueError):
            self.candidate(fragment=fragment)
        for ids in ([], ["unknown"], self.link["comparison_ids"] * 2):
            with self.subTest(ids=ids):
                link = deepcopy(self.link)
                link["comparison_ids"] = ids
                with self.assertRaises(ValueError):
                    self.candidate(link=link)

    def test_no_declared_join_is_not_absence_of_function(self):
        result = _compose(ROOT, self.spec, self.view, "P11444:H297")
        self.assertEqual(result["matches"], [])
        self.assertEqual(result["empty_match"], "no_declared_reviewed_join_not_absence_of_functional_evidence")

    def test_stale_source_package_and_reviewed_code_fail_closed(self):
        context = deepcopy(self.spec["fragment_contexts"][self.link["fragment_context_id"]])
        context["fragment_bundle"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "source binding differs"):
            _fragment_query(ROOT, context)
        def changed_code(root, relative):
            raw = _raw(root, relative)
            return raw + b"\n" if relative == "src/catalytic_earth/atlas_reference_outcomes.py" else raw
        with patch("catalytic_earth.atlas_reference_outcomes._raw", side_effect=changed_code):
            with self.assertRaisesRegex(ValueError, "review binding differs"):
                query_reference_outcomes(ROOT, site_id="P11444:E317")

    def test_reviewed_public_query_and_cli_filter_semantics(self):
        result = query_reference_outcomes(ROOT, site_id="P11444:E317")
        self.assertEqual(result["relation_count"], 1)
        self.assertEqual(len(result["source_witnesses"]), 1)
        run = subprocess.run([sys.executable, str(ROOT / "scripts/query_atlas_perturbations.py"),
                              "--reference-site", "P11444:E317", "--check"],
                             cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["projected_outcomes"], 4)
        empty = subprocess.run([sys.executable, str(ROOT / "scripts/query_atlas_perturbations.py"),
                                "--reference-site", "P11444:H297", "--check"],
                               cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(empty.returncode, 0, empty.stderr)
        self.assertEqual(json.loads(empty.stdout)["relation_count"], 0)
        self.assertEqual(json.loads(empty.stdout)["empty_match"], result["empty_match"])
        bad = subprocess.run([sys.executable, str(ROOT / "scripts/query_atlas_perturbations.py"),
                              "--reference-site", "P11444:E317", "--study", "mandelate_1995_e317q"],
                             cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn("do not combine selection filters", bad.stderr)

    def test_unrelated_cryoannealing_addition_preserves_local_acceptance(self):
        before = json.loads((ROOT / "data/atlas/perturbations/projection.json").read_text())
        before["panels"] = [row for row in before["panels"] if row["id"] != "nitrogenase2016-cryoannealing"]
        before["model_links"] = [row for row in before["model_links"]
                                 if row["id"] != "nitrogenase_2016:WT:cryoannealing_state_coupling"]
        with self.reviewed_projection(before):
            view = project(ROOT)
            self.assertEqual(len(view["observations"]), len(self.view["observations"]) - 2)
            old = query_reference_outcomes(ROOT, site_id="P11444:E317")
        current = query_reference_outcomes(ROOT, site_id="P11444:E317")
        self.assertEqual(old["matches"], current["matches"])
        self.assertEqual(old["review"], current["review"])

    def test_selected_output_assay_interpretation_and_witness_changes_require_review(self):
        outcome_id = self.link["observation_ids"][0]
        assay_id = next(row["assay_id"] for row in self.view["observations"] if row["id"] == outcome_id)
        for change in ("value", "endpoint", "assay", "background", "interpretation", "witness"):
            for site in (None, "P11444:E317", "P11444:H297"):
                with self.subTest(change=change, filter=site):
                    view = deepcopy(self.view)
                    row = next(row for row in view["observations"] if row["id"] == outcome_id)
                    if change == "value":
                        row["value"] += 1
                    elif change == "endpoint":
                        row["endpoint_kind"] = "changed_endpoint"
                    elif change == "assay":
                        view["assays"][assay_id]["qualification_scope"] = "changed interpretation"
                    elif change == "background":
                        view["constructs"][row["background_id"]]["identity_scope"] = "changed background"
                    elif change == "interpretation":
                        view["evidence_context"][self.link["primary_source"]].append("changed interpretation")
                    else:
                        witness = next(item for item in view["source_witnesses"]
                                       if any(ref["source"] == self.link["primary_source"]
                                              for ref in item["source_bindings"]))
                        witness["source_url"] = "https://example.invalid/changed-witness"
                    with patch("catalytic_earth.atlas_reference_outcomes.project", return_value=view):
                        with self.assertRaisesRegex(ValueError, "scientific composition differs"):
                            query_reference_outcomes(ROOT, site_id=site)

    def test_globally_reviewed_selected_assay_change_still_requires_local_review(self):
        projection = json.loads((ROOT / "data/atlas/perturbations/projection.json").read_text())
        assay_id = next(row["assay_id"] for row in self.view["observations"]
                        if row["id"] == self.link["observation_ids"][0])
        projection["assays"][assay_id]["qualification_scope"] = "changed interpretation"
        with self.reviewed_projection(projection):
            changed = project(ROOT)
            self.assertEqual(_compose(ROOT, self.spec, changed), _compose(ROOT, self.spec, self.view))
            for site in ("P11444:E317", "P11444:H297"):
                with self.assertRaisesRegex(ValueError, "scientific composition differs"):
                    query_reference_outcomes(ROOT, site_id=site)

    def test_unrelated_context_sharing_reference_source_does_not_expand_acceptance(self):
        projection = json.loads((ROOT / "data/atlas/perturbations/projection.json").read_text())
        projection["evidence_context"]["unrelated-reference-context"] = [
            {"source": "mr_reference", "pointer": "/features/8"}]
        expected = query_reference_outcomes(ROOT, site_id="P11444:E317")
        with self.reviewed_projection(projection):
            self.assertIn("unrelated-reference-context", project(ROOT)["evidence_context"])
            actual = query_reference_outcomes(ROOT, site_id="P11444:E317")
        self.assertEqual(actual["matches"], expected["matches"])
        self.assertEqual(actual["review"], expected["review"])

    def test_output_fault_cannot_hide_behind_empty_filter(self):
        def changed_output(*args, **kwargs):
            result = _compose(*args, **kwargs)
            result["matches"][0]["identity_scope"] = "unreviewed output interpretation"
            return result
        with patch("catalytic_earth.atlas_reference_outcomes._compose", side_effect=changed_output):
            for site in ("P11444:E317", "P11444:H297"):
                with self.assertRaisesRegex(ValueError, "scientific composition differs"):
                    query_reference_outcomes(ROOT, site_id=site)

    def test_unrelated_witness_sharing_reference_source_does_not_expand_acceptance(self):
        projection = json.loads((ROOT / "data/atlas/perturbations/projection.json").read_text())
        expected = _acceptance_payload(_compose(ROOT, self.spec, self.view), self.view, projection)
        view = deepcopy(self.view)
        witness = deepcopy(view["source_witnesses"][0])
        witness["source_bindings"] = [{"source": "mr_reference", "pointer": "/features/8"}]
        view["source_witnesses"].append(witness)
        actual = _acceptance_payload(_compose(ROOT, self.spec, view), view, projection)
        self.assertEqual(actual, expected)

    def test_selected_scientific_review_records_remain_directly_bound(self):
        for name in ("source_review.json", "chemical_endpoints_review.json"):
            selected = "data/atlas/study_context/mandelate_1995_e317q/" + name
            def changed_review(root, relative):
                raw = _raw(root, relative)
                return raw + b"\n" if relative == selected else raw
            with self.subTest(path=selected):
                with patch("catalytic_earth.atlas_reference_outcomes._raw", side_effect=changed_review):
                    with self.assertRaisesRegex(ValueError, "review binding differs"):
                        query_reference_outcomes(ROOT, site_id="P11444:H297")

    def test_selected_raw_evidence_and_missing_binding_fail_even_for_empty_filter(self):
        projection = json.loads((ROOT / "data/atlas/perturbations/projection.json").read_text())
        payload = _acceptance_payload(_compose(ROOT, self.spec, self.view), self.view, projection)
        paths = {binding["path"] for binding in payload["source_bindings"].values()}
        self.assertEqual(len(paths), 4)  # primary, endpoint, recovery and reference snapshot
        for selected in paths:
            def changed_source(root, relative):
                raw = _raw(root, relative)
                return raw + b"\n" if relative == selected else raw
            with self.subTest(path=selected):
                with patch("catalytic_earth.atlas_reference_outcomes._raw", side_effect=changed_source):
                    with self.assertRaisesRegex(ValueError, "review binding differs"):
                        query_reference_outcomes(ROOT, site_id="P11444:H297")
                def omitted_binding(root, relative):
                    raw = _raw(root, relative)
                    if relative == REVIEW_PATH:
                        review = json.loads(raw)
                        del review["reviewed_bindings"][selected]
                        return json.dumps(review).encode()
                    return raw
                with patch("catalytic_earth.atlas_reference_outcomes._raw", side_effect=omitted_binding):
                    with self.assertRaisesRegex(ValueError, "review omits selected source"):
                        query_reference_outcomes(ROOT, site_id="P11444:H297")

    def test_local_acceptance_never_bypasses_global_review(self):
        with patch("catalytic_earth.atlas_reference_outcomes.project",
                   side_effect=ValueError("global source review is stale")) as global_project:
            with self.assertRaisesRegex(ValueError, "global source review is stale"):
                query_reference_outcomes(ROOT, site_id="P11444:H297")
        global_project.assert_called_once_with(ROOT)


if __name__ == "__main__":
    unittest.main()
