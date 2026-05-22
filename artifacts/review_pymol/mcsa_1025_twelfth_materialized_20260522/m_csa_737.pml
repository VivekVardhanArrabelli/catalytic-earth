load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_1XRS.cif", m_csa_737
hide everything
show cartoon, m_csa_737
color gray70, m_csa_737
set cartoon_transparency, 0.8, m_csa_737
select m_csa_737_left, m_csa_737 and chain B and resi 144 and resn LYS
select m_csa_737_right, m_csa_737 and chain A and resi 370 and resn LYS
show sticks, m_csa_737_left or m_csa_737_right
color tv_red, m_csa_737_left
color tv_blue, m_csa_737_right
distance m_csa_737_distance, (m_csa_737 and chain B and resi 144 and resn LYS and name CA), (m_csa_737 and chain A and resi 370 and resn LYS and name CA)
label m_csa_737_distance, "20.470 A"
zoom m_csa_737_left or m_csa_737_right, 8
set dash_width, 3
set label_size, 18
