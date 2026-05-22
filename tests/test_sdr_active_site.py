import unittest

from catalytic_earth.sdr_active_site import (
    extract_source_free_sdr_catalytic_axis,
    extract_source_free_sdr_nad_p_pocket_proxy,
)


def _atom(
    group: str,
    code: str,
    chain: str,
    resid: str,
    atom: str,
    x: float,
    y: float,
    z: float,
    *,
    element: str | None = None,
) -> dict[str, object]:
    return {
        "group_PDB": group,
        "auth_comp_id": code,
        "label_comp_id": code,
        "auth_asym_id": chain,
        "label_asym_id": chain,
        "auth_seq_id": resid,
        "label_seq_id": resid,
        "auth_atom_id": atom,
        "label_atom_id": atom,
        "type_symbol": element or atom[0],
        "Cartn_x": x,
        "Cartn_y": y,
        "Cartn_z": z,
    }


def _residue(
    code: str,
    chain: str,
    resid: str,
    sidechain_atom: str,
    x: float,
    y: float,
    z: float,
) -> list[dict[str, object]]:
    return [
        _atom("ATOM", code, chain, resid, "CA", x + 0.2, y, z),
        _atom("ATOM", code, chain, resid, sidechain_atom, x, y, z),
    ]


class SdrActiveSiteTests(unittest.TestCase):
    def test_yxxxk_geometry_without_nad_ligand_is_partial(self) -> None:
        atoms = [
            *_residue("TYR", "A", "10", "OH", 0.0, 0.0, 0.0),
            *_residue("CYS", "A", "11", "SG", 5.0, 0.0, 0.0),
            *_residue("VAL", "A", "12", "CG1", 6.0, 0.0, 0.0),
            *_residue("SER", "A", "13", "OG", 7.0, 0.0, 0.0),
            *_residue("LYS", "A", "14", "NZ", 4.1, 0.0, 0.0),
        ]

        axis = extract_source_free_sdr_catalytic_axis(
            atoms,
            row_id="uniprot:TEST",
            accession="TEST",
            structure_id="AF-TEST-F1",
        )

        self.assertEqual(
            axis["status"], "source_free_sdr_catalytic_axis_without_nad_p_ligand"
        )
        self.assertTrue(axis["source_free_coordinate_evidence"])
        self.assertFalse(axis["text_or_label_fields_used_for_predictive_score"])
        self.assertFalse(axis["source_active_site_annotations_used"])
        self.assertEqual(axis["yxxxk_candidate_count"], 1)
        self.assertTrue(axis["source_free_catalytic_axis_resolved"])
        self.assertFalse(axis["source_free_full_sdr_axis_ready"])
        self.assertEqual(axis["selected_candidate"]["motif"], "YCVSK")
        self.assertAlmostEqual(
            axis["selected_candidate"]["tyr_lys_distance_angstrom"], 4.1
        )

    def test_local_nad_ligand_resolves_full_review_only_axis(self) -> None:
        atoms = [
            *_residue("TYR", "A", "10", "OH", 0.0, 0.0, 0.0),
            *_residue("ALA", "A", "11", "CB", 5.0, 0.0, 0.0),
            *_residue("ALA", "A", "12", "CB", 6.0, 0.0, 0.0),
            *_residue("ALA", "A", "13", "CB", 7.0, 0.0, 0.0),
            *_residue("LYS", "A", "14", "NZ", 4.0, 0.0, 0.0),
            _atom("HETATM", "NAP", "A", "500", "C1N", 2.0, 0.0, 0.0),
        ]

        axis = extract_source_free_sdr_catalytic_axis(atoms)

        self.assertEqual(
            axis["status"], "source_free_sdr_catalytic_and_nad_p_site_resolved"
        )
        self.assertTrue(axis["source_free_full_sdr_axis_ready"])
        self.assertEqual(axis["nad_p_like_ligand_site_count"], 1)
        self.assertTrue(
            axis["selected_candidate"]["nearest_nad_p_like_ligand"]["within_cutoff"]
        )

    def test_missing_yxxxk_motif_fails_closed(self) -> None:
        atoms = [
            *_residue("TYR", "A", "10", "OH", 0.0, 0.0, 0.0),
            *_residue("ALA", "A", "11", "CB", 5.0, 0.0, 0.0),
            *_residue("ALA", "A", "12", "CB", 6.0, 0.0, 0.0),
            *_residue("ALA", "A", "13", "CB", 7.0, 0.0, 0.0),
            *_residue("ARG", "A", "14", "NH1", 4.0, 0.0, 0.0),
        ]

        axis = extract_source_free_sdr_catalytic_axis(atoms)

        self.assertEqual(axis["status"], "no_source_free_sdr_catalytic_axis")
        self.assertEqual(axis["yxxxk_candidate_count"], 0)
        self.assertFalse(axis["source_free_catalytic_axis_resolved"])
        self.assertFalse(axis["source_free_full_sdr_axis_ready"])

    def test_strict_nad_p_pocket_proxy_resolves_as_review_only(self) -> None:
        atoms = []
        motif_codes = ["THR", "GLY", "ALA", "ALA", "ALA", "GLY", "ALA", "GLY"]
        for offset, code in enumerate(motif_codes, start=1):
            atoms.extend(_residue(code, "A", str(offset), "CB", float(offset), 0.0, 0.0))
        for resid in range(9, 20):
            atoms.extend(_residue("ALA", "A", str(resid), "CB", float(resid), 0.0, 0.0))
        atoms.extend(_residue("TYR", "A", "20", "OH", 20.0, 0.0, 0.0))
        atoms.extend(_residue("ALA", "A", "21", "CB", 21.0, 0.0, 0.0))
        atoms.extend(_residue("ALA", "A", "22", "CB", 22.0, 0.0, 0.0))
        atoms.extend(_residue("ALA", "A", "23", "CB", 23.0, 0.0, 0.0))
        atoms.extend(_residue("LYS", "A", "24", "NZ", 24.0, 0.0, 0.0))

        proxy = extract_source_free_sdr_nad_p_pocket_proxy(atoms)

        self.assertEqual(
            proxy["status"],
            "source_free_sdr_catalytic_axis_with_nad_p_pocket_proxy_review_only",
        )
        self.assertTrue(proxy["source_free_catalytic_axis_resolved"])
        self.assertTrue(proxy["source_free_nad_p_pocket_proxy_resolved"])
        self.assertFalse(proxy["source_free_full_sdr_axis_ready"])
        self.assertFalse(proxy["proxy_axis_ready_for_threshold_calibration"])
        self.assertFalse(proxy["text_or_label_fields_used_for_predictive_score"])
        self.assertFalse(proxy["source_active_site_annotations_used"])
        self.assertEqual(proxy["selected_pocket_proxy"]["motif"], "TGAAAGAG")
        self.assertTrue(
            proxy["selected_pocket_proxy"][
                "source_free_nad_p_pocket_proxy_resolved"
            ]
        )

    def test_loose_glycine_motif_does_not_count_as_sdr_pocket_proxy(self) -> None:
        atoms = []
        motif_codes = ["VAL", "GLY", "VAL", "VAL", "PHE", "GLY", "SER", "GLY"]
        for offset, code in enumerate(motif_codes, start=1):
            atoms.extend(_residue(code, "A", str(offset), "CB", float(offset), 0.0, 0.0))
        for resid in range(9, 20):
            atoms.extend(_residue("ALA", "A", str(resid), "CB", float(resid), 0.0, 0.0))
        atoms.extend(_residue("TYR", "A", "20", "OH", 20.0, 0.0, 0.0))
        atoms.extend(_residue("ALA", "A", "21", "CB", 21.0, 0.0, 0.0))
        atoms.extend(_residue("ALA", "A", "22", "CB", 22.0, 0.0, 0.0))
        atoms.extend(_residue("ALA", "A", "23", "CB", 23.0, 0.0, 0.0))
        atoms.extend(_residue("LYS", "A", "24", "NZ", 24.0, 0.0, 0.0))

        proxy = extract_source_free_sdr_nad_p_pocket_proxy(atoms)

        self.assertEqual(
            proxy["status"],
            "source_free_sdr_catalytic_axis_without_nad_p_pocket_proxy",
        )
        self.assertTrue(proxy["source_free_catalytic_axis_resolved"])
        self.assertFalse(proxy["source_free_nad_p_pocket_proxy_resolved"])
        self.assertEqual(proxy["pocket_proxy_candidate_count"], 0)
        self.assertIsNone(proxy["selected_pocket_proxy"])


if __name__ == "__main__":
    unittest.main()
