load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_1PMI.cif", m_csa_880
hide everything
show cartoon, m_csa_880
color gray70, m_csa_880
set cartoon_transparency, 0.8, m_csa_880
select m_csa_880_left, m_csa_880 and chain A and resi 137 and resn GLU
select m_csa_880_right, m_csa_880 and chain A and resi 309 and resn LYS
show sticks, m_csa_880_left or m_csa_880_right
color tv_red, m_csa_880_left
color tv_blue, m_csa_880_right
distance m_csa_880_distance, (m_csa_880 and chain A and resi 137 and resn GLU and name CA), (m_csa_880 and chain A and resi 309 and resn LYS and name CA)
label m_csa_880_distance, "20.318 A"
zoom m_csa_880_left or m_csa_880_right, 8
set dash_width, 3
set label_size, 18
