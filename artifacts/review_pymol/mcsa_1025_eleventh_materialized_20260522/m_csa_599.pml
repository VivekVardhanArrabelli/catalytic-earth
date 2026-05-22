load "artifacts/v3_mcsa_pymol_eleventh_materialized_coordinates_20260522/pdb_1FY2.cif", m_csa_599
hide everything
show cartoon, m_csa_599
color gray70, m_csa_599
set cartoon_transparency, 0.8, m_csa_599
select m_csa_599_left, m_csa_599 and chain A and resi 88 and resn GLY
select m_csa_599_right, m_csa_599 and chain A and resi 192 and resn GLU
show sticks, m_csa_599_left or m_csa_599_right
color tv_red, m_csa_599_left
color tv_blue, m_csa_599_right
distance m_csa_599_distance, (m_csa_599 and chain A and resi 88 and resn GLY and name CA), (m_csa_599 and chain A and resi 192 and resn GLU and name CA)
label m_csa_599_distance, "14.462 A"
zoom m_csa_599_left or m_csa_599_right, 8
set dash_width, 3
set label_size, 18
