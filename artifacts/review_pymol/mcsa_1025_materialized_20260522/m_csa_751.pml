load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1TZ3.cif", m_csa_751
hide everything
show cartoon, m_csa_751
color gray70, m_csa_751
set cartoon_transparency, 0.8, m_csa_751
select m_csa_751_left, m_csa_751 and chain A and resi 272 and resn ASP
select m_csa_751_right, m_csa_751 and chain A and resi 270 and resn ALA
show sticks, m_csa_751_left or m_csa_751_right
color tv_red, m_csa_751_left
color tv_blue, m_csa_751_right
distance m_csa_751_distance, (m_csa_751 and chain A and resi 272 and resn ASP and name CA), (m_csa_751 and chain A and resi 270 and resn ALA and name CA)
label m_csa_751_distance, "5.619 A"
zoom m_csa_751_left or m_csa_751_right, 8
set dash_width, 3
set label_size, 18
