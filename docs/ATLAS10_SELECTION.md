# Atlas-10 follow-on selection

**Status:** frozen before follow-on compilation

**Frozen:** 2026-07-14

**Baseline commit:** `c129735c45a09ecc366ce71607e448dffe6669e7`

**Selection SHA-256:** `9bc114aaf793c51ec3b6273466f62a83974512a2dcf969d95d8b97453dd2795e`

Atlas-10 extends the immutable Atlas-3 kernel with seven deliberately difficult
cases. This is a build selection, not a representative benchmark, accuracy
sample, or claim that ten equally detailed mechanisms already exist.

The machine contract is
[`data/atlas/atlas10_selection.json`](../data/atlas/atlas10_selection.json).
Its schema and semantic validator freeze case identities, authoritative source
handles, source granularity, structure applicability, comparison relationships,
queries, compute ceilings, review packets, the incumbent-source baseline, and
the inherited TEM-1 assay boundary before compilation begins.

## What remains inherited

The following Atlas-3 cases and selection digest remain immutable:

- AdoCbl methylmalonyl-CoA mutase: radical rearrangement;
- *E. coli* MnSOD: metal redox/PCET and wrong same-EC transfer refusal;
- TEM-1 beta-lactamase: covalent acyl enzyme, competing base proposals, and the
  sole candidate assay lane.

Atlas-10 adds records under `data/atlas/atlas10/`. It does not rewrite the
Atlas-3 kernel or protected historical registries.

## The seven follow-on cases

| Case | Direct anchors | Pressure on the atlas | Required truth behavior |
| --- | --- | --- | --- |
| Human carbonic anhydrase II | P00918, RHEA:10748, 1CA2, M0216, CATH:3.10.200.10 | Zinc-bound hydroxide, proton relay, solvent/protonation state, geometry | Preserve unresolved proton wires and never call static geometry turnover evidence |
| Hen egg-white lysozyme | P00698, 1DPX, M0203, CATH:1.10.530.10; frozen Rhea EC-query gap | Covalent glycosyl enzyme and historically competing descriptions | Keep alternatives separate and do not invent a Rhea identifier |
| *F. oxysporum* trypsin | P35049, 1PQ5, M0173, CATH:2.40.10.10; frozen Rhea EC-query gap | Ser-His-Asp acyl enzyme in the trypsin fold | Answer a convergence query without importing subtilisin numbering or evidence |
| Subtilisin BPN' | P00782, direct unmutated 1SUP, M0723, CATH:3.40.50.200; engineered 1S01 retained separately; frozen Rhea EC-query gap | Same catalytic strategy in an unrelated fold plus a structure-applicability trap | Ground the target to 1SUP; keep 1S01 explicitly engineered |
| *P. putida* mandelate racemase | P11444, RHEA:13945, 1MNS, M0187, CATH:3.20.20.120 | Metal-stabilized enolate and stereospecific racemization | Keep inhibitor/modified structure context and inferred return-step uncertainty visible |
| *C. tetanomorphum* methylaspartate ammonia-lyase | Q05514, RHEA:12829, 1KCZ, M0468, CATH:3.20.20.120 plus its N-terminal domain | Same catalytic fold/common enolate logic but E1cB ammonia elimination | Preserve different chemistry and allow a null historical fingerprint bridge |
| Human cyclophilin A | P62937, RHEA:16237, 1M9C, non-detailed M0189, CATH:2.40.100.10 | Isomerization, polymer components, complex-specific applicability, unsupported step detail | Produce useful site/transition-state knowledge while mechanically abstaining from fabricated atom, bond, electron, proton, or ordered-step edits |

The point is not that these are the seven most important enzymes. They are the
smallest follow-on set found that attacks representation failures Atlas-3 did
not yet expose.

## Two useful relationship queries

### Convergent strategy across unrelated folds

The trypsin/subtilisin query must return the shared Ser-His-Asp acyl-enzyme
strategy alongside distinct CATH folds, protein-specific sites and numbering,
source-scoped steps, reaction-source gaps, uncertainty, and the engineered
1S01 warning. A shared fingerprint or catalytic-triad label is not evidence for
transferring any field.

### Shared fold with divergent chemistry

The mandelate-racemase/ammonia-lyase query must return the shared enolase-like
catalytic-domain anchor and metal-stabilized enolate logic alongside different
reactions, outcomes, residue roles, domains, inferred steps, and historical
fingerprint scope. Shared fold is a relationship to query, not a license to
copy a mechanism.

## Three explicit Rhea gaps

The frozen official Rhea EC queries for lysozyme, trypsin, and subtilisin did
not return direct reaction records at selection time. Their M-CSA participant
classes remain useful source-scoped knowledge, but they cannot be relabeled as
Rhea records. A later discovered or newly released Rhea record requires a
reviewed selection amendment with retrieval date and content hash.

This distinguishes three statements that are easy to conflate:

1. no direct record was returned by the frozen query;
2. other sources describe a reaction;
3. no reaction exists.

Only the first is asserted here.

## Mandatory non-detailed mechanism behavior

