load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_4E5K.cif", m_csa_984
hide everything
show cartoon, m_csa_984
color gray70, m_csa_984
set cartoon_transparency, 0.8, m_csa_984
select m_csa_984_left, m_csa_984 and chain B and resi 53 and resn MET
select m_csa_984_right, m_csa_984 and chain B and resi 237 and resn ARG
show sticks, m_csa_984_left or m_csa_984_right
color tv_red, m_csa_984_left
color tv_blue, m_csa_984_right
distance m_csa_984_distance, (m_csa_984 and chain B and resi 53 and resn MET and name CA), (m_csa_984 and chain B and resi 237 and resn ARG and name CA)
label m_csa_984_distance, "11.767 A"
zoom m_csa_984_left or m_csa_984_right, 8
set dash_width, 3
set label_size, 18
