load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_1HT1.cif", m_csa_678
hide everything
show cartoon, m_csa_678
color gray70, m_csa_678
set cartoon_transparency, 0.8, m_csa_678
select m_csa_678_left, m_csa_678 and chain A and resi 45 and resn GLY
select m_csa_678_right, m_csa_678 and chain A and resi 124 and resn SER
show sticks, m_csa_678_left or m_csa_678_right
color tv_red, m_csa_678_left
color tv_blue, m_csa_678_right
distance m_csa_678_distance, (m_csa_678 and chain A and resi 45 and resn GLY and name CA), (m_csa_678 and chain A and resi 124 and resn SER and name CA)
label m_csa_678_distance, "14.426 A"
zoom m_csa_678_left or m_csa_678_right, 8
set dash_width, 3
set label_size, 18
