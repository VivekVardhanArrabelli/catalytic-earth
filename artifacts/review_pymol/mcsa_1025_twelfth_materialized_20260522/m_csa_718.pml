load "artifacts/v3_mcsa_pymol_seventh_materialized_coordinates_20260522/pdb_2FQQ.cif", m_csa_718
hide everything
show cartoon, m_csa_718
color gray70, m_csa_718
set cartoon_transparency, 0.8, m_csa_718
select m_csa_718_left, m_csa_718 and chain A and resi 118 and resn HIS
select m_csa_718_right, m_csa_718 and chain B and resi 74 and resn GLU
show sticks, m_csa_718_left or m_csa_718_right
color tv_red, m_csa_718_left
color tv_blue, m_csa_718_right
distance m_csa_718_distance, (m_csa_718 and chain A and resi 118 and resn HIS and name CA), (m_csa_718 and chain B and resi 74 and resn GLU and name CA)
label m_csa_718_distance, "18.389 A"
zoom m_csa_718_left or m_csa_718_right, 8
set dash_width, 3
set label_size, 18
