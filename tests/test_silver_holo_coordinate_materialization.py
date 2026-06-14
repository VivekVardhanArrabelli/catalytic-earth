from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from catalytic_earth.registry_io import load_json
from catalytic_earth.silver_holo_coordinate_materialization import (
    build_silver_holo_coordinate_materialization,
    write_silver_holo_coordinate_materialization,
)


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _row(
    *,
    entry_id: str,
    fp: str,
    cofactors: list[str],
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
        "rationale": "synthetic row for silver holo coordinate materialization tests",
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


class SilverHoloCoordinateMaterializationTests(unittest.TestCase):
    def test_reuses_existing_artifact_coordinate_when_sha_matches(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifacts = root / "artifacts"
            coord = artifacts / "nested" / "pdb_1ABC.cif"
            coord.parent.mkdir(parents=True)
            coord.write_text("verified_coordinate\n", encoding="utf-8")
            candidate = _row(
                entry_id="uniprot:CANDIDATE",
                fp="metal_dependent_hydrolase",
                cofactors=["Zn(2+)"],
                coordinate_sha256=_sha("verified_coordinate\n"),
            )
            audit = build_silver_holo_coordinate_materialization(
                expansion_payload=_population(candidate),
                cohesion_threshold=0.5,
                artifacts_root=artifacts,
                fetch_limit=0,
            )

        row = [r for r in audit["rows"] if r["entry_id"] == "uniprot:CANDIDATE"][0]
        self.assertEqual(row["decision"], "materialized_from_existing_artifact")
        self.assertEqual(audit["counts"]["registry_coordinate_updates"], 1)
        updated = [
            r for r in audit["materialized_registry"] if r["entry_id"] == "uniprot:CANDIDATE"
        ][0]
        structure = updated["evidence"]["structure_provenance"]
        self.assertEqual(structure["coordinate_path"], str(coord))
        self.assertEqual(
            structure["holo_coordinate_materialization"]["source"],
            "existing_artifact_coordinate",
        )
        self.assertEqual(updated["tier"], "bronze")

    def test_existing_coordinate_sha_mismatch_is_held(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifacts = root / "artifacts"
            coord = artifacts / "nested" / "pdb_1ABC.cif"
            coord.parent.mkdir(parents=True)
            coord.write_text("wrong_coordinate\n", encoding="utf-8")
            candidate = _row(
                entry_id="uniprot:CANDIDATE",
                fp="metal_dependent_hydrolase",
                cofactors=["Zn(2+)"],
                coordinate_sha256=_sha("expected_coordinate\n"),
            )
            audit = build_silver_holo_coordinate_materialization(
                expansion_payload=_population(candidate),
                cohesion_threshold=0.5,
                artifacts_root=artifacts,
                fetch_limit=0,
            )

        row = [r for r in audit["rows"] if r["entry_id"] == "uniprot:CANDIDATE"][0]
        self.assertEqual(row["decision"], "deferred_over_fetch_limit")
        self.assertIn("mismatch", row)
        self.assertEqual(audit["counts"]["existing_local_coordinate_sha_mismatch"], 1)
        self.assertEqual(audit["counts"]["registry_coordinate_updates"], 0)

    def test_fetches_bounded_coordinate_when_sha_matches(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            coordinate_dir = root / "coords"
            candidate = _row(
                entry_id="uniprot:CANDIDATE",
                fp="metal_dependent_hydrolase",
                cofactors=["Zn(2+)"],
                coordinate_sha256=_sha("fetched_coordinate\n"),
            )
            audit = build_silver_holo_coordinate_materialization(
                expansion_payload=_population(candidate),
                cohesion_threshold=0.5,
                artifacts_root=root / "empty_artifacts",
                coordinate_dir=coordinate_dir,
                cif_fetcher=lambda pdb_id: "fetched_coordinate\n",
                fetch_limit=1,
            )

            path = coordinate_dir / "pdb_1ABC.cif"
            self.assertTrue(path.exists())
            row = [r for r in audit["rows"] if r["entry_id"] == "uniprot:CANDIDATE"][0]
            self.assertEqual(row["decision"], "materialized_from_rcsb_refetch")
            self.assertEqual(audit["counts"]["fetched_and_materialized_coordinate"], 1)
            self.assertEqual(audit["counts"]["registry_coordinate_updates"], 1)

    def test_apply_writes_expansion_only_and_preserves_frozen(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            expansion = root / "external.json"
            frozen = root / "curated.json"
            out = root / "artifact.json"
            report = root / "report.md"
            coordinate_dir = root / "coords"
            candidate = _row(
                entry_id="uniprot:CANDIDATE",
                fp="metal_dependent_hydrolase",
                cofactors=["Zn(2+)"],
                coordinate_sha256=_sha("fetched_coordinate\n"),
            )
            expansion.write_text(json.dumps(_population(candidate)), encoding="utf-8")
            frozen.write_text("[]\n", encoding="utf-8")

            summary = write_silver_holo_coordinate_materialization(
                out_path=out,
                report_path=report,
                expansion_registry_path=expansion,
                frozen_benchmark_path=frozen,
                coordinate_dir=coordinate_dir,
                artifacts_root=root / "empty_artifacts",
                cif_fetcher=lambda pdb_id: "fetched_coordinate\n",
                apply=True,
                fetch_limit=1,
                cohesion_threshold=0.5,
            )

            written = load_json(expansion)
            updated = [r for r in written if r["entry_id"] == "uniprot:CANDIDATE"][0]
            self.assertTrue(summary["expansion_registry_written"])
            self.assertFalse(summary["frozen_benchmark_registry_written"])
            self.assertTrue(summary["frozen_benchmark_byte_unchanged"])
            self.assertEqual(frozen.read_text(encoding="utf-8"), "[]\n")
            self.assertEqual(
                updated["evidence"]["structure_provenance"]["coordinate_status"],
                "holo_experimental_pdb_coordinate_materialized",
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())


if __name__ == "__main__":
    unittest.main()
