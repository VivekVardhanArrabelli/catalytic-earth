load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_1AVQ.cif", m_csa_836
hide everything
show cartoon, m_csa_836
color gray70, m_csa_836
set cartoon_transparency, 0.8, m_csa_836
select m_csa_836_left, m_csa_836 and chain A and resi 111 and resn ASP
select m_csa_836_right, m_csa_836 and chain A and resi 95 and resn GLU
show sticks, m_csa_836_left or m_csa_836_right
color tv_red, m_csa_836_left
color tv_blue, m_csa_836_right
distance m_csa_836_distance, (m_csa_836 and chain A and resi 111 and resn ASP and name CA), (m_csa_836 and chain A and resi 95 and resn GLU and name CA)
label m_csa_836_distance, "29.544 A"
zoom m_csa_836_left or m_csa_836_right, 8
set dash_width, 3
set label_size, 18
