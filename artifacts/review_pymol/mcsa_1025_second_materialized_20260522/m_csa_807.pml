load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_6U7T.cif", m_csa_807
hide everything
show cartoon, m_csa_807
color gray70, m_csa_807
set cartoon_transparency, 0.8, m_csa_807
select m_csa_807_left, m_csa_807 and chain A and resi 43 and resn GLU
select m_csa_807_right, m_csa_807 and chain A and resi 144 and resn ASP
show sticks, m_csa_807_left or m_csa_807_right
color tv_red, m_csa_807_left
color tv_blue, m_csa_807_right
distance m_csa_807_distance, (m_csa_807 and chain A and resi 43 and resn GLU and name CA), (m_csa_807 and chain A and resi 144 and resn ASP and name CA)
label m_csa_807_distance, "10.721 A"
zoom m_csa_807_left or m_csa_807_right, 8
set dash_width, 3
set label_size, 18
