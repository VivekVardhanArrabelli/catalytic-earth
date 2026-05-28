# Router Queue Leakage Canary Audit - 2026-05-28

Review-only leakage, duplicate, and canary safety check. No labels, registries, thresholds, scoring, imports, or model outputs changed.

## Gates

- leakage gate passed: `True`
- canary gate passed: `True`
- duplicate conflicts needing review: `4`

## Canary Table

- `clean_near_orphan_anchor` `m_csa:97`: cytidine deaminase
- `clean_near_orphan_anchor` `m_csa:211`: oxygen insensitive NAD(P)H nitroreductase
- `clean_near_orphan_anchor` `m_csa:250`: chloride peroxidase (heme dependent)
- `clean_near_orphan_anchor` `m_csa:517`: carbonate dehydratase (beta class)
- `clean_near_orphan_anchor` `m_csa:686`: diisopropyl-fluorophosphatase
- `fold_conflict_anchor` `m_csa:217`: (S)-hydroxynitrile lyase
- `fold_conflict_anchor` `m_csa:428`: mannan endo-1,4-beta-mannosidase
- `fold_conflict_anchor` `m_csa:477`: picornain 3C
- `oos_router_control` `m_csa:10`: 3-hydroxydecanoyl-[acyl-carrier-protein] dehydratase
- `oos_router_control` `m_csa:30`: formate C-acetyltransferase
- `oos_router_control` `m_csa:31`: thymidylate synthase
- `oos_router_control` `m_csa:116`: NAD(P)+ transhydrogenase (AB-specific)
- `oos_router_control` `m_csa:191`: protein disulfide-isomerase (eukaryotic)
- `external_boundary_hard_negative` `m_csa:1`: glutamate racemase
- `external_boundary_hard_negative` `m_csa:108`: 2,4-dienoyl-CoA reductase (NADPH)
- `external_boundary_hard_negative` `m_csa:109`: dihydroorotate oxidase (class II)
- `external_boundary_hard_negative` `m_csa:110`: D-amino-acid oxidase
- `external_boundary_hard_negative` `m_csa:113`: sarcosine oxidase
- `parent_positive_control` `m_csa:249`: adenosylmethionine--8-amino-7-oxononanoate transaminase
- `parent_positive_control` `m_csa:411`: aromatic-amino-acid transaminase
- `parent_positive_control` `m_csa:424`: phosphoserine transaminase
- `parent_positive_control` `m_csa:66`: D-alanine transaminase
- `parent_positive_control` `m_csa:854`: 4-aminobutyrate transaminase
