load "artifacts/v3_mcsa_pymol_sixth_materialized_coordinates_20260522/pdb_2ABK.cif", m_csa_888
hide everything
show cartoon, m_csa_888
color gray70, m_csa_888
set cartoon_transparency, 0.8, m_csa_888
select m_csa_888_left, m_csa_888 and chain A and resi 120 and resn LYS
select m_csa_888_right, m_csa_888 and chain A and resi 138 and resn ASP
show sticks, m_csa_888_left or m_csa_888_right
color tv_red, m_csa_888_left
color tv_blue, m_csa_888_right
distance m_csa_888_distance, (m_csa_888 and chain A and resi 120 and resn LYS and name CA), (m_csa_888 and chain A and resi 138 and resn ASP and name CA)
label m_csa_888_distance, "8.371 A"
zoom m_csa_888_left or m_csa_888_right, 8
set dash_width, 3
set label_size, 18
