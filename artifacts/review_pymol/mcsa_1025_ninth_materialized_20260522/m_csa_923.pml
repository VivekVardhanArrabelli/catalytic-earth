load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_2ACY.cif", m_csa_923
hide everything
show cartoon, m_csa_923
color gray70, m_csa_923
set cartoon_transparency, 0.8, m_csa_923
select m_csa_923_left, m_csa_923 and chain A and resi 23 and resn ARG
select m_csa_923_right, m_csa_923 and chain A and resi 41 and resn ASN
show sticks, m_csa_923_left or m_csa_923_right
color tv_red, m_csa_923_left
color tv_blue, m_csa_923_right
distance m_csa_923_distance, (m_csa_923 and chain A and resi 23 and resn ARG and name CA), (m_csa_923 and chain A and resi 41 and resn ASN and name CA)
label m_csa_923_distance, "7.827 A"
zoom m_csa_923_left or m_csa_923_right, 8
set dash_width, 3
set label_size, 18
