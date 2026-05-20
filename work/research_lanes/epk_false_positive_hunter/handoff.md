# ePK false-positive hunter handoff

- Started: 2026-05-20T15:16:47Z
- Ended: 2026-05-20T16:06:49Z
- Measured minutes: 50.03
- Primary outcome: search_surface_exhausted
- Rule under attack: `epk_mek_erk_tyr_or_n_terminal_substrate_mode_counteraxis_v0` plus `epk_mek_erk_source_free_topology_ambiguity_counteraxis_v0`.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search Surface

Four bounded cross-chain non-ePK ATP-like/Mg stress surfaces were executed:

- general complex text surface: 148 reviewed rows, 78 local ATP/Mg-hydroxyl rows, 0 cross-chain substrate-mode rows.
- interface/oligomer text surface: 150 reviewed rows, 95 local ATP/Mg-hydroxyl rows, 0 cross-chain substrate-mode rows.
- component ATP-like+Mg offset surface: 220 reviewed rows, 165 local ATP/Mg-hydroxyl rows, 0 cross-chain substrate-mode rows.
- acceptor-targeted text surface: 150 reviewed rows, 99 local ATP/Mg-hydroxyl rows, 0 cross-chain substrate-mode rows.

Total reviewed: 668 rows, 574 unique PDB IDs. Seed attack IDs included: 7CAG, 8BMS, 9L3M, 9L3U, 7ZE5, 4KFT, 5TT6, 6NOO, 9NBW. No raw coordinate files were written; mmCIFs were fetched in memory and reduced to compact chain/distance evidence.

## Result

No counterexample was found. The bounded cross-chain surface is exhausted for this run: 0 topology-clear cross-chain substrate-mode hits and 0 counterexample candidates. This is evidence against the tested cross-chain false-positive hypothesis, not production safety evidence.

## Pressure Cases

The search found 105 same-chain substrate-mode pressure cases. The closest examples remain topology-confounded rather than cross-chain topology-clear:

- 3M6G: ATP PG to SER14 OG on chain A = 2.928 A; ligand chain A; same_chain_topology_detected=true; title=Crystal structure of actin in complex with lobophorolide
- 3EA0: ATP PG to SER16 OG on chain B = 2.946 A; ligand chain B; same_chain_topology_detected=true; title=Crystal Structure of ParA Family ATPase from Chlorobium tepidum TLS
- 3EA0: ATP PG to SER16 OG on chain A = 2.96 A; ligand chain A; same_chain_topology_detected=true; title=Crystal Structure of ParA Family ATPase from Chlorobium tepidum TLS
- 1RFQ: ATP PG to SER14 OG on chain B = 3.007 A; ligand chain B; same_chain_topology_detected=true; title=Actin Crystal Dynamics: Structural Implications for F-actin Nucleation, Polymerization and Branching Mediated by the Anti-parallel Dimer
- 1RFQ: ATP PG to SER14 OG on chain A = 3.248 A; ligand chain A; same_chain_topology_detected=true; title=Actin Crystal Dynamics: Structural Implications for F-actin Nucleation, Polymerization and Branching Mediated by the Anti-parallel Dimer
- 5TT6: ATP PG to TYR37 OH on chain A = 3.297 A; ligand chain A; same_chain_topology_detected=true; title=T4 RNA Ligase 1 (K99M)
- 1MA9: ATP PG to SER14 OG on chain B = 3.31 A; ligand chain B; same_chain_topology_detected=true; title=Crystal structure of the complex of human vitamin D binding protein and rabbit muscle actin
- 4B9Q: ATP PG to THR11 OG1 on chain B = 3.356 A; ligand chain B; same_chain_topology_detected=true; title=Open conformation of ATP-bound Hsp70 homolog DnaK
- 1B38: ATP PG to THR14 OG1 on chain A = 3.37 A; ligand chain A; same_chain_topology_detected=true; title=HUMAN CYCLIN-DEPENDENT KINASE 2
- 4B9Q: ATP PG to THR11 OG1 on chain A = 3.387 A; ligand chain A; same_chain_topology_detected=true; title=Open conformation of ATP-bound Hsp70 homolog DnaK

## Interpretation

The cross-chain adversarial search did not break the current topology counteraxis. The material signal remains same-chain: 361 unique local ATP/Mg-hydroxyl hit PDB IDs were seen and all 361 of those topology-hit IDs carried same-chain topology. The ATPase/transporter seeds with reciprocal cross-chain-like contacts still did not satisfy the Tyr-or-N-terminal-STY substrate-mode filter cross-chain.

## Next Query

Target ligand-chain assignment artifacts and gamma-like non-ATP analogs: cases where auth_asym_id may attach ATP-like ligand to the putative acceptor chain, and GTP/transition-state analog Mg structures with Tyr or N-terminal STY geometry.

## Files

- `artifacts/research_lanes/epk_false_positive_hunter/cross_chain_search_summary_20260520.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `tools/research_lanes/epk_false_positive_hunter/cross_chain_substrate_mode_stress.py`
- `tools/research_lanes/epk_false_positive_hunter/component_cross_chain_substrate_mode_stress.py`
