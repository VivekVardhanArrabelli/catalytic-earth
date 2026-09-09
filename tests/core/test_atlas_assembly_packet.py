"""False-join regression tests for the reviewed assembly annotation."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "data/atlas/assembly_context/6ha3"
SPEC = importlib.util.spec_from_file_location("assembly_packet", ROOT / "scripts/build_atlas_assembly_context.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class AssemblyPacketTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = json.loads((PACKET / "spec.json").read_text(encoding="utf-8"))
        self.study = json.loads((ROOT / "data/atlas/study_context/6ha3/evidence_projection.json").read_text(encoding="utf-8"))
        self.inventory = json.loads((ROOT / "data/atlas/study_context/6ha3/source_inventory.json").read_text(encoding="utf-8"))

    def test_packet_replays_with_source_review(self) -> None:
        result = MODULE.check(PACKET, ROOT)
        self.assertFalse(result["geometry_to_function_causation"])
        self.assertFalse(result["complete_active_site"])

    def test_role_cannot_attach_to_a_different_copy(self) -> None:
        self.spec["assembly_spec"]["selections"][1]["operator_ids"] = ["1"]
        with self.assertRaisesRegex(ValueError, "source role/copy binding"):
            MODULE._validate_context(self.spec, self.study, self.inventory)

    def test_nondetection_cannot_attach_to_different_variant_or_endpoint(self) -> None:
        for key, value, error in [
            ("compared_variant", "E999Q", "compared variant"),
            ("functional_observation_id", "invented-assay", "functional observation"),
            ("same_variant_as_structure", True, "variant equivalence"),
            ("selective_partner_only_intervention", True, "selective-copy"),
        ]:
            with self.subTest(key=key):
                spec = copy.deepcopy(self.spec)
                spec["source_reviewed_context"]["relation"][key] = value
                with self.assertRaisesRegex(ValueError, error):
                    MODULE._validate_context(spec, self.study, self.inventory)

    def test_reporter_and_nondetection_do_not_become_a_zero_rate(self) -> None:
        self.spec["source_reviewed_context"]["functional_panel"]["numeric_detection_floor"] = 0
        with self.assertRaisesRegex(ValueError, "quantitative nondetection"):
            MODULE._validate_context(self.spec, self.study, self.inventory)
        self.spec["source_reviewed_context"]["functional_panel"]["numeric_detection_floor"] = None
        self.spec["source_reviewed_context"]["separate_turnover_observation"]["endpoint"] = self.spec["source_reviewed_context"]["functional_panel"]["endpoint"]
        with self.assertRaisesRegex(ValueError, "separate turnover endpoint"):
            MODULE._validate_context(self.spec, self.study, self.inventory)

    def test_source_hash_and_doi_cannot_be_borrowed(self) -> None:
        for mutate, error in [
            (lambda spec: spec["source_reviewed_context"]["sources"][0].update(sha256="0" * 64), "source/inventory"),
            (lambda spec: spec["source_reviewed_context"]["functional_panel"].update(study_doi="10.fake/other"), "study DOI"),
            (lambda spec: spec["source_reviewed_context"]["functional_panel"].update(source_artifact_ids=["unretained-paper"]), "evidence source"),
        ]:
            with self.subTest(error=error):
                spec = copy.deepcopy(self.spec)
                mutate(spec)
                with self.assertRaisesRegex(ValueError, error):
                    MODULE._validate_context(spec, self.study, self.inventory)

    def test_unreviewed_projection_edit_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            packet = Path(directory) / "packet"
            shutil.copytree(PACKET, packet)
            path = packet / "review.json"
            review = json.loads(path.read_text(encoding="utf-8"))
            review["reviewed_sha256"]["spec.json"] = "0" * 64
            path.write_text(json.dumps(review), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "review pins"):
                MODULE.check(packet, ROOT)


if __name__ == "__main__":
    unittest.main()
