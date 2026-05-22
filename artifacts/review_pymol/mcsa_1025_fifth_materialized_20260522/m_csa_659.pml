load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_1K82.cif", m_csa_659
hide everything
show cartoon, m_csa_659
color gray70, m_csa_659
set cartoon_transparency, 0.8, m_csa_659
select m_csa_659_left, m_csa_659 and chain A and resi 1 and resn PRO
select m_csa_659_right, m_csa_659 and chain A and resi 2 and resn GLU
show sticks, m_csa_659_left or m_csa_659_right
color tv_red, m_csa_659_left
color tv_blue, m_csa_659_right
distance m_csa_659_distance, (m_csa_659 and chain A and resi 1 and resn PRO and name CA), (m_csa_659 and chain A and resi 2 and resn GLU and name CA)
label m_csa_659_distance, "3.823 A"
zoom m_csa_659_left or m_csa_659_right, 8
set dash_width, 3
set label_size, 18
