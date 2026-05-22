load "artifacts/v3_mcsa_pymol_third_materialized_coordinates_20260522/pdb_2BLE.cif", m_csa_982
hide everything
show cartoon, m_csa_982
color gray70, m_csa_982
set cartoon_transparency, 0.8, m_csa_982
select m_csa_982_left, m_csa_982 and chain A and resi 210 and resn THR
select m_csa_982_right, m_csa_982 and chain A and resi 311 and resn GLU
show sticks, m_csa_982_left or m_csa_982_right
color tv_red, m_csa_982_left
color tv_blue, m_csa_982_right
distance m_csa_982_distance, (m_csa_982 and chain A and resi 210 and resn THR and name CA), (m_csa_982 and chain A and resi 311 and resn GLU and name CA)
label m_csa_982_distance, "7.910 A"
zoom m_csa_982_left or m_csa_982_right, 8
set dash_width, 3
set label_size, 18
