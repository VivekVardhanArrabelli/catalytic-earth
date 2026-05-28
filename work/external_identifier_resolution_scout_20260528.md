# External identifier resolution scout

- Mapping rows emitted: 27
- First materialization tranche: 10
- Coordinate fetches performed: False
- Confidence counts: {'high_local_mcsa_geometry_reference': 19, 'high_uniprot_spot_check_with_pdb_and_afdb': 8}

## First tranche
- mh_064 Metallo-beta-lactamase NDM-1: best_coordinate=3PG4 uniprot=C7C422 risk=bounded_small_pdb_or_afdb_fetch_after_approval
- mh_065 Metallo-beta-lactamase VIM-like enzyme: best_coordinate=1DDK uniprot=Q79MP6 risk=bounded_small_pdb_or_afdb_fetch_after_approval
- mh_067 Carbonic anhydrase 2: best_coordinate=12CA uniprot=P00918 risk=bounded_small_pdb_or_afdb_fetch_after_approval
- mh_068 Arylsulfatase A: best_coordinate=1AUK uniprot=P15289 risk=bounded_small_pdb_or_afdb_fetch_after_approval
- mh_072 Enolase: best_coordinate=1E9I uniprot=P0A6P9 risk=bounded_small_pdb_or_afdb_fetch_after_approval
- mh_073 GTPase HRas: best_coordinate=121P uniprot=P01112 risk=bounded_small_pdb_or_afdb_fetch_after_approval
- mh_035 beta-lactamase (Class B1): best_coordinate=1ZNB uniprot=None risk=no_fetch_needed_existing_local_geometry_row
- mh_037 cerebroside-sulfatase: best_coordinate=1AUK uniprot=None risk=no_fetch_needed_existing_local_geometry_row
- mh_048 carbonate dehydratase (alpha class): best_coordinate=1CA2 uniprot=None risk=no_fetch_needed_existing_local_geometry_row
- mh_054 4-hydroxybutanoyl-CoA dehydratase: best_coordinate=1U8V uniprot=None risk=no_fetch_needed_existing_local_geometry_row

Caveat: this blocker bucket is metal-hydrolase-tail only; other panel stress rows already had local coordinates or were not in this materialization blocker bucket.
