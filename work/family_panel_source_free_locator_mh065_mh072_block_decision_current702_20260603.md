# Source-Free Locator mh_065/mh_072 Block Decision - current702

Run: 2026-06-03T00:19:02Z

Human decision for the `mh_065`/`mh_072` accession-equivalence locator blocker.

## Status

- source_free_locator_mh065_mh072_block_decision_leave_blocked_review_only
- Blocked rows: 2
- Matching replacement coordinates: 0
- Remapped locator approvals: 0
- Ready for predicted-geometry scoring: 0

## Decision

Leave `mh_065` and `mh_072` blocked.

Do not copy the raw `1DDK`/`1E9I` locators. Do not approve remapped locators
from the current evidence. These rows remain review-only and non-countable.

## Evidence

| row | source accession | selected PDB | selected PDB struct_ref | matching replacements | same-accession AFDB | AFDB residue-code match |
| --- | --- | --- | --- | ---: | ---: | --- |
| mh_065 | uniprot:Q79MP6 | 1DDK | Q932P5 | 0 | 1 | 0/3 |
| mh_072 | uniprot:P0A6P9 | 1E9I | P08324 | 0 | 1 | 0/3 |

The matching-coordinate scout scanned 712 local coordinate files and found no
matching non-AFDB coordinates. The selected PDB structures map to different
accessions than the intended source rows, and the only same-accession AFDB
models already failed residue-code transfer.

## Unblock Conditions

- Provide a matching frozen coordinate whose `struct_ref` maps to Q79MP6 for
  `mh_065` or P0A6P9 for `mh_072`.
- Or provide a real expert alignment/remapping that resolves the residue-code
  mismatch, not just a numeric offset.
- After either unblock condition, rerun locator schema/integrity review before
  any source-free predicted-geometry scoring.

## Guardrails

- No locator sidecars copied.
- No coordinates fetched.
- No predicted-geometry scores created.
- No labels, registries, ontologies, imports, or thresholds changed.
