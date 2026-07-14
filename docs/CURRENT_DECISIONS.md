# Current Decisions

## 2026-07-14: Atlas-10 seven-case follow-on frozen before compilation

Decision: preserve the complete Atlas-3 kernel by content hash and add seven
cases chosen to expose missing representation and truth-boundary behavior, not
to estimate performance or flatter the current system. The frozen contract is
`data/atlas/atlas10_selection.json`; compilation writes only under
`data/atlas/atlas10/`.

Durable rulings:

1. Atlas-10 means ten selected biological cases, not ten equally detailed
   mechanisms and not a representative benchmark.
2. Lysozyme, trypsin, and subtilisin retain explicit frozen Rhea-query gaps;
   no canonical reaction identifier may be invented from another source.
3. Cyclophilin A's M-CSA M0189 is non-detailed despite its high rating. The
   atlas must abstain from unsupported atom, bond, charge, electron, proton,
   covalent-intermediate, and ordered-step edits.
4. Subtilisin is grounded directly to unmutated P00782/1SUP. Engineered PDB
   1S01 remains source-reference applicability evidence, never the unmodified
   target structure.
5. Trypsin/subtilisin test convergent catalytic strategy across unrelated
   folds. Mandelate racemase/methylaspartate ammonia-lyase test shared
   enolase-fold logic with different chemistry. Relationships enable queries;
   they do not license field transfer.
6. The usefulness comparator is the same frozen source stack opened
   separately, without Atlas-derived joins or generated synthesis. It is not a
   biological-accuracy benchmark.
7. Five to ten bounded review packets and external-review attempts are
   required. A no-response record is acceptable for bounded phase completion
   but never counts as independent review.
8. The follow-on phase allows 48 CPU hours, zero GPU hours, 1,200 requests, and
   800 MiB as stop ceilings, not targets. Larger compute needs a separate
   information-gain amendment.
9. No new assay is selected. The inherited TEM-1 lane remains candidate-only,
   uncommitted, and separately preregistered before outcomes are exposed.

## 2026-07-14: Atlas-3 compiled as the first non-fixture biological kernel

Decision: advance from the frozen selection to nine separately counted
objects—Tier-0 reaction, Tier-1 source mechanism, and Tier-2 grounded
hypothesis for each of the three cases—with a bounded source package and local
query. The compilation is useful Atlas knowledge, not a benchmark or a
biological-validation claim.

Durable rulings:

1. The checked compilation spec is human-auditable scientific input; the
   generated kernel, packaged copy, and expected query must be byte-current.
2. Every site must reconcile UniProt natural positions, PDB author numbering,
   mmCIF label numbering, and coordinate residue identity.
3. MnSOD has an explicit abstaining Tier-1 object. Same-EC Cu/Zn M-CSA M0138
   remains counterevidence and contributes no MnSOD step or site.
4. M-CSA M0062's inconsistent cobalt oxidation-state wording is preserved and
   flagged; it is not silently promoted into the Tier-2 hypothesis.
5. TEM-1's lower-rated Lys73 activation route remains an explicit alternative.
   Nitrocefin activity cannot automatically upgrade the detailed mechanism.
6. Literature bodies are not bundled. Four DOI items and one PMCID remain
   reference-only handles under article-specific terms.
7. Clean packaged reproduction passed the Windows/Linux Python 3.10/3.12 CI
   matrix, PR #25 was merged, and tag `snapshot/atlas3-kernel-20260714`
   preserves the checkpoint. The assay lane remains separately unstarted.

## 2026-07-13: Atlas-3 first biological-kernel selection frozen before compilation

Decision: begin the first real atlas kernel with three deliberately
representation-stressing cases: AdoCbl methylmalonyl-CoA mutase, E. coli MnSOD,
and TEM-1. Their identifiers, source handles, target Tier 2, compute ceilings,
stop conditions, and one candidate assay are frozen in
`data/atlas/atlas3_selection.json` before evidence compilation.

Durable rulings:

1. Atlas-3 is the first non-fixture biological kernel; the P0 golden result
   remains synthetic software/reproducibility evidence.
2. M-CSA M0138 is Cu/Zn SOD and is counterevidence against same-EC transfer to
   the selected MnSOD, not its source mechanism.
3. The historical fingerprint is an interoperability bridge, never evidence
   for the detailed Atlas-3 mechanism.
4. Each case targets Tier 2. Upstream curated sources do not make the compiled
   project interpretation independently reviewed Tier 3.
5. TEM-1 nitrocefin hydrolysis is candidate-only. Activity and detailed
   mechanism outcomes remain separate objects.
6. Atlas-3 writes under `data/atlas`; it does not open or bypass the protected
   registry-expansion latch.

The selection is a start checkpoint. Atlas-3 completes only after the three
typed records, provenance snapshots, uncertainty/counterevidence, local query,
and cross-platform lean reproduction pass their exit gates.

## 2026-07-13: Truth reset — canonical claims, evidence tiers, and exposure state govern historical results

Decision: preserve the full-atlas North Star while correcting the scientific
record before further expansion. `CLAIMS.md`, `ERRATA.md`,
`docs/ATLAS_TRUTH_POLICY.md`, `data/governance/claim_ledger.json`, and the
append-only `data/governance/exposure_ledger.jsonl` are the canonical truth
surfaces. Older entries remain historical evidence but do not override them.

Durable rulings:

1. The atlas is the mission; the typed IR/compiler is its engine and benchmarks
   are internal truth controls.
2. Reactions, source mechanisms, hypotheses, families/fingerprints, protein
   records, and experimental observations are counted separately.
3. The 10,001 total means 8,305 positive fingerprint assignments plus 1,696 OOS
   protein-label records, not 10,001 mechanisms.
4. The “about 2% of mechanism space” claim is retracted because neither unit nor
   denominator was defined.
5. The 76.19% chemistry endpoint is coarse cofactor-bucket consistency; exact
   fingerprint recovery was 65/210 (30.95%).
6. The June 28 M-CSA result is retrospective analysis of an already exposed,
   now exhausted surface, not a never-touched independent validation.
7. The June 29 Swiss-Prot/PDB-holo surface is spent EC-proxy evidence, not
   independent stepwise-mechanism gold; report 45/64 overall, 2/16 metal, and
   2/72 OOS false positives together.
8. Automated geometry/residue checks are computational consistency evidence,
   not expert or experimental verification.
9. An exposed or exhausted surface never becomes fresh through renaming,
   branching, a new agent, a new endpoint, or a later preregistration.
10. The P0 truth-governance, reproducible-environment, and live-manifest gates
    have passed. Registry expansion remains separately latched until an
    explicit reviewed admission decision; new performance headlines still
    require a scientifically valid fresh evaluation contract.

No historical result was deleted. No registry, ontology, threshold, model, or
scientific artifact was changed by this decision.
