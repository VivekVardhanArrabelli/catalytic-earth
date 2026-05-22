import unittest

from catalytic_earth.serine_active_site import extract_source_free_ser_his_acid_triad


def _atom(
    *,
    group: str = "ATOM",
    comp: str,
    chain: str = "A",
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


class SerineActiveSiteTest(unittest.TestCase):
    def test_coordinate_only_ser_his_acid_triad_resolves_roles(self) -> None:
        atoms = [
            _atom(comp="SER", resid="10", atom="CA", x=0, y=0, z=0, element="C"),
            _atom(comp="SER", resid="10", atom="OG", x=0, y=1.0, z=0, element="O"),
            _atom(comp="HIS", resid="57", atom="CA", x=0, y=3.0, z=0, element="C"),
            _atom(comp="HIS", resid="57", atom="NE2", x=0, y=3.2, z=0, element="N"),
            _atom(comp="ASP", resid="102", atom="CA", x=0, y=5.7, z=0, element="C"),
            _atom(comp="ASP", resid="102", atom="OD1", x=0, y=5.9, z=0, element="O"),
        ]

        entry = extract_source_free_ser_his_acid_triad(
            atoms,
            row_id="uniprot:TEST",
            accession="TEST",
            structure_id="TEST1",
        )

        self.assertEqual(entry["status"], "ser_his_acid_triad_resolved")
        self.assertTrue(entry["source_free_coordinate_evidence"])
        self.assertFalse(entry["text_or_label_fields_used_for_predictive_score"])
        roles = {
            role
            for residue in entry["residues"]
            for role in residue.get("roles", [])
        }
        self.assertIn("nucleophile", roles)
        self.assertIn("general_base", roles)
        self.assertIn("acid_or_orienter", roles)

    def test_missing_acid_keeps_status_explicit(self) -> None:
        atoms = [
            _atom(comp="SER", resid="10", atom="CA", x=0, y=0, z=0, element="C"),
            _atom(comp="SER", resid="10", atom="OG", x=0, y=1.0, z=0, element="O"),
            _atom(comp="HIS", resid="57", atom="CA", x=0, y=3.0, z=0, element="C"),
            _atom(comp="HIS", resid="57", atom="NE2", x=0, y=3.2, z=0, element="N"),
        ]

        entry = extract_source_free_ser_his_acid_triad(
            atoms,
            row_id="uniprot:TEST",
            accession="TEST",
            structure_id="TEST2",
        )

        self.assertEqual(entry["status"], "no_source_free_ser_his_acid_triad")
        self.assertEqual(entry["resolved_residue_count"], 0)


if __name__ == "__main__":
    unittest.main()
