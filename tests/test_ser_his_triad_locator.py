from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from catalytic_earth.ser_his_triad_locator import (
    assess_ser_his_candidate,
    build_ser_his_triad_locator_scan,
    confirm_catalytic_triad,
    is_serine_hydrolase_ec,
    write_ser_his_triad_locator_scan,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
FROZEN_PATH = REPO_ROOT / "data/registries/curated_mechanism_labels.json"
EXPANSION_PATH = REPO_ROOT / "data/registries/external_bronze_labels.json"


def _atom(comp, resid, atom_name, x, y, z, chain="A"):
    return {
        "group_PDB": "ATOM",
        "label_comp_id": comp,
        "auth_comp_id": comp,
        "label_asym_id": chain,
        "auth_asym_id": chain,
        "label_seq_id": str(resid),
        "auth_seq_id": str(resid),
        "label_atom_id": atom_name,
        "auth_atom_id": atom_name,
        "Cartn_x": x,
        "Cartn_y": y,
        "Cartn_z": z,
    }


def _triad_atoms(ser_resid=250, his_resid=227, asp_resid=253):
    """Ser-OG ~3.1A from His-NE2; His-ND1 ~2.8A from Asp-OD1 -- a resolved triad."""
    atoms = []
    # Serine nucleophile
    atoms.append(_atom("SER", ser_resid, "CA", 0.0, 0.0, 0.0))
    atoms.append(_atom("SER", ser_resid, "OG", 1.0, 0.0, 0.0))
    # Histidine base: NE2 ~3.1A from Ser-OG, ND1 on the other side
    atoms.append(_atom("HIS", his_resid, "CA", 5.0, 0.0, 0.0))
    atoms.append(_atom("HIS", his_resid, "NE2", 4.0, 0.0, 0.0))  # 3.0A from OG
    atoms.append(_atom("HIS", his_resid, "ND1", 6.0, 0.0, 0.0))
    # Aspartate orienter: OD1 ~2.8A from His-ND1
    atoms.append(_atom("ASP", asp_resid, "CA", 9.0, 0.0, 0.0))
    atoms.append(_atom("ASP", asp_resid, "OD1", 8.5, 0.0, 0.0))  # 2.5A from ND1
    return atoms


def _metal_only_atoms():
    atoms = [
        _atom("HIS", 10, "NE2", 0.0, 0.0, 0.0),
        _atom("HIS", 12, "NE2", 20.0, 0.0, 0.0),
        _atom("GLU", 30, "OE1", 40.0, 0.0, 0.0),
    ]
    return atoms


class IsSerineHydrolaseEcTests(unittest.TestCase):
    def test_serine_endopeptidase(self) -> None:
        self.assertTrue(is_serine_hydrolase_ec(["3.4.21.4"]))

    def test_carboxylesterase(self) -> None:
        self.assertTrue(is_serine_hydrolase_ec(["3.1.1.3"]))

    def test_nuclease_prefix_is_not_triad(self) -> None:
        # 3.1.11/3.1.13 share the 3.1.1 text but are nucleases, not triad hydrolases
        self.assertFalse(is_serine_hydrolase_ec(["3.1.11.1"]))
        self.assertFalse(is_serine_hydrolase_ec(["3.1.13.1"]))

    def test_metallopeptidase_is_not_serine(self) -> None:
        self.assertFalse(is_serine_hydrolase_ec(["3.4.17.10"]))

    def test_empty(self) -> None:
        self.assertFalse(is_serine_hydrolase_ec([]))


class ConfirmTriadTests(unittest.TestCase):
    def test_resolved_and_corroborated_when_act_site_matches(self) -> None:
        atoms = _triad_atoms(ser_resid=250, his_resid=227, asp_resid=253)
        result = confirm_catalytic_triad(atoms, {250, 227, 253})
        self.assertTrue(result["geometric_triad_resolved"])
        self.assertTrue(result["annotation_corroborated"])
        self.assertEqual(result["status"], "ser_his_triad_annotation_corroborated")
        self.assertGreaterEqual(result["annotated_act_site_overlap_count"], 2)

    def test_resolved_but_uncorroborated_when_act_site_elsewhere(self) -> None:
        atoms = _triad_atoms()
        result = confirm_catalytic_triad(atoms, {900, 901})
        self.assertTrue(result["geometric_triad_resolved"])
        self.assertFalse(result["annotation_corroborated"])
        self.assertEqual(result["status"], "ser_his_triad_resolved_uncorroborated")

    def test_no_triad_on_metal_only(self) -> None:
        result = confirm_catalytic_triad(_metal_only_atoms(), {10, 12, 30})
        self.assertFalse(result["geometric_triad_resolved"])
        self.assertFalse(result["annotation_corroborated"])
        self.assertEqual(result["status"], "no_ser_his_triad")


class AssessCandidateTests(unittest.TestCase):
    def _row(self, *, ec, cofactors=(), coord_path=None, act_positions=()):
        return {
            "entry_id": "uniprot:TEST",
            "evidence": {
                "mechanism_evidence": {
                    "ec_numbers": list(ec),
                    "cofactors": [{"name": c} for c in cofactors],
                    "active_site_residues": [
                        {"feature_code": "ACT_SITE", "position": p}
                        for p in act_positions
                    ],
                },
                "structure_provenance": {"coordinate_path": coord_path},
            },
        }

    def test_skip_non_serine_ec(self) -> None:
        d = assess_ser_his_candidate(self._row(ec=["3.4.24.1"]))
        self.assertEqual(d["decision"], "skip")

    def test_hold_when_cofactor_annotated(self) -> None:
        d = assess_ser_his_candidate(
            self._row(ec=["3.4.21.4"], cofactors=["Zn(2+)"])
        )
        self.assertEqual(d["decision"], "hold")
        self.assertEqual(d["reason"], "catalytic_cofactor_annotated")

    def test_hold_when_no_coordinates(self) -> None:
        d = assess_ser_his_candidate(self._row(ec=["3.4.21.4"], coord_path=None))
        self.assertEqual(d["decision"], "hold")
        self.assertEqual(d["reason"], "no_staged_coordinates_for_triad_confirmation")

    def test_assign_when_triad_corroborated(self) -> None:
        with TemporaryDirectory() as tmp:
            cif = Path(tmp) / "model.cif"
            # write a tiny CIF the parser understands by round-tripping atoms is
            # complex; instead patch via the coordinate file using a real local CIF
            # is unnecessary -- assemble atoms through the geometry path directly.
            # Here we assert the rule wiring by giving a coordinate file whose
            # parsed atoms form the triad. We reuse the structure writer.
            from catalytic_earth.structure import parse_atom_site_loop  # noqa: F401

            # Build a minimal mmCIF atom_site loop with a resolved triad.
            atoms = _triad_atoms(ser_resid=250, his_resid=227, asp_resid=253)
            cif.write_text(_atoms_to_cif(atoms), encoding="utf-8")
            row = self._row(
                ec=["3.4.21.4"],
                coord_path=str(cif),
                act_positions=(250, 227, 253),
            )
            d = assess_ser_his_candidate(row)
            self.assertEqual(d["decision"], "assign_ser_his")
            self.assertEqual(d["fingerprint_id"], "ser_his_acid_hydrolase")


def _atoms_to_cif(atoms) -> str:
    header = [
        "data_test",
        "loop_",
        "_atom_site.group_PDB",
        "_atom_site.label_comp_id",
        "_atom_site.auth_comp_id",
        "_atom_site.label_asym_id",
        "_atom_site.auth_asym_id",
        "_atom_site.label_seq_id",
        "_atom_site.auth_seq_id",
        "_atom_site.label_atom_id",
        "_atom_site.auth_atom_id",
        "_atom_site.Cartn_x",
        "_atom_site.Cartn_y",
        "_atom_site.Cartn_z",
    ]
    rows = []
    for a in atoms:
        rows.append(
            " ".join(
                str(a[k])
                for k in (
                    "group_PDB",
                    "label_comp_id",
                    "auth_comp_id",
                    "label_asym_id",
                    "auth_asym_id",
                    "label_seq_id",
                    "auth_seq_id",
                    "label_atom_id",
                    "auth_atom_id",
                    "Cartn_x",
                    "Cartn_y",
                    "Cartn_z",
                )
            )
        )
    return "\n".join(header + rows) + "\n"


class BuildScanTests(unittest.TestCase):
    def test_scan_is_non_destructive_and_sizes_deficit(self) -> None:
        frozen = [
            {"fingerprint_id": "ser_his_acid_hydrolase", "label_type": "seed_fingerprint"}
            for _ in range(42)
        ]
        expansion = []
        audit = build_ser_his_triad_locator_scan(
            frozen, expansion, cif_paths=None, target_floor=100
        )
        self.assertEqual(audit["ser_his_counts"]["combined"], 42)
        self.assertEqual(audit["acquisition_contract"]["deficit_to_floor"], 58)
        g = audit["guardrails"]
        self.assertFalse(g["frozen_benchmark_written"])
        self.assertEqual(g["labels_emitted_to_registry"], 0)
        self.assertTrue(g["ec_used_for_scope_assignment_only_never_predictive"])

    def test_control_panel_measures_incidental_rate(self) -> None:
        # CIF round-trip through a temp file to drive the control panel
        with TemporaryDirectory() as tmp:
            cif = Path(tmp) / "m.cif"
            cif.write_text(_atoms_to_cif(_triad_atoms()), encoding="utf-8")
            audit = build_ser_his_triad_locator_scan(
                [], [], cif_paths=[cif], control_sample_limit=5
            )
            cp = audit["control_panel"]
            self.assertEqual(cp["structures_checked"], 1)
            self.assertEqual(cp["geometric_triad_resolved"], 1)


class WriteScanRealRegistryTests(unittest.TestCase):
    def test_writes_without_touching_registries(self) -> None:
        frozen_before = FROZEN_PATH.read_bytes()
        expansion_before = EXPANSION_PATH.read_bytes()
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "scan.json"
            report = Path(tmp) / "scan.md"
            audit = write_ser_his_triad_locator_scan(
                out_path=out,
                report_path=report,
                frozen_benchmark_path=FROZEN_PATH,
                expansion_registry_path=EXPANSION_PATH,
                coordinate_glob="artifacts/**/__no_such_dir__/*.cif",
                control_sample_limit=0,
            )
            self.assertTrue(out.exists())
            self.assertTrue(report.exists())
            self.assertEqual(audit["ser_his_counts"]["frozen"], 42)
            # 87 ser_his expansion labels were sourced 2026-06-11 (ser_his_hole_sourcing);
            # the recovery scan still confirms 0 here because it is given no coordinates.
            self.assertEqual(audit["ser_his_counts"]["expansion"], 87)
            self.assertEqual(audit["recovery_scan"]["confirmed_ser_his_recoveries"], 0)
            self.assertEqual(FROZEN_PATH.read_bytes(), frozen_before)
            self.assertEqual(EXPANSION_PATH.read_bytes(), expansion_before)


if __name__ == "__main__":
    unittest.main()
