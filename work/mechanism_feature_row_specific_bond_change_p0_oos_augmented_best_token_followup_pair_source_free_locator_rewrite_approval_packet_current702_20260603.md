# Mechanism Feature Row-Specific Bond-Change P0 OOS-Augmented Best-Token Follow-Up Pair Source-Free Locator Rewrite Approval Packet - current702

Run: 2026-06-03T10:19:59Z

Review-only approval intake packet for priority-1 current702 source-free locator rewrites. It converts the rewrite preflight into pending approve/reject records with candidate and planned-payload hashes required by the materialization gate. It does not approve rows, copy locator sidecars, score heldout rows, or apply the frozen residual threshold.

## Status

- p0_oos_augmented_best_token_followup_pair_source_free_locator_rewrite_approval_packet_ready_review_only
- Preflight rows: 55
- Decision stubs: 55
- Pending reviewer decisions: 55
- Materialization-ready if approved rows: 55
- Clean review rows: 49
- Warning review rows: 6
- Blockers: reviewer_decisions_not_recorded

## Decision

- Approval packet ready for review: True
- Approved locator rewrites available: False
- Approved source-free locator surface ready: False
- Apply frozen pair threshold now: False
- Heldout read once performed: False
- Next gate: Review the pending stubs, move approved rows into an approval-decision artifact using the accepted approval value and unchanged hashes, then rerun the locator rewrite materialization gate with the approval artifact and explicit write flag.

## Decision Stubs

