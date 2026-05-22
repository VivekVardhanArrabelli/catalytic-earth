load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_4XB6.cif", m_csa_949
hide everything
show cartoon, m_csa_949
color gray70, m_csa_949
set cartoon_transparency, 0.8, m_csa_949
select m_csa_949_left, m_csa_949 and chain D and resi 244 and resn CYS
select m_csa_949_right, m_csa_949 and chain D and resi 32 and resn GLY
show sticks, m_csa_949_left or m_csa_949_right
color tv_red, m_csa_949_left
color tv_blue, m_csa_949_right
distance m_csa_949_distance, (m_csa_949 and chain D and resi 244 and resn CYS and name CA), (m_csa_949 and chain D and resi 32 and resn GLY and name CA)
label m_csa_949_distance, "35.991 A"
zoom m_csa_949_left or m_csa_949_right, 8
set dash_width, 3
set label_size, 18
