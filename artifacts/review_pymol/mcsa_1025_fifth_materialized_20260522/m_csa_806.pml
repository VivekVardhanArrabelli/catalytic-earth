load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_1CVR.cif", m_csa_806
hide everything
show cartoon, m_csa_806
color gray70, m_csa_806
set cartoon_transparency, 0.8, m_csa_806
select m_csa_806_left, m_csa_806 and chain A and resi 244 and resn CYS
select m_csa_806_right, m_csa_806 and chain A and resi 152 and resn GLU
show sticks, m_csa_806_left or m_csa_806_right
color tv_red, m_csa_806_left
color tv_blue, m_csa_806_right
distance m_csa_806_distance, (m_csa_806 and chain A and resi 244 and resn CYS and name CA), (m_csa_806 and chain A and resi 152 and resn GLU and name CA)
label m_csa_806_distance, "14.617 A"
zoom m_csa_806_left or m_csa_806_right, 8
set dash_width, 3
set label_size, 18
