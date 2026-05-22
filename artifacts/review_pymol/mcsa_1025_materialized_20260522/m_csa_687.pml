load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1ROZ.cif", m_csa_687
hide everything
show cartoon, m_csa_687
color gray70, m_csa_687
set cartoon_transparency, 0.8, m_csa_687
select m_csa_687_left, m_csa_687 and chain A and resi 288 and resn HIS
select m_csa_687_right, m_csa_687 and chain B and resi 137 and resn GLU
show sticks, m_csa_687_left or m_csa_687_right
color tv_red, m_csa_687_left
color tv_blue, m_csa_687_right
distance m_csa_687_distance, (m_csa_687 and chain A and resi 288 and resn HIS and name CA), (m_csa_687 and chain B and resi 137 and resn GLU and name CA)
label m_csa_687_distance, "40.834 A"
zoom m_csa_687_left or m_csa_687_right, 8
set dash_width, 3
set label_size, 18
