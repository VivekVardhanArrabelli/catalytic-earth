import unittest

from catalytic_earth.geometry_retrieval import score_entry_against_fingerprint
from catalytic_earth.plp_active_site import extract_source_free_plp_active_site


def atom(
    group: str,
    comp: str,
    atom_name: str,
    chain: str,
    resid: str,
    x: float,
    y: float,
    z: float,
) -> dict:
    return {
        "group_PDB": group,
        "auth_comp_id": comp,
        "label_comp_id": comp,
        "auth_atom_id": atom_name,
        "label_atom_id": atom_name,
        "auth_asym_id": chain,
        "label_asym_id": chain,
        "auth_seq_id": resid,
        "label_seq_id": resid,
        "Cartn_x": x,
        "Cartn_y": y,
        "Cartn_z": z,
    }


class PlpActiveSiteExtractorTest(unittest.TestCase):
    def test_plp_aldimine_anchor_maps_source_free_triplet(self) -> None:
        atoms = [
            atom("HETATM", "PLP", "C4A", "A", "900", 0.0, 0.0, 0.0),
            atom("HETATM", "PLP", "O1P", "A", "900", 5.0, 0.0, 0.0),
            atom("ATOM", "LYS", "NZ", "A", "201", 1.45, 0.0, 0.0),
            atom("ATOM", "LYS", "CA", "A", "201", 2.0, 1.0, 0.0),
            atom("ATOM", "ASP", "OD1", "A", "179", 0.0, 2.8, 0.0),
            atom("ATOM", "ASP", "CA", "A", "179", 0.0, 4.0, 0.0),
            atom("ATOM", "SER", "OG", "A", "198", 5.0, 2.5, 0.0),
            atom("ATOM", "SER", "CA", "A", "198", 5.0, 3.5, 0.0),
        ]

        result = extract_source_free_plp_active_site(atoms, accession="PTEST")

        self.assertEqual(result["status"], "source_free_plp_active_site_ready")
        self.assertFalse(result["text_or_label_fields_used_for_predictive_score"])
        self.assertEqual(result["plp_like_comp_ids_observed"], ["PLP"])
        self.assertEqual(
            [(row["code"], row["roles"][0]) for row in result["residues"]],
            [("LYS", "plp_anchor"), ("ASP", "acid_base"), ("SER", "phosphate_binder")],
        )
        self.assertEqual(result["ligand_context"]["cofactor_families"], ["plp"])

    def test_llp_modified_residue_maps_as_covalent_lysine_anchor(self) -> None:
        atoms = [
            atom("HETATM", "LLP", "C4A", "B", "217", 0.0, 0.0, 0.0),
            atom("HETATM", "LLP", "OP1", "B", "217", 4.0, 0.0, 0.0),
            atom("ATOM", "TYR", "OH", "B", "194", 0.0, 2.6, 0.0),
            atom("ATOM", "TYR", "CA", "B", "194", 0.0, 3.6, 0.0),
            atom("ATOM", "THR", "OG1", "B", "214", 4.0, 2.5, 0.0),
            atom("ATOM", "THR", "CA", "B", "214", 4.0, 3.5, 0.0),
        ]

        result = extract_source_free_plp_active_site(atoms, accession="LTEST")

        self.assertEqual(result["status"], "source_free_plp_active_site_ready")
        anchor = result["residues"][0]
        self.assertEqual(anchor["code"], "LYS")
        self.assertEqual(anchor["resid"], "217")
        self.assertEqual(
            anchor["source_free_evidence"]["evidence_type"],
            "modified_residue_comp_id",
        )
        self.assertEqual(result["ligand_context"]["ligand_codes"], ["LLP"])

    def test_phosphate_binder_uses_nearest_phosphate_atom(self) -> None:
        atoms = [
            atom("HETATM", "PLP", "C4A", "A", "900", 0.0, 0.0, 0.0),
            atom("HETATM", "PLP", "O1P", "A", "900", 3.0, 0.0, 0.0),
            atom("ATOM", "LYS", "NZ", "A", "201", 1.45, 0.0, 0.0),
            atom("ATOM", "ASP", "OD1", "A", "179", 0.0, 2.8, 0.0),
            atom("ATOM", "SER", "OG", "A", "198", 0.5, 0.0, 0.0),
        ]

        result = extract_source_free_plp_active_site(atoms, accession="PHOS")

        self.assertEqual(result["status"], "source_free_plp_active_site_ready")
        binder = result["residues"][2]
        self.assertEqual(binder["code"], "SER")
        self.assertEqual(binder["roles"][0], "phosphate_binder")
        self.assertEqual(binder["source_free_evidence"]["ligand_atom"], "O1P")
        self.assertEqual(
            binder["source_free_evidence"]["evidence_type"],
            "nearest_plp_phosphate_contact",
        )

    def test_absent_plp_site_does_not_emit_geometry_evidence(self) -> None:
        result = extract_source_free_plp_active_site(
            [atom("ATOM", "LYS", "NZ", "A", "1", 0.0, 0.0, 0.0)],
            accession="ABSENT",
        )

        self.assertEqual(result["status"], "plp_like_cofactor_absent")
        self.assertEqual(result["residue_count"], 0)
        self.assertEqual(result["residues"], [])
        self.assertEqual(result["ligand_context"], {})

    def test_extracted_triplet_scores_plp_without_text_fields(self) -> None:
        atoms = [
            atom("HETATM", "PLP", "C4A", "A", "900", 0.0, 0.0, 0.0),
            atom("HETATM", "PLP", "O1P", "A", "900", 5.0, 0.0, 0.0),
            atom("ATOM", "LYS", "NZ", "A", "201", 1.45, 0.0, 0.0),
            atom("ATOM", "ASP", "OD1", "A", "179", 0.0, 2.8, 0.0),
            atom("ATOM", "SER", "OG", "A", "198", 5.0, 2.5, 0.0),
        ]
        result = extract_source_free_plp_active_site(atoms, accession="PTEST")
        fingerprint = {
            "id": "plp_dependent_enzyme",
            "name": "Pyridoxal phosphate dependent enzyme",
            "active_site_signature": [
                {"role": "plp_anchor", "residue": "Lys"},
                {"role": "acid_base", "residue": "Asp/Glu/His/Tyr"},
                {"role": "phosphate_binder", "residue": "Gly/Ser/Thr"},
            ],
            "cofactors": ["pyridoxal phosphate"],
        }

        score = score_entry_against_fingerprint(result, fingerprint)

        self.assertFalse(score["text_or_label_fields_used_for_score"])
        self.assertEqual(score["fingerprint_id"], "plp_dependent_enzyme")
        self.assertEqual(score["residue_match_fraction"], 1.0)
        self.assertEqual(score["role_match_fraction"], 1.0)
        self.assertGreater(score["score"], 0.4115)


if __name__ == "__main__":
    unittest.main()
