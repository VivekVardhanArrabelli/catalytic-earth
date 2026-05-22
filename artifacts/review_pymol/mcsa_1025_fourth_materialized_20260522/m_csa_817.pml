load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1ITX.cif", m_csa_817
hide everything
show cartoon, m_csa_817
color gray70, m_csa_817
set cartoon_transparency, 0.8, m_csa_817
select m_csa_817_left, m_csa_817 and chain A and resi 247 and resn TYR
select m_csa_817_right, m_csa_817 and chain A and resi 168 and resn ASP
show sticks, m_csa_817_left or m_csa_817_right
color tv_red, m_csa_817_left
color tv_blue, m_csa_817_right
distance m_csa_817_distance, (m_csa_817 and chain A and resi 247 and resn TYR and name CA), (m_csa_817 and chain A and resi 168 and resn ASP and name CA)
label m_csa_817_distance, "18.212 A"
zoom m_csa_817_left or m_csa_817_right, 8
set dash_width, 3
set label_size, 18
