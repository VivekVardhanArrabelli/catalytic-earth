# P0 truth-reset completion record

**Effective:** 2026-07-13

**Source:** Section 9 of `docs/reviews/catalytic-earth-full-review-2026-07-10.md`

**Machine gate:** `python scripts/validate_repository_contracts.py`

This document maps every priority-cleanup instruction to an implementation,
evidence, and validation path. “Complete” means the repository contains the
control and it passes locally. Cross-platform claims additionally require the
four GitHub jobs in `.github/workflows/p0-contracts.yml` on the exact release
commit. “Guarded deferment” means the requested mutation would be destructive,
legally unresolved, or pointless before its stated prerequisites; the block is
recorded and machine-visible rather than hidden behind a false completion
claim.

P0 makes the project truth-enterable and reproducible. It does not make a
biological result correct, turn the core fixture into a benchmark, or shrink
the atlas mission. Passing P0 is software validation, not biological validation.

## P0A — correct the scientific record

| # | Requirement | Status | Evidence and enforcement |
|---:|---|---|---|
| 1 | Four-status claim ledger | Complete | `CLAIMS.md`, `data/governance/claim_ledger.json`, and `truth_guard.py` enforce Supported / Diagnostic / Superseded / Retracted and CE-001–CE-016. |
| 2 | Relabel the June 28 M-CSA holdout | Complete | CE-005 and ER-001 call it retrospective analysis of a permanently exhausted surface. |
| 3 | Retire 76% mechanism recovery | Complete | CE-003 and ER-002 report 160/210 coarse cofactor-bucket consistency beside 65/210 exact fingerprint recovery and the failed novelty boundary. |
| 4 | Rename counted objects | Complete | CE-002 distinguishes 8,305 positive assignments and 1,696 OOS protein-label records from mechanisms. |
| 5 | Remove “about 2%” | Complete | CE-004 and ER-005 retract the percentage and require a defined unit and denominator. |
| 6 | Rename misleading gold surfaces | Complete | CE-001 and CE-006 preserve historical IDs while current wording calls them project benchmark labels and an EC-proxy surface, never project gold. |
| 7 | Downgrade “active-site verified” | Complete | CE-008 limits automated checks to computational consistency and requires an evidence tier. |
| 8 | Mark post-hoc family results exploratory | Complete | CE-014 and ER-008 require a `posthoc/` namespace and a fresh disjoint test. |
| 9 | Preserve the failed original predictor | Complete | CE-015 and ER-009 retain the Pfam-resolved structural-orphan negative result. |
| 10 | Publish GFAT2 and later errors | Complete | CE-016 retracts the GFAT2 PLP proxy mapping; ER-007 records it. ER-010 corrects the later full-suite attribution error. |

The public ledgers control current wording; historical artifacts remain
byte-preserved. Silent result rewriting is not a correction mechanism.

## P0B — make evaluation memory mechanical

| Requirement | Status | Evidence and enforcement |
|---|---|---|
| Append-only event history | Complete | `data/governance/exposure_ledger.jsonl` contains nine immutable events over four known surfaces; exhausted state cannot reset. |
| One row per data item and surface | Complete | `data/governance/exposure_rows.jsonl` contains 1,000 rows; its manifest binds the file, exact member sets, source commits, and source hashes. |
| Historical first-exposure identity | Complete | Rows are reconstructed from first-exposure Git commits. Current checkout bytes are diagnostics only and LF-normalized so CRLF cannot manufacture drift. |
| Computed one-shot status | Complete | `compute_one_shot_status` derives eligibility from events and exposed fields; caller booleans have no authority. |
| Fail-closed evaluator | Complete | Independent-test requests must match the exact frozen row set and refuse exposed, exhausted, or development-contaminated rows. |
| Signed preregistration | Complete | `preregistration-v1.schema.json` and the guard bind code commit, data and row-set hashes, role, namespace, threshold, metric, seed, endpoint, and content signature. |
| Separate post-hoc namespace | Complete | Confirmatory requests outside the frozen contract fail; exploratory analysis must use `posthoc/`. |

## P0C — make the repository legally and technically enterable

| # | Requirement | Status | Evidence and enforcement |
|---:|---|---|---|
| 1 | Code license | Complete | Apache-2.0 `LICENSE`. |
| 2 | Notice and source/data rights matrix | Complete | `NOTICE` and `docs/SOURCE_DATA_RIGHTS.md` cover 12 named sources and default unresolved rights to blocked. |
| 3 | Citation and release metadata | Complete | `CITATION.cff`, package version 0.1.0, and the exact release manifest. |
| 4 | Dependency groups | Complete | `pyproject.toml` declares core, ML, PLM, structure, and development groups. |
| 5 | Locks and external environment | Complete | Exact core/build/ML locks plus core, ML-test, and scientific-tool/model manifests. Unknown model revisions and unavailable external binaries remain explicit, not guessed. |
| 6 | CI contract | Complete; externally verified per release | Linux and Windows on CPython 3.10/3.12 use a blob-filtered sparse checkout, validate governance/registries/manifests/docs/paths, run core tests, build both release forms, and restore from empty directories. |
| 7 | Packaging and CWD independence | Complete | Package data includes typed schemas and fixture records. The wheel is installed with `--no-deps` and executed from an unrelated empty directory. |
| 8 | Machine paths and private SSH examples | Complete | Active code/docs resolve tools from configuration/PATH and use public HTTPS instructions; the validator rejects known private-path markers. |
| 9 | Fresh Linux and Windows path | Complete; externally verified per release | The CI matrix starts from GitHub-hosted clean machines. Local `verify_core_release.py` separately proves empty-directory wheel and source execution. |
| 10 | Triage 74 failures and 20 errors | Complete | `data/governance/test_baseline.json` preserves the original 2,559/74/20/1 run, corrects its root-cause attribution, and binds the pinned green 2,585/0/0/1 run and compressed log. No scientific snapshot was bulk-refreshed. |