| row | accession | decision | class | locators | warnings | candidate sha | planned payload sha |
| --- | --- | --- | --- | ---: | ---: | --- | --- |
| m_csa:3 | P15559 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 42ff54f4954c | a0a60195fe08 |
| m_csa:9 | P31153 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 790bbeacd166 | a4674a271c4a |
| m_csa:32 | Q04760 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 3 | 0 | c9e6611728bf | 3b92532aa5bf |
| m_csa:43 | P80366 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 4 | 0 | ebea185c6563 | 2d6ac9b66074 |
| m_csa:44 | P00634 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 4 | 0 | e13bc109a437 | e9ad66fe5b44 |
| m_csa:45 | P43379 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 6 | 0 | 1fe27d6a8a20 | 53356957d271 |
| m_csa:46 | P14385 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 7f87a66b0c32 | ffb8d22e2b58 |
| m_csa:56 | Q9WZW0 | pending_reviewer_decision | candidate_minimum_locator_warning_pending_explicit_approval | 2 | 1 | 085801b9296e | 72307959480b |
| m_csa:97 | P0ABF6 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 3 | 0 | 7b42f883a507 | ff98428555a1 |
| m_csa:109 | Q02127 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 9b0806b5a712 | 59eaf945f802 |
| m_csa:115 | Q9T0N8 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 675e62c5c0f9 | 256a973f19f4 |
| m_csa:121 | P07850 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 86a900acf739 | fb8a0536418e |
| m_csa:131 | P20586 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 60112fb53a87 | 345233608704 |
| m_csa:159 | P0A434 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 3 | 0 | 158eefd65277 | 897bfdd90ae2 |
| m_csa:163 | P0A7Y4 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 3 | 0 | 83f33623ebd6 | 6512d642433a |
| m_csa:171 | P00730 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 3 | 0 | 27985b834072 | 67be225eac94 |
| m_csa:180 | P35505 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 5 | 0 | 6bb753016c94 | f3ba4365eb4d |
| m_csa:188 | P09147 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | d8d98f7b3d45 | 9de94358ab70 |
| m_csa:199 | P04425 | pending_reviewer_decision | candidate_minimum_locator_warning_pending_explicit_approval | 2 | 1 | 016b9cc7deb1 | 9c781093f41e |
| m_csa:211 | P38489 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 07ad06982288 | 0f889ddb91f4 |
| m_csa:220 | P20906 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 3 | 0 | c0453a65c1bf | 42a6503c376d |
| m_csa:239 | P00433 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 100cc978dd8f | 51f408b21fa8 |
| m_csa:242 | Q8I914 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 3 | 0 | 152b26793f3c | 3174826cde60 |
| m_csa:250 | P04963 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 4f4680c11ad2 | e662a66a2b35 |
| m_csa:311 | P00924 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 3 | 0 | 78ef6dc69d85 | b7183aa69c01 |
| m_csa:321 | P09155 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 4 | 0 | b918b34b9fb4 | 2061ee7e2278 |
| m_csa:323 | P05314 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | a35816db6c68 | 21e54ba16f6f |
| m_csa:333 | Q9RUB5 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 3 | 0 | 53089c149cd6 | ecae8633e16f |
| m_csa:352 | P00949 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 3 | 0 | eb94099747e3 | c94984ac3b77 |
| m_csa:356 | P14769 | pending_reviewer_decision | candidate_minimum_locator_warning_pending_explicit_approval | 2 | 1 | aa2a4209438a | 4b8fe60cc073 |
| m_csa:370 | O75164 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 4 | 0 | 16744e25071e | 0d78649caec2 |
| m_csa:384 | P23395 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 4 | 0 | c74dd58283f8 | 773185d5f5bf |
| m_csa:392 | P07801 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 8e893f85958f | b4149b9b5df1 |
| m_csa:397 | P04063 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 5 | 0 | 034354c84eb5 | c3c5e40c805f |
| m_csa:403 | P07584 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 4 | 0 | 46a9c7adf19d | dd1d794e533c |
| m_csa:418 | P37821 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 14c56207f647 | e586310a02a1 |
| m_csa:419 | O52552 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 5962c580b12b | 1e574b6ec862 |
| m_csa:480 | P26214 | pending_reviewer_decision | candidate_minimum_locator_warning_pending_explicit_approval | 2 | 1 | fa3e14658b95 | 84bb38c0d67d |
| m_csa:497 | Q9FDN7 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 94ba644bcdba | adf0006585f8 |
| m_csa:517 | P61517 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 4 | 0 | 629a67ea7dad | b49a47ca029d |
| m_csa:526 | P11708 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 8b139037f428 | 168a0fb66097 |
| m_csa:541 | P75430 | pending_reviewer_decision | candidate_minimum_locator_warning_pending_explicit_approval | 2 | 1 | 18cb3ba71be8 | 2bcb200849e6 |
| m_csa:545 | Q7M523 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 9595bd4dacc7 | da3e79b0eb12 |
| m_csa:551 | P15245 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 6076140ae57d | 8035d967905b |
| m_csa:599 | P36936 | pending_reviewer_decision | candidate_minimum_locator_warning_pending_explicit_approval | 2 | 1 | 10038769e058 | 9434d886bada |
| m_csa:709 | P00431 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 395036670744 | 55e4b9a14b12 |
| m_csa:710 | P25524 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 4 | 0 | 98de534e795b | 8a8552a8cf47 |
| m_csa:714 | P0ABI8 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | dbac59f6f007 | 42849403bf0a |
| m_csa:723 | P00782 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 6 | 0 | efcb69d51daa | 62576dfbf4f8 |
| m_csa:750 | P55792 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 7f4df9672042 | 0ea1f0395a15 |
| m_csa:853 | P31570 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 2cd421549bcd | 2f99b42cc873 |
| m_csa:854 | P80147 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | cd93e11df0a2 | d2f606b06fdb |
| m_csa:916 | P9WI55 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 3 | 0 | ce382ac24f0a | 8ecb5ef3d37b |
| m_csa:990 | Q8GS60 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 8 | 0 | 839b94497902 | f82d18a37be2 |
| m_csa:994 | Q9Y3Z3 | pending_reviewer_decision | candidate_clean_pending_explicit_approval | 4 | 0 | d90320a00b68 | d94bd0a01222 |

## Interpretation

- 55 pending locator rewrite decisions were prepared; 0 rows are approved by this packet.
- Make explicit approve/reject decisions outside this packet, preserve the candidate and planned-payload hashes for every approved row, and keep the frozen residual threshold unapplied until materialized locators and event-axis linkers exist.
