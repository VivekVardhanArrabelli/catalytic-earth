load "artifacts/v3_mcsa_pymol_ninth_materialized_coordinates_20260522/pdb_1PZ3.cif", m_csa_667
hide everything
show cartoon, m_csa_667
color gray70, m_csa_667
set cartoon_transparency, 0.8, m_csa_667
select m_csa_667_left, m_csa_667 and chain A and resi 294 and resn GLU
select m_csa_667_right, m_csa_667 and chain A and resi 175 and resn GLU
show sticks, m_csa_667_left or m_csa_667_right
color tv_red, m_csa_667_left
color tv_blue, m_csa_667_right
distance m_csa_667_distance, (m_csa_667 and chain A and resi 294 and resn GLU and name CA), (m_csa_667 and chain A and resi 175 and resn GLU and name CA)
label m_csa_667_distance, "10.399 A"
zoom m_csa_667_left or m_csa_667_right, 8
set dash_width, 3
set label_size, 18
