load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1DJ7.cif", m_csa_980
hide everything
show cartoon, m_csa_980
color gray70, m_csa_980
set cartoon_transparency, 0.8, m_csa_980
select m_csa_980_left, m_csa_980 and chain A and resi 57 and resn CYS
select m_csa_980_right, m_csa_980 and chain A and resi 76 and resn CYS
show sticks, m_csa_980_left or m_csa_980_right
color tv_red, m_csa_980_left
color tv_blue, m_csa_980_right
distance m_csa_980_distance, (m_csa_980 and chain A and resi 57 and resn CYS and name CA), (m_csa_980 and chain A and resi 76 and resn CYS and name CA)
label m_csa_980_distance, "12.001 A"
zoom m_csa_980_left or m_csa_980_right, 8
set dash_width, 3
set label_size, 18
