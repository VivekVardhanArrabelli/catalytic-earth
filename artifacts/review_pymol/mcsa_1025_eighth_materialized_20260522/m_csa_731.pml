load "artifacts/v3_mcsa_pymol_second_materialized_coordinates_20260522/pdb_1MT5.cif", m_csa_731
hide everything
show cartoon, m_csa_731
color gray70, m_csa_731
set cartoon_transparency, 0.8, m_csa_731
select m_csa_731_left, m_csa_731 and chain A and resi 203 and resn GLY
select m_csa_731_right, m_csa_731 and chain A and resi 106 and resn LYS
show sticks, m_csa_731_left or m_csa_731_right
color tv_red, m_csa_731_left
color tv_blue, m_csa_731_right
distance m_csa_731_distance, (m_csa_731 and chain A and resi 203 and resn GLY and name CA), (m_csa_731 and chain A and resi 106 and resn LYS and name CA)
label m_csa_731_distance, "15.880 A"
zoom m_csa_731_left or m_csa_731_right, 8
set dash_width, 3
set label_size, 18
