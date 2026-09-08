# A mechanism case with discriminating evidence

## Objective — 2026-09-08

Answer one consequential mechanistic question using exact source edits,
protein/site context, competing explanations and published experiments that
distinguish those explanations. Continue from PR #52, merged as
`d80d365c02545be714800cd94d336aa94321a806`; local main and post-merge CI are clean.
Work branch: `codex/mechanism-evidence-case`.

## Assignments

- Root: choose the question, set acquisition bounds, integrate, verify and
  publish the result.
- progress_evidence_audit: M0187 mutation/kinetic evidence and alternatives.
- source_ingestion: compare M0173 and M0222 as alternative useful cases.
- state_contracts: reuse existing evidence/query contracts before proposing
  another representation.

Initial work is read-only case selection, using retained records and public
primary-source discovery. Agents may browse sources but root alone acquires
repository assets under a recorded bound after selecting the question.

## Scientific boundary

This is retrospective interpretation of published experiments. It is not a
new laboratory result, prospective prediction, calibrated ranking or independent
expert review. An unsuccessful assay does not by itself identify the disrupted
mechanistic step. Source applicability and discriminating controls must carry
that conclusion. Agent roles share model limitations; objections are resolved
with evidence rather than vote count.

Existing Atlas-3/10, reviewed transformations/site query, source-draft batches,
protected registries and July review packets remain unchanged. Source-label,
atom-identity and structure-state abstentions persist unless new evidence
explicitly addresses that exact edge.

## Selected question and acquisition bound

Working case: does loss of detectable racemization in M0187 H297N establish
loss of every catalytic capability, or does substrate-specific alpha-proton
exchange support a narrower defect? The public primary abstract for PMID
1909893 provides the discriminant. K166R (PMID 7893690) is a useful boundary:
severely reduced racemization is explicitly nonzero, and it must not become an
assumed reciprocal knockout.

Acquire only these two official PubMed records and, if needed, their public
primary metadata/access records: at most 12 HTTP requests and 2 MiB of response
bodies, no paid access. This is a new named M0187 source-annotation check under
the September owner-authorized development policy, not the frozen July plan.
Record actual URLs, status, timestamps, sizes and hashes. Keep raw abstract
responses in local analysis storage; distribute only attributed factual
projections and receipts. Unknown assay conditions and detection limits remain
unknown. Public web discovery above is separate from this capture ledger.

Review objection: evidence for a stepwise overall reaction is insufficient to
disprove concerted proton transfers within one step. Do not turn isotope-effect
or source-panel language into an elementary-event timing conclusion. The chosen
question instead distinguishes measured endpoints and their narrower mechanistic
implications.

## Source challenge and choice

M0187 was selected because its original reviewed transformation can now be
connected to a direct functional discriminator. The two official captures
succeeded in two requests, 16,968 response bytes, with no redirects or retries.
Both PubMed abstracts are truncated; no complete protocol or numerical
detection floor was inspected. H297N's general racemase nondetection is not
assigned a reaction direction or the pD of its separate exchange assay.
Only the S/R exchange observations carry pD 7.5 and D2O. The separate alternate-
substrate elimination observation cannot become evidence of racemization.

The M0222 alternative has a useful mobile Tyr363/Lys146 question, but its exact
kinetic-table/methods details were accessible to the source agent only through
search-indexed text of an archived dissertation reprint. Direct inspection and
retention of that primary reprint should precede a quantitative case. Its mixed
proposal scope and C1/C3 labeling conflict also remain. M0173's sharper Asp
protonation evidence concerns bovine protein and an inhibitor, whereas the
retained case is fungal trypsin at pH 5; that transfer would be inappropriate.

The implementation is one reviewed evidence sidecar and offline query. Root
owns data, CLI, packaging and docs; state_contracts owns
`src/catalytic_earth/atlas_mechanism_evidence.py`; draft_integration_review owns
the subsequent focused regression suite. Existing observations are source
reports, and adjudication is a separately identified project interpretation.

## Adjudicated source corrections

- The H297N abstract does not itself name organism or UniProt accession.
  The K166R abstract names P. putida and cites H297N. P11444 remains existing
  Atlas reference-site context, with exact assayed constructs uninspected.
- H297N S exchange is catalytic activity, not evidence of retained S-to-R
  racemization. The R-exchange interpretation describes enantiomer-dependent
  endpoints without localizing an elementary molecular step.
- Short witnesses now identify the variant and retained exchange/residual
  turnover explicitly: 25 quoted words from PMID 1909893 and 22 from
  PMID 7893690, each checked against the actual retained XML.
- K166R's inspected abstract reports 5000-fold R-to-S and 1000-fold S-to-R
  kcat reductions but does not name the comparison reference. An assumed WT
  comparator was removed. Only H297N S exchange has an explicit WT comparator.
- The source-reported H297N structural comparison has no identified comparison
  structure or mutant PDB accession in the inspected abstract. Its comparator
  is null. Existing 1MNS is an inhibitor/modified-Lys166 context and is not
  relabeled as either mutant or an observed turnover state.
- Code review found that a focal conclusion could otherwise rest solely on
  contextual K166R evidence after repinning. The validator now requires a
  supporting discriminant with direct focal-variant evidence, in addition to
  exact focal mutation/site, upstream hashes and source bindings.

`source_ingestion` approved the source-to-conclusion payload
`dd62c8fbbde725e8567a6a2462cb456c26b5c77c4b239ed18ad3e05f468e3241`
after checking both retained abstracts and the optional raw-source audit.
`state_contracts` reviewed the builder, package, CLI and release checks with
no remaining integration objection. `draft_integration_review` supplies the
adversarial regression suite and final implementation challenge.

This review is informed and uses the same model family. Neither role separation
nor agreement supplies statistical independence or an accuracy estimate.
The builder binds factual projections to capture receipts and compares typed
observations exactly. It checks witness substrings when the local raw responses
are supplied; it does not adjudicate scientific prose or refresh the review pin.

## Verification and publication handoff

`draft_integration_review` approved that same payload and the final module
`c827491f3c41c80bfdba4f99a8ed3308be354d79281efad4becc0adbbe9fb7d6`.
Its ten tests plus four CLI tests pass. The full core tier passes 453 tests;
repository contracts, original transformation/candidate builders and the new
source/package check pass. The original Atlas-10 runtime remains
`57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb`.

The final wheel matches the reviewed module, CLI and evidence bytes and passes
the Atlas-10/draft/transformation/site/candidate/evidence release verifier from
an empty working directory with network connections blocked. Its SHA-256 is
`019c937e27af2cfb86e4214cd7bd2c763a4d99495add8452eec051c57d50f374`.
Published-observation projections remain six; new experiments and independently
reviewed mechanisms remain zero for this increment.

Root will publish this tested tree as a PR, require all four repository CI
jobs, merge only that checked head, and verify local/remote main and the merged
tree. GitHub retains the eventual PR/check/merge status; this pre-publication
record does not assert those external actions are already complete.
