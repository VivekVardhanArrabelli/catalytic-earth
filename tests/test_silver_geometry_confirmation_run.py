from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from catalytic_earth.silver_geometry_confirmation_run import (
    build_silver_geometry_confirmation_run,
    write_silver_geometry_confirmation_run,
)


def _cif_text() -> str:
    return """data_test
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
_atom_site.auth_atom_id
_atom_site.auth_comp_id
_atom_site.auth_asym_id
_atom_site.auth_seq_id
ATOM 1 N N LYS A 10 0.0 0.0 0.0 N LYS A 10
ATOM 2 C CA LYS A 10 0.0 0.0 0.0 CA LYS A 10
ATOM 3 N N ASP A 20 4.0 0.0 0.0 N ASP A 20
ATOM 4 C CA ASP A 20 4.0 0.0 0.0 CA ASP A 20
ATOM 5 N N SER A 30 0.0 4.0 0.0 N SER A 30
ATOM 6 C CA SER A 30 0.0 4.0 0.0 CA SER A 30
HETATM 7 P P PLP A 901 1.0 1.0 0.0 P PLP A 901
#
"""


def _row(
    *,
    entry_id: str,
    fp: str = "plp_dependent_enzyme",
    coordinate_path: str | None = None,
    coordinate_sha256: str | None = None,
    structure_positions: bool = False,
) -> dict:
    cofactor_name = "Zn(2+)" if fp == "metal_dependent_hydrolase" else "pyridoxal phosphate"
    residues = []
    for code, position in [("LYS", 10), ("ASP", 20), ("SER", 30)]:
        residue = {
            "feature_code": "BINDING",
            "feature_type": "Binding site",
            "ligand_name": cofactor_name,
            "position": position,
            "exact": True,
        }
        if structure_positions:
            residue["structure_positions"] = [
                {
                    "pdb_id": "1PLP",
                    "chain_name": "A",
                    "resid": str(position),
                    "code": code,
                    "mapping_source": "pdb_residue_mapping_from_mmcif_struct_ref_seq",
                    "uniprot_position": position,
                }
            ]
        residues.append(residue)
    return {
        "entry_id": entry_id,
        "label_type": "seed_fingerprint",
        "fingerprint_id": fp,
        "tier": "bronze",
        "review_status": "automation_curated",
        "confidence": "high",
        "evidence_score": 0.8,
        "rationale": "synthetic row for silver geometry confirmation tests",
        "evidence": {
            "sources": ["unit_test"],
            "mechanism_evidence": {
                "cofactors": [{"name": cofactor_name}],
                "active_site_residues": residues,
                "active_site_residue_count": len(residues),
                "binding_residue_count": len(residues),
                "catalytic_residue_count": 0,
            },
            "structure_provenance": {
                "coordinate_path": coordinate_path,
                "pdb_ids": ["1PLP"],
                "holo_pdb_confirmation": {
                    "status": "holo_experimental_coordinate_confirmed",
                    "pdb_id": "1PLP",
                    "cofactor_comp_ids_present": ["PLP"],
                    "coordinate_sha256": coordinate_sha256,
                },
            },
            "pending_promotion_audits": [
                "geometry_inverse_gate_confirmation_on_holo_or_cofactor_fused_structure"
            ],
            "predictive_evidence": [],
        },
    }


def _population(candidate: dict) -> list[dict]:
    rows = [_row(entry_id=f"plp{i}") for i in range(8)]
    rows.extend(_row(entry_id=f"metal{i}", fp="metal_dependent_hydrolase") for i in range(8))
    rows.append(candidate)
    return rows


class SilverGeometryConfirmationRunTests(unittest.TestCase):
    def test_build_run_scores_local_geometry_without_source_roles(self) -> None:
        with TemporaryDirectory() as tmp:
            coord = Path(tmp) / "holo.cif"
            text = _cif_text()
            coord.write_text(text, encoding="utf-8")
            candidate = _row(
                entry_id="candidate",
                coordinate_path=str(coord),
                coordinate_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
                structure_positions=True,
            )
            audit = build_silver_geometry_confirmation_run(
                _population(candidate),
                cohesion_threshold=0.5,
                abstain_threshold=0.4,
            )
        row = [item for item in audit["rows"] if item["entry_id"] == "candidate"][0]
        self.assertEqual(row["decision"], "pass_geometry_confirmation")
        self.assertEqual(row["proposed_tier"], "silver")
        self.assertFalse(row["tier_changed"])
        self.assertFalse(audit["guardrails"]["source_annotation_roles_used_for_score"])
        self.assertFalse(row["geometry_evidence"]["source_annotation_roles_used_for_score"])
        self.assertEqual(audit["counts"]["silver_flips_applied"], 0)

    def test_apply_flips_only_external_registry_and_preserves_frozen(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            coord = root / "holo.cif"
            text = _cif_text()
            coord.write_text(text, encoding="utf-8")
            candidate = _row(
                entry_id="candidate",
                coordinate_path=str(coord),
                coordinate_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
                structure_positions=True,
            )
            expansion = root / "external.json"
            frozen = root / "frozen.json"
            expansion.write_text(json.dumps(_population(candidate)), encoding="utf-8")
            frozen.write_text(json.dumps([]), encoding="utf-8")
            before_sha = hashlib.sha256(frozen.read_bytes()).hexdigest()
            out = root / "audit.json"
            audit = write_silver_geometry_confirmation_run(
                out_path=out,
                report_path=None,
                expansion_registry_path=expansion,
                frozen_benchmark_path=frozen,
                cohesion_threshold=0.5,
                abstain_threshold=0.4,
                apply=True,
            )
            after_sha = hashlib.sha256(frozen.read_bytes()).hexdigest()
            updated = json.loads(expansion.read_text(encoding="utf-8"))
        updated_candidate = [row for row in updated if row["entry_id"] == "candidate"][0]
        self.assertEqual(updated_candidate["tier"], "silver")
        self.assertEqual(updated_candidate["evidence"]["predictive_evidence"], [])
        self.assertEqual(before_sha, after_sha)
        self.assertTrue(audit["frozen_benchmark_byte_unchanged"])
        self.assertEqual(audit["counts"]["silver_flips_applied"], 1)
        self.assertEqual(audit["silver_confirmed_delta"], 1)
        self.assertEqual(
            updated_candidate["evidence"]["structure_provenance"][
                "silver_geometry_confirmation"
            ]["status"],
            "silver_geometry_confirmed_local_holo_pdb",
        )

    def test_apply_refuses_frozen_registry_target(self) -> None:
        with TemporaryDirectory() as tmp:
            frozen = Path(tmp) / "frozen.json"
            frozen.write_text(json.dumps([]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "frozen current702"):
                write_silver_geometry_confirmation_run(
                    out_path=Path(tmp) / "audit.json",
                    report_path=None,
                    expansion_registry_path=frozen,
                    frozen_benchmark_path=frozen,
                    apply=True,
                )


if __name__ == "__main__":
    unittest.main()
