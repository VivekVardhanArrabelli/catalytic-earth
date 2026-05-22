load "artifacts/v3_mcsa_pymol_materialized_coordinates_20260522/pdb_1FDY.cif", m_csa_553
hide everything
show cartoon, m_csa_553
color gray70, m_csa_553
set cartoon_transparency, 0.8, m_csa_553
select m_csa_553_left, m_csa_553 and chain A and resi 165 and resn LYS
select m_csa_553_right, m_csa_553 and chain A and resi 137 and resn TYR
show sticks, m_csa_553_left or m_csa_553_right
color tv_red, m_csa_553_left
color tv_blue, m_csa_553_right
distance m_csa_553_distance, (m_csa_553 and chain A and resi 165 and resn LYS and name CA), (m_csa_553 and chain A and resi 137 and resn TYR and name CA)
label m_csa_553_distance, "4.714 A"
zoom m_csa_553_left or m_csa_553_right, 8
set dash_width, 3
set label_size, 18
