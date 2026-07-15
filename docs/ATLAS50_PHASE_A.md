# Atlas-50 Phase A precompilation checkpoint

## Status

Atlas-50 Phase A is a deterministic, review-aware precompilation package. It
does not freeze the Atlas-50 selection and does not compile any proposed
follow-on mechanism. The full useful atlas remains the mission; Atlas-50 is a
representation checkpoint, not a benchmark destination.

The package starts from merge
`89498a7b0e6e5ea419654bb8ff563512ab36bb89`, treats the Atlas-10 scientific
exit gate as passed, and preserves Atlas-3, Atlas-10, and the protected
registries. The expansion freeze remains active.

## Deterministic outputs

The generated package under [`data/atlas/atlas50/phase_a/`](../data/atlas/atlas50/phase_a/)
contains:

- `crosswalk_draft.json`: exactly 57 source-linked fingerprint rows. Every row
  has a classification, rationale, uncertainty, thirteen source-family link or
  gap objects, and `review_status=unreviewed`. The classification counts are 1
  exact-duplicate candidate, 26 aggregations, 24 specializations, 4
  interoperability bridges, 0 genuinely missing concepts, and 2
  unsupported/ill-defined rows. These are machine-draft classifications, not
  completed review decisions.
- `candidate_matrix.json`: exactly 40 deliberately difficult follow-on rows
  with source availability, explicit gaps, rights boundaries, representation
  pressures, contingent object-tier expectations, per-row compute ceilings,
  stop conditions, and five fail-closed gates.
- `proposed_panel.json`: immutable Atlas-10 plus 37 passing additions, for a
  47-case proposal. This is a proposal, not a selection freeze.
- `blocker_report.json`: the exact three excluded cases and the general
  representation contracts required before they can be reconsidered.
- `package_manifest.json`: SHA-256 and byte counts for the machine-readable
  inputs, schemas, and deterministic generated outputs.

The human-auditable inputs are `crosswalk_spec.json`, `candidate_spec.json`,
`source_catalog.json`, `job_ledger.json`, and `inherited_baseline.json` in the
same directory. The JSON Schemas are versioned under
[`src/catalytic_earth/schemas/`](../src/catalytic_earth/schemas/).

## Crosswalk truth boundary

The crosswalk links, where a defensible lookup key exists, to M-CSA mechanisms,
M-CSA arrow-environment lookup keys, Rhea/ChEBI, EC-BLAST, EnzymeMap,
MechFind/EzMechanism, EnzyMM, and EC/InterPro/Pfam/CATH. A link is a candidate
handle or query key only. An explicit gap is emitted when no defensible handle
was frozen.

No row asserts that an EC number is a unique mechanism, that source-reported
ChEBI participants form a balanced Rhea reaction, that a fold licenses
mechanism transfer, or that a tool lookup was run. Upstream curation is not
independent review. No reviewer, outreach, agreement, atom map, bond edit,
catalytic role, mechanism step, or canonical identifier was invented.

## Follow-on feasibility result

All 40 candidates pass the declared source, diversity, identifiers-only rights,
and provenance gates for this bounded precompilation task. Thirty-seven also
pass the shared-representation projection. Three fail closed:

1. M0212 nitrogenase lacks a general contract for coupled component,
   metallocluster, electron-delivery, and redox-state transitions.
2. M0753 imidazole glycerol phosphate synthase lacks a general contract for
   coupled subunit conformations, channel state, and transported-intermediate
   provenance.
3. M0970 peptidoglycan glycosyltransferase lacks a general contract for polymer
   chain state, reaction-instance boundaries, and processivity.

No family-specific field was added to make these cases pass. Their exact
unlock conditions remain open in `blocker_report.json`.

The precompilation projection counts the 10 already represented Atlas-10 cases
plus the 37 passing additions: 47 of the eventual 50-case surface, or 94%,
appear representable without family-specific ad hoc fields. This is only a
field projection. It is not the final Section 10.2 result, which still requires
selection freeze, source reacquisition where needed, case compilation, and
case-level validation.

The proposed surface pressures radicals, metal and metallocluster chemistry,
redox/cofactor states, covalent intermediates, proton ambiguity,
conformational gating, same-net/different-mechanism pairs, the inherited
Atlas-10 convergent-fold and divergent-chemistry relationships, source
alternatives, literature conflicts that still require adjudication, unresolved
mechanisms, applicability gaps, and abstention.

## Source, rights, and compute boundary

The bounded source inventory records retrieval dates, live or frozen versions,
response hashes, redistribution boundaries, reference-only resources, and five
failed acquisitions. Raw M-CSA pages, article bodies, EnzymeMap reactions,
MechFind rules/arrow environments, EnzyMM templates, EC-BLAST results, and
EzMechanism outputs are not bundled.

Each material job was recorded before execution with its question, cheapest
credible method, expected information gain, budget, reusable output, and stop
condition. Phase A used zero GPU work. More GPU capacity does not change that
decision because the unresolved work is source, rights, review, and shared
representation governance rather than a compute bottleneck.

## Immutable inheritance proof

`inherited_baseline.json` anchors nine baseline Git objects containing 96
Atlas-3/Atlas-10 data, selection, packaged-data, and canonical documentation
files. Validation requires the current Git object IDs and normalized content
sets to match the baseline and each scoped worktree to remain clean. It also
checks the four protected registry hashes against
[`data/governance/expansion_freeze.json`](../data/governance/expansion_freeze.json)
and requires `frozen=true`.

## Reproduction

From the repository root:

```bash
python scripts/build_atlas50_phase_a.py --check
python scripts/validate_atlas50_phase_a.py
python scripts/run_test_tier.py "core/unit"
python scripts/validate_repository_contracts.py
```

The builder uses only the standard library and canonical sorted JSON. The
validator rebuilds the package in memory, compares exact bytes, verifies all
semantic gates, and rechecks inherited objects and protected hashes.

## What remains

Phase A completes only the machine draft and precompilation proposal. A later
phase must obtain real crosswalk review, decide any missing general contracts,
freeze a fail-closed selection, reacquire and verify source records under their
rights boundaries, and then compile selected mechanisms. The Section 10.3
independent annotation, 200-row bronze audit, fresh benchmark, modern baseline
suite, external coordination, and any assay work remain separate and undone.

This checkpoint supports no accuracy, speedup, independent-validation,
discovery, design-readiness, assay, or atlas-coverage claim.
