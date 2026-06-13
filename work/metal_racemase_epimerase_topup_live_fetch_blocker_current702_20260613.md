# Metal Racemase/Epimerase Top-Up Live Fetch Blocker

Run: 2026-06-13T19:27:33Z

- Status: blocked_before_preview_artifact_write_then_resolved_by_windowed_preview.
- Attempted command: `PYTHONPATH=src python scripts/source_metal_racemase_epimerase_family.py --max-records-per-lane 500 --cap-ceiling 150 --out artifacts/v3_metal_racemase_epimerase_non_plp_topup_sourcing_preview_current702_20260613.json --report work/metal_racemase_epimerase_non_plp_topup_sourcing_current702_20260613.md`.
- Blocker: sequential live UniProt entry fetch did not finish quickly enough before artifact write; interrupted in fetch_uniprot_entry HTTPS connection.
- Resolution: added record_offset_per_lane/record_limit_per_lane support and ran the 320:80 window successfully.
- Resolved preview: `artifacts/v3_metal_racemase_epimerase_non_plp_window320_80_sourcing_preview_current702_20260613.json`.
- Resolved report: `work/metal_racemase_epimerase_non_plp_window320_80_sourcing_current702_20260613.md`.
