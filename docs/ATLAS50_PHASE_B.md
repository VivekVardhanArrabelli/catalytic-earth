# Atlas-50 Phase B review and selection-freeze readiness

> **2026-09-05 scope update:** this document describes the frozen July
> contract. Its human-review and acquisition restrictions continue to apply
> to that package. New source-scoped development proceeds under the
> [computational policy and review](COMPUTATIONAL_DEVELOPMENT_REVIEW.md),
> without waiting for human submissions. The corrected crosswalk and state
> probe do not alter these packets or claim their human review is complete.

## Status

Phase B has started from merged Phase A commit
`375548419e7435efa2bffc89be5e32aa70864875`. The current checkpoint is ready
for attributable scientific review but is blocked for selection freeze. It is
not a completed review, a frozen Atlas-50 selection, source reacquisition, or
mechanism compilation.

The complete useful atlas remains the mission. This checkpoint makes the next
human and governance decisions inspectable without substituting automation,
upstream curation, packet preparation, or an outreach attempt for real review.

On 2026-09-05, local append-only intake was added around this frozen package.
It makes the packets usable without changing their bytes or claiming that a
submission has occurred. No submission was supplied in that maintenance run.

## Deterministic package

[`data/atlas/atlas50/phase_b/`](../data/atlas/atlas50/phase_b/) contains:

- `review_spec.json`: the review evidence, panel disposition, append-only
  submission, freeze, source, and claim-boundary contract;
- `crosswalk_review_queue.json`: exactly 57 packets reproducing each Phase A
  machine-draft classification, rationale, uncertainty, and thirteen source
  link/gap objects;
- `panel_review_queue.json`: exactly 40 packets reproducing the proposed
  inclusion or fail-closed exclusion, five gates, pressures, rights, expected
  tiers, abstentions, uncertainties, and stop conditions;
- `review_attempts.json`: an empty, truthful attempt ledger with zero reviewers,
  zero submissions, zero external messages, and no review claim;
- `freeze_candidate.json`: the exact immutable Atlas-10 plus 37-addition
  proposal, still explicitly unfrozen at 47 total cases;
- `source_reacquisition_plan.json`: ten source lanes for each of the 37 passing
  additions, with zero pre-freeze requests and no invented post-freeze budget;
- `inheritance_proof.json`: normalized byte proof for all ten merged Phase A
  files plus the inherited Atlas/protected-registry validation summary;
- `readiness_report.json`: the exact open blockers and next action boundary;
- `package_manifest.json`: hashes and byte counts for the contracts and
  deterministic outputs.

The corresponding versioned schemas are under
[`src/catalytic_earth/schemas/`](../src/catalytic_earth/schemas/), including an
attributable review-submission contract. Builders never edit a queue packet to
pretend review occurred. Future real submissions belong in the declared
append-only `review_submissions` namespace and must bind the exact packet hash,
reviewer identity/context, attestation, decisions, evidence references,
conflicts, and timestamp.

## Review boundary

All 97 packets remain `unreviewed`. No reviewer is identified, no message has
been sent, and no one has agreed to review. Upstream curation and agent output
do not count. A valid crosswalk submission must decide the classification and
all thirteen source families. A valid panel submission must address source,
diversity, rights, provenance, shared representation, object-tier,
abstention, and stop-condition dimensions. Revisions require evidence;
conflicts and unresolved fields remain explicit.

This review contract is not the Section 10.3 independent-annotation contract.
It cannot support an independent-review, inter-reviewer-agreement, or expert-
agreement claim. The project author flag is recorded so author review cannot be
presented as independent annotation.

## Local review intake

The review command operates from a source checkout and validates the complete
Phase A/B package before accepting any input:

```bash
python scripts/atlas50_review.py list
python scripts/atlas50_review.py packet \
  --packet-id atlas50.phase-b.crosswalk.ser_his_acid_hydrolase \
  --output ../atlas50-packet.json
python scripts/atlas50_review.py template \
  --packet-id atlas50.phase-b.crosswalk.ser_his_acid_hydrolase \
  --output ../atlas50-review-draft.json
# After a real reviewer completes the draft:
python scripts/atlas50_review.py validate \
  --submission ../atlas50-review-draft.json
python scripts/atlas50_review.py record \
  --submission ../atlas50-review-draft.json
python scripts/atlas50_review.py status
```

