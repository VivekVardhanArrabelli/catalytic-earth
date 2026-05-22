load "artifacts/v3_mcsa_pymol_fourth_materialized_coordinates_20260522/pdb_6FKW.cif", m_csa_997
hide everything
show cartoon, m_csa_997
color gray70, m_csa_997
set cartoon_transparency, 0.8, m_csa_997
select m_csa_997_left, m_csa_997 and chain A and resi 301 and resn ASP
select m_csa_997_right, m_csa_997 and chain A and resi 172 and resn GLU
show sticks, m_csa_997_left or m_csa_997_right
color tv_red, m_csa_997_left
color tv_blue, m_csa_997_right
distance m_csa_997_distance, (m_csa_997 and chain A and resi 301 and resn ASP and name CA), (m_csa_997 and chain A and resi 172 and resn GLU and name CA)
label m_csa_997_distance, "10.916 A"
zoom m_csa_997_left or m_csa_997_right, 8
set dash_width, 3
set label_size, 18
