load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_2AR8.cif", m_csa_977
hide everything
show cartoon, m_csa_977
color gray70, m_csa_977
set cartoon_transparency, 0.8, m_csa_977
select m_csa_977_left, m_csa_977 and chain A and resi 79 and resn LYS
select m_csa_977_right, m_csa_977 and chain A and resi 346 and resn GLU
show sticks, m_csa_977_left or m_csa_977_right
color tv_red, m_csa_977_left
color tv_blue, m_csa_977_right
distance m_csa_977_distance, (m_csa_977 and chain A and resi 79 and resn LYS and name CA), (m_csa_977 and chain A and resi 346 and resn GLU and name CA)
label m_csa_977_distance, "12.031 A"
zoom m_csa_977_left or m_csa_977_right, 8
set dash_width, 3
set label_size, 18
