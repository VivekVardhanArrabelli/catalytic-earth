# ePK Ligand-State Policy Freeze Review

Date: 2026-05-20
Subagent: B
Status: review-only policy freeze, not production activation

## Decision

The ligand-state policy can be frozen now for a future fresh ePK tranche selected after the freeze. It cannot be activated now. The current evidence supports a conservative prospective boundary, but threshold calibration, real external hard-negative scored re-audit, broad controls, and registry/label-factory gates remain blocked.

Frozen policy id: `epk_ligand_state_evidence_policy_v0_20260520`.

## 1. Predictive Ligand States

Predictive use is allowed only for active-gamma donor states that are pre-whitelisted before candidate selection and pass all local structure checks:

- `ATP`: predictive only when terminal gamma atom, local metal context, catalytic-site locality, and source-free acceptor/role features co-materialize in the same structure.
- `ANP`: predictive as a gamma-capable ATP-state analog only under the same checks. ANP plus a substrate/acceptor analog is not enough.
- `AMP-PNP`: predictive only through a frozen ligand-code alias map. Current repo evidence effectively treats `ANP` as the materialized AMP-PNP-like code; any additional aliases must be listed before tranche selection.

All predictive features must be mmCIF/local-geometry derived. No mechanism text, EC/Rhea/UniProt prose, source ids, labels, or source-reviewed role/acceptor assignments can enter the score.

## 2. Review-Only States

These can support review, blocker routing, or post-score adjudication, but not predictive scoring:

- `ADP` / `ADP+Mg`: product or post-transfer nucleotide context; no gamma-distance measurement.
- Product-state rows: ADP plus phosphorylated product/substrate, SEP/TPO context, or product-like co-complexes.
- Substrate/acceptor analogs: B31/KAN-like or other ligand analogs that mimic acceptor chemistry.
- ATP/ANP/AMP-PNP structures missing terminal gamma, local metal, same-structure co-materialization, or source-free acceptor/role features.
- Source-reviewed kinase-substrate evidence such as current 5HVK/4EKK-style rows.

## 3. Forbidden Predictive Context

Forbidden as predictive input:

- after-the-fact source review for kinase/substrate role, phosphosite, or acceptor identity
- candidate-specific alternate-structure repair
- cross-PDB split-state fusion, such as ATP-state context from one structure and product-state acceptor context from another
- product-state ADP without gamma geometry
- substrate/acceptor analog-only support
- homomeric chain choice as substrate mapping
- post-hoc ligand-code expansion or threshold selection after seeing fresh outcomes
- mechanism prose, entry names, labels, EC/Rhea identifiers, UniProt text, M-CSA ids/source ids, and expert rationale

## 4. Exact Frozen Policy

For a future fresh tranche:

1. Freeze the scorer implementation, ligand alias map, atom parser, metal rules, distance/abstention rules, duplicate exclusions, and threshold policy before candidate selection.
2. Select candidate structures only after that freeze and record the exact query/date/manifest.
3. Score per structure using only source-free mmCIF-derived local features.
4. Allow `ATP`, `ANP`, and frozen `AMP-PNP` aliases as active-gamma donor states only if terminal gamma-equivalent atom, local metal context, catalytic-site locality, and pre-frozen source-free acceptor/role features all pass in the same structure.
5. Abstain on ADP-only, product-state-only, split-state, substrate-analog-only, source-review-dependent, or post-hoc-repair rows.
6. Keep source review separate for post-score adjudication and reporting only.

## 5. Data Required Before Activation

Before any production activation, collect:

- fresh post-freeze tranche manifest and exclusion list for development rows
- per-row ligand-state calls, terminal-gamma materialization, metal context, acceptor/role features, and abstention reasons
- sibling-family and broad-stress controls scored under the exact frozen policy
- real external hard-negative scored re-audit, not just feature abstention
- threshold and abstention calibration on pre-declared data
- source-review separation audit proving no source context entered predictive features
- label-factory and registry gate artifacts for any future ePK fingerprint activation

## Evidence Notes

The preregistration and activation audit already block product-state ADP-without-gamma, mechanism text, and homomeric chain choice. The control re-audit is diagnostically clean on current rows but was not frozen before those rows were selected and lacks a real scored external hard-negative re-audit. The `m_csa:640` ANP/B31 result is useful review evidence for an active-gamma analog state, but B31-style acceptor analog context remains non-predictive. The 5LI1 and ligand-specific scout evidence reinforce the same rule: active-state context alone is insufficient unless source-free acceptor/role features co-materialize.

Bottom line: freeze this conservative policy for the next fresh tranche; do not activate ePK scoring yet.
