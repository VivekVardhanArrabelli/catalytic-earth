# Deposited variant context — 2026-09-09

- Parent owner: `01a08759-ebbb-73a1-ab7c-8b4ced7a36c8:097537c6-fc15-4f1a-b86d-9fb55ef0b484`.
- Start: 18:07:08 UTC; base `d775313aea8e751169df77367595f1b66563ca45`;
  branch `codex/deposited-variant-query-20260909`.
- Question: can a variant query expose the exact-citation deposited K166R
  context beside primary-abstract evidence without assay-specimen equivalence
  or a new functional observation?
- Expected gain: a reusable query relation that preserves deposited variant,
  ligand-state and conflicting organism context while retaining the six
  original observations and their endpoint-specific conclusion.
- Alternative considered: another same-case geometry calculation or a fresh
  acquisition. Neither resolves the immediate missing evidence link; the
  inherited source batch has reached its request sublimit.
- Stop: no enzyme-specific runtime, source promotion or weakened join. Stop
  if no concrete variant-evidence query improves. No new source acquisition.
- Ownership: parent alone edits, owns Git and lock. Reviewers read retained
  sources and return findings; the parent maintains this compact board.
- Review lanes: source provenance; chemical representation; adversarial query
  and usefulness. Same-model review is computational, not independent human review.

## Findings and decisions

- Startup: clean main, no open PR or recovery, prior merge CI34385235075
  passed all four jobs. Fetch and fast-forward synchronization completed.
- Source review: exact PMID/DOI, reported substitution and the deposited
  entity/reference/alignment/difference chain support a citation/variant
  relation. The abstract does not identify the assay specimen or its sequence.
  Organism assertions and depositor-inferred product origin stay unresolved.
- Representation: accepted a separately versioned opt-in context query.
  Variant filters both planes; endpoint filters only original observations.
  K166R/structure returns zero observations and one source context; H297N
  returns no retained deposit context. Full-case adjudication remains intact.
- Adversarial review found a real one-way equality gap: a primary projection
  with only observation IDs could pass after coherent re-pinning. The source
  builder and runtime now share exact required projection fields. A complete
  H297N citation/sequence substitution with refreshed pins fails against the
  retained 1MDL source, and conflicting-organism normalization also fails.
- Scope corrections: raw bound bytes are hashed before decoding; source
  annotation status, reference scope, claim binding, finding roles and
  abstentions are checked. The relation enumerates asserted citation/variant
  equality and unresolved assay, physical-state and organism equivalences.
  Source-specific required roles live in data; no case ID controls runtime.
  Prose remains under manual source-review pins, not interpreted by a validator.
- Distinct numbering is preserved: author position is checked against author
  coordinate numbering, label position against label numbering. No generic
  equality or missing-code interpretation is imposed between namespaces.
- Integration review caught and removed a binary gzip path mistakenly added
  to the repository's JSON-only list; the shared builder verifies that source.
- All three computational review lanes accepted the final code and source
  scope. Their models were gpt-5.6-sol/ultra; they are not independent humans.
- Verification: 516 core tests pass without skips; installed-wheel Atlas-3
  and Atlas-10/draft/transformation/site/candidate checks pass with network
  blocked. All 16 original variant/endpoint query combinations are byte-identical
  to the base implementation. Final repository contracts and reviewed-head CI
  remain publication gates, recorded in the Git-local receipt.
- Reconsideration: source-format reuse needs no enzyme-specific code; accepted
  annotation and primary projections are reused without retyping observations.
  The useful addition is a computable source relation that prevents mistaken
  transfer, not biology unavailable from competent PubMed/PDB use. No measured
  human-time, speedup, accuracy, assay or evidence-tier claim is made. Further
  same-case wrappers and geometry have no justified information gain here.
- Acquisition: zero new scientific-source requests. All inherited cumulative
  budgets remain unchanged; M0187 remains at its 12-request sublimit.
- Next-action adjudication: a reviewer proposed a same-EC M0052/M0222 negative
  comparator. The parent checked the current draft documentation and earlier
  coordination: that metal-assisted/Schiff-base contrast is already exposed.
  Repeating it would add little information. Instead, the next run should
  pursue the unresolved primary M0222 mobile-catalyst functional discriminator
  (PMID17728250 / DOI10.1074/jbc.M704968200), with full methods/kinetic-table
  inspection and carried acquisition accounting before any quantitative join.
  The current projection and `work/coordination_mechanism_case.md` document
  the source-access and protein-context gaps. All reviewers have stopped.
