from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from catalytic_earth.registry_io import load_json
from catalytic_earth.silver_pdb_residue_mapping import (
    build_silver_pdb_residue_mapping,
    write_silver_pdb_residue_mapping,
)


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _cif() -> str:
    return """data_1ABC
loop_
_struct_ref_seq.align_id
_struct_ref_seq.ref_id
_struct_ref_seq.pdbx_PDB_id_code
_struct_ref_seq.pdbx_strand_id
_struct_ref_seq.seq_align_beg
_struct_ref_seq.pdbx_seq_align_beg_ins_code
_struct_ref_seq.seq_align_end
_struct_ref_seq.pdbx_seq_align_end_ins_code
_struct_ref_seq.pdbx_db_accession
_struct_ref_seq.db_align_beg
_struct_ref_seq.pdbx_db_align_beg_ins_code
_struct_ref_seq.db_align_end
_struct_ref_seq.pdbx_db_align_end_ins_code
_struct_ref_seq.pdbx_auth_seq_align_beg
_struct_ref_seq.pdbx_auth_seq_align_end
1 1 1ABC A 1 ? 100 ? CANDIDATE 1 ? 100 ? 1 100
#
loop_
_pdbx_poly_seq_scheme.asym_id
_pdbx_poly_seq_scheme.entity_id
_pdbx_poly_seq_scheme.seq_id
_pdbx_poly_seq_scheme.mon_id
_pdbx_poly_seq_scheme.ndb_seq_num
_pdbx_poly_seq_scheme.pdb_seq_num
_pdbx_poly_seq_scheme.auth_seq_num
_pdbx_poly_seq_scheme.pdb_mon_id
_pdbx_poly_seq_scheme.auth_mon_id
_pdbx_poly_seq_scheme.pdb_strand_id
_pdbx_poly_seq_scheme.pdb_ins_code
_pdbx_poly_seq_scheme.hetero
A 1 10 SER 10 10 110 SER SER A . n
A 1 20 HIS 20 20 120 HIS HIS A . n
A 1 30 ASP 30 30 130 ASP ASP A . n
#
"""


def _row(
    *,
    entry_id: str,
    fp: str,
    cofactors: list[str],
    coordinate_path: str | None = None,
    coordinate_sha256: str | None = None,
) -> dict:
    residues = [
        {
            "feature_code": "BINDING",
            "feature_type": "Binding site",
            "ligand_name": cofactors[0] if cofactors else None,
            "position": position,
            "exact": True,
        }
        for position in (10, 20, 30)
    ]
    structure_provenance = {"pdb_ids": []}
    if coordinate_sha256 is not None:
        structure_provenance = {
            "coordinate_path": coordinate_path,
            "pdb_ids": ["1ABC"],
            "holo_pdb_confirmation": {
                "status": "holo_experimental_coordinate_confirmed",
                "pdb_id": "1ABC",
                "cofactor_comp_ids_present": ["ZN"],
                "coordinate_sha256": coordinate_sha256,
            },
        }
    return {
        "entry_id": entry_id,
        "label_type": "seed_fingerprint",
        "fingerprint_id": fp,
        "tier": "bronze",
        "review_status": "automation_curated",
        "ontology_version_at_decision": "label_factory_v1_37fp",
        "confidence": "high",
        "evidence_score": 0.8,
        "rationale": "synthetic row for silver PDB residue mapping tests",
        "evidence": {
            "sources": ["unit_test"],
            "mechanism_evidence": {
                "cofactors": [{"name": cofactor} for cofactor in cofactors],
                "active_site_residues": residues,
                "active_site_residue_count": len(residues),
                "binding_residue_count": len(residues),
                "catalytic_residue_count": 0,
            },
            "structure_provenance": structure_provenance,
            "source_provenance": {"accession": entry_id.split(":", 1)[1]},
            "predictive_evidence": [],
        },
    }


def _population(candidate: dict) -> list[dict]:
    rows = [candidate]
    for index in range(8):
        rows.append(
            _row(
                entry_id=f"uniprot:M{index}",
                fp="metal_dependent_hydrolase",
                cofactors=["Zn(2+)"],
            )
        )
    for index in range(8):
        rows.append(
            _row(
                entry_id=f"uniprot:P{index}",
                fp="plp_dependent_enzyme",
                cofactors=["pyridoxal 5'-phosphate"],
            )
        )
    return rows


class SilverPdbResidueMappingTests(unittest.TestCase):
    def test_maps_uniprot_positions_through_mmcif_alignment_tables(self) -> None:
        with TemporaryDirectory() as tmp:
            coord = Path(tmp) / "pdb_1ABC.cif"
            cif = _cif()
            coord.write_text(cif, encoding="utf-8")
            candidate = _row(
                entry_id="uniprot:CANDIDATE",
                fp="metal_dependent_hydrolase",
                cofactors=["Zn(2+)"],
                coordinate_path=str(coord),
                coordinate_sha256=_sha(cif),
            )
            audit = build_silver_pdb_residue_mapping(
                expansion_payload=_population(candidate),
                cohesion_threshold=0.5,
            )

        row = [r for r in audit["rows"] if r["entry_id"] == "uniprot:CANDIDATE"][0]
        self.assertEqual(row["decision"], "mapped_explicit_pdb_residue_positions")
        self.assertEqual(row["mapped_residue_count"], 3)
        self.assertEqual(audit["counts"]["rows_mapped"], 1)
        updated = [
            r for r in audit["mapped_registry"] if r["entry_id"] == "uniprot:CANDIDATE"
        ][0]
        first_mapping = updated["evidence"]["mechanism_evidence"]["active_site_residues"][0][
            "structure_positions"
        ][0]
        self.assertEqual(first_mapping["chain_name"], "A")
        self.assertEqual(first_mapping["resid"], "110")
        self.assertEqual(first_mapping["uniprot_position"], 10)
        self.assertEqual(updated["tier"], "bronze")

    def test_apply_writes_expansion_only_and_preserves_frozen(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            expansion = root / "external.json"
            frozen = root / "curated.json"
            out = root / "artifact.json"
            report = root / "report.md"
            coord = root / "pdb_1ABC.cif"
            cif = _cif()
            coord.write_text(cif, encoding="utf-8")
            candidate = _row(
                entry_id="uniprot:CANDIDATE",
                fp="metal_dependent_hydrolase",
                cofactors=["Zn(2+)"],
                coordinate_path=str(coord),
                coordinate_sha256=_sha(cif),
            )
            expansion.write_text(json.dumps(_population(candidate)), encoding="utf-8")
            frozen.write_text("[]\n", encoding="utf-8")

            summary = write_silver_pdb_residue_mapping(
                out_path=out,
                report_path=report,
                expansion_registry_path=expansion,
                frozen_benchmark_path=frozen,
                apply=True,
                cohesion_threshold=0.5,
            )

            written = load_json(expansion)
            updated = [r for r in written if r["entry_id"] == "uniprot:CANDIDATE"][0]
            self.assertTrue(summary["expansion_registry_written"])
            self.assertFalse(summary["frozen_benchmark_registry_written"])
            self.assertTrue(summary["frozen_benchmark_byte_unchanged"])
            self.assertEqual(frozen.read_text(encoding="utf-8"), "[]\n")
            self.assertEqual(
                updated["evidence"]["structure_provenance"][
                    "pdb_residue_mapping_provenance"
                ]["status"],
                "pdb_residue_mapping_from_mmcif_struct_ref_seq",
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())


if __name__ == "__main__":
    unittest.main()
