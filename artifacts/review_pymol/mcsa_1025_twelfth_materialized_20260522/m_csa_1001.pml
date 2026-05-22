load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_5M4G.cif", m_csa_1001
hide everything
show cartoon, m_csa_1001
color gray70, m_csa_1001
set cartoon_transparency, 0.8, m_csa_1001
select m_csa_1001_left, m_csa_1001 and chain A and resi 271 and resn ASP
select m_csa_1001_right, m_csa_1001 and chain A and resi 393 and resn ARG
show sticks, m_csa_1001_left or m_csa_1001_right
color tv_red, m_csa_1001_left
color tv_blue, m_csa_1001_right
distance m_csa_1001_distance, (m_csa_1001 and chain A and resi 271 and resn ASP and name CA), (m_csa_1001 and chain A and resi 393 and resn ARG and name CA)
label m_csa_1001_distance, "30.173 A"
zoom m_csa_1001_left or m_csa_1001_right, 8
set dash_width, 3
set label_size, 18
