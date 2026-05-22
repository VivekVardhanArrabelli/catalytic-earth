load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_2BHG.cif", m_csa_763
hide everything
show cartoon, m_csa_763
color gray70, m_csa_763
set cartoon_transparency, 0.8, m_csa_763
select m_csa_763_left, m_csa_763 and chain A and resi 85 and resn ASP
select m_csa_763_right, m_csa_763 and chain A and resi 164 and resn ALA
show sticks, m_csa_763_left or m_csa_763_right
color tv_red, m_csa_763_left
color tv_blue, m_csa_763_right
distance m_csa_763_distance, (m_csa_763 and chain A and resi 85 and resn ASP and name CA), (m_csa_763 and chain A and resi 164 and resn ALA and name CA)
label m_csa_763_distance, "9.608 A"
zoom m_csa_763_left or m_csa_763_right, 8
set dash_width, 3
set label_size, 18
