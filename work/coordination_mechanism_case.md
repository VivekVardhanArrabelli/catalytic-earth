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

## Ownership increment — 2026-09-09

Starting truth: clean `main` at `6f79c1cc` (PR #53), exactly synchronized with
`origin/main` after fetch; no open PRs. Current instructions, claim/errata
ledgers, truth policy, current state/decisions, source-draft and evidence docs
were read. The September computational-development permission supersedes the
old human-only prerequisite for scoped curation. Historical kernels and
protected registries remain immutable.

Assignments: root integrates and verifies; scientific_bottleneck independently
compares scientific priorities and challenges sources; reuse_audit examines
representation/curation reuse. Both agents use gpt-5.6-sol with ultra reasoning,
as requested. This is informed same-model work, not independent expert review.
Agents send evidence to root, which maintains this single board.

Missing capability: residue-grounded cases do not yet expose the deposited
chemical state and alternate atom conformations needed to judge whether a
structure is suitable as a catalytic-arrangement reference. Candidate scope
is a shared coordinate evidence extraction for existing trypsin and subtilisin.
The strongest alternative is another functional-evidence case; the current
M0187 implementation encodes abstract-specific assumptions that would need
reconsideration before reuse. Another graph retrieval increment would leave
the structural applicability gap unchanged.

A source finding changes the priority: the retained 1SUP mmCIF explicitly has
`_struct_conn.id=covale1`, Ser221 OG to PMS278 S (author chain A; label chains A
and D). His64 ND1/NE2 carry A/B alternatives at 0.80/0.20 occupancy. Distances
calculated from deposited coordinates give Ser221 OG--His64 NE2 7.347 A (A)
and 3.214 A (B). The kernel only flags static structure and unmutated target
scope. Native sequence does not establish an unmodified catalytic chemical
state. No solution-state populations or productive rotamer follow from these
occupancies. The 1PQ5 comparison remains pH 5 and condition-specific.

Reconsideration observation: if exact retained connections or conformer
identities fail source reconciliation, leave that edge unresolved. If a shared
coordinate projection requires enzyme-specific branches, simplify the
representation rather than add exceptions. If the result merely restates
what competent M-CSA/PDB use already yields, claim interoperability and
prevention of a concrete unsupported transfer, not discovery or superiority.

Source acquisition: use retained CC0 PDB coordinate files and existing
source bindings. Root browsed the official RCSB 1SUP and 1PQ5 entry pages for
adjudication (two discovery opens). No new asset capture, paid services,
outreach, GPU work, experiment, or benchmark was authorized or performed.

Source challenge added 1PQ5's noncovalent context: the primary trypsin paper
identifies a partially occupied autoproteolytic arginine/peptide fragment in
the pH-5 dataset, and Table II maps that dataset to 1PQ5. Its article-level
occupancy summary is not substituted for the retained per-atom ARG703 values
(0.19-0.48 among heavy atoms). The generic extractor will retain non-water
nonpolymer instances in both structures, not infer an empty active site from
absence of a selected-site covalent connection.

A bounded local capture is now permitted for the single already-cited primary
trypsin paper, DOI 10.1074/jbc.M306944200, from coauthor Wojciech Rypniewski's
institutional article copy: at most six HTTP requests and 5 MiB response bytes.
Retain the PDF outside the repository for review only, and record receipt,
article identity and short factual projection inside the source specification.
Do not redistribute the article PDF. This does not acquire a new atlas case.

The source-review agent supports this choice over another graph query: the
legacy geometry documentation uses centroid/CA representations, while the
current kernel carries residue roles and mappings without atom/conformer
state. Root and agent independently checked the retained 1SUP linkage and
alt-atom rows. Root also rendered the trypsin paper's Table II to confirm the
1PQ5/pH-5 mapping. The single capture used one request and 318,096 bytes.

Reconsideration A/B: the existing M0187 evidence builder hardcodes truncated
abstract inspection, no PDB IDs, and that case's acquisition limits. Extending
that validator would preserve first-case assumptions rather than generalize
published evidence. We did not add another such exception. The chosen shared
extractor derives both structural cases from a single data specification,
reusing the existing strict mmCIF parser. Atom choice and source interpretation
still need manual scientific review; no elapsed-time savings were measured.

Reconsideration C: all observed facts and distances are obtainable with fair
M-CSA/UniProt/PDB searches and a competent viewer. The value is interoperable
state/identity joins and prevention of the concrete unmutated-to-unmodified
transfer error, not biological discovery or a superiority benchmark.

A promising next candidate is the existing K166R functional evidence together
with 1MDL (PMID 7893690). The source scout reports substrate stereochemistry
and organism-context conflicts between deposition and paper that must be
adjudicated before any exact structure-to-assayed-variant link. This is a
research lead, not an established link or a new acquisition in this increment.

Verification caught a repository-specific constraint: the historical Atlas-10
kernel/selection documentation is itself in the immutable inherited baseline.
Root removed the proposed notices from those two frozen files. The correction
is instead on current README/claims/errata/state/decisions and current CLI
output, preserving all 96 inherited files and the frozen result. The truth
ledger now contains CE-018; its existing expected claim count was updated from
17 to 18. Neither fix changes historical scientific source bytes.

Final source review approves specification
`2a2258ad2a1debd0663578f3f6410932cea54969eb83e167df23123d6e7cfdf1`
and derived scientific bundle
`d7f8b917cd8a6a9313b3288957eee09cf69c7f8e0ba3bd3d94f819e11c59c149`.
Review pins are manually maintained and checked separately from generated
package hashes. The shared extractor has no enzyme-specific chemistry branch.
The bounded v1 selection requires one context per PDB and one unambiguous
mapping per site; broader assembly or alternative-mapping support is open.

Final local verification: all 465 core tests passed with one skip; repository
contracts passed, including the source/package rebuild, 96-file inherited
baseline and 18-claim ledger. Nine structural tests protect source hashes,
residue-number joins, alternate conformers, cross-model separation and whole-
residue modification retention. Three CLI tests protect visible corrections,
output preservation and packaged interpretation integrity. The original
Atlas-10 runtime hash remains
`57fb5e4708d6963b994a9ffd125549b822effe060da3e735c1afd987f1c84bdb`.

The final wheel is 3,192,240 bytes, SHA-256
`f8441b227571b87a1d6204c7d802d9b13c727f1b0f474ec8c0218aaa63548f89`;
all 265 packaged source assets match the current source bytes. The fresh-
directory Atlas-10/draft/transformation/site/candidate/functional-evidence/
structural-context verifier passed with network connections blocked.
These checks protect computation and distribution, not chemistry or activity.
The increment adds two annotations, six sites and nine conformer-specific
distance calculations over six declared pairs; biological coverage and newly
performed experiments both increase by zero.

Publication check: PR #54's first CI run exposed a stale report-archive index.
That manifest reads staged Git blobs, so the pre-staging local contract check
still saw the old coordination record. The scientific source/package check
passed in CI. Root staged this final board record, regenerated only the archive
membership metadata, and checked the exact-index/partial-clone contract path
against the PR base before pushing the correction. No scientific payload,
review pin or package source changed. GitHub's PR checks and merge record are
authoritative for the subsequent publication status.
