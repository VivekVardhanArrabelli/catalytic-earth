# TDPn3 substrate-window test: complete, mixed primary result

All 20 assigned RF3 predictions were produced and identified. The prespecified
contact-count outcome is **mixed/inconclusive**. Neither reproducible loss,
reproducible gain nor contact retention across both seeds meets the saved rule.
No extra seeds, rescues, templates, pose restraints or sequence changes were used.

| Peptide | Seed | Zn–G7 O <3.2 Å | Median Zn–G7 O (Å) | Median E147–water O (Å) | Median water O–G7 C–G7 O angle |
| --- | ---: | ---: | ---: | ---: | ---: |
| 10 residues | 0 | 4/5 | 3.109 | 2.644 | 97.3° |
| 10 residues | 1 | 3/5 | 3.099 | 2.725 | 92.2° |
| 12 residues | 0 | 3/5 | 2.714 | 5.261 | 45.5° |
| 12 residues | 1 | 4/5 | 3.009 | 4.976 | 33.0° |

The secondary geometry is consequential. Across all samples, Zn remains near
its enzyme ligands: H146/H150 distances span 1.96–2.09 Å and the nearer E45
oxygen spans 1.99–2.22 Å. Thus the changes are not explained by global loss of
the modeled metal site. The longer window shifts the base/water arrangement
in both seeds, even though its target-contact count does not consistently drop.
A Zn–carbonyl contact alone does not establish catalytic preorganization.

G7 is the closest peptide amide carbonyl in all ten short-window samples and
eight long-window samples. In the two remaining long-window samples, S5–W6
(seed 0/sample 1) or M11–L12 (seed 1/sample 3) is closest. These are predicted
alternative arrangements, **not observed alternative cleavage sites**. Some
water/metal and donor distances are unusually short; the raw values remain
visible rather than being filtered into a favorable geometry set.

These secondary observations do not convert the mixed primary result into a
positive prespecified window-loss finding. Samples share trunk calculations,
seeds are not biological replicates, and adding ML also changes the free terminus.
The experiment does not isolate terminal charge, reproduce the fusion substrate,
measure activity or show an Atlas design advantage.

## Runtime and reproducibility

The two inputs and decision were committed at `62464126` before inference.
The real RF3 parser preserved the exact protein/peptide sequences, ordinary
peptide bonds, Zn formal charge +2 and disconnected neutral water. The pinned
Foundry commit is `0932f1cb165ae7d413c11b1a7acc04ee31758817`; the official
3,038,876,446-byte checkpoint was hashed before loading:
`364ef592fd8042a9cf4176d045015190f8322f961ccca38d891b20ca578d3bb0`.
That is a recorded content identity, not an independently supplied vendor hash.

Cached MACE descriptors were absent. The installed code used zero descriptor
tensors and absence masks; inert checkpoint inspection confirmed enabled
consumers of those features. This is the supported missing-feature path, not
proof of equivalent quality with the descriptors present. RDKit reference
conformers are separate. The [runtime warning audit](mace_warning_audit.json)
retains source hashes, excerpts and checkpoint scalar evidence. No MSA was used.

- [All 20 measurements](all_20_measurements.csv): distances in Å; the two angle columns in degrees; confidence in native RF3 scale.
- [Machine-readable result](result_summary.json): full primary groups, secondary seed summaries, runtime and rental identity.
- [Complete raw bundle](result_bundle.tar.gz): all 20 assigned CIFs, four additional native ranked/aggregate CIFs, confidence files, native input maps, assignment receipts, scripts, versions and logs. The four aggregate outputs are not additional samples.
- [Measurement adapter](../rf3_measure_outputs.py) and [exact remote bootstrap](remote_bootstrap.sh).

Bundle SHA256: `6a09d98e8145b7805de35fc0a12b6d9a115cef57a85a66abe598fe33e184dc82`.
Every assigned CIF hash was independently verified after retrieval. Extract the
bundle and run the adapter with its `output`, `input`, and saved decision paths
to reproduce the measurements using Biotite 1.4.0. Preserve the original output
JSON and choose a fresh output filename for any recomputation.

The authorized A100 was terminated through the provider after 17 minutes,
well inside $5/45 minutes. Creation-to-termination at $1.20/hour is approximately
$0.34; the provider has not yet reported the final charge. Weights and credentials
are not included in the result bundle.

## Decision and next action

Stop this window comparison without rescue sampling. It shows why target-contact
and confidence filters cannot alone qualify catalytic geometry. The next bounded
step is native RFD3 acceptance of the already reconstructed fixed-target input:
preserve the intended chemical identities and coordinate masks before treating
it as a design-ready constraint. New scaffold generation needs a prospective
comparison and a downstream biochemical evaluation plan; this RF3 result does
not qualify an activity filter or justify an open-ended design campaign.
