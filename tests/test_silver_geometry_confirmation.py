from __future__ import annotations

import hashlib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from catalytic_earth.silver_geometry_confirmation import (
    build_silver_geometry_confirmation_audit,
    write_silver_geometry_confirmation_audit,
)


def _row(
    *,
    entry_id: str,
    fp: str,
    cofactors: list[str],
    coordinate_path: str | None = None,
    structure_positions: bool = False,
    exact_positions: list[int] | None = None,
    coordinate_sha256: str | None = None,
) -> dict:
    residues = []
    for position in exact_positions or [10, 20, 30]:
        residue = {
            "feature_code": "BINDING",
            "feature_type": "Binding site",
            "ligand_name": cofactors[0] if cofactors else None,
            "position": position,
            "exact": True,
        }
        if structure_positions:
            residue["structure_positions"] = [
                {
                    "pdb_id": "1ABC",
                    "chain_name": "A",
                    "resid": str(position),
                    "code": "SER",
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
        "rationale": "synthetic row for silver geometry audit tests",
        "evidence": {
            "mechanism_evidence": {
                "cofactors": [{"name": cofactor} for cofactor in cofactors],
                "active_site_residues": residues,
                "active_site_residue_count": len(residues),
                "binding_residue_count": len(residues),
                "catalytic_residue_count": 0,
            },
            "structure_provenance": {
                "coordinate_path": coordinate_path,
                "pdb_ids": ["1ABC"],
                "holo_pdb_confirmation": {
                    "status": "holo_experimental_coordinate_confirmed",
                    "pdb_id": "1ABC",
                    "cofactor_comp_ids_present": ["ZN"],
                    "coordinate_sha256": coordinate_sha256,
                },
            },
            "pending_promotion_audits": [
                "geometry_inverse_gate_confirmation_on_holo_or_cofactor_fused_structure"
            ],
        },
    }


def _population(candidate: dict) -> list[dict]:
    rows = []
    for index in range(8):
        rows.append(
            _row(
                entry_id=f"metal{index}",
                fp="metal_dependent_hydrolase",
                cofactors=["Zn(2+)"],
            )
        )
    for index in range(8):
        rows.append(
            _row(
                entry_id=f"plp{index}",
                fp="plp_dependent_enzyme",
                cofactors=["pyridoxal 5'-phosphate"],
            )
        )
    rows.append(candidate)
    return rows


class SilverGeometryConfirmationAuditTests(unittest.TestCase):
    def test_holo_row_blocks_without_explicit_pdb_residue_mapping(self) -> None:
        candidate = _row(
            entry_id="candidate",
            fp="metal_dependent_hydrolase",
            cofactors=["Zn(2+)"],
        )
        audit = build_silver_geometry_confirmation_audit(
            _population(candidate),
            cohesion_threshold=0.5,
        )
        blocked = [row for row in audit["rows"] if row["entry_id"] == "candidate"][0]
        self.assertEqual(blocked["decision"], "blocked_before_geometry_confirmation")
        self.assertIn("missing_explicit_pdb_residue_mapping", blocked["blockers"])
        self.assertFalse(blocked["tier_changed"])
        self.assertEqual(audit["counts"]["silver_flips_applied"], 0)

    def test_fully_materialized_row_is_runnable_but_not_promoted(self) -> None:
        with TemporaryDirectory() as tmp:
            coord = Path(tmp) / "holo.cif"
            content = "data_test\n"
            coord.write_text(content, encoding="utf-8")
            candidate = _row(
                entry_id="candidate",
                fp="metal_dependent_hydrolase",
                cofactors=["Zn(2+)"],
                coordinate_path=str(coord),
                structure_positions=True,
                coordinate_sha256=hashlib.sha256(content.encode("utf-8")).hexdigest(),
            )
            audit = build_silver_geometry_confirmation_audit(
                _population(candidate),
                cohesion_threshold=0.5,
            )
        ready = [row for row in audit["rows"] if row["entry_id"] == "candidate"][0]
        self.assertEqual(ready["decision"], "ready_for_geometry_confirmation_run")
        self.assertEqual(ready["blockers"], [])
        self.assertFalse(ready["tier_changed"])
        self.assertFalse(ready["geometry_confirmation_run"])
        self.assertEqual(audit["counts"]["silver_flips_applied"], 0)

    def test_local_coordinate_must_match_holo_confirmation_sha(self) -> None:
        with TemporaryDirectory() as tmp:
            coord = Path(tmp) / "holo.cif"
            coord.write_text("different_coordinate\n", encoding="utf-8")
            candidate = _row(
                entry_id="candidate",
                fp="metal_dependent_hydrolase",
                cofactors=["Zn(2+)"],
                coordinate_path=str(coord),
                structure_positions=True,
                coordinate_sha256=hashlib.sha256(b"expected_coordinate\n").hexdigest(),
            )
            audit = build_silver_geometry_confirmation_audit(
                _population(candidate),
                cohesion_threshold=0.5,
            )
        blocked = [row for row in audit["rows"] if row["entry_id"] == "candidate"][0]
        self.assertEqual(blocked["decision"], "blocked_before_geometry_confirmation")
        self.assertIn("local_coordinate_sha_mismatch_holo_confirmation", blocked["blockers"])
        self.assertFalse(blocked["coordinate_sha256_matches_holo_confirmation"])

    def test_write_summary_omits_full_rows_and_is_non_destructive(self) -> None:
        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            registry = tmp_path / "expansion.json"
            registry.write_text("[]\n", encoding="utf-8")
            out = tmp_path / "audit.json"
            report = tmp_path / "audit.md"
            audit = write_silver_geometry_confirmation_audit(
                out_path=out,
                report_path=report,
                expansion_registry_path=registry,
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertEqual(audit["counts"]["silver_ready_input_rows"], 0)
            self.assertNotIn('"rows"', out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
