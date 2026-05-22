load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_1Q91.cif", m_csa_812
hide everything
show cartoon, m_csa_812
color gray70, m_csa_812
set cartoon_transparency, 0.8, m_csa_812
select m_csa_812_left, m_csa_812 and chain A and resi 145 and resn ASP
select m_csa_812_right, m_csa_812 and chain A and resi 12 and resn ASP
show sticks, m_csa_812_left or m_csa_812_right
color tv_red, m_csa_812_left
color tv_blue, m_csa_812_right
distance m_csa_812_distance, (m_csa_812 and chain A and resi 145 and resn ASP and name CA), (m_csa_812 and chain A and resi 12 and resn ASP and name CA)
label m_csa_812_distance, "8.109 A"
zoom m_csa_812_left or m_csa_812_right, 8
set dash_width, 3
set label_size, 18
