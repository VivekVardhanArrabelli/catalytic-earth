load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_1EZ1.cif", m_csa_665
hide everything
show cartoon, m_csa_665
color gray70, m_csa_665
set cartoon_transparency, 0.8, m_csa_665
select m_csa_665_left, m_csa_665 and chain A and resi 279 and resn GLU
select m_csa_665_right, m_csa_665 and chain A and resi 363 and resn ARG
show sticks, m_csa_665_left or m_csa_665_right
color tv_red, m_csa_665_left
color tv_blue, m_csa_665_right
distance m_csa_665_distance, (m_csa_665 and chain A and resi 279 and resn GLU and name CA), (m_csa_665 and chain A and resi 363 and resn ARG and name CA)
label m_csa_665_distance, "21.147 A"
zoom m_csa_665_left or m_csa_665_right, 8
set dash_width, 3
set label_size, 18
