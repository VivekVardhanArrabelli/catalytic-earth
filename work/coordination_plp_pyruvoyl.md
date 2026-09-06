# PLP and pyruvoyl source batch: internal message board

## Objective and starting state

Implement the next decision-relevant chemistry batch: M0066 D-alanine
transaminase, M0213 alanine racemase, M0186 serine ammonia-lyase, and M0049
pyruvoyl-dependent histidine decarboxylase. Shared PLP or Schiff-base chemistry
does not establish mechanism equivalence. M0482 is deferred because the live
entry has a blank step rather than a detailed ordered proposal.

Work starts from clean main `1024cae9bf3d6a7cc01ba59023dc2fed7382e886`
(PR #38 merged, Actions 34007869417 passed all four jobs), on
`codex/plp-pyruvoyl-source-batch`. The original Atlas-10 and both existing
source batches are preserved. No registry expansion, benchmark rescoring,
human-review completion, experimental validation, or exact-reaction admission
is implied by this source-scoped work.

## Ownership and coordination

| Agent | Owned work | Handoff |
| --- | --- | --- |
| Root | Batch registration, generic fixes, existing tests, documentation, integration and publication | Integrate reviewed outputs and verify installed wheel |
| source_ingestion | New raw source package, manifest, attribution, compiled records and wheel assets | Exact captured bytes and source counts to chemical reviewer |
| state_contracts | New spec, probe, adjudications, review bindings, status and focused batch tests | Capture permission first; final scoped controls after actual review |
| draft_integration_review | New challenge.json and scientific challenge; subsequent read-only integration review | Source-to-claim objections and actual review verdict |

Agents message one another directly when dependencies are ready. Root records
material decisions here to avoid concurrent edits to the board. These agents
share a model and prior context; their review is correlated computational
review, not independent human validation.

## Admission questions

- M0066: preserve the D-enzyme/entry reaction versus L-glutamate Step 1
  contradiction; do not silently correct stereochemistry or claim exact
  reaction/step applicability.
- M0213: preserve direction-dependent acid/base assignments and the reference
  structure's analogue context.
- M0186: retain inferred phosphate roles and hydrolysis outside the enzyme.
- M0049: preserve the pyruvoyl post-translational modification and processed
  chain numbering; retain it as valid atlas chemistry outside the PLP relation.

Capture uses the existing bounded source-acquisition path with truthful request
receipts. Browser inspections are ancillary observations, not raw-package
receipts. Final compilation depends on the captured-source challenge.

## Execution log

- All three workstreams activated. Root registered the additive batch and used
  Computer Use to inspect the official M0049 entry and its displayed pyruvoyl
  residue table; the source capture remains a separate API/scheme operation.
- The source agent captured the exact four entries and 36 scheme panels in 37
  requests, totaling 589,303 response bytes. Every scheme returned HTTP 200
  and parsed successfully. The bundle contains 32 nonterminal steps, four
  terminal states and 99 arrows. No repeated download was needed for review.
- Chemical review found additional identifier conflicts: M0049 scheme panels
  1–6 carry CHEBI:32526 while its entry specifies CHEBI:57595; M0213 retains
  CHEBI:57972 through its terminal panel while its entry product is
  CHEBI:57416 and the drawing changes wedge orientation. The source agent and
  reviewer reconciled exactly which panels carry each identifier. No CIP
  assignment or chemical identity repair was inferred from those labels.
- M0186 exposed a compiler omission: explicit `we infer` and `we assume`
  wording was not recognized alongside `inferred`. Root added those exact
  markers; prose remains the authority for the scope of the inference. Both
  previous compiled bundles still rebuild byte-for-byte unchanged.
- The new batch exposed two extension assumptions: predecessors were fixed to
  the original six cases, and new identities had to occur in the frozen
  candidate list. Root generalized configured predecessor inheritance, retained
  review-claim/objection prefixes, and identity checks against captured official
  snapshots for new cases. Frozen identities and all old artifact pins remain
  enforced. The thirteen-case successor probe passes its deterministic check.
- Root verified 155 pre-existing scientific files against the starting commit;
  none changed. Final source adjudication, compilation and integration checks
  are in progress.
- The final challenge preserves eighteen predecessor claims and four objections
  unchanged, adding six focused claims and four scoped objections. Its reviewed
  payload is `40a81af713986f2c50116bf0e60e971ff5267af2403d44687ae2857823981c64`.
  State controls and the chemical reviewer reconciled all four final decisions:
  source annotation/drafting permitted, exact instances blocked. The prior nine
  adjudications remain unchanged. Missing-source, protein-identity and inherited
  decision tamper checks pass.
- Offline replay produced the final source package without new network traffic.
  The compiled bundle is
  `7f21e56cdb778e6c92008b740aa2dbce9b1b3de5700f730ffe47d4e922c11227`;
  it contains four Tier-1 drafts, four proposals, 32 reaction steps, four
  terminal states and 99 arrows. The source manifest is
  `15324e95d003df2bc85793fe8284014d03e743906dbe5b486ebb3792adb6d92c`.
- Local integration passed: 243 core tests (242 passed, one optional jsonschema
  skip), plus the final nine batch tests after adding negative assertions;
  repository contracts; and fresh-directory installed-wheel queries with
  networking blocked. The Atlas-10 runtime hash remains
  `57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb`.
  All 166 pre-existing atlas/source/package files are byte-identical to the
  starting commit. The generated architecture inventory changed only its path
  count, from 17,358 to 17,376, to include the eighteen new files.
- The final read-only implementation audit found no material blocking defect.
  It checked compact/full/empty query scopes, all-batch witnesses, inference
  flags, distinct M0186 panels, no input mutation, and the generalized ancestry
  and captured-identity checks. Publication and remote CI follow this locally
  verified state.
