load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_1KAZ.cif", m_csa_656
hide everything
show cartoon, m_csa_656
color gray70, m_csa_656
set cartoon_transparency, 0.8, m_csa_656
select m_csa_656_left, m_csa_656 and chain A and resi 199 and resn ASP
select m_csa_656_right, m_csa_656 and chain A and resi 71 and resn GLU
show sticks, m_csa_656_left or m_csa_656_right
color tv_red, m_csa_656_left
color tv_blue, m_csa_656_right
distance m_csa_656_distance, (m_csa_656 and chain A and resi 199 and resn ASP and name CA), (m_csa_656 and chain A and resi 71 and resn GLU and name CA)
label m_csa_656_distance, "16.108 A"
zoom m_csa_656_left or m_csa_656_right, 8
set dash_width, 3
set label_size, 18
