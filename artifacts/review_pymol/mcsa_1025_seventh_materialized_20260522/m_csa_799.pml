load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1F48.cif", m_csa_799
hide everything
show cartoon, m_csa_799
color gray70, m_csa_799
set cartoon_transparency, 0.8, m_csa_799
select m_csa_799_left, m_csa_799 and chain A and resi 45 and resn ASP
select m_csa_799_right, m_csa_799 and chain A and resi 20 and resn GLY
show sticks, m_csa_799_left or m_csa_799_right
color tv_red, m_csa_799_left
color tv_blue, m_csa_799_right
distance m_csa_799_distance, (m_csa_799 and chain A and resi 45 and resn ASP and name CA), (m_csa_799 and chain A and resi 20 and resn GLY and name CA)
label m_csa_799_distance, "12.231 A"
zoom m_csa_799_left or m_csa_799_right, 8
set dash_width, 3
set label_size, 18
