load "artifacts/v3_mcsa_pymol_tenth_materialized_coordinates_20260522/pdb_1QBA.cif", m_csa_899
hide everything
show cartoon, m_csa_899
color gray70, m_csa_899
set cartoon_transparency, 0.8, m_csa_899
select m_csa_899_left, m_csa_899 and chain A and resi 512 and resn ASP
select m_csa_899_right, m_csa_899 and chain A and resi 513 and resn GLU
show sticks, m_csa_899_left or m_csa_899_right
color tv_red, m_csa_899_left
color tv_blue, m_csa_899_right
distance m_csa_899_distance, (m_csa_899 and chain A and resi 512 and resn ASP and name CA), (m_csa_899 and chain A and resi 513 and resn GLU and name CA)
label m_csa_899_distance, "3.799 A"
zoom m_csa_899_left or m_csa_899_right, 8
set dash_width, 3
set label_size, 18
