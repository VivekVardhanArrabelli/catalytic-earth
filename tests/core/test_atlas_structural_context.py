"""Regression tests for source-bound Atlas structural context."""

from __future__ import annotations

from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from catalytic_earth.atlas_structural_context import (
    build_structural_context,
    load_and_build_structural_context,
    query_structural_context,
)
from catalytic_earth.canonical_hash import canonical_file_sha256


REPO = Path(__file__).resolve().parents[2]
SPEC_PATH = REPO / "data/atlas/structural_context/spec.json"
KERNEL_PATH = REPO / "data/atlas/atlas10/kernel.json"
COORDINATE_PATHS = {
    "1PQ5": REPO / "data/atlas/atlas10/sources/pdb/1PQ5.cif.gz",
    "1SUP": REPO / "data/atlas/atlas10/sources/pdb/1SUP.cif.gz",
}


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical_payload_sha256(value: object) -> str:
    payload = (
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _single_structure(spec: dict, pdb_id: str) -> dict:
    result = deepcopy(spec)
    result["structures"] = [
        row for row in result["structures"] if row["pdb_id"] == pdb_id
    ]
    return result


def _context(bundle: dict, pdb_id: str) -> dict:
    return next(row for row in bundle["structures"] if row["pdb_id"] == pdb_id)


def _pair(context: dict, pair_id: str) -> dict:
    return next(row for row in context["distance_pairs"] if row["pair_id"] == pair_id)


def _alter_atom_rows(text: str, predicate, transform) -> tuple[str, int]:
    """Alter whitespace-delimited rows in the retained files' atom-site loop."""

    output = []
    changed = 0
    for line in text.splitlines():
        fields = line.split()
        if (
            len(fields) == 21
            and fields[0] in {"ATOM", "HETATM"}
            and predicate(fields)
        ):
            fields = transform(fields)
            line = " ".join(fields)
            changed += 1
        output.append(line)
    return "\n".join(output) + "\n", changed


class AtlasStructuralContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = _read_json(SPEC_PATH)
        cls.kernel = _read_json(KERNEL_PATH)
        cls.bundle = load_and_build_structural_context(
            SPEC_PATH,
            KERNEL_PATH,
            REPO,
        )

    def test_retained_sources_rebuild_the_exact_checked_in_bundle(self) -> None:
        self.assertEqual(
            self.bundle,
            _read_json(REPO / "data/atlas/structural_context/bundle.json"),
        )
        self.assertEqual(self.bundle["context_count"], 2)
        self.assertEqual(self.bundle["site_count"], 6)
        self.assertEqual(self.bundle["distance_pair_count"], 6)
        self.assertEqual(self.bundle["distance_measurement_count"], 9)

    def test_coordinate_binding_hash_change_is_rejected(self) -> None:
        spec = _single_structure(self.spec, "1SUP")
        spec["structures"][0]["coordinate_binding"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "coordinate binding hash differs"):
            build_structural_context(
                spec,
                atlas10_kernel=self.kernel,
                coordinate_paths={"1SUP": COORDINATE_PATHS["1SUP"]},
            )

    def test_altered_dual_numbering_mapping_is_rejected_after_source_repin(self) -> None:
        spec = _single_structure(self.spec, "1SUP")
        with TemporaryDirectory() as directory:
            source = gzip.open(
                COORDINATE_PATHS["1SUP"], "rt", encoding="utf-8"
            ).read()

            def is_catalytic_serine(fields: list[str]) -> bool:
                return (
                    fields[5] == "SER"
                    and fields[8] == "221"
                    and fields[16] == "221"
                    and fields[18] == "A"
                )

            def change_author_number(fields: list[str]) -> list[str]:
                fields[16] = "222"
                return fields

            altered, count = _alter_atom_rows(
                source, is_catalytic_serine, change_author_number
            )
            self.assertGreater(count, 0)
            path = Path(directory) / "1SUP-altered.cif"
            path.write_text(altered, encoding="utf-8")
            spec["structures"][0]["coordinate_binding"]["sha256"] = (
                canonical_file_sha256(path)
            )
            with self.assertRaisesRegex(
                ValueError, "Atlas-10 site mapping has no deposited atom rows"
            ):
                build_structural_context(
                    spec,
                    atlas10_kernel=self.kernel,
                    coordinate_paths={"1SUP": path},
                )

    def test_alternate_conformers_are_separate_and_never_averaged(self) -> None:
        context = _context(self.bundle, "1SUP")
        pair = _pair(context, "serine-oxygen--histidine-ne2")
        observed = [
            (
                row["right_label_alt_id"],
                row["right_occupancy"],
                row["distance_angstrom"],
            )
            for row in pair["measurements"]
        ]
        self.assertEqual(
            observed,
            [("A", 0.8, 7.347397), ("B", 0.2, 3.214043)],
        )
        self.assertNotIn("distance_angstrom", pair)
        self.assertNotIn("mean_distance_angstrom", pair)
        self.assertIn("no_preferred_or_averaged_distance", pair["measurement_semantics"])

    def test_same_residue_alternate_cross_mixing_is_excluded(self) -> None:
        spec = _single_structure(self.spec, "1SUP")
        structure = spec["structures"][0]
        structure["selected_sites"] = [
            row
            for row in structure["selected_sites"]
            if row["site_id"] == "P00782:H171"
        ]
        structure["declared_distance_pairs"] = [
            {
                "pair_id": "histidine-nd1--histidine-ne2",
                "left": {"site_id": "P00782:H171", "atom_name": "ND1"},
                "right": {"site_id": "P00782:H171", "atom_name": "NE2"},
            }
        ]
        bundle = build_structural_context(
            spec,
            atlas10_kernel=self.kernel,
            coordinate_paths={"1SUP": COORDINATE_PATHS["1SUP"]},
        )
        measurements = bundle["structures"][0]["distance_pairs"][0][
            "measurements"
        ]
        self.assertEqual(
            [
                (row["left_label_alt_id"], row["right_label_alt_id"])
                for row in measurements
            ],
            [("A", "A"), ("B", "B")],
        )
        self.assertTrue(
            all(
                row["alternate_coexistence"] == "compatible_within_same_residue"
                for row in measurements
            )
        )

    def test_cross_model_site_data_is_rejected_after_source_repin(self) -> None:
        spec = _single_structure(self.spec, "1PQ5")
        with TemporaryDirectory() as directory:
            source = gzip.open(
                COORDINATE_PATHS["1PQ5"], "rt", encoding="utf-8"
            ).read()

            def is_catalytic_serine(fields: list[str]) -> bool:
                return (
                    fields[5] == "SER"
                    and fields[8] == "180"
                    and fields[16] == "195"
                    and fields[18] == "A"
                )

            def move_to_model_two(fields: list[str]) -> list[str]:
                fields[20] = "2"
                return fields

            altered, count = _alter_atom_rows(
                source, is_catalytic_serine, move_to_model_two
            )
            self.assertGreater(count, 0)
            path = Path(directory) / "1PQ5-two-model.cif"
            path.write_text(altered, encoding="utf-8")
            spec["structures"][0]["coordinate_binding"]["sha256"] = (
                canonical_file_sha256(path)
            )
            with self.assertRaisesRegex(
                ValueError, "does not cover every deposited model"
            ):
                build_structural_context(
                    spec,
                    atlas10_kernel=self.kernel,
                    coordinate_paths={"1PQ5": path},
                )

    def test_incident_connection_resolves_unselected_pms_endpoint(self) -> None:
        context = _context(self.bundle, "1SUP")
        connection = next(
            row
            for row in context["incident_connections"]
            if row["connection_id"] == "covale1"
        )
        self.assertEqual(connection["incident_site_ids"], ["P00782:S328"])
        self.assertEqual(connection["connection_type"], "covale")
        self.assertEqual(connection["deposited_distance_angstrom"], 1.53)
        pms_endpoint = next(
            row
            for row in connection["endpoints"]
            if row["label_component_id"] == "PMS"
        )
        self.assertEqual(pms_endpoint["selected_site_ids"], [])
        self.assertEqual(
            [
                (
                    atom["label_atom_id"],
                    atom["occupancy"],
                    atom["requested_for_distance"],
                )
                for atom in pms_endpoint["atom_rows"]
            ],
            [("S", 0.7, False)],
        )
        self.assertEqual(
            [row["category"] for row in context["modification_features"]],
            ["Covalent chemical modification"],
        )

    def test_arg703_heavy_atom_occupancies_are_not_normalized(self) -> None:
        context = _context(self.bundle, "1PQ5")
        arginine = next(
            row
            for row in context["nonwater_nonpolymer_components"]
            if row["component_id"] == "ARG"
        )
        instance = next(
            row
            for row in arginine["instances"]
            if row["author_residue_number"] == 703
        )
        observed = {
            row["author_atom_id"]: row["occupancy"]
            for row in instance["atom_rows"]
            if row["element"] != "H"
        }
        self.assertEqual(
            observed,
            {
                "C": 0.19,
                "CA": 0.22,
                "CB": 0.48,
                "CD": 0.44,
                "CG": 0.38,
                "CZ": 0.37,
                "N": 0.35,
                "NE": 0.42,
                "NH1": 0.34,
                "NH2": 0.33,
                "O": 0.42,
            },
        )
        self.assertGreater(len(set(observed.values())), 1)

    def test_empty_and_site_queries_retain_complete_selection_scope(self) -> None:
        unfiltered = query_structural_context(self.bundle)
        self.assertEqual(
            unfiltered["filters"],
            {"case_id": None, "pdb_id": None, "site_id": None},
        )
        self.assertEqual(unfiltered["context_count"], 2)
        self.assertEqual([len(row["sites"]) for row in unfiltered["structures"]], [3, 3])

        by_site = query_structural_context(self.bundle, site_id="P00782:H171")
        self.assertEqual(by_site["context_count"], 1)
        self.assertEqual(len(by_site["structures"][0]["sites"]), 3)
        self.assertTrue(
            by_site["query_semantics"][
                "site_filter_does_not_prune_sibling_sites_or_interpretation"
            ]
        )

        absent = query_structural_context(self.bundle, pdb_id="9ZZZ")
        self.assertEqual(absent["filters"]["pdb_id"], "9ZZZ")
        self.assertEqual(absent["context_count"], 0)
        self.assertEqual(absent["structures"], [])
        self.assertEqual(
            absent["query_semantics"]["empty_result"],
            "no_matching_packaged_context_not_absence_of_structure_or_catalysis",
        )


if __name__ == "__main__":
    unittest.main()
