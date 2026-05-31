"""Predicted-geometry novelty-abstention probe (deployment-valid).

Tests whether the hand-router geometry top1 score, computed on PREDICTED
(AlphaFold) structure, separates in-scope held-out rows from out-of-scope rows --
and in particular flags the cofactor-confounded OOS rows where the cofactor
channel is confidently wrong.

Uses only the predicted-geometry rows from the robustness audit (NOT the
experimental teacher-side geometry retrieval, which retains ligand/cofactor
context and is not deployment-valid). Nothing is fit here; the top1_score is an
existing per-row artifact value. Writes /tmp/predgeom.json.

Run: python scripts/predicted_geometry_abstention_probe.py
"""
import json

AUDIT = "artifacts/v3_predicted_geometry_robustness_audit_current702_20260529.json"
CONFOUNDED = ["m_csa:30", "m_csa:31", "m_csa:80", "m_csa:191",
              "m_csa:267", "m_csa:448", "m_csa:549", "m_csa:563"]


def auc_in_gt_oos(in_scope, oos):
    if not in_scope or not oos:
        return None
    greater = sum(1 for a in in_scope for b in oos if a > b)
    ties = sum(1 for a in in_scope for b in oos if a == b)
    return round((greater + 0.5 * ties) / (len(in_scope) * len(oos)), 4)


def main():
    d = json.load(open(AUDIT))
    rows = {r["entry_id"]: r for r in d["hand_router_on_predicted_geometry"]["rows"]}

    inscope, oos = [], []
    for r in rows.values():
        if r.get("split_assignment") != "heldout":
            continue
        if not r.get("predicted_geometry_joined"):
            continue
        score = r.get("top1_score")
        if score is None:
            continue
        (inscope if r.get("true_fingerprint_id") else oos).append(float(score))

    conf, per = [], {}
    for e in CONFOUNDED:
        r = rows.get(e)
        if r and r.get("top1_score") is not None and r.get("predicted_geometry_joined"):
            conf.append(float(r["top1_score"]))
            per[e] = round(float(r["top1_score"]), 4)
        else:
            per[e] = None

    result = {
        "n_inscope": len(inscope),
        "n_oos": len(oos),
        "n_confounded": len(conf),
        "pred_geom_top1_auc_in_gt_all_oos": auc_in_gt_oos(inscope, oos),
        "pred_geom_top1_auc_in_gt_confounded_oos": auc_in_gt_oos(inscope, conf),
        "inscope_mean": round(sum(inscope) / len(inscope), 4) if inscope else None,
        "all_oos_mean": round(sum(oos) / len(oos), 4) if oos else None,
        "confounded_mean": round(sum(conf) / len(conf), 4) if conf else None,
        "per_confounded_pred_geom_top1_score": per,
    }
    open("/tmp/predgeom.json", "w").write(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
