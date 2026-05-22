load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_1PVI.cif", m_csa_897
hide everything
show cartoon, m_csa_897
color gray70, m_csa_897
set cartoon_transparency, 0.8, m_csa_897
select m_csa_897_left, m_csa_897 and chain A and resi 70 and resn LYS
select m_csa_897_right, m_csa_897 and chain A and resi 58 and resn ASP
show sticks, m_csa_897_left or m_csa_897_right
color tv_red, m_csa_897_left
color tv_blue, m_csa_897_right
distance m_csa_897_distance, (m_csa_897 and chain A and resi 70 and resn LYS and name CA), (m_csa_897 and chain A and resi 58 and resn ASP and name CA)
label m_csa_897_distance, "9.672 A"
zoom m_csa_897_left or m_csa_897_right, 8
set dash_width, 3
set label_size, 18
