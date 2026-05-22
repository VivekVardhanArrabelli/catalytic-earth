load "artifacts/v3_foldseek_coordinates_1000/pdb_3CMM.cif", m_csa_939
hide everything
show cartoon, m_csa_939
color gray70, m_csa_939
set cartoon_transparency, 0.8, m_csa_939
select m_csa_939_left, m_csa_939 and chain A and resi 773 and resn ASP
select m_csa_939_right, m_csa_939 and chain A and resi 594 and resn ARG
show sticks, m_csa_939_left or m_csa_939_right
color tv_red, m_csa_939_left
color tv_blue, m_csa_939_right
distance m_csa_939_distance, (m_csa_939 and chain A and resi 773 and resn ASP and name CA), (m_csa_939 and chain A and resi 594 and resn ARG and name CA)
label m_csa_939_distance, "10.587 A"
zoom m_csa_939_left or m_csa_939_right, 8
set dash_width, 3
set label_size, 18
