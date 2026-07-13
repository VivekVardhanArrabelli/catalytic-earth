# Catalytic Earth: rapid full-atlas operating map

**Audit snapshot:** `3ee9d320` on 2026-07-10
**Strategic amendment:** 2026-07-13
**Full rationale:** [truth-first full review](catalytic-earth-full-review-2026-07-10.md)

## North Star

> **Build the world's computable catalytic-mechanism atlas: a continuously expanding, provenance-grounded map connecting canonical reactions, alternative elementary mechanisms, catalytic residues and geometry, protein/evolutionary evidence, uncertainty, design constraints, assays, and experimental outcomes.**

The atlas is the mission. The mechanism IR/evidence compiler is its engine. Benchmarks and exposure ledgers are internal truth controls. Search/API surfaces deliver it. Prospective loops correct it.

## Tiered atlas

1. canonical reaction record;
2. explicit mechanism hypothesis;
3. protein/site-grounded hypothesis;
4. independently reviewed mechanism;
5. experimentally tested positive or negative outcome.

Breadth can grow rapidly, but every record keeps its tier. Automated hypotheses are useful knowledge; they are not gold.

## Truth baseline

- This bounded public-repository audit found no evidence of fabricated raw data; repository evidence cannot establish private intent.
- The June 28 M-CSA “never-touched” holdout had already been scored and declared spent; retract it as independent validation.
- The “76% mechanism recovery” is 76% cofactor-bucket consistency; exact fingerprint recovery was 31%. The reported ID/OOS medians do not establish novelty separation by themselves.
- `current702` is 685 bronze, 17 silver, zero project-gold; 683/702 rows are automation-curated.
- The 10,001 count is **8,305 positive fingerprint assignments plus 1,696 OOS protein-label records**, not 10,001 mechanisms.
- “About 2% of mechanism space” has no defensible mechanism unit or denominator and is withdrawn.
- The June 29 Swiss-Prot result is a narrow EC-proxy result, not mechanism gold.
- Structure beat pairwise Smith–Waterman on a selected set; Pfam/HMM and other modern baselines were not run.
- The preserved Python 3.13 audit ran 2,559 tests with 74 failures, 20 errors, and one skip. A later Git-blob audit corrected the attribution: 54 failed tests contained 179 CRLF-only hash comparisons, and one genuine historical lineage mismatch was quarantined without rehashing. After bounded dependency, portability, compatibility, and fixture repairs, the pinned expanded suite ran 2,585 tests with zero failures, zero errors, and one skip. This is software validation, not biological validation.

## Stop now

- new family and bronze expansion;
- feature/threshold tuning on exposed surfaces;
- new performance headlines;
- more dated artifacts without a canonical release;
- calling automated checks “verified”;
- asking outsiders to review the whole repository;
- training a broad model.

## Two clocks

- **35-day computational atlas loop.** Complete the first end-to-end atlas cycle in five weeks.
- **60–90-day experimental target.** Begin on day one using an existing assay and ready lab/core/vendor. This target is conditional on physical execution capacity.

## Hours 0–48: truth reset

1. Freeze exposed surfaces and further scaling.
2. Publish `CLAIMS.md` with Supported / Diagnostic / Superseded / Retracted.
3. Publish `ERRATA.md` and correct the listed claims.
4. Create the append-only exposure ledger; spent means spent forever.
5. Freeze the five atlas tiers and six counted-object definitions.
6. Name one canonical README/MAP/roadmap path.

**Gate:** no document calls an exposed set untouched, a cofactor endpoint mechanism recovery, or a protein-label count a mechanism count.

## Days 3–7: atlas kernel

1. Define the typed mechanism IR.
2. Encode three deliberately different mechanisms.
3. Add locked core dependencies and minimal Linux/Windows CI.
4. Create a live release/artifact manifest.
5. Publish a lean source release or blob-filtered sparse-clone path.
6. Materialize one local DuckDB/SQLite/Parquet query.
7. Begin M-CSA, Rhea/ChEBI, and project-record adapters.

**Gate:** a fresh environment reproduces the three mechanism records without loading the multi-gigabyte artifact tree.

## Days 8–14: Atlas-10

- encode ten difficult mechanisms spanning radicals, metals/redox, covalent intermediates, proton ambiguity, alternative mechanisms, convergent folds, changed chemistry, conflicting literature, abstention, and design geometry;
- crosswalk them to incumbent reaction/mechanism/site resources;
- implement two useful queries;
- run one strong external baseline pipeline;
- publish one-command reproduction;
- obtain bounded outside review of five to ten cases.

**Gate:** the schema is converging and one query adds measurable value beyond opening incumbent resources separately.

## Days 15–30: Atlas-50 alpha

- expand to 50 only if the Atlas-10 schema is stable;
- draft-crosswalk all 57 existing fingerprints as duplicate / aggregation / specialization / bridge / genuinely missing / unsupported;
- audit 50 bronze rows to identify error modes;
- ship a searchable public alpha;
- publish weekly immutable release manifests;
- record external task failures as first-class data.

Stretch work: expand the audit toward 200, add a second reviewer, run broader baselines, and begin machine-import drafts for the detailed M-CSA mechanism core.

## Days 31–35: first complete computational loop

Input:

```text
one canonical reaction + one candidate protein/structure
```

Output:

- atom-mapped transformation;
- ranked alternatives and exact source analogues;
- protein/site evidence and counterevidence;
- calibrated decision or abstention;
- atomic constraints only where justified;
- assay, controls, and falsification contract;
- compact reproducible release.

This completes a computational atlas loop. It is not experimental discovery.

## Parallel days 1–90: experimental route

- select a mechanism with an existing cheap assay;
- engage one lab, core, CRO, or vendor immediately;
- define a tiny candidate/control panel;
- stage materials while the atlas kernel is built;
- freeze the computational decision before outcomes are seen;
- store positive and negative outcomes at the experimental tier.

If no ready execution route exists, finish the 35-day computational loop without claiming biological validation.

## Full-atlas expansion

```text
Atlas-3
→ Atlas-10
→ Atlas-50
→ detailed M-CSA mechanism core
→ Rhea/MechFind-scale hypothesis layer
→ protein/site grounding
→ continuous review and experiments
```

The kernel is not discarded or “completed before” the atlas. It is the atlas’s first trusted vertical slice.

## Compute rule

The project is compute-disciplined, not compute-poor. Every material job records:

```text
scientific question
→ cheapest credible baseline
→ expected information gain
→ maximum compute budget
→ stop condition
→ content-hashed reusable output
```

Spend compute on frozen uncertainties and reusable atlas layers. Do not train a broad model, bulk-score without a user question, rerun spent data, or generate hypotheses nobody will adjudicate.

## Permanent red lines

- A spent row is never untouched again.
- A post-hoc endpoint is never presented as preregistered.
- Upstream expert curation is never independent review of a downstream automated label.
- Reactions, mechanisms, fingerprints, protein records, and experiments are counted separately.
- Automated consistency is never experimental verification.
- Negative results are never deleted.
- Speed never comes from weakening evidence labels.

## The map in one sentence

**Keep the full atlas as the mission; build its smallest correct kernel in 14 days, ship Atlas-50 in 30, complete one computational loop in 35, pursue physical testing in parallel, and make every fast step preserve evidence tier, exposure history, and falsifiability.**