`packet` and `template` require a new output path outside the repository. The
template is intentionally invalid until a real reviewer fills every required
identity, attestation, outcome, rationale, uncertainty, and field decision.
The attestation must exactly match the frozen text in `review_spec.json`.
`validate` checks structure and frozen-contract consistency but does not record
the file. `record` repeats validation, rejects duplicate submission IDs, and
preserves the supplied bytes under a SHA-256-derived filename in the append-only
`review_submissions` namespace.

`status` scans recorded submissions without rewriting a queue or advancing a
freeze gate. It reports valid-submission coverage, decision variants, conflicts,
and unresolved work. In CI, pass the merge base or previous commit with
`--baseline-ref SHA` so append-only verification also covers submissions that
were already committed before the current change. `--output` writes the status
JSON to a new path outside the repository.

Successful structural validation means only that the supplied assertions fit
the contract and bind the stated packet. It cannot authenticate reviewer
identity, establish the scientific quality of a decision, resolve conflicting
submissions, support independent annotation, or approve a selection freeze.

## Unfrozen candidate and blockers

The freeze candidate preserves the Phase A 47-case proposal byte-for-byte in
substance: immutable Atlas-10 plus 37 passing additions and three exclusions.
It does not add cases to reach a round number. Nitrogenase, imidazole glycerol
phosphate synthase, and peptidoglycan glycosyltransferase remain excluded
pending reviewed, generic—not family-specific—contract dispositions.

Six freeze conditions are blocked:

1. all 57 crosswalk packets need attributable submissions;
2. all 40 panel packets need attributable submissions;
3. resulting revisions, conflicts, and unresolved fields must be preserved;
4. the three generic-contract dispositions need real review;
5. a bounded post-freeze source budget must be approved;
6. an explicit selection-freeze approval artifact must be recorded.

The inheritance condition passes. It does not make the selection ready: the
freeze candidate records `selection_frozen=false` and `freeze_ready=false`.

## Source and compute boundary

The source plan covers M-CSA mechanisms/arrow environments, Rhea/ChEBI,
UniProt, PDB/CATH, EC/InterPro/Pfam, EC-BLAST, EnzymeMap,
MechFind/EzMechanism, EnzyMM, and primary literature. Every lane has a
scientific question, cheapest credible method, expected output, rights
boundary, and stop condition.

Execution is prohibited before a reviewed selection freeze. Pre-freeze request
and download ceilings are zero; post-freeze CPU, request, and download budgets
remain null pending explicit approval. No source record was reacquired. GPU use
is zero because review, rights, provenance, and freeze governance—not compute—
are the active bottlenecks.

## Reproduction

```bash
python scripts/build_atlas50_phase_b.py --check
python scripts/validate_atlas50_phase_b.py
python scripts/run_test_tier.py "core/unit"
python scripts/validate_repository_contracts.py
```

The standard-library builder regenerates all derived JSON in canonical key
order. The validator compares exact bytes, rejects invented reviewer or source
activity, rejects compiled chemistry in review queues, keeps the selection
unfrozen, and revalidates Phase A plus inherited Atlas/protected objects.

## What remains

Local review intake is ready. The next scientific gate requires actual
attributable human submissions, and contacting a reviewer requires explicit
outreach authority. Until valid submissions exist and their unresolved or
conflicting decisions are handled, Phase B remains blocked for selection
freeze. Execution of this July acquisition/compilation plan remains prohibited; the
separate September policy permits its explicitly named draft operations.
Section 10.3 independent annotation, the 200-row bronze audit, fresh benchmark,
modern baselines, external task work, and assays remain separate and undone.

This checkpoint supports no accuracy, speedup, independent-validation,
discovery, design-readiness, assay, or atlas-coverage claim.
