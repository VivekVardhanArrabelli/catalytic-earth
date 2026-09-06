from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from catalytic_earth.atlas10_source_adapters import parse_mcsa_scheme_flows
from catalytic_earth.atlas_draft_batch import ALDOLASE_TRANSKETOLASE_BATCH
from catalytic_earth.atlas_draft_sources import (
    MANIFEST_PATH,
    build_entry_request_url,
    default_draft_record_ids,
    load_draft_sources,
    validate_atlas_draft_source_manifest,
    validate_official_mcsa_url,
)
from scripts.build_atlas_draft_sources import AcquisitionMeter, CapturedResponses


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

    def test_live_fetch_rejects_redirects_before_reading_the_body(self) -> None:
        requested_url = build_entry_request_url(("M0106",))

        class RedirectedResponse:
            status = 200
            headers: dict[str, str] = {}

            def __init__(self, final_url: str) -> None:
                self.final_url = final_url
                self.read_called = False

            def __enter__(self) -> RedirectedResponse:
                return self

            def __exit__(self, *args: object) -> None:
                return None

            def geturl(self) -> str:
                return self.final_url

            def read(self, size: int = -1) -> bytes:
                self.read_called = True
                raise AssertionError("redirected response body must not be read")

        redirected_urls = (
            "https://example.com/thornton-srv/m-csa/api/entries/?format=json",
            "https://www.ebi.ac.uk/unrelated/entries/?format=json",
        )
        for final_url in redirected_urls:
            with self.subTest(final_url=final_url):
                response = RedirectedResponse(final_url)
                meter = AcquisitionMeter(requests_max=2, download_bytes_max=1024)
                with patch(
                    "scripts.build_atlas_draft_sources.urlopen",
                    return_value=response,
                ):
                    with self.assertRaises(ValueError):
                        meter.fetch(
                            requested_url,
                            request_kind="entry_batch",
                            record_ids=["M0106"],
                            mechanism_id=None,
                            step_id=None,
                        )
                self.assertFalse(response.read_called)

    def test_reordered_capture_ledger_fails_before_raw_files_are_used(self) -> None:
        def receipt(index: int, kind: str) -> dict[str, object]:
            return {
                "final_url": "https://www.ebi.ac.uk/example",
                "http_status": 200,
                "mechanism_id": None if kind == "entry_batch" else 1,
                "record_ids": ["M0106"],
                "request_index": index,
                "request_kind": kind,
                "response_bytes": 0,
                "response_sha256": "0" * 64,
                "retrieval_status": "source_response_downloaded",
                "retrieved_at": "2026-09-05T00:00:01Z",
                "source_url": "https://www.ebi.ac.uk/example",
                "started_at": "2026-09-05T00:00:00Z",
                "step_id": None if kind == "entry_batch" else 1,
            }

        ledger = {
            "schema_version": "catalytic-earth.temp-source-receipts.v1",
            "selection": ["M0106"],
            "limits": {"maximum_requests": 5, "maximum_download_bytes": 1024},
            "preflight": {
                "entry_requests": 1,
                "linked_scheme_requests": 1,
                "total_requests": 2,
            },
            "responses": [receipt(2, "step_scheme"), receipt(1, "entry_batch")],
            "aggregate": {
                "all_expected_responses_present": True,
                "download_bytes_remaining": 1024,
                "download_bytes_used": 0,
                "requests_remaining": 3,
                "requests_used": 2,
            },
            "completed_at": "2026-09-05T00:00:02Z",
        }
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "receipts.json").write_text(
                json.dumps(ledger), encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "response order differs"):
                CapturedResponses(
                    Path(directory),
                    record_ids=("M0106",),
                    meter=AcquisitionMeter(
                        requests_max=5, download_bytes_max=1024
                    ),
                )


class AldolaseTransketolaseDraftSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest, cls.entries = load_draft_sources(
            ROOT, batch=ALDOLASE_TRANSKETOLASE_BATCH
        )

    def test_successor_default_selects_only_new_draft_permitted_cases(self) -> None:
        expected = ("M0052", "M0219", "M0222")
        self.assertEqual(
            default_draft_record_ids(ROOT, batch=ALDOLASE_TRANSKETOLASE_BATCH),
            expected,
        )
        self.assertEqual(tuple(self.manifest["selection"]["record_ids"]), expected)
        self.assertEqual(
            self.manifest["selection"]["basis"],
            "development_gate_default_mechanism_draft_cases",
        )
        self.assertEqual(self.manifest["acquisition"]["external_requests_used"], 31)
        self.assertEqual(self.manifest["acquisition"]["download_bytes_used"], 569327)
        self.assertEqual(
            {
                record["record_id"]: record["snapshot_sha256"]
                for record in self.manifest["records"]
            },
            {
                "M0052": "b3d4ce2f44433d1be906bfd7bb696d3a899bb90bd1e70a2a7b39d28b35ead7d5",
                "M0219": "054f1c3bee9ff38938b59e81b6b4065fe4d4204cb899171f4f68c284bad7d01c",
                "M0222": "a798aef39309cdf3af82a003112b13949b160f9d305339c6ab9c08a3273908a7",
            },
        )

    def test_explicit_selection_cannot_claim_mechanism_draft_permission(self) -> None:
        changed = copy.deepcopy(self.manifest)
        changed["selection"]["basis"] = "explicit_record_ids"
        with self.assertRaisesRegex(
            ValueError, "explicit source-draft selection must request source_annotation"
        ):
            validate_atlas_draft_source_manifest(
                changed,
                repo_root=ROOT,
                batch=ALDOLASE_TRANSKETOLASE_BATCH,
            )

    def test_all_new_alternatives_steps_and_flows_survive(self) -> None:
        expected_steps = {
            "M0052": {1: list(range(1, 6))},
            "M0219": {1: list(range(1, 9)), 2: list(range(1, 7))},
            "M0222": {1: list(range(1, 12))},
        }
        observed_steps = 0
        observed_flows = 0
        for record_id, expected_mechanisms in expected_steps.items():
            entry = self.entries[record_id]
            self.assertEqual(
                {
                    mechanism["mechanism_id"]: [
                        step["step_id"] for step in mechanism["steps"]
                    ]
                    for mechanism in entry["mechanisms"]
                },
                expected_mechanisms,
            )
            for mechanism in entry["mechanisms"]:
                self.assertEqual(
                    sum(step["is_product"] for step in mechanism["steps"]), 1
                )
                for step in mechanism["steps"]:
                    scheme = entry["scheme_index"][
                        (mechanism["mechanism_id"], step["step_id"])
                    ]
                    parsed = parse_mcsa_scheme_flows(scheme)
                    self.assertEqual(
                        len(parsed["electron_flows"]), scheme["electron_flow_count"]
                    )
                    observed_steps += 1
                    observed_flows += len(parsed["electron_flows"])
        self.assertEqual(observed_steps, 30)
        self.assertEqual(observed_flows, 98)

    def test_source_conflicts_and_applicability_abstentions_survive(self) -> None:
        controls = {
            row["record_id"]: row
            for row in self.manifest["development_gate"]["case_controls"]
        }
        m0052_steps = self.entries["M0052"]["mechanisms"][0]["steps"]
        self.assertIn("inferred step", m0052_steps[2]["description"])
        self.assertIn("outside the enzyme active site", m0052_steps[3]["description"])
        self.assertIn(
            "all_steps_enzyme_catalysed",
            {item["clause_id"] for item in controls["M0052"]["mandatory_abstentions"]},
        )

        m0219 = self.entries["M0219"]
        mechanism_two = next(
            item for item in m0219["mechanisms"] if item["mechanism_id"] == 2
        )
        self.assertIn("D-xylulose-5-phosphate", mechanism_two["steps"][0]["description"])
        self.assertIn("D-erythrose-4-phosphate", mechanism_two["steps"][3]["description"])
        self.assertIn("chebi:57483", m0219["scheme_index"][(2, 1)]["content_utf8"])
        self.assertEqual(m0219["reference_uniprot_id"], "P29401")
        self.assertEqual(
            {
                sequence["uniprot_id"]
                for residue in m0219["residues"]
                for sequence in residue["residue_sequences"]
            },
            {"", "P23254"},
        )
        self.assertTrue(
            {
                "proposal_specific_reaction_context",
                "proposal_protein_applicability",
                "typed_cofactor_redox_state",
            }
            <= {
                item["clause_id"]
                for item in controls["M0219"]["mandatory_abstentions"]
            }
        )

        m0222 = self.entries["M0222"]
        self.assertIn(
            "D-glyceraldehyde 3- phosphate",
            m0222["mechanisms"][0]["steps"][0]["description"],
        )
        self.assertIn("chebi:57642", m0222["scheme_index"][(1, 1)]["content_utf8"])
        self.assertIn("evidence in archea", m0222["mechanisms"][0]["steps"][9]["description"])
        self.assertTrue(
            {"step_1_substrate_identity", "protein_specific_mechanism_applicability"}
            <= {
                item["clause_id"]
                for item in controls["M0222"]["mandatory_abstentions"]
            }
        )


if __name__ == "__main__":
    unittest.main()
