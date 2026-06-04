# Lever 2 Current Extended OOS Mechanism Overlap Readout - current702

Run: 2026-06-04T16:59:22Z

Lever 2 train/cal readout comparing the frozen row-specific mechanism residual surface against the current Lever 3 extended train/cal OOS surface. It uses fixed thresholds only, evaluates non-heldout current OOS rows with existing train/cal mechanism features, and does not read or tune heldout.

## Status

- lever2_current_extended_oos_mechanism_overlap_readout_research_only
- Result class: research_only
- Current surface: combined_mean_geometry_fold < 0.44155 abstains
- Mechanism residual > 3.21469422 abstains
- Current extended OOS overlap: 21/204 scored rows
- Best source-free axis current-extended OOS catches: 3/4
- Best source-free axis current-retained OOS catches: 2
- Valid primary overlap: 0/34
- Existing source-free coordinate-anchor candidate overlap with missing rows: 0 primary, 0 current-retained OOS

## Measured Readout

| surface | overlap rows | abstained | recall |
| --- | ---: | ---: | ---: |
| current geometry/fold | 21 | 8 | 0.380952 |
| full mechanism residual | 21 | 18 | 0.857143 |
| OR union | 21 | 19 | 0.904762 |

## Current-Retained OOS Catches

- Current-retained overlap rows: 13
- Current-retained rows caught by mechanism: 11
- Catch fraction: 0.846154
- Union minus current abstain recall on overlap: 0.52381

## Event-Feature Context

| subset | rows | bond-change | proton-transfer | electron-transfer | mechanism abstained | retained caught |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all overlap | 21 | 16 | 17 | 6 | 18 | 11 |
| current-retained overlap | 13 | 9 | 11 | 5 | 11 | 11 |

## Source-Free Best-Axis Current Surface Overlap

- Best single axis: electron_flow
- New OOS catches on current extended OOS: 3/4
- New current-retained OOS catches: 2

| row | in current extended OOS | current score | current abstains | best-axis residual | current retained catch |
| --- | --- | ---: | --- | ---: | --- |
| m_csa:154 | False | None | None | 1.90740451 | False |
| m_csa:221 | True | 0.6042 | False | 1.90740451 | True |
| m_csa:224 | True | 0.4011 | True | 1.90740451 | False |
| m_csa:256 | True | 0.61925 | False | 2.71877433 | True |

## Existing Source-Free Candidate Reuse

- Coordinate-anchor candidate files checked: 126
- Missing current primary rows covered by existing candidates: 0
- Missing current-retained OOS rows covered by existing candidates: 0
- Missing already-abstained OOS rows covered by existing candidates: 0

## OOS Overlap Rows

| row | current score | current abstains | mechanism residual | mechanism abstains | caught retained OOS | electron | proton | bond |
| --- | ---: | --- | ---: | --- | --- | --- | --- | --- |
| m_csa:17 | 0.45885 | False | 6.02277599 | True | True | False | True | True |
| m_csa:23 | 0.4787 | False | 3.74834254 | True | True | False | True | True |
| m_csa:25 | 0.6241 | False | 3.67227966 | True | True | False | False | True |
| m_csa:40 | 0.41725 | True | 3.63849194 | True | False | False | False | True |
| m_csa:59 | 0.60775 | False | 4.23431067 | True | True | True | True | False |
| m_csa:70 | 0.47955 | False | 3.26807732 | True | True | False | True | True |
| m_csa:78 | 0.4054 | True | 2.33596541 | False | False | False | True | True |
| m_csa:85 | 0.49955 | False | 4.96150995 | True | True | False | True | False |
| m_csa:149 | 0.37655 | True | 3.55609944 | True | False | False | True | True |
| m_csa:194 | 0.4559 | False | 5.12488835 | True | True | True | True | True |
| m_csa:221 | 0.6042 | False | 3.84686852 | True | True | False | True | True |
| m_csa:222 | 0.52675 | False | 5.21496062 | True | True | False | True | True |
| m_csa:224 | 0.4011 | True | 4.13211893 | True | False | False | True | False |
| m_csa:246 | 0.5171 | False | 1.71494092 | False | False | True | True | True |
| m_csa:253 | 0.5158 | False | 4.44010536 | True | True | False | True | True |
| m_csa:256 | 0.61925 | False | 2.79157886 | False | False | True | False | False |
| m_csa:263 | 0.42965 | True | 4.28326141 | True | False | True | True | True |
| m_csa:273 | 0.4133 | True | 3.92572474 | True | False | False | True | True |
| m_csa:287 | 0.41145 | True | 4.61602905 | True | False | False | False | True |
| m_csa:312 | 0.5714 | False | 4.23552349 | True | True | True | True | False |
| m_csa:318 | 0.34875 | True | 3.3510611 | True | False | False | True | True |

## Missing Evidence

