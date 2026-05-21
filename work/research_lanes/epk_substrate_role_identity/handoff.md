# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-21T13:13:54-0500

Primary outcome: `candidate_evidence_rows_emitted`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Measured run time: 49.02 minutes (`2026-05-21T17:24:53Z` to
`2026-05-21T18:13:54Z`).

Run note: disk free space was 24 GiB, above the 10 GiB stop threshold. Normal
`git fetch origin` and `git pull --ff-only origin
research/epk-substrate-role-identity` were attempted at run start but the
sandbox could not write the linked-worktree `FETCH_HEAD`. `git fetch
--no-write-fetch-head origin` succeeded. Local `HEAD` still appears stale and
dirty relative to `origin/research/epk-substrate-role-identity`; continue using
the remote-tip temporary-index commit/push workaround if normal git metadata
operations remain blocked.

## What Was Emitted

This run added one bounded source-free coordinate modality: active-site
contact-interface materialization. The helper fetches coordinates in memory,
emits compact residue-shell/contact summaries, and writes no raw coordinate
dumps.

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_active_site_contact_interface_audit_v1_20260521.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/active_site_contact_interface_audit.py`

Inputs:

- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_evidence_v1_20260521.json`
- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_conflict_decision_v1_20260521.json`
- `artifacts/research_lanes/epk_substrate_role_identity/epk_phosphoproduct_materialization_audit_v1_20260521.json`

The helper reused 211 candidate/state rows, 54 PDB-level conflict rows, and 135
phosphoproduct materialization rows. It scanned 54 diagnostic PDBs in memory and
emitted 220 compact contact-interface rows:

- candidate gamma/acceptor pair rows: 204
- state-only rows: 16
- nonterminal phosphoproduct product/ADP/split rows re-emitted as state-only
  contact blockers: 9
- contact signature rows: 27
- mixed positive/counterexample contact signatures: 4

No PDB titles, UniProt prose, EC/Rhea, paper/source text, mechanism labels,
curated substrate names, post-hoc source repair, candidate-specific threshold
tuning, production labels, registries, fingerprints, migration manifests, or
raw coordinate dumps were used or changed.

## Evidence Summary

Coordinate states observed:

- `active_gamma=205`
- `adp_state=5`
- `product_state=4`
- `split_state=1`
- `ligand_absent=4`
- `ambiguous_coordinate_state=1`

Contact materiality classes:

- `same_chain_broad_intramolecular_active_site_contact=146`
- `same_chain_local_intramolecular_active_site_contact=18`
- `cross_chain_terminal_or_short_peptide_interface=24`
- `cross_chain_reciprocal_nucleotide_bearing_interface=10`
- `cross_chain_extended_folded_interface=5`
- `cross_chain_internal_fragment_contact=1`
- `product_state_no_active_gamma_interface=4`
- `adp_state_no_active_gamma_interface=5`
- `split_state_no_active_gamma_interface=1`
- `ligand_absent_no_active_gamma_interface=4`
- `ambiguous_coordinate_state_no_active_gamma_interface=1`
- `active_gamma_no_acceptor_candidate=1`

Blocker classes:

- `topology_ambiguity=174`
- `none=19`
- `product_state_evidence=9`
- `active_gamma_geometry=7`
- `ligand_materialization=5`
- `substrate_role_identity=4`
- `split_state_evidence=1`
- `internal_fragment_mimicry=1`

The no-promotion conflict projection remains unchanged:

- TP=14
- FP=0
- TN=8
- FN=0
- Abstained positives=6
- Abstained negatives=26

## Decisive Result

The blocker is not cleared source-free.

Contact materiality gives useful review-routing evidence, but it is not
biological substrate-role identity. Four contact signatures still mix positives
and counterexamples. The decisive reciprocal folded Tyr signature
`34fc26e9924a` is shared by review positives `9UUR` and `9UUX` and
counterexample `9UW4`.

Other hard cases:

- `3TM0` has same-chain broad active-site contact materialization, but that same
  class is heavily mixed with counterexamples, including same-chain pressure
  rows.
- `7B56` still materializes a cross-chain active-site contact; it remains
  blocked by internal-fragment mimicry, showing contact materiality alone is not
  substrate-role identity.
- `3QHR` and `3QHW` remain source-free `product_state` rows from
  phosphoproduct chemistry, but product chemistry is review-only biological
  context, not an active-gamma substrate-role proof.
- `1L0O` remains ADP-only product-state evidence.
- `4HPU` remains split-state counterpressure against promoting product/split
  chemistry into positive substrate-role calls.

The positive-only `cross_chain_terminal_or_short_peptide_interface` class is
not a new rescue rule; it mirrors the already-known strict terminal/short-peptide
support class and does not address product/ADP, reciprocal folded-chain, or
same-chain topology abstentions.

## Interpretation

The useful refinement is narrow: source-free coordinates can now show whether a
candidate acceptor chain physically occupies the nucleotide/gamma active-site
interface, and can route state-only product/ADP/split rows alongside active
gamma candidates. The feature still cannot adjudicate biological substrate role
for reciprocal folded-chain, same-chain, ADP-only, or analog/state-specific
cases without review context.

This is review-only blocker evidence. It is not a production rule and does not
support ePK production readiness.

## Verification

- `python -m json.tool` passed for the new artifact.
- Full run-log JSONL validation passed; final line has
  `primary_outcome=candidate_evidence_rows_emitted` and
  `measured_minutes=49.02`.
- Required run-record field validation passed.
- `python -m py_compile` passed for the new helper.
- No raw `.pdb`, `.cif`, or `.mmcif` files were written in the lane paths.
- No production label registries, mechanism fingerprints, migration manifests,
  or label imports were touched.

## Exact Next Experiment

Stop contact/interface scalar probing. Only resume this lane for a genuinely
new source-free modality that can distinguish reciprocal folded-chain biology
or ADP/analog state without review-context leakage. Otherwise preserve
source-reviewed adjudication for product/ADP, split-state, substrate-analog,
reciprocal folded-chain, and same-chain substrate biology.
