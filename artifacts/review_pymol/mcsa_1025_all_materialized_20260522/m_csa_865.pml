load "artifacts/v3_mcsa_pymol_twelfth_materialized_coordinates_20260522/pdb_1OAS.cif", m_csa_865
hide everything
show cartoon, m_csa_865
color gray70, m_csa_865
set cartoon_transparency, 0.8, m_csa_865
select m_csa_865_left, m_csa_865 and chain A and resi 41 and resn LYS
select m_csa_865_right, m_csa_865 and chain A and resi 272 and resn SER
show sticks, m_csa_865_left or m_csa_865_right
color tv_red, m_csa_865_left
color tv_blue, m_csa_865_right
distance m_csa_865_distance, (m_csa_865 and chain A and resi 41 and resn LYS and name CA), (m_csa_865 and chain A and resi 272 and resn SER and name CA)
label m_csa_865_distance, "13.464 A"
zoom m_csa_865_left or m_csa_865_right, 8
set dash_width, 3
set label_size, 18
