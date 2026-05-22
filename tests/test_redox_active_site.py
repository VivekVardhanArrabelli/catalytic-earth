import unittest

from catalytic_earth.redox_active_site import (
    extract_source_free_flavin_site,
    extract_source_free_heme_site,
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
    atom: str,
    x: float,
    y: float,
    z: float,
) -> list[dict[str, object]]:
    return [
        _atom("ATOM", code, chain, resid, "CA", x + 0.4, y, z),
        _atom("ATOM", code, chain, resid, atom, x, y, z),
    ]


class RedoxActiveSiteTests(unittest.TestCase):
    def test_heme_site_uses_coordinate_contacts_only(self) -> None:
        atoms = [
            _atom("HETATM", "HEM", "A", "500", "FE", 0.0, 0.0, 0.0, element="FE"),
            _atom("HETATM", "HEM", "A", "500", "NA", 1.0, 0.0, 0.0),
            *_residue("HIS", "A", "100", "NE2", 2.0, 0.0, 0.0),
            *_residue("ARG", "A", "101", "NH1", 0.0, 3.2, 0.0),
            *_residue("TYR", "A", "102", "OH", 0.0, 0.0, 3.4),
        ]

        site = extract_source_free_heme_site(
            atoms,
            row_id="uniprot:TEST",
            accession="TEST",
            structure_id="1ABC",
        )

        self.assertEqual(site["status"], "source_free_heme_active_site_resolved")
        self.assertTrue(site["source_free_coordinate_evidence"])
        self.assertFalse(site["text_or_label_fields_used_for_predictive_score"])
        self.assertEqual(site["selected_ligand"]["code"], "HEM")
        self.assertGreaterEqual(site["role_contact_counts"]["heme_ligand"], 1)
        self.assertGreaterEqual(site["role_contact_counts"]["acid_base"], 1)
        self.assertGreaterEqual(site["role_contact_counts"]["electron_transfer_path"], 1)
        roles = {role for residue in site["residues"] for role in residue["roles"]}
        self.assertIn("heme_ligand", roles)
        self.assertIn("acid_base", roles)
        self.assertIn("electron_transfer_path", roles)

    def test_flavin_site_uses_coordinate_contacts_only(self) -> None:
        atoms = [
            _atom("HETATM", "FMN", "A", "400", "N5", 0.0, 0.0, 0.0),
            _atom("HETATM", "FMN", "A", "400", "O2", 1.0, 0.0, 0.0),
            *_residue("SER", "A", "10", "OG", 2.5, 0.0, 0.0),
            *_residue("GLU", "A", "11", "OE1", 0.0, 3.4, 0.0),
            *_residue("TYR", "A", "12", "OH", 0.0, 0.0, 3.8),
        ]

        site = extract_source_free_flavin_site(
            atoms,
            row_id="uniprot:TEST",
            accession="TEST",
            structure_id="2ABC",
        )

        self.assertEqual(site["status"], "source_free_flavin_redox_site_resolved")
        self.assertTrue(site["source_free_coordinate_evidence"])
        self.assertFalse(site["text_or_label_fields_used_for_predictive_score"])
        self.assertEqual(site["selected_ligand"]["code"], "FMN")
        self.assertGreaterEqual(site["role_contact_counts"]["flavin_binder"], 1)
        self.assertGreaterEqual(site["role_contact_counts"]["redox_acid_base"], 1)
        self.assertGreaterEqual(site["role_contact_counts"]["electron_transfer_path"], 1)
        roles = {role for residue in site["residues"] for role in residue["roles"]}
        self.assertIn("flavin_binder", roles)
        self.assertIn("redox_acid_base", roles)
        self.assertIn("electron_transfer_path", roles)

    def test_missing_cofactor_fails_closed(self) -> None:
        atoms = [*_residue("HIS", "A", "1", "NE2", 0.0, 0.0, 0.0)]

        heme = extract_source_free_heme_site(atoms)
        flavin = extract_source_free_flavin_site(atoms)

        self.assertEqual(heme["status"], "no_source_free_heme_active_site")
        self.assertEqual(flavin["status"], "no_source_free_flavin_redox_site")
        self.assertEqual(heme["resolved_residue_count"], 0)
        self.assertEqual(flavin["resolved_residue_count"], 0)


if __name__ == "__main__":
    unittest.main()
