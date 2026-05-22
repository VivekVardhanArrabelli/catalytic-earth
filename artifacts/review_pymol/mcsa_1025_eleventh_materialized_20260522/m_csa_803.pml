load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1O04.cif", m_csa_803
hide everything
show cartoon, m_csa_803
color gray70, m_csa_803
set cartoon_transparency, 0.8, m_csa_803
select m_csa_803_left, m_csa_803 and chain A and resi 192 and resn LYS
select m_csa_803_right, m_csa_803 and chain A and resi 399 and resn GLU
show sticks, m_csa_803_left or m_csa_803_right
color tv_red, m_csa_803_left
color tv_blue, m_csa_803_right
distance m_csa_803_distance, (m_csa_803 and chain A and resi 192 and resn LYS and name CA), (m_csa_803 and chain A and resi 399 and resn GLU and name CA)
label m_csa_803_distance, "23.414 A"
zoom m_csa_803_left or m_csa_803_right, 8
set dash_width, 3
set label_size, 18
