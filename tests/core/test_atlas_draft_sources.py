from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from catalytic_earth.atlas10_source_adapters import parse_mcsa_scheme_flows
from catalytic_earth.atlas_draft_sources import (
    MANIFEST_PATH,
    default_draft_record_ids,
    load_draft_sources,
    validate_atlas_draft_source_manifest,
    validate_official_mcsa_url,
)


ROOT = Path(__file__).resolve().parents[2]


class AtlasDraftSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest, cls.entries = load_draft_sources(ROOT)

    def test_default_selection_is_derived_from_current_draft_permissions(self) -> None:
        expected = ("M0106", "M0107", "M0212", "M0753")
        self.assertEqual(default_draft_record_ids(ROOT), expected)
        self.assertEqual(tuple(self.manifest["selection"]["record_ids"]), expected)
        self.assertEqual(set(self.entries), set(expected))
        self.assertEqual(self.manifest["acquisition"]["external_requests_used"], 49)
        self.assertEqual(self.manifest["acquisition"]["external_requests_expected"], 49)
        self.assertLessEqual(
            self.manifest["acquisition"]["download_bytes_used"],
            self.manifest["acquisition"]["download_bytes_max"],
        )

    def test_all_alternatives_ordered_steps_terminal_states_and_flows_survive(self) -> None:
        expected_steps = {
            "M0106": {1: list(range(1, 10))},
            "M0107": {2: list(range(1, 9)), 3: list(range(1, 9))},
            "M0212": {1: list(range(1, 17))},
            "M0753": {1: list(range(1, 8))},
        }
        observed_scheme_count = 0
        for record_id, expected_mechanisms in expected_steps.items():
            entry = self.entries[record_id]
            observed_mechanisms = {
                mechanism["mechanism_id"]: [step["step_id"] for step in mechanism["steps"]]
                for mechanism in entry["mechanisms"]
            }
            self.assertEqual(observed_mechanisms, expected_mechanisms)
            for mechanism in entry["mechanisms"]:
                terminal_steps = [step for step in mechanism["steps"] if step["is_product"]]
                self.assertEqual(len(terminal_steps), 1)
                for step in mechanism["steps"]:
                    scheme = entry["scheme_index"][
                        (mechanism["mechanism_id"], step["step_id"])
                    ]
                    self.assertEqual(
                        scheme["flow_parse_status"], "source_curved_arrows_preserved"
                    )
                    parsed = parse_mcsa_scheme_flows(scheme)
                    self.assertEqual(
                        len(parsed["electron_flows"]), scheme["electron_flow_count"]
                    )
                    if step["is_product"]:
                        self.assertEqual(parsed["electron_flows"], [])
                    observed_scheme_count += 1
        self.assertEqual(observed_scheme_count, 48)

    def test_gate_controls_preserve_case_specific_source_uncertainty(self) -> None:
        controls = {
            row["record_id"]: row
            for row in self.manifest["development_gate"]["case_controls"]
        }
        m0106_scope = controls["M0106"]["scope"]
        self.assertIn("P11961", m0106_scope)
        self.assertIn("structure context", m0106_scope)
        self.assertNotIn("P11961", self.entries["M0106"]["proteins"])
        self.assertEqual(
            set(self.entries["M0106"]["proteins"]), {"P21873", "P21874"}
        )
        self.assertEqual(
            {item["clause_id"] for item in controls["M0106"]["mandatory_abstentions"]},
            {"attachment_site", "carrier_host_identity", "structure_localization"},
        )

        m0753_abstentions = {
            item["clause_id"]: item["reason"]
            for item in controls["M0753"]["mandatory_abstentions"]
        }
        self.assertIn("resolved_aspartate_roles", m0753_abstentions)
        self.assertIn("Asp130 as proton acceptor", m0753_abstentions["resolved_aspartate_roles"])
        self.assertIn("Asp11 as donor", m0753_abstentions["resolved_aspartate_roles"])
        step_five = self.entries["M0753"]["mechanisms"][0]["steps"][4]["description"]
        self.assertIn("Asp 130 deprotonates", step_five)
        self.assertIn("Asp 11 supplying the proton", step_five)

        self.assertEqual(
            {item["clause_id"] for item in controls["M0212"]["mandatory_abstentions"]},
            {"complete_target_state"},
        )
        self.assertEqual(
            [item["mechanism_id"] for item in self.entries["M0107"]["mechanisms"]],
            [2, 3],
        )

    def test_snapshot_tampering_and_non_official_scheme_hosts_fail_closed(self) -> None:
        changed = copy.deepcopy(self.manifest)
        changed["records"][0]["snapshot_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "snapshot hash differs"):
            validate_atlas_draft_source_manifest(changed, repo_root=ROOT)
        with self.assertRaisesRegex(ValueError, "non-official M-CSA URL rejected"):
            validate_official_mcsa_url(
                "https://example.com/thornton-srv/m-csa/media/schemes/step.mrv",
                kind="step_scheme",
            )

    def test_manifest_on_disk_passes_offline_validation(self) -> None:
        manifest = json.loads((ROOT / MANIFEST_PATH).read_text(encoding="utf-8"))
        summary = validate_atlas_draft_source_manifest(manifest, repo_root=ROOT)
        self.assertEqual(summary["source_records"], 4)
        self.assertEqual(summary["mechanisms"], 5)
        self.assertEqual(summary["source_steps"], 48)


if __name__ == "__main__":
    unittest.main()
