# Family Admission Architecture Default Decisions - current702

Run: 2026-06-08T03:50:47Z

Reviewed decision artifact materialized from architecture non-counting family-admission defaults. It may reject/preserve or keep rows review-only, but it cannot accept/import/promote labels.

## Status

- architecture_default_decisions_ready
- Proposal rows seen: 6
- Architecture default decision rows: 6
- Decisions: {'keep_family_panel_review_only_require_more_evidence': 2, 'reject_family_panel_import_candidate': 4}
- Skipped rows: 0
- Violations: 0

## Decisions

| row | panel | decision | confidence | rationale |
| --- | --- | --- | --- | --- |
| m_csa:10 | near_orphan_glycoside_or_nucleoside_hydrolase_controls | reject_family_panel_import_candidate | high | The row is already framed as an OOS-tier control and the fold/geometry channel abstains below threshold. Default action should preserve the row as non-counting OOS/reject signal instead of escalating it to human import review. |
| m_csa:30 | glycyl_radical_or_thiamine_radical_lyase_boundary | reject_family_panel_import_candidate | medium_high | The row is an OOS boundary/control and abstains under the fold/geometry channel. The cofactor signal is not strong enough to justify preserving the row as a family-admission candidate, so the default is non-counting reject/OOS signal. |
| m_csa:31 | glycyl_radical_or_thiamine_radical_lyase_boundary | reject_family_panel_import_candidate | medium_high | The row is an OOS boundary/control and abstains under the fold/geometry channel. The cofactor signal is not strong enough to justify preserving the row as a family-admission candidate, so the default is non-counting reject/OOS signal. |
| m_csa:191 | thiol_disulfide_oxidoreductase_isomerase_boundary | reject_family_panel_import_candidate | medium_high | The row is an OOS boundary/control and abstains under the fold/geometry channel. The cofactor signal is not strong enough to justify preserving the row as a family-admission candidate, so the default is non-counting reject/OOS signal. |
| m_csa:448 | lipoamide_or_sulfur_transfer_redox_boundary | keep_family_panel_review_only_require_more_evidence | medium | The row is OOS-like and abstains under the fold/geometry channel, but the family axis is a boundary signal worth preserving. Use as review-only evidence unless a future family-specific locator/import gate clears it. |
| m_csa:973 | flavin_monooxygenase_and_flavin_oxygen_transfer | keep_family_panel_review_only_require_more_evidence | medium | FMO/oxygen-transfer is a real boundary against the current flavin redox bucket, but the row should not become countable until coordinate/active-site cleanliness is resolved. Strong cofactor signal alone is not sufficient for family admission. |

## Next Action

- Apply this artifact through the existing expert-decision application, then rerun the family label admission pipeline.
