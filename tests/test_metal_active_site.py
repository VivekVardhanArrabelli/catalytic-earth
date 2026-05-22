import unittest

from catalytic_earth.metal_active_site import (
    extract_source_free_metal_hydrolase_site,
    extract_source_free_metal_phosphatase_pocket_proxy,
)


def _atom(
    *,
    group: str,
    comp: str,
    chain: str,
    resid: str,
    atom: str,
    x: float,
    y: float,
    z: float,
    element: str | None = None,
) -> dict:
    return {
        "group_PDB": group,
        "auth_comp_id": comp,
        "label_comp_id": comp,
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


class MetalActiveSiteTest(unittest.TestCase):
    def test_coordinate_only_metal_phosphate_site_resolves_roles(self) -> None:
        atoms = [
            _atom(
                group="HETATM", comp="MG", chain="A", resid="900",
                atom="MG", x=0, y=0, z=0, element="MG",
            ),
            _atom(
                group="HETATM", comp="PGA", chain="A", resid="901",
                atom="P", x=2.2, y=0, z=0, element="P",
            ),
            _atom(
                group="HETATM", comp="PGA", chain="A", resid="901",
                atom="O1P", x=2.8, y=0, z=0, element="O",
            ),
            _atom(
                group="ATOM", comp="ASP", chain="A", resid="10",
                atom="CA", x=0, y=1.5, z=0, element="C",
            ),
            _atom(
                group="ATOM", comp="ASP", chain="A", resid="10",
                atom="OD1", x=0, y=2.2, z=0, element="O",
            ),
            _atom(
                group="ATOM", comp="GLU", chain="A", resid="12",
                atom="CA", x=0, y=-1.6, z=0, element="C",
            ),
            _atom(
                group="ATOM", comp="GLU", chain="A", resid="12",
                atom="OE1", x=0, y=-2.3, z=0, element="O",
            ),
            _atom(
                group="ATOM", comp="LYS", chain="A", resid="44",
                atom="CA", x=3.5, y=0, z=0, element="C",
            ),
            _atom(
                group="ATOM", comp="LYS", chain="A", resid="44",
                atom="NZ", x=3.3, y=0, z=0, element="N",
            ),
        ]

        entry = extract_source_free_metal_hydrolase_site(
            atoms,
            row_id="uniprot:TEST",
            accession="TEST",
            structure_id="TEST1",
        )

        self.assertEqual(entry["status"], "metal_phosphate_site_resolved")
        self.assertTrue(entry["source_free_coordinate_evidence"])
        self.assertFalse(entry["text_or_label_fields_used_for_predictive_score"])
        roles = {
            role
            for residue in entry["residues"]
            for role in residue.get("roles", [])
        }
        self.assertIn("metal_ligand", roles)
        self.assertIn("water_activator", roles)
        self.assertIn("leaving_group_stabilizer", roles)

    def test_metal_cluster_without_phosphate_is_explicit_status(self) -> None:
        atoms = [
            _atom(
                group="HETATM", comp="MG", chain="A", resid="900",
                atom="MG", x=0, y=0, z=0, element="MG",
            ),
            _atom(
                group="ATOM", comp="ASP", chain="A", resid="10",
                atom="CA", x=0, y=1.4, z=0, element="C",
            ),
            _atom(
                group="ATOM", comp="ASP", chain="A", resid="10",
                atom="OD1", x=0, y=2.1, z=0, element="O",
            ),
            _atom(
                group="ATOM", comp="GLU", chain="A", resid="12",
                atom="CA", x=0, y=-1.5, z=0, element="C",
            ),
            _atom(
                group="ATOM", comp="GLU", chain="A", resid="12",
                atom="OE1", x=0, y=-2.2, z=0, element="O",
            ),
        ]

        entry = extract_source_free_metal_hydrolase_site(
            atoms,
            row_id="uniprot:TEST",
            accession="TEST",
            structure_id="TEST2",
        )

        self.assertEqual(
            entry["status"], "metal_cluster_without_phosphate_or_substrate_ligand"
        )
        self.assertEqual(entry["phosphate_like_site_count"], 0)
        self.assertEqual(entry["resolved_residue_count"], 2)

    def test_phosphate_pocket_proxy_resolves_without_ligand(self) -> None:
        atoms = [
            _atom(
                group="HETATM", comp="MG", chain="A", resid="900",
                atom="MG", x=0, y=0, z=0, element="MG",
            ),
            _atom(
                group="ATOM", comp="ASP", chain="A", resid="10",
                atom="OD1", x=0, y=2.1, z=0, element="O",
            ),
            _atom(
                group="ATOM", comp="GLU", chain="A", resid="12",
                atom="OE1", x=0, y=-2.2, z=0, element="O",
            ),
            _atom(
                group="ATOM", comp="LYS", chain="A", resid="44",
                atom="NZ", x=4.0, y=0, z=0, element="N",
            ),
            _atom(
                group="ATOM", comp="THR", chain="A", resid="45",
                atom="OG1", x=0, y=4.4, z=0, element="O",
            ),
            _atom(
                group="ATOM", comp="ASN", chain="A", resid="46",
                atom="ND2", x=0, y=0, z=5.0, element="N",
            ),
        ]

        entry = extract_source_free_metal_phosphatase_pocket_proxy(
            atoms,
            row_id="uniprot:TEST",
            accession="TEST",
            structure_id="TEST3",
        )

        proxy = entry["phosphate_pocket_proxy"]
        self.assertEqual(
            entry["terminal_review_status"],
            "phosphate_pocket_proxy_resolved_review_only",
        )
        self.assertTrue(proxy["proxy_detected"])
        self.assertEqual(proxy["radius_angstrom"], 6.0)
        self.assertGreaterEqual(proxy["non_metal_ligand_contact_count"], 3)
        self.assertGreaterEqual(proxy["polar_or_basic_non_metal_contact_count"], 3)
        self.assertFalse(proxy["text_or_label_fields_used_for_predictive_score"])

    def test_phosphate_pocket_proxy_remains_blocked_without_supporting_contacts(self) -> None:
        atoms = [
            _atom(
                group="HETATM", comp="MG", chain="A", resid="900",
                atom="MG", x=0, y=0, z=0, element="MG",
            ),
            _atom(
                group="ATOM", comp="ASP", chain="A", resid="10",
                atom="OD1", x=0, y=2.1, z=0, element="O",
            ),
            _atom(
                group="ATOM", comp="GLU", chain="A", resid="12",
                atom="OE1", x=0, y=-2.2, z=0, element="O",
            ),
        ]

        entry = extract_source_free_metal_phosphatase_pocket_proxy(
            atoms,
            row_id="uniprot:TEST",
            accession="TEST",
            structure_id="TEST4",
        )

        proxy = entry["phosphate_pocket_proxy"]
        self.assertEqual(entry["terminal_review_status"], "needs_new_extractor_or_structure")
        self.assertFalse(proxy["proxy_detected"])
        self.assertEqual(proxy["non_metal_ligand_contact_count"], 0)
        self.assertTrue(
            proxy["requirements"]["no_threshold_calibration_from_outcomes"]
        )


if __name__ == "__main__":
    unittest.main()
