# N-ribosyl hydrolase aggregate blocked below batch gate

Created: 2026-06-15T16:13:28Z

Completed offset-paged aggregate admitted 61 labels after dedup, novelty replay, and cap guard.
Unique labels before aggregate gate: 61; held at cap: 0; novelty throttled/rejected: 0.
Fetched rows across source previews: 319; off-target held: 6; holds: 94.
Raw mechanism-corroborated window sum was 166, but the deeper offset-paged synonym windows overlapped earlier accessions, leaving only 61 unique labels.
Row guardrail status: row_guardrails_pass_but_batch_gate_blocks_apply with 0 problem rows.

Do not apply this aggregate. It is useful source-handle evidence, but it remains below the 150-row batch gate; the next scaling action is reliable UniProt cursor pagination or a stronger source path for more unique reviewed entries.