M-CSA M0189 for cyclophilin A is high-rated but non-detailed. Rating and
granularity are independent dimensions. Atlas-10 must be able to emit a
site-grounded Tier-2 transition-state/isomerization hypothesis with zero
invented discrete electron-flow steps. If the current mechanism IR cannot
express that cleanly, the IR must be extended; the case must not be distorted
to fit the schema.

This is an anti-cheating gate. A fuller-looking record is a worse result when
the extra detail is unsupported.

## Structure-applicability gate

Subtilisin M0723 points to engineered PDB 1S01. Atlas-10 freezes unmutated PDB
1SUP as the direct target structure and retains 1S01 as an engineered
source-reference object. Validation fails if 1S01 is relabeled direct or if
1SUP is removed.

The same general rule applies to every case: static, inhibitor-bound,
condition-specific, engineered, or complex-specific structures can provide
identity, site, and geometry evidence only within their recorded scope.

## Compute contract

These are stop ceilings, not spending targets or timelines:

| Resource | Each new case | Shared Atlas-10 phase ceiling |
| --- | ---: | ---: |
| CPU | 6 hours | 48 hours |
| GPU | 0 hours | 0 hours |
| External requests | 150 | 1,200 |
| Downloads | 100 MiB | 800 MiB |

The seven case ceilings total 42 CPU hours, 1,050 requests, and 700 MiB,
leaving bounded shared overhead. Selection and evidence compilation do not
need GPU work. This does not ban useful higher compute later: any GPU or larger
job requires a separate content-hashed amendment naming the uncertainty,
cheapest credible baseline, expected information gain, ceiling, reusable
output, and stop condition.

## Incumbent-source baseline

Atlas usefulness must be measured against opening the same frozen UniProtKB,
Rhea, PDB, M-CSA, DOI, and CATH sources separately. The comparator cannot use
Atlas-derived joins, generated synthesis, relationship inference, or hidden
labels. It records time, request count, field completeness, unresolved source
conflicts, applicability errors, unsupported detail, and query completeness.

This tests whether integration is useful. It is not a biological-accuracy
benchmark or a discovery claim.

## Review contract

Atlas-10 will produce five to ten small claim packets, each asking the same
bounded questions about reaction/source gaps, sites and numbering, source-step
fidelity, applicability, abstention, and evidence-tier boundaries. External
review must be attempted. A response is desirable but is not a condition for
bounded compilation when no reviewer answers.

A no-response outcome is recorded with date, channel, and packet hash. It is
never relabeled independent review, and upstream database curation is never
called review of Catalytic Earth's downstream interpretation.

## Assay boundary

No new Atlas-10 case is an assay candidate. The sole lane remains the inherited
TEM-1 nitrocefin candidate, unstarted and uncommitted. Physical work still
requires a separate preregistration, executor, materials, controls, acceptance
criteria, and frozen computational decision before results are exposed.

## Immediate execution sequence

Implementation status on 2026-07-14: steps 1–6 have computational artifacts.
The source package, v3 compiler, 21 follow-on records, two query expectations,
same-source comparator, and seven review packets are frozen and reproducible.
Step 6 is not fully exited because the review ledger records zero real external
attempts. Step 7 passed a local fresh-directory wheel check on
Windows/Python 3.13 but still needs the supported Windows/Linux Python
3.10/3.12 CI matrix on the published branch. See
[`ATLAS10_KERNEL.md`](ATLAS10_KERNEL.md).

1. Snapshot or reference the 45 frozen source handles with retrieval metadata,
   rights, hashes, and explicit gap/applicability records.
2. Freeze the Atlas-10 compilation specification and extend the mechanism IR
   only where these cases prove a missing concept.
3. Compile separate reaction/source-annotation/protein-hypothesis objects,
   including abstaining objects rather than padded records.
4. Materialize the two relationship queries and their expected results.
5. Run the unintegrated-source comparator without feeding Atlas outputs into
   it.
6. Emit five to ten content-hashed review packets and record outreach outcomes.
7. Reproduce from a clean package on Windows and Linux while Atlas-3 and
   protected registries remain unchanged.

Only then is the Atlas-10 computational phase complete.

## Validation

```bash
python scripts/validate_atlas3_selection.py
python scripts/validate_atlas10_selection.py
python scripts/validate_repository_contracts.py
python scripts/run_test_tier.py "core/unit"
git diff --check
```

The selection JSON Schema is
[`src/catalytic_earth/schemas/atlas10-selection-v1.schema.json`](../src/catalytic_earth/schemas/atlas10-selection-v1.schema.json),
and semantic enforcement lives in
[`src/catalytic_earth/atlas10_selection.py`](../src/catalytic_earth/atlas10_selection.py).
Compiled records use
[`src/catalytic_earth/schemas/mechanism-record-v3.schema.json`](../src/catalytic_earth/schemas/mechanism-record-v3.schema.json)
inside
[`src/catalytic_earth/schemas/atlas10-kernel-v1.schema.json`](../src/catalytic_earth/schemas/atlas10-kernel-v1.schema.json).
