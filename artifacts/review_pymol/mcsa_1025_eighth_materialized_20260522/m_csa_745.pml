load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_1AB4.cif", m_csa_745
hide everything
show cartoon, m_csa_745
color gray70, m_csa_745
set cartoon_transparency, 0.8, m_csa_745
select m_csa_745_left, m_csa_745 and chain A and resi 3 and resn ARG
select m_csa_745_right, m_csa_745 and chain A and resi 93 and resn TYR
show sticks, m_csa_745_left or m_csa_745_right
color tv_red, m_csa_745_left
color tv_blue, m_csa_745_right
distance m_csa_745_distance, (m_csa_745 and chain A and resi 3 and resn ARG and name CA), (m_csa_745 and chain A and resi 93 and resn TYR and name CA)
label m_csa_745_distance, "28.739 A"
zoom m_csa_745_left or m_csa_745_right, 8
set dash_width, 3
set label_size, 18
