load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_4E7K.cif", m_csa_989
hide everything
show cartoon, m_csa_989
color gray70, m_csa_989
set cartoon_transparency, 0.8, m_csa_989
select m_csa_989_left, m_csa_989 and chain A and resi 188 and resn ASP
select m_csa_989_right, m_csa_989 and chain A and resi 224 and resn GLU
show sticks, m_csa_989_left or m_csa_989_right
color tv_red, m_csa_989_left
color tv_blue, m_csa_989_right
distance m_csa_989_distance, (m_csa_989 and chain A and resi 188 and resn ASP and name CA), (m_csa_989 and chain A and resi 224 and resn GLU and name CA)
label m_csa_989_distance, "10.463 A"
zoom m_csa_989_left or m_csa_989_right, 8
set dash_width, 3
set label_size, 18
