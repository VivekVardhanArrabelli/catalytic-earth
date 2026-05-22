load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1B5D.cif", m_csa_700
hide everything
show cartoon, m_csa_700
color gray70, m_csa_700
set cartoon_transparency, 0.8, m_csa_700
select m_csa_700_left, m_csa_700 and chain A and resi 148 and resn CYS
select m_csa_700_right, m_csa_700 and chain A and resi 60 and resn GLU
show sticks, m_csa_700_left or m_csa_700_right
color tv_red, m_csa_700_left
color tv_blue, m_csa_700_right
distance m_csa_700_distance, (m_csa_700 and chain A and resi 148 and resn CYS and name CA), (m_csa_700 and chain A and resi 60 and resn GLU and name CA)
label m_csa_700_distance, "16.031 A"
zoom m_csa_700_left or m_csa_700_right, 8
set dash_width, 3
set label_size, 18
