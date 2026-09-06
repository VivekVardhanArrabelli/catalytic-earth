"""Verify the packaged Atlas-10 query surface from an empty working directory."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import venv
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory


EXPECTED_RUNTIME_RESULT_SHA256 = (
    "57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb"
)


def _venv_python(root: Path) -> Path:
    return root / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def verify_wheel(wheel: Path, *, include_source_drafts: bool = False) -> dict[str, object]:
    wheel = wheel.resolve()
    if include_source_drafts:
        with zipfile.ZipFile(wheel) as archive:
            if any(name.lower().endswith(".cif") for name in archive.namelist()):
                raise ValueError("raw primary structures must not enter the wheel")
    with TemporaryDirectory(dir=Path.home()) as tmp:
        root = Path(tmp)
        environment = root / "venv"
        empty_cwd = root / "empty"
        empty_cwd.mkdir()
        venv.EnvBuilder(with_pip=True, clear=True).create(environment)
        python = _venv_python(environment)
        subprocess.run(
            [str(python), "-m", "pip", "install", "--no-deps", str(wheel)],
            cwd=empty_cwd,
            check=True,
            capture_output=True,
            text=True,
        )
        completed = subprocess.run(
            [str(python), "-m", "catalytic_earth.core_cli", "atlas10"],
            cwd=empty_cwd,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(completed.stdout)
        if include_source_drafts:
            # A packaged query must work without the checkout, raw snapshots,
            # inherited PYTHONPATH, or a network connection.
            isolated_env = dict(os.environ)
            isolated_env.pop("PYTHONPATH", None)
            query = (
                "import contextlib, io, json, sys\n"
                "def block_network(event, args):\n"
                "    if event == 'socket.connect':\n"
                "        raise RuntimeError('network is forbidden during offline query')\n"
                "sys.addaudithook(block_network)\n"
                "from catalytic_earth.core_cli import main\n"
                "def run_query(*args):\n"
                "    output = io.StringIO()\n"
                "    with contextlib.redirect_stdout(output):\n"
                "        main(['atlas-drafts', *args])\n"
                "    return json.loads(output.getvalue())\n"
                "print(json.dumps({\n"
                "    'all': run_query('--steps'),\n"
                "    'ammonium': run_query('--reactant', '28938', '--product', '58278'),\n"
                "    'carbon_dioxide': run_query('--product', 'CHEBI:16526'),\n"
                "    'new_batch': run_query('--batch', 'aldolase-transketolase', '--steps'),\n"
                "    'aldolases': run_query('--batch', 'aldolase-transketolase', '--reactant', '57642', '--product', '49299'),\n"
                "    'primary': run_query('--batch', 'aldolase-transketolase', '--mcsa-id', 'M0222', '--text', 'DHAP-derived covalent moiety'),\n"
                "    'transketolase_context': run_query('--batch', 'aldolase-transketolase', '--mcsa-id', 'M0219', '--text', 'P29401'),\n"
                "    'plp_pyruvoyl': run_query('--batch', 'plp-pyruvoyl', '--steps'),\n"
                "    'pyruvoyl_event': run_query('--batch', 'plp-pyruvoyl', '--mechanism-component', 'decarboxylation'),\n"
                "    'extra_enzymatic': run_query('--batch', 'plp-pyruvoyl', '--mechanism-component', 'reaction occurs outside the enzyme'),\n"
                "    'events': run_query('--batch', 'all', '--mechanism-component', 'schiff base formed'),\n"
                "    'full_events': run_query('--batch', 'all', '--mechanism-component', 'schiff base formed', '--steps'),\n"
                "    'split_proposal': run_query('--batch', 'all', '--mechanism-component', 'decoordination from a metal ion', '--mechanism-component', 'decarboxylation'),\n"
                "    'step_contexts': run_query('--batch', 'plp-pyruvoyl', '--step-evidence'),\n"
                "    'step_contexts_full': run_query('--batch', 'plp-pyruvoyl', '--step-evidence', '--steps'),\n"
                "    'step_plp': run_query('--batch', 'all', '--step-cofactor', 'PLP'),\n"
                "    'step_extra': run_query('--batch', 'plp-pyruvoyl', '--step-enzyme-context', 'extra_enzymatic'),\n"
                "    'step_false_join': run_query('--batch', 'plp-pyruvoyl', '--step-cofactor', 'PLP', '--step-enzyme-context', 'extra_enzymatic'),\n"
                "    'step_inferred': run_query('--batch', 'plp-pyruvoyl', '--step-source-assertion', 'explicitly_inferred'),\n"
                "    'step_assumed': run_query('--batch', 'plp-pyruvoyl', '--step-source-assertion', 'explicitly_assumed'),\n"
                "    'observed_contexts': run_query('--batch', 'all', '--observed-state-context'),\n"
                "    'observed_contexts_full': run_query('--batch', 'all', '--observed-state-context', '--steps'),\n"
                "    'observed_analogue': run_query('--batch', 'all', '--observed-state', 'bound_ligand_analogue', '--observed-component', 'PDD'),\n"
                "    'observed_step_join': run_query('--batch', 'plp-pyruvoyl', '--observed-state', 'bound_ligand_adduct', '--step-enzyme-context', 'extra_enzymatic'),\n"
                "    'observed_false_join': run_query('--batch', 'all', '--observed-component', 'PDD', '--observed-component', 'PLV'),\n"
                "}))\n"
            )
            draft_run = subprocess.run(
                [str(python), "-c", query], cwd=empty_cwd, env=isolated_env,
                check=True, capture_output=True, text=True,
            )
            queries = json.loads(draft_run.stdout)
            drafts = queries["all"]
            records = drafts["records"]
            if {record["mcsa_id"] for record in records} != {"M0106", "M0107", "M0212", "M0753"}:
                raise ValueError("installed source draft batch differs")
            if len(records) != 4 or any(record["evidence_tier"] != 1 for record in records):
                raise ValueError("installed source drafts overstate their record count or tier")
            hisf = next(record for record in records if record["mcsa_id"] == "M0753")
            if not any(item["clause_id"] == "resolved_aspartate_roles"
                       for item in hisf["mandatory_abstentions"]):
                raise ValueError("installed source draft lost HisF source conflict")
            if not any(proposal["mechanism_steps"] for record in records
                       for proposal in record["mechanism_proposals"]):
                raise ValueError("installed source draft package lacks source steps")
            ammonium = queries["ammonium"]["records"]
            if len(ammonium) != 1 or ammonium[0]["mcsa_id"] != "M0753":
                raise ValueError("installed chemical query confused source reaction sides")
            if [row["source_row_index"] for row in ammonium[0]["participant_matches"]] != [1, 5]:
                raise ValueError("installed chemical query lost matching source evidence")
            if {r["mcsa_id"] for r in queries["carbon_dioxide"]["records"]} != {"M0106", "M0107"}:
                raise ValueError("installed chemical query lost distinct source reactions")
            if queries["carbon_dioxide"]["query_semantics"]["shared_participant_implies_reaction_equivalence"] is not False:
                raise ValueError("installed chemical query overstates participant matching")
            additional = queries["new_batch"]["records"]
            if {r["mcsa_id"] for r in additional} != {"M0052", "M0219", "M0222"} or len(additional) != 3:
                raise ValueError("installed successor source batch differs")
            if {r["mcsa_id"] for r in queries["aldolases"]["records"]} != {"M0052", "M0222"}:
                raise ValueError("installed chemical query lost the distinct aldolase sources")
            expected_abstentions = {
                "M0222": {"step_1_substrate_identity", "protein_specific_mechanism_applicability"},
                "M0219": {"proposal_specific_reaction_context", "proposal_protein_applicability"},
            }
            for record in additional:
                actual = {a["clause_id"] for a in record["mandatory_abstentions"]}
                if not expected_abstentions.get(record["mcsa_id"], set()) <= actual:
                    raise ValueError("installed successor source batch lost a source conflict")
            primary_records = queries["primary"]["records"]
            if len(primary_records) != 1 or primary_records[0]["mcsa_id"] != "M0222":
                raise ValueError("installed primary-evidence text query differs")
            primary = primary_records[0]["primary_evidence_annotations"]
            full = next(r for r in additional if r["mcsa_id"] == "M0222")
            if primary != full["primary_evidence_annotations"] or len(primary) != 1:
                raise ValueError("compact/full primary evidence differs")
            claim = primary[0]["claim"]
            if (claim["structure_site"]["author_residue_number"] != 229
                    or claim["sequence_mapping"]["sequence_position"] != 230
                    or claim["sequence_mapping"]["uniprot_id"] != "P00883"):
                raise ValueError("installed primary evidence lost the residue mapping")
            if claim["observed_state"]["normalized_chebi_id"] is not None:
                raise ValueError("installed primary evidence equated bound and free species")
            if primary_records[0]["evidence_tier"] != 1:
                raise ValueError("primary evidence changed the source-record tier")
            context_records = queries["transketolase_context"]["records"]
            if len(context_records) != 1 or context_records[0]["mcsa_id"] != "M0219":
                raise ValueError("installed transketolase context query differs")
            contexts = context_records[0]["primary_evidence_annotations"]
            full_tkt = next(r for r in additional if r["mcsa_id"] == "M0219")
            if len(contexts) != 1 or contexts != full_tkt["primary_evidence_annotations"]:
                raise ValueError("compact/full transketolase context differs")
            context = contexts[0]
            if context["proposal_binding"] != {
                "proposal_id": "atlas-draft.m0219.mechanism-2",
                "source_mechanism_id": 2,
                "reference_pubmed_id": "33828899",
            }:
                raise ValueError("installed transketolase context lost its proposal binding")
            context_claim = context["claim"]
            if context_claim["protein_context"] != {
                "pdb_id": "4KXV", "chain_id": "A", "uniprot_id": "P29401",
            } or context_claim["site_mappings"] != [
                {"residue_name": "LYS", "author_residue_number": 244,
                 "uniprot_sequence_position": 244},
                {"residue_name": "HIS", "author_residue_number": 258,
                 "uniprot_sequence_position": 258},
            ]:
                raise ValueError("installed transketolase protein/site mapping differs")
            support = context_claim["support_scope"]
            if (support["residue_roles"] != "computational_only"
                    or support["protonation_states"] != "computational_only"
                    or support["full_mechanism"] != "not_validated"
                    or context_records[0]["evidence_tier"] != 1):
                raise ValueError("installed transketolase context overstates evidence")
            events = queries["events"]
            if (events["searched_batch_ids"] != ["aldolase-transketolase", "default", "plp-pyruvoyl"]
                    or events["searched_record_count"] != 11
                    or events["record_count"] != 5
                    or events["mechanism_proposal_match_count"] != 5):
                raise ValueError("installed all-batch event query differs")
            event_records = {
                record["mcsa_id"]: record
                for batch in events["batches"] for record in batch["result"]["records"]
            }
            if set(event_records) != {"M0753", "M0222", "M0049", "M0066", "M0213"}:
                raise ValueError("installed event query lost a batch or added a false match")
            for batch, full_batch in zip(events["batches"], queries["full_events"]["batches"]):
                result, full_result = batch["result"], full_batch["result"]
                if result["selection"] != full_result["selection"]:
                    raise ValueError("installed event query changed the source selection")
                for record, whole in zip(result["records"], full_result["records"]):
                    if (record["mechanism_component_matches"] != whole["mechanism_component_matches"]
                            or record["mandatory_abstentions"] != whole["mandatory_abstentions"]
                            or record["evidence_tier"] != 1):
                        raise ValueError("installed compact/full event evidence differs")
                    for witness in record["mechanism_component_matches"]:
                        if witness["matched_labels"] != ["schiff base formed"]:
                            raise ValueError("installed event query lost its exact source label")
            if event_records["M0222"]["primary_evidence_annotations"] != primary:
                raise ValueError("installed event query lost primary evidence")
            split = queries["split_proposal"]
            if (split["record_count"] != 0 or split["mechanism_proposal_match_count"] != 0
                    or len(split["batches"]) != 3
                    or any(not batch["result"]["selection"] for batch in split["batches"])):
                raise ValueError("installed query combined alternative proposals or lost empty-batch scope")
            new_records = {r["mcsa_id"]: r for r in queries["plp_pyruvoyl"]["records"]}
            if set(new_records) != {"M0049", "M0066", "M0186", "M0213"}:
                raise ValueError("installed PLP/pyruvoyl batch identity differs")
            if any(r["evidence_tier"] != 1 or not r["mandatory_abstentions"]
                   for r in new_records.values()):
                raise ValueError("installed PLP/pyruvoyl batch lost its review boundary")
            required_limits = {
                "M0049": {"entry_scheme_substrate_identity", "pyruvoyl_maturation_mapping", "plp_equivalence"},
                "M0066": {"step_1_substrate_stereochemistry"},
                "M0186": {"plp_phosphate_base_assignment", "all_steps_enzyme_catalysed"},
                "M0213": {"direction_specific_role_assignment", "terminal_product_identity", "analogue_structure_context"},
            }
            for mcsa_id, limits in required_limits.items():
                if not limits <= {a["clause_id"] for a in new_records[mcsa_id]["mandatory_abstentions"]}:
                    raise ValueError("installed PLP/pyruvoyl record lost a specific scientific objection")
            if [r["mcsa_id"] for r in queries["pyruvoyl_event"]["records"]] != ["M0049"]:
                raise ValueError("installed decarboxylation query conflates PLP and pyruvoyl")
            if [r["mcsa_id"] for r in queries["extra_enzymatic"]["records"]] != ["M0186"]:
                raise ValueError("installed source query lost extra-enzymatic hydrolysis")
            serine_steps = new_records["M0186"]["mechanism_proposals"][0]["mechanism_steps"]
            if not all(serine_steps[i]["is_inferred"] is True for i in (3, 4)):
                raise ValueError("installed source steps lost explicit inference/assumption wording")
            contexts = queries["step_contexts"]
            if contexts["step_evidence_match_count"] != 32:
                raise ValueError("installed step context coverage differs")
            for compact, full in zip(contexts["records"], queries["step_contexts_full"]["records"]):
                if (compact["step_evidence_annotations"] != full["step_evidence_annotations"]
                        or compact["step_evidence_source_context"] != full["step_evidence_source_context"]
                        or compact["mandatory_abstentions"] != full["mandatory_abstentions"]):
                    raise ValueError("installed compact step query lost its source witnesses")
            step_plp = queries["step_plp"]
            if {r["mcsa_id"] for b in step_plp["batches"] for r in b["result"]["records"]} != {"M0066", "M0186", "M0213"}:
                raise ValueError("installed step cofactor query conflates source labels")
            extra_records = queries["step_extra"]["records"]
            if ([r["mcsa_id"] for r in extra_records] != ["M0186"]
                    or [a["step_binding"]["source_step_id"] for a in extra_records[0]["step_evidence_annotations"]] != [6, 7]
                    or queries["step_false_join"]["record_count"] != 0):
                raise ValueError("installed step query joined different enzyme/cofactor steps")
            inferred = {
                (r["mcsa_id"], a["step_binding"]["source_step_id"]): a["context"]["source_assertion"]["scope"]
                for r in queries["step_inferred"]["records"] for a in r["step_evidence_annotations"]
            }
            if inferred != {("M0049", 7): "whole_step", ("M0186", 4): "stated_detail_only"}:
                raise ValueError("installed step query confused inference scope")
            pyruvoyl_primary = [
                a for a in new_records["M0049"].get("primary_evidence_annotations", [])
                if a["annotation_id"] == "m0049.1pya.processed-pyruvoyl-site"
            ]
            if (len(pyruvoyl_primary) != 1
                    or pyruvoyl_primary[0]["claim"]["structure_site"]["author_residue_number"] != 82
                    or pyruvoyl_primary[0]["claim"]["sequence_mapping"]["status"] != "not_asserted"):
                raise ValueError("installed pyruvoyl observation confuses numbering or mapping scope")
            assumed = queries["step_assumed"]["records"]
            if ([r["mcsa_id"] for r in assumed] != ["M0186"]
                    or [a["step_binding"]["source_step_id"] for a in assumed[0]["step_evidence_annotations"]] != [5]):
                raise ValueError("installed step query confused inference and assumption")
            observed = queries["observed_contexts"]
            if observed["record_count"] != 11 or observed["observed_state_context_count"] != 3:
                raise ValueError("installed observed-state annotation coverage differs")
            for batch in observed["batches"]:
                result = batch["result"]
                if result["observed_state_context_count"]:
                    bindings = result["primary_evidence"].get("source_bindings", [])
                    if not any(b["artifact_kind"] == "primary_source_projection" for b in bindings):
                        raise ValueError("installed query lost abstract-projection provenance")
                    for record in result["records"]:
                        for annotation in record["observed_state_contexts"]:
                            if not annotation["projection_excerpt"]["support_edges"] or not annotation["projection_excerpt"]["locators"]:
                                raise ValueError("installed query lost observed-state source witnesses")
            observed_rows = {
                r["mcsa_id"]: r for b in observed["batches"] for r in b["result"]["records"]
            }
            full_observed_rows = {
                r["mcsa_id"]: r for b in queries["observed_contexts_full"]["batches"]
                for r in b["result"]["records"]
            }
            for name, row in observed_rows.items():
                if (row["observed_state_contexts"] != full_observed_rows[name]["observed_state_contexts"]
                        or row.get("primary_evidence_annotations") != full_observed_rows[name].get("primary_evidence_annotations")):
                    raise ValueError("compact/full observed-state evidence differs")
            if any(observed_rows[name]["observed_state_contexts"] for name in ("M0219", "M0222")):
                raise ValueError("installed query inferred a typed state for a legacy annotation")
            adduct = observed_rows["M0186"]["observed_state_contexts"][0]["claim"]
            if adduct["chemical_reconciliation"]["status"] != "unresolved_source_description_vs_deposit":
                raise ValueError("installed query lost the paper/deposited chemistry disagreement")
            analogue = [r for b in queries["observed_analogue"]["batches"] for r in b["result"]["records"]]
            if [r["mcsa_id"] for r in analogue] != ["M0213"]:
                raise ValueError("installed query confused analogue designation and bound adduct")
            instance = next(i for i in analogue[0]["observed_state_contexts"][0]["claim"]["structure_instances"]
                            if i["atom_author_chain_id"] == "B")
            if (instance["atom_author_residue_number"] != 1390
                    or instance["source_author_residue_number"] != 390
                    or instance["label_seq_id"] is not None):
                raise ValueError("installed query conflated deposited residue namespaces")
            joined = queries["observed_step_join"]
            if (joined["record_count"] != 1 or joined["step_evidence_match_count"] != 2
                    or joined["records"][0]["mcsa_id"] != "M0186"
                    or joined["query_semantics"]["observed_state_grounds_step"] is not False
                    or queries["observed_false_join"]["record_count"] != 0):
                raise ValueError("installed observed-state filter overstates the evidence join")
            print("Fresh-directory source draft query passed with network connections blocked")
    expected_counts = {
        "case_count": 10,
        "record_count": 30,
        "follow_on_case_count": 7,
        "follow_on_record_count": 21,
        "documented_rhea_gap_count": 3,
        "non_detailed_abstention_count": 1,
        "source_mechanism_step_count": 21,
        "source_electron_flow_count": 61,
    }
    if any(payload.get(field) != value for field, value in expected_counts.items()):
        raise ValueError("installed Atlas-10 case/truth counts differ")
    if payload.get("runtime_result_sha256") != EXPECTED_RUNTIME_RESULT_SHA256:
        raise ValueError("installed Atlas-10 runtime result hash differs")
    query_results = payload.get("relationship_query_results", {})
    if {query_id: len(rows) for query_id, rows in query_results.items()} != {
        "atlas10.query.convergent-strategy": 2,
        "atlas10.query.shared-fold-divergent-chemistry": 2,
    }:
        raise ValueError("installed Atlas-10 relationship query rows differ")
    if not payload.get("matches_expected"):
        raise ValueError("installed Atlas-10 did not match its packaged expectation")
    if any(
        payload.get(field) is not False
        for field in ("network_used", "external_binary_used", "accelerator_used")
    ):
        raise ValueError("installed Atlas-10 used an undeclared runtime dependency")
    rendered = json.dumps(payload)
    for required in (
        "engineered_source_reference",
        "documented_query_gap",
        "historical_fingerprint_bridge",
        "inferred=1",
    ):
        if required not in rendered:
            raise ValueError(f"installed Atlas-10 lost required boundary: {required}")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel", type=Path, required=True)
    parser.add_argument("--include-source-drafts", action="store_true")
    args = parser.parse_args()
    wheel = args.wheel
    if wheel.is_dir():
        wheels = sorted(wheel.glob("catalytic_earth-*.whl"))
        if len(wheels) != 1:
            raise SystemExit(f"expected one wheel in {wheel}, found {len(wheels)}")
        wheel = wheels[0]
    payload = verify_wheel(wheel, include_source_drafts=args.include_source_drafts)
    print(
        "Fresh-directory Atlas-10 wheel verification passed: "
        f"cases={payload['case_count']}, records={payload['record_count']}, "
        f"runtime_result_sha256={payload['runtime_result_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
