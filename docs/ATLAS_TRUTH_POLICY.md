# Atlas truth policy

**Effective:** 2026-07-13

This policy defines what Catalytic Earth counts, what its evidence tiers mean,
how claims change, and when an evaluation surface is spent. It governs current
work even when an older artifact uses different terminology.

## Six counted objects

Every headline count must name exactly one object type. Mixed totals must show
their components and may not inherit the name of one component.

### Net reaction

A balanced, normalized transformation between reactants and products, normally
linked to Rhea/ChEBI or equivalent identifiers. A Net reaction is not a
stepwise catalytic mechanism.

### Source mechanism

A literature-grounded stepwise account from a named source and version, with
the source's uncertainty preserved. One curated example is not automatically
true for every homolog.

### Mechanism hypothesis

One explicit proposed sequence of elementary steps for a reaction or protein.
It may be imported, rule-generated, model-generated, or manually encoded. It
remains a hypothesis until evidence adjudicates it.

### Mechanism family/fingerprint

A project-defined grouping or retrieval category. A broad cofactor bucket may
be operationally useful but must not be counted as a distinct fine mechanism.

### Protein annotation record

A protein associated with a reaction, family, hypothesis, or evidence bundle.
Homolog expansion creates protein records, not new mechanisms by definition.

### Experimental observation

A measured activity, kinetic, structural, mutational, binding, or negative
result with conditions and controls. A database annotation or computational
consistency check is not an Experimental observation.

## Atlas evidence tiers

Tiers describe the evidence carried by an atlas object. Higher tiers add
evidence; they do not erase lower-tier provenance or disagreements.

### Tier 0 — canonical reaction

- balanced and normalized net transformation;
- stable source/release identity and atom mapping where available;
- no stepwise mechanism, protein grounding, or validation implied.

### Tier 1 — mechanism hypothesis

- explicit ordered steps or rule composition;
- alternatives, chemical assumptions, and source/model provenance;
- no protein-specific or experimental validation implied.

### Tier 2 — protein/site-grounded hypothesis

- sequence/structure mapping, catalytic residues or atoms, cofactor and
  geometry evidence, counterevidence, applicability domain, and abstention;
- computational support only unless a higher tier is also present.

### Tier 3 — independently reviewed mechanism

- claim-level adjudication by a qualified person or process outside the
  author/agent loop that generated the record;
- reviewer identity/date, conflicts, and unresolved alternatives preserved;
- upstream expert curation alone does not independently review a downstream
  automated transfer.

### Tier 4 — experimentally tested outcome

- assay conditions, materials, positive and negative controls, and measured
  result;
- positive and negative outcomes have equal record status;
- measured activity may still leave the detailed mechanism unresolved.

## Claim statuses

- **Supported:** directly supported at the exact stated unit, scope, endpoint,
  and evidence tier.
- **Diagnostic:** informative but insufficient for the broader conclusion a
  reader might otherwise infer.
- **Superseded:** the underlying record remains, but a newer interpretation or
  decision controls current use.
- **Retracted:** the wording must not be used as a current claim; the historical
  record remains visible.

Every current headline must have a `CE-###` entry in `CLAIMS.md` and
`data/governance/claim_ledger.json`.

## Exposure states

- **frozen_unscored:** row identities, endpoint, rule, and decision bar are
  fixed before any outcome is viewed; no score or adjudication is recorded.
- **exposed:** outcomes, labels, errors, or aggregate scores have been viewed
  by the project and may influence future choices.
- **exhausted:** the surface cannot support a new independent-validation claim.

An exposed or exhausted surface never becomes fresh again. Renaming it,
changing branches, starting a new agent session, changing the endpoint, or
writing a new preregistration does not reset exposure. Any view used for
feature choice, family admission, thresholds, error analysis, model selection,
or narrative selection counts as exposure.

All freeze, score, review, and correction events are appended to
`data/governance/exposure_ledger.jsonl`. Historical backfills are labeled as
such. Existing lines are never edited to improve the story; corrections append
new events and preserve the prior event.

## Expansion freeze and admission

Until the truth-governance, environment, and live-manifest gates pass:

- no new label/family expansion;
- no threshold or feature tuning on exposed surfaces;
- no new performance headline;
- no bulk artifact refresh that makes failing checks appear green without
  explaining the underlying drift.

Allowed work includes corrections, exposure backfill, tests, schema and IR
work, packaging, source crosswalks, strong-baseline integration, bounded
external review, and experimental-access preparation.

After the freeze lifts, a new atlas record must declare its counted object,
evidence tier, source/version lineage, exposure relationship, and whether the
record is a hypothesis, review, or observation.

## Endpoint and baseline rules

- The primary endpoint is frozen before outcomes are inspected.
- Post-hoc endpoints are labeled exploratory and shown beside the original.
- Exact and coarse endpoints are never substituted for each other.
- Baselines must match the scientific question and use the strongest
  applicable incumbent method reasonably available.
- Calibration, pilot, retrospective, and external validation are distinct
  labels.
- Uncertainty and abstention are reported with coverage, not as selective
  precision alone.

## Negative-result rule

Negative outcomes, failed gates, corrections, and superseded interpretations
remain addressable. They may be compressed behind an index, but not deleted or
silently overwritten. The atlas earns trust by retaining the route by which it
learned that a claim was wrong.