The 54 tests once described as stale-hash failures contained 179 comparisons
that matched canonical Git LF blobs and differed only after Windows CRLF
checkout conversion. Exactly one genuine historical lineage mismatch is
listed in `data/governance/historical_lineage_quarantine.json` and excluded
from the canonical release without changing its embedded hash.

## P0D — shrink without destroying provenance

| # | Requirement | Status | Evidence and enforcement |
|---:|---|---|---|
| 1 | One canonical release surface | Complete | The 0.1.0 wheel plus deterministic lean source ZIP expose `catalytic-earth reproduce`; historical research commands are explicitly legacy. |
| 2 | Exact release manifest | Complete | `release/release_manifest.json` binds the source commit/tree, datasets and splits, commands, seed, environment, known unavailable inputs, source files, asset SHA-256s, rights, and restore proof. |
| 3 | Externalize bulky immutable artifacts | Guarded deferment for the historical 5.1 GB tree; canonical release assets complete | The wheel, lean source, report bundle, and manifest are release assets. The 15,281-file historical artifact surface remains bound by `release/live_artifact_manifest.json` and exact Git objects. A second bulk upload is blocked until every bundled source has redistribution clearance and a durable destination; no deletion or history rewrite is permitted first. |
| 4 | Restore from empty directory | Complete | `verify_core_release.py` creates a new virtual environment and unrelated empty working directories, then checks the declared result hash from the installed wheel and extracted source. Duration and pass state are in the release manifest. |
| 5 | Lean release and blobless Git entry | Complete | Both canonical source assets are below 100 MiB. CI proves `remote.origin.promisor=true`, sparse checkout, and absence of an `artifacts/` worktree before running. |
| 6 | Archive superseded reports | Complete | All 1,316 `work/` reports are Git-object-indexed in `release/report_archive_index.json` and packaged as a deterministic release bundle; they are absent from the lean release. |
| 7 | Shorten tracked paths | Complete | Three over-ceiling paths were renamed with Git provenance preserved; the architecture gate rejects any relative path over 180 characters. |
| 8 | Preserve existing history | Complete | No artifact was deleted and no history was rewritten. Future externalization prevents future growth only; any split/rewrite remains a separate reviewed migration after upload and restore verification. |

The guarded deferment in item 3 is intentional truthfulness, not an invitation
to ignore storage. Duplicating 5.1 GB into an arbitrary destination would not
make the existing Git history lean and could illegally redistribute
reference-only source material. The lean release solves entry now; the full
historical surface remains restorable at the exact source commit.

## P0E — freeze architectural entropy

| Requirement | Status | Evidence and enforcement |
|---|---|---|
| Freeze five giant modules | Complete | Their exact byte counts and SHA-256s are frozen in `data/governance/architecture_freeze.json`; changes require an explicit architecture migration. |
| Stop family-specific Python growth | Complete | The exact 47-module grandfathered set is hashed; a 48th family source module fails the builder. |
| Declarative family onboarding | Complete | `config/family_onboarding.example.json`, a versioned schema, and `family_onboarding.py` produce deterministic proposal-only plans and never mutate registries. |
| Versioned typed mechanism objects | Complete | `mechanism-record.v1` exists as strict Python types and JSON Schema; unsupported object types and ad-hoc fields fail closed. |
| Explicit test tiers | Complete | Every test is assigned exactly once to core/unit, scientific-small, artifact-regression, or external/integration; external integration is opt-in. |
| Inject clocks and seeds | Complete for the replacement path | The bounded architecture uses `ExecutionContext`; the freeze scanner rejects direct clock/random calls in deterministic modules. Legacy output code is frozen outside the core guarantee. |
| Deprecate noncanonical CLI paths | Complete | `catalytic-earth` is the one supported core command; the old surface moved to `catalytic-earth-legacy` and is frozen. |
| One golden command/result | Complete | `catalytic-earth reproduce` returns the declared SHA-256 `a2374c6530dfd3b4681db5c3db691fdcdedbf645604c6e7dfe0b95ab7e89ea98` on CPU without network, accelerator, external binary, or third-party data. |

## Stranger completion gate

The exact release must pass this chain:

```text
wheel or deterministic lean source, or blob-filtered sparse Git clone
→ locked standard-library core environment
→ catalytic-earth reproduce on CPU
→ exact declared result SHA-256
→ explicit non-biological claim boundary
```

The empty-directory duration must be greater than zero and below 600 seconds;
`build_release_manifest.py --check` rejects a release that misses the target.
The four-platform CI contract must pass for the release commit before the
release is described as cross-platform verified.

## What may proceed

P0 completion permits the rapid atlas work that does not mutate protected
registries: source crosswalks, typed record ingestion, evidence/counterevidence
compilation, scientist-facing reports, strong baselines, assay-contract
preparation, and preregistered proposals. The CE-012 registry latch remains
active until a separate reviewed decision deliberately opens it. That decision
must not reset evaluation exposure or weaken the evidence tiers.
