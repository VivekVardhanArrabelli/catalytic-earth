load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_1OYG.cif", m_csa_875
hide everything
show cartoon, m_csa_875
color gray70, m_csa_875
set cartoon_transparency, 0.8, m_csa_875
select m_csa_875_left, m_csa_875 and chain A and resi 60 and resn ASP
select m_csa_875_right, m_csa_875 and chain A and resi 221 and resn ASP
show sticks, m_csa_875_left or m_csa_875_right
color tv_red, m_csa_875_left
color tv_blue, m_csa_875_right
distance m_csa_875_distance, (m_csa_875 and chain A and resi 60 and resn ASP and name CA), (m_csa_875 and chain A and resi 221 and resn ASP and name CA)
label m_csa_875_distance, "26.503 A"
zoom m_csa_875_left or m_csa_875_right, 8
set dash_width, 3
set label_size, 18
