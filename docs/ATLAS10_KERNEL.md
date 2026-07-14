# Atlas-10 compiled query surface

**Compiled:** 2026-07-14
**Status:** computational artifacts, local wheel verification, and supported
PR CI complete; external review-attempt gate pending

Atlas-10 is the immutable Atlas-3 kernel plus seven source-bound follow-on
cases. It is useful atlas knowledge and a representation stress test, not a
representative biological benchmark and not ten equally detailed mechanisms.

## What now exists

- 10 selected biological cases and 30 separately counted truth objects;
- 21 new `mechanism-record.v3` objects: one reaction/source-gap, one source
  annotation, and one bounded Tier-2 hypothesis for each follow-on case;
- 45 case/source bindings over 44 unique records;
- 36 redistributed snapshots and eight verified DOI reference-only handles;
- seven UniProt records, seven Rhea records or frozen queries, seven M-CSA
  entries with linked schemes, eight PDB mmCIF archives, and seven unique CATH
  records (one is shared by two cases);
- three zero-row official Rhea EC queries retained as source gaps;
- 21 detailed non-product M-CSA source steps and 61 source-ordered curved-arrow
  objects, with no inferred atom map or compiled bond-edit list;
- one high-rated but explicitly non-detailed cyclophilin proposal with zero
  discrete compiled steps and a machine-visible abstention;
- two dependency-free SQLite relationship queries with frozen expected rows;
- a same-source unintegrated comparator and seven content-hashed review packets.

The follow-on kernel is
[`data/atlas/atlas10/kernel.json`](../data/atlas/atlas10/kernel.json). It binds
the source snapshot-set digest
`a6b6a0059835e8f3f78cd5da9897afb599560bc844c59e82ba523f9387d0550d`
and the unchanged Atlas-3 file digest
`0733a029b3eaa0900ff4124276c2060f94204ce3f3bf0b9bcf2c80e7589d674b`.

## Case truth boundaries

| Follow-on case | Reaction | Source granularity | Main boundary |
| --- | --- | --- | --- |
| Human carbonic anhydrase II | RHEA:10748 | 3 detailed source steps | Static 1CA2 does not resolve a unique solvent proton wire or protonation state |
| Hen egg-white lysozyme | Frozen zero-row EC query | Two detailed proposals, ratings 3 and 1 | Both source proposals remain separate; the lower-rated historical route is not independently readjudicated |
| *Fusarium* trypsin | Frozen zero-row EC query | 4 detailed source steps | pH-5 1PQ5 grounds sites but not productive physiological protonation through turnover |
| Subtilisin BPN' | Frozen zero-row EC query | 4 detailed source steps | P00782/1SUP is direct; engineered 1S01 is source-reference applicability evidence only |
| *Pseudomonas* mandelate racemase | RHEA:13945 | 3 detailed source steps | The inferred return step and inhibitor/chemical-modification structure context stay explicit |
| *Clostridium* methylaspartate ammonia-lyase | RHEA:12829 | 3 detailed source steps | The inferred return step and additional N-terminal domain are preserved |
| Human cyclophilin A | RHEA:16237 | Non-detailed, rating 3 | Zero discrete steps; the missing HTTP-404 scheme and substrate-specific 1M9C context block invented detail |

M-CSA sometimes lists a residue without a role string. The v3 schema permits an
empty role list, and the compiled lysozyme sites preserve it. The compiler does
not fill the gap with a plausible-sounding role.

## Relationship queries

The convergence query returns trypsin and subtilisin together with their
different CATH superfamilies, protein-specific residue numbering and source
steps, both Rhea gaps, evidence, uncertainty, and the 1S01 engineered warning.
It supports a shared role-level Ser-His-Asp strategy, not residue, substrate,
step, structure, or confidence transfer.

The divergent-chemistry query returns mandelate racemase and methylaspartate
ammonia-lyase with their shared CATH 3.20.20.120 anchor and anionic-intermediate
logic while preserving racemization versus ammonia elimination, different
bases and steps, the extra CATH 3.30.390.10 domain, inferred-step flags, and the
ammonia-lyase's null historical fingerprint bridge.

The frozen runtime-result digest is:

```text
57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb
```

## Same-source comparator

The preregistered baseline opens the same frozen sources separately and uses no
Atlas output as input. On the structural required-field contract it fills
68.75% equivalent fields; the integrated queries fill 100%. Five cross-source
conflicts remain unintegrated in the baseline and are explicitly represented,
not biologically adjudicated, in Atlas.

No observed human baseline was run. Human minutes, speedup, and applicability
error rates are therefore `null`. The comparison is not evidence of biological
accuracy, discovery utility, or a 20x time improvement.

## Review state and remaining gate

Seven bounded packets ask the five frozen micro-questions. Their manifest and
honesty ledger are under
[`data/atlas/atlas10/review/`](../data/atlas/atlas10/review/). No recipient or
external channel has been supplied, so all seven ledger rows correctly say
`not_attempted_missing_reviewer_channel`. No outreach or independent review is
claimed.

The computational artifacts are ready. A wheel built from this tree passed
fresh-directory Atlas-3 and Atlas-10 verification on Windows with Python 3.13;
the Atlas-10 runtime digest above reproduced exactly, and the raw source
snapshots were absent from the wheel. The published PR #27 matrix then passed
all four supported Ubuntu/Windows Python 3.10/3.12 jobs in
[Actions run 29364282230](https://github.com/VivekVardhanArrabelli/catalytic-earth/actions/runs/29364282230),
including clean-wheel reproduction.

Atlas-10 is not phase-exit complete until at least one real external review
attempt is recorded. A response is welcome but is not required for this
bounded phase; a non-response still must be recorded as a non-response. This
bounded attempt is not the two-expert independent-annotation requirement in
Section 10.3 of the truth-first review.

## Reproduce and audit

From the repository:

```bash
python scripts/build_atlas10_sources.py
python scripts/build_atlas10_kernel.py --check
python scripts/build_atlas10_runtime.py --check
python scripts/build_atlas10_baseline.py --check
python scripts/build_atlas10_comparator.py --check
python scripts/build_atlas10_review_packets.py --check
python scripts/run_test_tier.py "core/unit"
```

From an installed wheel:

```bash
catalytic-earth atlas10
```

Runtime execution is standard-library-only and reports zero network,
accelerator, and external-binary use. Raw upstream snapshots remain repository
audit inputs; the wheel packages the compiled kernel, queries, expected result,
source hashes, and attribution boundary.

## What this checkpoint does not support

It does not support representative coverage, mechanism accuracy rates,
independent biological validation, prospective discovery, atom-mapped bond
edits, complete turnover trajectories, universal substrate applicability,
design readiness, or a completed assay. The sole assay lane remains inherited
TEM-1, candidate-only and unrun.
