load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_3AIE.cif", m_csa_1002
hide everything
show cartoon, m_csa_1002
color gray70, m_csa_1002
set cartoon_transparency, 0.8, m_csa_1002
select m_csa_1002_left, m_csa_1002 and chain A and resi 234 and resn ASP
select m_csa_1002_right, m_csa_1002 and chain A and resi 345 and resn ASP
show sticks, m_csa_1002_left or m_csa_1002_right
color tv_red, m_csa_1002_left
color tv_blue, m_csa_1002_right
distance m_csa_1002_distance, (m_csa_1002 and chain A and resi 234 and resn ASP and name CA), (m_csa_1002 and chain A and resi 345 and resn ASP and name CA)
label m_csa_1002_distance, "11.959 A"
zoom m_csa_1002_left or m_csa_1002_right, 8
set dash_width, 3
set label_size, 18
