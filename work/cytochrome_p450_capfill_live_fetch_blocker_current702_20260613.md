# Cytochrome P450 cap-fill live-fetch blocker

Run: 2026-06-13T22:07:34Z

Attempted a non-destructive cap-fill preview for `cytochrome_p450_monooxygenase`, which is
currently 248/250 under its non-confusable cap:

`PYTHONPATH=src python scripts/source_cytochrome_p450_family.py --max-records-per-lane 500 --cap-ceiling 250 --out artifacts/v3_cytochrome_p450_capfill_probe_sourcing_preview_current702_20260613.json --report work/cytochrome_p450_capfill_probe_sourcing_current702_20260613.md`

The preview was interrupted after repeated polling intervals before artifact write. The traceback
was inside `fetch_uniprot_entry` during `ssl.SSLSocket.do_handshake`, matching the live UniProt
entry-fetch blocker seen in recent handoffs.

No labels were generated, no registry was written, and the attempted preview/report files were not
created. Because no preview artifact exists, no novelty, governor, trust-tier, cap, dedup, or
frozen-sha gates are available for apply.

Guardrails remain unchanged: EC/name/P450/O2/heme handles are scope/admission context only;
EC is never a counted corroborator; `predictive_evidence` remains empty.

Next safe action: add row-window/checkpoint support or run a smaller bounded live-entry preview
before any P450 cap-fill apply. Do not broaden the P450 fingerprint or admit EC/name-only rows.
