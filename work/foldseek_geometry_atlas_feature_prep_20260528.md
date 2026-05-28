# Foldseek + Geometry Atlas Feature Prep

Created: 2026-05-28T12:51:02Z

This packet turns the overnight Wave 1.1 result into a bounded next engineering lane. It is read-only: no labels, registries, ontologies, thresholds, imports, production scoring, or model outputs were changed.

## Why This Lane

Wave 1.1 answered the immediate question conservatively:

- Learned representations add limited, non-decision-grade value where Foldseek is weak.
- In near-orphan geometry-rescue rows, geometry is 17/17, Foldseek is 13/17, and ESM-2 150M is 9/17.
- In wrong-Foldseek-transfer rows, corrected ESM-C rescues 2/4, but geometry rescues 4/4.
- Child-label and mixed-chemistry cells do not yet have row-aligned child-label prediction exports.

So the next useful engine is not a bigger model run. It is a Foldseek-plus-local-geometry router/dossier lane that explains when structure-neighbor transfer is safe, misleading, or unavailable.

## Row Cells

Clean near-orphan anchors:

`m_csa:97`, `m_csa:211`, `m_csa:250`, `m_csa:517`, `m_csa:686`, `m_csa:916`, `m_csa:990`

Fold-conflict reference anchors:

`m_csa:217`, `m_csa:428`, `m_csa:477`

OOS router controls:

`m_csa:10`, `m_csa:30`, `m_csa:31`, `m_csa:116`, `m_csa:191`, `m_csa:369`, `m_csa:440`, `m_csa:634`, `m_csa:651`

Quarantine before any model claim:

`m_csa:403`, `m_csa:497`, `m_csa:714`, `m_csa:723`, `m_csa:735`, `m_csa:750`, `m_csa:994`

## Feature Plan

The atlas feature lane should join four evidence families per row:

1. Foldseek neighborhood:
   nearest train entry, nearest fingerprint, max TM/probability/bits, same/different fingerprint neighbor counts, OOS-neighbor counts, no-neighbor flag, fold-conflict flags.

2. Source-free local geometry:
   active-site residue types, resolved/missing catalytic residues, pairwise distances, compactness bins, cofactor-locality flags, proximal ligands, and pocket composition.

3. Policy routing:
   geometry-supported anchor, fold-conflict wrong-transfer candidate, OOS router control, local-tail canary, or quarantine.

4. Evidence dossier:
   one human-readable row record explaining the structural neighbor, local chemistry evidence, unsafe failure mode, and next action.

## Diagnostics Only

Do not turn these into benchmark claims yet. The allowed measurements are review-only:

- near-orphan geometry rescue
- wrong-Foldseek-transfer rescue
- OOS unsafe nonabstention
- local-tail expected-pattern failures
- disagreement dossiers for human/agent review

## Next Allowed Work

Build a read-only dossier compiler that emits per-row Foldseek+geometry evidence packets. In parallel, build the external/v2 acquisition priority pack so child labels and external stress panels can catch up with the modeling plan.

The supervised active-site smoke scaffold remains idle until the user explicitly approves training.