| gap | required | valid now | missing now | why it matters |
| --- | ---: | ---: | ---: | --- |
| current_primary_mechanism_retention_gate | 34 | 0 | 34 | A deployable or promotable Lever 2 operating-point claim requires primary retention cost on the same current geometry/fold calibration-primary split. |
| current_extended_retained_oos_mechanism_features | 132 | 13 | 119 | These are current-surface retained OOS rows where mechanism evidence would be most valuable if it transfers. |
| current_extended_abstained_oos_mechanism_features | 72 | 8 | 64 | These complete the current extended OOS surface but are lower priority because geometry/fold already abstains. |

## Exact Missing Row Sets

- Current primary rows still requiring mechanism features (34): m_csa:27, m_csa:38, m_csa:41, m_csa:87, m_csa:102, m_csa:160, m_csa:165, m_csa:173, m_csa:216, m_csa:233, m_csa:277, m_csa:305, m_csa:319, m_csa:320, m_csa:338, m_csa:387, m_csa:399, m_csa:410, m_csa:473, m_csa:482, m_csa:556, m_csa:630, m_csa:694, m_csa:754, m_csa:800, m_csa:837, m_csa:865, m_csa:879, m_csa:900, m_csa:912, m_csa:922, m_csa:933, m_csa:973, m_csa:988
- Current-retained extended OOS rows still requiring mechanism features (119): m_csa:7, m_csa:8, m_csa:21, m_csa:35, m_csa:36, m_csa:39, m_csa:48, m_csa:52, m_csa:54, m_csa:60, m_csa:61, m_csa:65, m_csa:74, m_csa:75, m_csa:82, m_csa:84, m_csa:89, m_csa:90, m_csa:91, m_csa:95, m_csa:99, m_csa:104, m_csa:106, m_csa:107, m_csa:119, m_csa:126, m_csa:127, m_csa:135, m_csa:136, m_csa:138, m_csa:143, m_csa:150, m_csa:151, m_csa:182, m_csa:187, m_csa:190, m_csa:200, m_csa:206, m_csa:207, m_csa:214 ...
- Already-abstained extended OOS rows still requiring mechanism features (64): m_csa:4, m_csa:22, m_csa:24, m_csa:51, m_csa:57, m_csa:72, m_csa:88, m_csa:93, m_csa:105, m_csa:130, m_csa:134, m_csa:137, m_csa:139, m_csa:140, m_csa:145, m_csa:146, m_csa:177, m_csa:178, m_csa:179, m_csa:184, m_csa:189, m_csa:209, m_csa:251, m_csa:259, m_csa:262, m_csa:264, m_csa:265, m_csa:276, m_csa:282, m_csa:288, m_csa:290, m_csa:301, m_csa:303, m_csa:309, m_csa:314, m_csa:326, m_csa:327, m_csa:332, m_csa:342, m_csa:345 ...

## Top Missing Current-Retained OOS Rows

| row | accession | current score |
| --- | --- | ---: |
| m_csa:367 | Q9LCV9 | 0.72395 |
| m_csa:308 | P12070 | 0.68115 |
| m_csa:601 | P05164 | 0.67005 |
| m_csa:99 | P38539 | 0.66455 |
| m_csa:187 | P11444 | 0.65175 |
| m_csa:269 | Q4K9X1 | 0.65065 |
| m_csa:104 | P13650 | 0.6498 |
| m_csa:348 | P05404 | 0.649 |
| m_csa:468 | Q05514 | 0.64225 |
| m_csa:488 | P32170 | 0.64045 |
| m_csa:289 | P07342 | 0.6398 |
| m_csa:206 | P71447 | 0.63845 |
| m_csa:268 | P13009 | 0.63655 |
| m_csa:190 | Q46822 | 0.6365 |
| m_csa:483 | A9CEQ8 | 0.6341 |
| m_csa:652 | P51016 | 0.6333 |
| m_csa:500 | Q9QYY9 | 0.61935 |
| m_csa:421 | P10342 | 0.61545 |
| m_csa:52 | P0AB71 | 0.6154 |
| m_csa:74 | P13000 | 0.61305 |

## Decision

- Local OOS signal measured: True
- Valid integrated operating point measurable: False
- Adds operating-point value beyond current surface: False
- Deployable now: False
- Research-only: True
- Next gate: Materialize split-aligned source-free mechanism fields for the 119 current-retained OOS rows and 34 current calibration-primary rows, then rerun this fixed-threshold readout before any heldout or deployment claim.

## Interpretation

- On the current extended OOS overlap, the mechanism residual catches 11/13 rows retained by the current geometry/fold surface.
- Research-only: the newer current OOS surface increases the train/cal mechanism overlap to 21 rows and raises overlap abstentions from 8 to 19 under a fixed OR gate, but valid primary overlap remains 0 rows.
- Build split-aligned source-free mechanism features for the current primary retention gate and current-retained OOS rows.
