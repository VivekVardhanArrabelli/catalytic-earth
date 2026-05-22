load "artifacts/v3_mcsa_pymol_eighth_materialized_coordinates_20260522/pdb_1L9X.cif", m_csa_747
hide everything
show cartoon, m_csa_747
color gray70, m_csa_747
set cartoon_transparency, 0.8, m_csa_747
select m_csa_747_left, m_csa_747 and chain B and resi 243 and resn GLU
select m_csa_747_right, m_csa_747 and chain B and resi 131 and resn CYS
show sticks, m_csa_747_left or m_csa_747_right
color tv_red, m_csa_747_left
color tv_blue, m_csa_747_right
distance m_csa_747_distance, (m_csa_747 and chain B and resi 243 and resn GLU and name CA), (m_csa_747 and chain B and resi 131 and resn CYS and name CA)
label m_csa_747_distance, "11.072 A"
zoom m_csa_747_left or m_csa_747_right, 8
set dash_width, 3
set label_size, 18
