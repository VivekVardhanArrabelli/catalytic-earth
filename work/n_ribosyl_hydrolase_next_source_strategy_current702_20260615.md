# N-ribosyl hydrolase next source strategy

Created: 2026-06-15T16:26:00Z

Current state: the 42fp `n_ribosyl_hydrolase` lane is fully wired, but no registry apply is
authorized. The best non-destructive aggregate has 61 unique novelty-safe labels after dedup,
novelty replay, and cap guard. Row guardrails pass with 0 problem rows, but the batch is below the
150-row mutation gate.

Observed source behavior:

- The synonym-handle windows `window00_40` and `window40_80` produced 61 unique labels.
- Deeper offset-paged synonym probes at offsets 80, 140, and 200 returned mechanism-corroborated
  rows, but their accessions overlapped the earlier windows; raw window-summed target rows reached
  166 while aggregate-unique labels stayed 61.
- The offset-paged artifacts keep the true REST offsets in `source_url`; their
  `record_offset_per_lane` field reflects local slicing after query fetch, so use `source_url` and
  aggregate-unique counts for source diagnostics.

Next bounded source actions:

1. Add a UniProt cursor-pagination fetch path for this runner or a reusable adapter helper, then
   rerun only the `n_ribosyl_hydrolase_nucleosidase_synonyms` lane with stable ordering and a
   bounded page count. Preserve the existing process timeout behavior.
2. If cursor pagination still yields fewer than 150 unique rows, test one additional reviewed,
   mechanism-bearing source path that is not EC-only: Rhea participant anchored N-glycosidic
   hydrolysis entries crosswalked to reviewed UniProt accessions, or Swiss-Prot catalytic-activity
   rows containing D-ribose / nucleobase products plus N-ribosyl/nucleosidase family text.
3. Rebuild a non-destructive aggregate from only completed windows, rerun row guardrails, and apply
   only if >=150 clean unique rows pass novelty, governor, dedup, cap, source-contract, leakage, and
   frozen-current702 SHA gates.

Do not pad the current 61-row aggregate. If no reviewed source path can reach the batch gate, pivot
to `metal_independent_phosphodiesterase` as the next new-fingerprint lane with a fresh OOS
preregistration for the then-current fingerprint universe.
