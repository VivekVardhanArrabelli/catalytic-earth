load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_3RFA.cif", m_csa_938
hide everything
show cartoon, m_csa_938
color gray70, m_csa_938
set cartoon_transparency, 0.8, m_csa_938
select m_csa_938_left, m_csa_938 and chain B and resi 118 and resn CYS
select m_csa_938_right, m_csa_938 and chain B and resi 129 and resn CYS
show sticks, m_csa_938_left or m_csa_938_right
color tv_red, m_csa_938_left
color tv_blue, m_csa_938_right
distance m_csa_938_distance, (m_csa_938 and chain B and resi 118 and resn CYS and name CA), (m_csa_938 and chain B and resi 129 and resn CYS and name CA)
label m_csa_938_distance, "18.765 A"
zoom m_csa_938_left or m_csa_938_right, 8
set dash_width, 3
set label_size, 18
