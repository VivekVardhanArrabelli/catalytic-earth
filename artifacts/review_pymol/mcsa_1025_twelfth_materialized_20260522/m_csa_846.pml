load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1DXE.cif", m_csa_846
hide everything
show cartoon, m_csa_846
color gray70, m_csa_846
set cartoon_transparency, 0.8, m_csa_846
select m_csa_846_left, m_csa_846 and chain A and resi 179 and resn ASP
select m_csa_846_right, m_csa_846 and chain A and resi 89 and resn ASP
show sticks, m_csa_846_left or m_csa_846_right
color tv_red, m_csa_846_left
color tv_blue, m_csa_846_right
distance m_csa_846_distance, (m_csa_846 and chain A and resi 179 and resn ASP and name CA), (m_csa_846 and chain A and resi 89 and resn ASP and name CA)
label m_csa_846_distance, "28.956 A"
zoom m_csa_846_left or m_csa_846_right, 8
set dash_width, 3
set label_size, 18
