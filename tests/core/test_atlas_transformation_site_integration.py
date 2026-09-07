from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from catalytic_earth import core_cli


class TransformationSiteIntegrationTests(unittest.TestCase):
    def command(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(core_cli.main(list(args)), 0)
        return json.loads(output.getvalue())

    def test_changed_oxygen_retains_original_review_and_protein_context(self):
        original = self.command("atlas-transformations", "--all", "--mcsa-id", "M0173")
        result = self.command("atlas-transformation-sites", "--mcsa-id", "M0173", "--source-atom", "a44")
        self.assertEqual(result["schema_version"], "catalytic-earth.transformation-site-query.v1")
        self.assertEqual(result["source_transformation_query"], original)
        expected = json.loads(core_cli._resource_bytes(core_cli.ATLAS10_EXPECTED))
        self.assertEqual(result["query_semantics"]["atlas10_bundle_sha256"], expected["kernel_sha256"])
        self.assertEqual((result["match_count"], result["changed_source_atom_count"],
                          result["resolved_source_atom_count"], result["unresolved_source_atom_count"]),
                         (1, 1, 1, 0))
        [match] = result["matches"]
        original_trypsin = next(row["result"] for row in original["sets"] if row["mcsa_id"] == "M0173")
        self.assertEqual(match["transformation"], original_trypsin["transformations"][0])
        self.assertEqual(match["transformation_payload_sha256"], original_trypsin["transformation_payload_sha256"])
        self.assertFalse(original_trypsin["review"]["human_review_performed"])
        [atom] = match["changed_source_atoms"]
        self.assertEqual(atom["source_atom_id"], "a44")
        self.assertEqual(atom["edit_ids"], ["e1", "e2"])
        self.assertEqual(atom["source_flow_ids"], ["o24"])
        self.assertIsNone(atom["deposited_atom_identity"]["atom_name"])
        self.assertEqual(atom["deposited_atom_identity"]["status"], "not_asserted")
        record = match["bound_atlas10_record"]
        self.assertEqual(record["record_id"], "mechanism:trypsin-fusarium-serine-protease-v1")
        self.assertEqual(record["evidence_tier"], 2)
        self.assertIn("condition_specific_pH_5", record["structures"][0]["context_flags"])
        self.assertEqual(self.command("atlas-transformations", "--all", "--mcsa-id", "M0173"), original)

    def test_unlabeled_proton_and_racemase_atoms_stay_unresolved(self):
        all_rows = self.command("atlas-transformation-sites")
        self.assertEqual((all_rows["match_count"], all_rows["changed_source_atom_count"],
                          all_rows["resolved_source_atom_count"], all_rows["unresolved_source_atom_count"]),
                         (2, 12, 2, 10))
        for mcsa_id, atom_id in (("M0173", "a50"), ("M0187", "a58"), ("M0187", "a63")):
            with self.subTest(mcsa_id=mcsa_id, atom_id=atom_id):
                result = self.command("atlas-transformation-sites", "--mcsa-id", mcsa_id, "--source-atom", atom_id)
                self.assertEqual((result["changed_source_atom_count"], result["resolved_source_atom_count"],
                                  result["unresolved_source_atom_count"]), (1, 0, 1))
        # A known catalyst in the right record is insufficient without the atom edge.
        missing_edge = self.command("atlas-transformation-sites", "--site-id", "P11444:H297")
        self.assertEqual(missing_edge["match_count"], 0)
        # A site in a different record cannot rescue an unrelated source atom.
        cross_case = self.command("atlas-transformation-sites", "--mcsa-id", "M0187", "--site-id", "P35049:S204")
        self.assertEqual(cross_case["match_count"], 0)

    def test_local_token_requires_record_and_output_cannot_overwrite(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                self.command("atlas-transformation-sites", "--source-atom", "a44")
            self.assertEqual(raised.exception.code, 2)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sites.json"
            args = ("atlas-transformation-sites", "--site-id", "P35049:S204", "--output", str(path))
            result = self.command(*args)
            raw = path.read_bytes()
            self.assertEqual(json.loads(raw), result)
            with self.assertRaises(FileExistsError):
                self.command(*args)
            self.assertEqual(path.read_bytes(), raw)

    def test_packaged_protein_context_must_match_immutable_kernel(self):
        resource_bytes = core_cli._resource_bytes
        kernel = json.loads(resource_bytes(core_cli.ATLAS10_KERNEL))
        record = next(row for row in kernel["follow_on_records"]
                      if row["record_id"] == "mechanism:trypsin-fusarium-serine-protease-v1")
        site = next(row for row in record["sites"] if row["site_id"] == "P35049:S204")
        site["pdb_mappings"][0]["author_position"] = 196

        def altered_resource(path):
            if path == core_cli.ATLAS10_KERNEL:
                return json.dumps(kernel).encode("utf-8")
            return resource_bytes(path)

        with patch.object(core_cli, "_resource_bytes", side_effect=altered_resource):
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    self.command("atlas-transformation-sites", "--site-id", "P35049:S204")
                self.assertEqual(raised.exception.code, 2)
