load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_1R30.cif", m_csa_767
hide everything
show cartoon, m_csa_767
color gray70, m_csa_767
set cartoon_transparency, 0.8, m_csa_767
select m_csa_767_left, m_csa_767 and chain A and resi 76 and resn CYS
select m_csa_767_right, m_csa_767 and chain A and resi 283 and resn ARG
show sticks, m_csa_767_left or m_csa_767_right
color tv_red, m_csa_767_left
color tv_blue, m_csa_767_right
distance m_csa_767_distance, (m_csa_767 and chain A and resi 76 and resn CYS and name CA), (m_csa_767 and chain A and resi 283 and resn ARG and name CA)
label m_csa_767_distance, "25.157 A"
zoom m_csa_767_left or m_csa_767_right, 8
set dash_width, 3
set label_size, 18
