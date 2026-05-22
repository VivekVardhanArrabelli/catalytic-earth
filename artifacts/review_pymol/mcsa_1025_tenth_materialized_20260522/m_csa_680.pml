load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_1NN4.cif", m_csa_680
hide everything
show cartoon, m_csa_680
color gray70, m_csa_680
set cartoon_transparency, 0.8, m_csa_680
select m_csa_680_left, m_csa_680 and chain D and resi 112 and resn HIS
select m_csa_680_right, m_csa_680 and chain A and resi 22 and resn ASP
show sticks, m_csa_680_left or m_csa_680_right
color tv_red, m_csa_680_left
color tv_blue, m_csa_680_right
distance m_csa_680_distance, (m_csa_680 and chain D and resi 112 and resn HIS and name CA), (m_csa_680 and chain A and resi 22 and resn ASP and name CA)
label m_csa_680_distance, "14.194 A"
zoom m_csa_680_left or m_csa_680_right, 8
set dash_width, 3
set label_size, 18
