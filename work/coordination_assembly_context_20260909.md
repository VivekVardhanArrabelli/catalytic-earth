# Assembly context research — 2026-09-09

Owner: `01a086b4-a813-7be1-84dd-fdec48d14288:46b8ba73-3a5f-4cea-afeb-a61080437d84`.
Start: 2026-09-09T15:06:35Z. Base: `c968007591c79b09c2ab41767a405cbc6683f134`.
The parent alone owns Git and the cooperative lock. Source and adversarial
lanes are read-only. The representation lane owns only the shared assembly
module, its tests and the mmCIF category allowlist.

## Question and decision

Does operator-qualified biological assembly identify a source-supported
cross-subunit catalytic constraint in 6HA3 that a single-chain design would
miss? Expected gain: a reusable partner-subunit identity relation with a
bounded chemical interpretation, or evidence that geometry-only extension
should stop. The strongest alternative is a separately supported experimental
perturbation rather than more descriptive geometry. Stop if the result adds
only distances, collapses operators/alternate states, or treats E160Q as a
selective geometric perturbation.

## Independent lanes

| Lane | Bounded question | Status |
| --- | --- | --- |
| Source | What source evidence supports E366-prime, its chemical role and any useful comparison? | Source/spec/docs accepted with explicit limits |
| Representation | What minimal reusable assembly/atom contract preserves operators and alternate states? | Shared module complete; 25 focused assembly/parser tests passed |
| Adversarial | Does this prevent a consequential transfer error beyond competent incumbent use? | Omission warning and generic code accepted; 17 targeted tests passed |

All conclusions require source adjudication. Same-model reviews are not
independent human or experimental evidence. Existing acquisition batch
`human-tkt-e160q-6ha3-geometry-function` starts at six direct captures and
2,987,157 bytes; no lane may acquire sources without parent coordination.

## Findings and adjudication

- The partner is source polymer asym A under assembly operator 2, not the
  nonpolymer label asym B. The operator is `(-x,y,-z)`; Q160 NE2/op1 to E366
  OE1/op2 is 2.804089 Å. Retain both glutamate oxygens and all declared pair
  distances; do not select the shortest oxygen as an inferred chemical bond.
- The deposited author/PISA dimer has `experimental_support=none`. Expansion
  provides coordinates for selected atoms, not experimental solution-assembly
  validation or a complete active site.
- Fig. 1d reports all five variant arms: WT/E160Q/E160A accumulate F6P–ThDP;
  E366Q/E165Q do not accumulate measurable covalent intermediates. Preserve the
  unknown numeric detection floor and the typical 30-second acid-quench
  endpoint, not a zero formation rate.
- Source review added decisive counterevidence: E366Q retains X5P/R5P turnover
  (kcat 0.012 ± 0.001 s⁻¹ versus WT 2.79 ± 0.06 s⁻¹), and its F6P stopped-flow
  values are unavailable because the reporter band is absent. These endpoints
  must remain separate from the NMR result and the E160Q crystal.
- E366Q changes the canonical cofactor-activating group across the protein
  homodimer; it is not an operator-2-only intervention or an interface-selective
  perturbation. E160Q is also not a selective geometry change. No protonation,
  LBHB causation, geometric tolerance or sufficient catalytic motif follows.
- Both source and adversarial lanes support a project-inferred omission
  warning: a single-copy crop leaves out a study-implicated group. The sources
  already contain these facts. Added value is the explicit atom/copy-to-evidence
  relation and prevention of endpoint conflation, not a measured speedup or new
  biological discovery.
- Source lane reviewed `spec.json` SHA-256
  `b3a6c9306cab59095c4c3943c35ec7b0cbddadbcc1180fced9e284cff8a4b675`
  and the new CE-019/documentation with no remaining source objection.
- The existing coordinate, study projection and literature captures are reused.
  One official wwPDB operator-expression documentation capture adds 17,727
  bytes: cumulative batch use is seven requests and 3,004,884 bytes. Prior
  unmeasured discovery traffic remains disclosed in the inherited inventory.
- Reconsideration: no enzyme-specific Python branch is warranted; operators
  are shared source-format semantics. No timed curation speedup is claimed.
  Stop further E160Q distance expansion after this increment unless another
  scientifically useful consumer needs it.

## Verification and publication checkpoint

- Parent and adversarial review independently checked the operator-product
  order, all eight distance outputs, source names and assembly support metadata.
- The assembly/API/false-join tests pass. The built wheel reproduces the exact
  projection from an empty directory under Python isolation. The complete
  installed Atlas-10/draft/transformation/site query verification passes with
  network access blocked by its verifier.
- The first core run found one expected-count mismatch after CE-019 increased
  the claim ledger from 18 to 19; that bookkeeping assertion was updated.
  Its optional JSON Schema test was skipped in the isolated build environment;
  the final core run uses the project Python with that dependency available.
- Parent review required bounded range expansion before allocation and unique
  atom row/alternate identities; these are now covered by regression checks.
  The source-proposed comma normalization was rejected and retracted.
- No agent remains authorized to edit. Parent owns final checks, Git publication
  and lock release. Exact final results are in the Git-local run receipt.

- Final local verification: all 498 core tests passed with no skips; full
  repository contracts passed. Source and code/diff review have no remaining
  blocker. The only architecture-manifest change is the tracked path count.
