"""Query data-declared chemical-role/atom/state/outcome joins using ordinary Python.

No enzyme-specific dispatch, prediction, causal scoring or geometry cutoff is
implemented here. The supplied relation declares the selected facts and their
applicability. This is a source-lane example, not a new Atlas runtime.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def load_reference(record_path, reference):
    path = record_path.parent / reference["path"]
    payload = path.read_bytes()
    if hashlib.sha256(payload).hexdigest() != reference["sha256"]:
        raise ValueError(f"Referenced evidence changed: {path}")
    return json.loads(payload)


def resolve_contrast(record_path, contrast):
    source=load_reference(record_path,contrast["evidence_record"])
    rows={x[contrast["relation_id_field"]]:x for x in source[contrast["relation_list_field"]]}
    return {"interpretation":contrast,"source_evidence_boundary":source["evidence_boundary"],"perturbation_relations":[rows[key] for key in contrast["relation_ids"]]}


def query(record_path, role_ids=None, recognition=False, contrast_ids=None):
    record_path = Path(record_path)
    relation = json.loads(record_path.read_text())
    measurements = load_reference(record_path, relation["model_measurements"])
    native = load_reference(record_path, relation["native_role_measurements"])
    outcome_index = {x["id"]:x for x in relation["measured_perturbation_and_outcome_evidence"]}
    answer = {
        "case_id": relation["case_id"],
        "record_status": relation["record_status"],
        "source": {k:relation["source"][k] for k in ("doi","version","posted_date","exposure")},
        "scissile_bond": relation["target"]["scissile_bond"],
        "model_to_assay_mapping": relation["target"]["model_to_assay_mapping"],
        "evidence_scope": relation["evidence_separation"],
    }
    if contrast_ids:
        contrasts={x["id"]:x for x in relation.get("role_contrasts",[])}
        answer["role_contrasts"]=[resolve_contrast(record_path,contrasts[key]) for key in contrast_ids]
        return answer
    if recognition:
        answer["recognition_constraints"] = relation["substrate_recognition_constraints"]
        answer["model_contacts"] = measurements["selected_ES_contacts"]
        answer["outcomes"] = [outcome_index[x] for x in relation["recognition_outcome_ids"]]
        return answer
    groups=relation["designed_chemistry_constraints"]["groups"]
    if role_ids:
        found={g["id"] for g in groups}
        if set(role_ids)-found:
            raise ValueError(f"Unknown role(s): {sorted(set(role_ids)-found)}; available: {sorted(found)}")
        groups=[g for g in groups if g["id"] in role_ids]
    answer["roles"]=[]
    for group in groups:
        item={"constraint":group}
        item["proposed_mechanism_steps"]=[step for step in relation["mechanism_hypothesis"]["ordered_steps"] if step["step"] in group["mechanism_step_ids"]]
        item["atoms_by_model_state"]=measurements["role_atoms"][group["model_atom_role_id"]]
        item["selected_state_metrics"]=[]
        for link in group["measurement_links"]:
            metrics={m["id"]:m for m in measurements["metrics"][link["model_state"]]}
            item["selected_state_metrics"].append({"model_state":link["model_state"],"model_file":measurements["model_files"][link["model_state"]],"metrics":[metrics[key] for key in link["metric_ids"]]})
        item["native_role_correspondences"]=[]
        for link in group["native_role_links"]:
            state=next(x for x in native["structures"] if x["pdb_id"]==link["pdb_id"])
            role=next(x for x in state["roles"] if x["role"]==link["role"])
            item["native_role_correspondences"].append({"correspondence":link,"state":state["state"],"source_sha256":state["source_sha256"],"role":role})
        item["outcomes"]=[outcome_index[x] for x in group["outcome_ids"]]
        contrast_index={x["id"]:x for x in relation.get("role_contrasts",[])}
        item["role_contrasts"]=[resolve_contrast(record_path,contrast_index[key]) for key in group.get("contrast_ids",[])]
        answer["roles"].append(item)
    answer["unresolved"]=relation["unresolved"]
    answer["design_decision"]=relation["decision"]
    return answer


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record",nargs="?",type=Path,default=Path(__file__).with_name("tdpn3_constraint_relation.json"))
    parser.add_argument("--role",action="append",help="Exact data-declared chemical role ID; repeat to select several.")
    parser.add_argument("--recognition",action="store_true",help="Return model contacts, transfer exclusions and substrate outcomes.")
    parser.add_argument("--contrast",action="append",help="Exact data-declared cross-design role contrast ID.")
    args=parser.parse_args()
    print(json.dumps(query(args.record,args.role,args.recognition,args.contrast),indent=2))


if __name__ == "__main__":
    main()
